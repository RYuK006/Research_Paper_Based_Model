"""
Structured Scientific Information Extractor.
Parses papers into the fixed Layer 2 schema:
material, composition, structure type, Tc, pressure, synthesis method, measurement type, and future work.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from extraction.models import ExtractedPaperRecord

logger = logging.getLogger("extractor")

# Standard periodic table element symbols
ELEMENTS_SYMBOLS = {
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac",
    "Th", "Pa", "U", "Np", "Pu"
}

SYNTHESIS_METHODS = [
    ("Laser-heated diamond anvil cell", r"\b(?:laser[- ]heated\s+diamond\s+anvil|LH-?DAC|high[- ]pressure\s+laser\s+heating)\b"),
    ("Pulsed laser deposition", r"\b(?:pulsed\s+laser\s+deposition|PLD)\b"),
    ("Solid-state reaction", r"\b(?:solid[- ]state\s+reaction|solid[- ]state\s+synthesis|ceramic\s+method)\b"),
    ("Flux growth", r"\b(?:flux\s+growth|self[- ]flux|molten\s+flux)\b"),
    ("Chemical vapor deposition", r"\b(?:chemical\s+vapor\s+deposition|CVD)\b"),
    ("Hydrothermal synthesis", r"\b(?:hydrothermal|solvothermal)\b"),
    ("Molecular beam epitaxy", r"\b(?:molecular\s+beam\s+epitaxy|MBE)\b"),
    ("Arc melting", r"\b(?:arc[- ]melting|arc\s+furnace)\b"),
    ("Sputtering", r"\b(?:magnetron\s+sputtering|rf\s+sputtering)\b"),
    ("Sol-gel method", r"\b(?:sol[- ]gel)\b"),
]

MEASUREMENT_TECHNIQUES = [
    ("Electrical resistivity", r"\b(?:electrical\s+resistivity|four[- ]probe|resistivity\s+measurement|transport\s+measurement)\b"),
    ("Magnetic susceptibility (SQUID)", r"\b(?:magnetic\s+susceptibility|SQUID|magnetization|Meissner\s+effect)\b"),
    ("Synchrotron X-ray diffraction", r"\b(?:synchrotron\s+(?:X-ray\s+diffraction|XRD)|powder\s+diffraction)\b"),
    ("Specific heat", r"\b(?:specific\s+heat|heat\s+capacity)\b"),
    ("ARPES", r"\b(?:angle[- ]resolved\s+photoemission|ARPES)\b"),
    ("Muon spin rotation", r"\b(?:muon\s+spin\s+rotation|muSR|$\mu$SR)\b"),
    ("Tunneling spectroscopy / STM", r"\b(?:scanning\s+tunneling|STM|tunneling\s+spectroscopy)\b"),
]

STRUCTURE_TYPES = [
    ("Perovskite", r"\b(?:perovskite|double\s+perovskite)\b"),
    ("Clathrate", r"\b(?:clathrate|sodalite[- ]like|cage[- ]like)\b"),
    ("Tetragonal PbO-type", r"\b(?:tetragonal|PbO[- ]type|1111|122|11\s+phase)\b"),
    ("Cubic", r"\b(?:cubic|fcc|bcc)\b"),
    ("Hexagonal", r"\b(?:hexagonal|honeycomb|kagome)\b"),
    ("Orthorhombic", r"\b(?:orthorhombic)\b"),
    ("Spinel", r"\b(?:spinel)\b"),
    ("Pyrochlore", r"\b(?:pyrochlore)\b"),
    ("Monoclinic", r"\b(?:monoclinic)\b"),
]


class StructuredExtractor:
    """
    Extracts fixed schema table fields from research paper abstracts and full text.
    Persists structured material entries into SQLite for downstream gap analysis.
    """

    def __init__(self, db_path: str = "data/papers.db") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Initializes structured_materials table in database."""
        if not self.db_path.exists():
            return
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS structured_materials (
                paper_id TEXT PRIMARY KEY,
                doi TEXT,
                year INTEGER,
                material TEXT,
                composition TEXT,
                elements_json TEXT,
                structure_type TEXT,
                tc_kelvin REAL,
                pressure_gpa REAL,
                synthesis_method TEXT,
                measurement_type TEXT,
                future_work TEXT,
                confidence REAL
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_mat_material ON structured_materials (material)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_mat_tc ON structured_materials (tc_kelvin)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_mat_pressure ON structured_materials (pressure_gpa)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_mat_structure ON structured_materials (structure_type)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_mat_synthesis ON structured_materials (synthesis_method)")
        conn.commit()
        conn.close()

    def extract_elements_from_formula(self, formula: str) -> List[str]:
        """Extracts unique chemical element symbols from formula string."""
        tokens = re.findall(r"([A-Z][a-z]?)", formula)
        return sorted(list(set(t for t in tokens if t in ELEMENTS_SYMBOLS)))

    def extract_chemical_formula(self, text: str) -> Tuple[str, List[str]]:
        """Identifies primary chemical formula and present elements."""
        # Match formulas like LaH10, YBa2Cu3O7, FeSe, MgB2, BaFe2As2
        candidates = re.findall(r"\b([A-Z][a-z]?[0-9]*(?:\.[0-9]+)?(?:[A-Z][a-z]?[0-9]*(?:\.[0-9]+)?)+)\b", text)
        for cand in candidates:
            elems = self.extract_elements_from_formula(cand)
            if len(elems) >= 2:
                return cand, elems

        # Single element or binary fallback
        elem_matches = re.findall(r"\b([A-Z][a-z]?)\b", text)
        valid_elems = sorted(list(set(e for e in elem_matches if e in ELEMENTS_SYMBOLS)))
        if valid_elems:
            return "-".join(valid_elems), valid_elems

        return "Unspecified Material", []

    def extract_tc(self, text: str) -> Optional[float]:
        """Extracts superconducting critical temperature in Kelvin."""
        match = re.search(r"T_?[cC][^0-9\n]{0,25}?([0-9]+(?:\.[0-9]+)?)\s*K\b", text, re.IGNORECASE)
        if match:
            try:
                val = float(match.group(1))
                if 0.0 < val <= 400.0:  # Physically meaningful range
                    return val
            except ValueError:
                pass
        return None

    def extract_pressure(self, text: str) -> Optional[float]:
        """Extracts pressure in GPa."""
        gpa_match = re.search(r"(?:pressure|at)\s*(?:of|around|~)?\s*([0-9]+(?:\.[0-9]+)?)\s*GPa\b", text, re.IGNORECASE)
        if gpa_match:
            try:
                return float(gpa_match.group(1))
            except ValueError:
                pass

        if re.search(r"\bambient\s+pressure\b", text, re.IGNORECASE):
            return 0.0001  # Ambient ~ 1 atm

        return None

    def extract_synthesis_method(self, text: str) -> str:
        """Matches synthesis methodology."""
        for label, pat in SYNTHESIS_METHODS:
            if re.search(pat, text, re.IGNORECASE):
                return label
        return "Standard synthesis"

    def extract_measurement_type(self, text: str) -> str:
        """Matches primary measurement technique."""
        for label, pat in MEASUREMENT_TECHNIQUES:
            if re.search(pat, text, re.IGNORECASE):
                return label
        return "Physical property measurement"

    def extract_structure_type(self, text: str) -> str:
        """Matches crystal lattice or structural family."""
        for label, pat in STRUCTURE_TYPES:
            if re.search(pat, text, re.IGNORECASE):
                return label
        return "Crystalline lattice"

    def extract_future_work(self, text: str) -> str:
        """Extracts concluding future work, next steps, or unconfirmed hypotheses."""
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        future_indicators = [
            "future", "remain", "open question", "warrant", "suggest", "propose",
            "further", "subsequent", "unexplored", "promising", "doping", "substitution"
        ]

        for sent in reversed(sentences):
            sent_lower = sent.lower()
            if any(ind in sent_lower for ind in future_indicators):
                return sent.strip()

        if len(sentences) >= 1:
            return sentences[-1].strip()
        return "Further chemical substitution and high-pressure investigation proposed."

    def extract_record(
        self,
        paper_id: str,
        title: str,
        abstract: str,
        year: int,
        doi: Optional[str] = None,
    ) -> ExtractedPaperRecord:
        """Extracts a complete structured record from paper metadata and abstract."""
        full_text = f"{title}. {abstract}"
        formula, elems = self.extract_chemical_formula(full_text)
        structure = self.extract_structure_type(full_text)
        tc = self.extract_tc(full_text)
        pressure = self.extract_pressure(full_text)
        synthesis = self.extract_synthesis_method(full_text)
        meas = self.extract_measurement_type(full_text)
        future = self.extract_future_work(abstract)

        # Confidence calculation
        score = 0.5
        if elems: score += 0.15
        if tc is not None: score += 0.15
        if pressure is not None: score += 0.1
        if synthesis != "Standard synthesis": score += 0.1
        confidence = min(round(score, 2), 1.0)

        return ExtractedPaperRecord(
            paper_id=paper_id,
            doi=doi,
            year=year,
            material=formula,
            composition=formula,
            elements=elems,
            structure_type=structure,
            tc_kelvin=tc,
            pressure_gpa=pressure,
            synthesis_method=synthesis,
            measurement_type=meas,
            future_work=future,
            confidence=confidence,
        )

    def extract_and_store_batch(self, limit: int = 500) -> int:
        """Batch extracts papers from papers table and stores into structured_materials table."""
        if not self.db_path.exists():
            return 0

        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("""
            SELECT id, title, abstract, year, doi
            FROM papers
            WHERE abstract IS NOT NULL AND length(abstract) > 50
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()

        records = []
        for r in rows:
            rec = self.extract_record(
                paper_id=r["id"],
                title=r["title"] or "",
                abstract=r["abstract"] or "",
                year=r["year"] or 2020,
                doi=r["doi"],
            )
            records.append(rec.to_sql_row())

        c.executemany("""
            INSERT OR REPLACE INTO structured_materials
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, records)
        conn.commit()
        conn.close()

        logger.info(f"Extracted and stored {len(records)} structured material records in {self.db_path}")
        return len(records)
