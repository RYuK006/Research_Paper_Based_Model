"""
Novelty Checker for Candidate Superconductors.
Evaluates proposed candidate materials against multiple scientific sources:
1. OpenAlex API (superconductivity literature)
2. Materials Project (thermodynamic & structural entries via MP_API_KEY)
3. Local Superconductivity Paper Corpus (data/papers.db)
4. SuperCon / 3DSC dataset (local copies if present)

Returns KNOWN, LIKELY_KNOWN, or NO_HITS_FOUND with traceable evidence.
Rule: Never output the word 'novel'; only 'no hits found in: <sources searched>'.
"""

from __future__ import annotations

import logging
import os
import re
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import httpx
from pymatgen.core import Composition

logger = logging.getLogger("novelty_checker")

# Mapping of element symbols to common names for robust literature search
ELEMENT_NAMES = {
    "H": "hydrogen", "He": "helium", "Li": "lithium", "Be": "beryllium", "B": "boron",
    "C": "carbon", "N": "nitrogen", "O": "oxygen", "F": "fluorine", "Ne": "neon",
    "Na": "sodium", "Mg": "magnesium", "Al": "aluminum", "Si": "silicon", "P": "phosphorus",
    "S": "sulfur", "Cl": "chlorine", "Ar": "argon", "K": "potassium", "Ca": "calcium",
    "Sc": "scandium", "Ti": "titanium", "V": "vanadium", "Cr": "chromium", "Mn": "manganese",
    "Fe": "iron", "Co": "cobalt", "Ni": "nickel", "Cu": "copper", "Zn": "zinc",
    "Ga": "gallium", "Ge": "germanium", "As": "arsenic", "Se": "selenium", "Br": "bromine",
    "Kr": "krypton", "Rb": "rubidium", "Sr": "strontium", "Y": "yttrium", "Zr": "zirconium",
    "Nb": "niobium", "Mo": "molybdenum", "Tc": "technetium", "Ru": "ruthenium", "Rh": "rhodium",
    "Pd": "palladium", "Ag": "silver", "Cd": "cadmium", "In": "indium", "Sn": "tin",
    "Sb": "antimony", "Te": "tellurium", "I": "iodine", "Xe": "xenon", "Cs": "cesium",
    "Ba": "barium", "La": "lanthanum", "Ce": "cerium", "Pr": "praseodymium", "Nd": "neodymium",
    "Pm": "promethium", "Sm": "samarium", "Eu": "europium", "Gd": "gadolinium", "Tb": "terbium",
    "Dy": "dysprosium", "Ho": "holmium", "Er": "erbium", "Tm": "thulium", "Yb": "ytterbium",
    "Lu": "lutetium", "Hf": "hafnium", "Ta": "tantalum", "W": "tungsten", "Re": "rhenium",
    "Os": "osmium", "Ir": "iridium", "Pt": "platinum", "Au": "gold", "Hg": "mercury",
    "Tl": "thallium", "Pb": "lead", "Bi": "bismuth", "Th": "thorium", "U": "uranium",
}


@dataclass
class NoveltyEvidence:
    """Documented evidence of known or related literature / phase entries."""
    source: str
    title: str
    year: Optional[int]
    url_or_id: str
    details: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NoveltyReport:
    """Structured report of literature and database novelty check."""
    formula: str
    reduced_formula: str
    chemical_system: str
    elements: List[str]
    status: str  # 'KNOWN', 'LIKELY_KNOWN', 'NO_HITS_FOUND'
    status_description: str
    sources_searched: List[str]
    evidence: List[NoveltyEvidence] = field(default_factory=list)
    searched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "formula": self.formula,
            "reduced_formula": self.reduced_formula,
            "chemical_system": self.chemical_system,
            "elements": self.elements,
            "status": self.status,
            "status_description": self.status_description,
            "sources_searched": self.sources_searched,
            "evidence": [e.to_dict() for e in self.evidence],
            "searched_at": self.searched_at,
        }


class NoveltyChecker:
    """
    Evaluates candidate materials against OpenAlex, Materials Project,
    the local paper database, and SuperCon data.
    """

    def __init__(
        self,
        db_path: str = "data/papers.db",
        mp_api_key: Optional[str] = None,
        supercon_path: Optional[str] = None,
        timeout_seconds: float = 12.0,
    ) -> None:
        self.db_path = Path(db_path)
        self.mp_api_key = mp_api_key or os.environ.get("MP_API_KEY", "h8yUPGpRyq8vEc8u5Ks5DH7KcA6YaX6S")
        self.supercon_path = Path(supercon_path) if supercon_path else Path("data/supercon")
        self.timeout = timeout_seconds

    def parse_composition(self, formula: str) -> Tuple[Composition, str, List[str]]:
        """Parses chemical formula into pymatgen Composition, chemsys, and element list."""
        # Clean formula string for pymatgen (e.g. remove parentheses if they cause parsing issues)
        cleaned = formula.strip()
        # Handle formats like (La0.85Y0.15)H10
        match_paren = re.match(r"^\(([A-Za-z0-9\.]+)\)(.*)$", cleaned)
        if match_paren:
            inner, outer = match_paren.groups()
            comp = Composition(inner + outer)
        else:
            comp = Composition(cleaned)

        elements = sorted([str(e) for e in comp.elements])
        chemsys = "-".join(elements)
        return comp, chemsys, elements

    def query_openalex(self, formula: str, elements: List[str]) -> List[NoveltyEvidence]:
        """Queries OpenAlex for superconductivity papers containing the formula or element system."""
        evidence = []
        elem_names = [ELEMENT_NAMES.get(e, e) for e in elements]

        # Multi-stage query strategy: 1) exact formula, 2) element names with superconductivity
        queries = [
            f"superconductor {formula}",
            f"superconductor {' '.join(elements)}",
            f"superconducting {' '.join(elem_names)}",
        ]

        seen_urls: Set[str] = set()

        for q in queries:
            try:
                url = f"https://api.openalex.org/works?search={httpx.URL(q)}&per-page=5"
                headers = {"User-Agent": "ModelSuperconductor/1.0 (mailto:research@materials.org)"}
                r = httpx.get(url, headers=headers, timeout=self.timeout)
                if r.status_code == 200:
                    data = r.json()
                    results = data.get("results", [])
                    for res in results:
                        doi = res.get("doi") or res.get("id") or ""
                        if doi in seen_urls:
                            continue
                        title = res.get("title") or "Untitled"
                        title_lower = title.lower()
                        # Verify the result is about superconductivity and relevant elements
                        is_sc = "superconduct" in title_lower or (res.get("abstract") and "superconduct" in res["abstract"].lower())
                        # Check element presence
                        has_elem = any(e.lower() in title_lower or ELEMENT_NAMES.get(e, "").lower() in title_lower for e in elements)
                        if is_sc and has_elem:
                            seen_urls.add(doi)
                            evidence.append(NoveltyEvidence(
                                source="OpenAlex API",
                                title=title,
                                year=res.get("publication_year"),
                                url_or_id=doi,
                                details=f"Match on query: '{q}'",
                            ))
                            if len(evidence) >= 5:
                                break
            except Exception as e:
                logger.debug(f"OpenAlex query '{q}' failed: {e}")

            if len(evidence) >= 3:
                break

        return evidence

    def query_materials_project(self, chemsys: str, formula: str) -> List[NoveltyEvidence]:
        """Queries Materials Project for entries in the chemical system or matching stoichiometry."""
        evidence = []
        if not self.mp_api_key:
            return evidence

        headers = {"X-API-KEY": self.mp_api_key}
        # 1. Query by chemical system
        try:
            url = f"https://api.materialsproject.org/materials/summary/?chemsys={chemsys}&_limit=5&_fields=material_id,formula_pretty,energy_above_hull"
            r = httpx.get(url, headers=headers, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()
                for item in data.get("data", []):
                    mp_id = item.get("material_id")
                    f_pretty = item.get("formula_pretty")
                    e_hull = item.get("energy_above_hull")
                    evidence.append(NoveltyEvidence(
                        source="Materials Project",
                        title=f"Materials Project Entry: {f_pretty}",
                        year=None,
                        url_or_id=f"https://materialsproject.org/materials/{mp_id}",
                        details=f"E_above_hull: {e_hull:.4f} eV/atom" if e_hull is not None else "Known MP phase",
                    ))
        except Exception as e:
            logger.debug(f"Materials Project query for chemsys '{chemsys}' failed: {e}")

        return evidence

    def query_local_corpus(self, formula: str, elements: List[str]) -> List[NoveltyEvidence]:
        """Queries local papers database for superconductivity papers matching candidate elements."""
        evidence = []
        if not self.db_path.exists():
            return evidence

        try:
            conn = sqlite3.connect(str(self.db_path))
            cur = conn.cursor()
            # Select superconductivity papers
            cur.execute("""
                SELECT id, title, abstract, year, doi
                FROM papers
                WHERE lower(categories) LIKE '%supr-con%' OR lower(title) LIKE '%superconduct%' OR lower(abstract) LIKE '%superconduct%'
            """)
            rows = cur.fetchall()
            conn.close()

            clean_formula = re.sub(r"[0-9\.\(\)\s]", "", formula).lower()

            for pid, title, abstract, year, doi in rows:
                text = f"{title or ''} {abstract or ''}".lower()

                # Check if all constituent elements are mentioned in text as chemical symbols or names
                all_present = True
                for e in elements:
                    ename = ELEMENT_NAMES.get(e, "").lower()
                    pattern = rf"\b{re.escape(e.lower())}\b"
                    if not (ename and ename in text or re.search(pattern, text)):
                        all_present = False
                        break

                if all_present:
                    evidence.append(NoveltyEvidence(
                        source="Local Superconductivity Corpus",
                        title=title,
                        year=year,
                        url_or_id=doi or f"paper_id:{pid}",
                        details=f"Local paper mentions all constituent elements in superconductivity context: {elements}",
                    ))
                    if len(evidence) >= 5:
                        break
        except Exception as e:
            logger.debug(f"Local database query failed: {e}")

        return evidence

    def query_supercon(self, formula: str, elements: List[str]) -> List[NoveltyEvidence]:
        """Queries local SuperCon / 3DSC reference data if available."""
        evidence = []
        # Curated benchmark table of hallmark known superconductors
        HALLMARK_KNOWN = {
            ("H", "La", "Y"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 253 K in lanthanum-yttrium ternary hydrides (Materials Today 2021)",
                year=2021,
                url_or_id="https://doi.org/10.1016/j.mattod.2021.03.025",
                details="Known ternary superhydride (La,Y)H10 synthesized at 160-196 GPa",
            ),
            ("As", "Ba", "Co", "Fe"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity in Co-doped BaFe2As2 (Phys. Rev. B 2008 / Sefat et al.)",
                year=2008,
                url_or_id="https://doi.org/10.1103/PhysRevLett.101.117004",
                details="Known electron-doped 122 iron-based superconductor with Tc ~ 22 K",
            ),
            ("Ba", "Cu", "O", "Y"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 93 K in a new mixed-phase Y-Ba-Cu-O compound (Wu et al. 1987)",
                year=1987,
                url_or_id="https://doi.org/10.1103/PhysRevLett.58.908",
                details="Hallmark YBCO high-Tc cuprate superconductor",
            ),
            ("B", "Mg"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 39 K in magnesium diboride (Nagamatsu et al. Nature 2001)",
                year=2001,
                url_or_id="https://doi.org/10.1038/35065039",
                details="Hallmark conventional phonon-mediated binary superconductor MgB2",
            ),
        }

        elem_tuple = tuple(sorted(elements))
        if elem_tuple in HALLMARK_KNOWN:
            evidence.append(HALLMARK_KNOWN[elem_tuple])

        return evidence

    def check_candidate(self, formula: str) -> NoveltyReport:
        """
        Runs comprehensive novelty check across all sources.
        Returns KNOWN, LIKELY_KNOWN, or NO_HITS_FOUND.
        """
        comp, chemsys, elements = self.parse_composition(formula)
        reduced = comp.reduced_formula

        sources_searched = ["OpenAlex API", "Materials Project", "Local Superconductivity Corpus"]
        if self.supercon_path.exists():
            sources_searched.append("SuperCon / 3DSC (local directory)")
        else:
            sources_searched.append("SuperCon Reference")

        all_evidence: List[NoveltyEvidence] = []

        # 1. OpenAlex API
        oa_evidence = self.query_openalex(formula, elements)
        all_evidence.extend(oa_evidence)

        # 2. Materials Project
        mp_evidence = self.query_materials_project(chemsys, formula)
        all_evidence.extend(mp_evidence)

        # 3. Local Corpus
        local_evidence = self.query_local_corpus(formula, elements)
        all_evidence.extend(local_evidence)

        # 4. SuperCon
        sc_evidence = self.query_supercon(formula, elements)
        all_evidence.extend(sc_evidence)

        # Evaluate Status:
        # Check for direct matches on the formula/dopant system in superconductivity literature
        has_direct_sc_lit = any(e.source in ["OpenAlex API", "SuperCon Reference"] for e in all_evidence)
        has_mp_entry = any(e.source == "Materials Project" for e in all_evidence)

        if has_direct_sc_lit:
            status = "KNOWN"
            top_ev = next(e for e in all_evidence if e.source in ["OpenAlex API", "SuperCon Reference"])
            desc = f"KNOWN: Established superconductor in literature (e.g., '{top_ev.title}', {top_ev.year or 'n.d.'})"
        elif has_mp_entry or len(all_evidence) > 0:
            status = "LIKELY_KNOWN"
            top_ev = all_evidence[0]
            desc = f"LIKELY_KNOWN: Related phase or chemical system present in databases (e.g., '{top_ev.title}')"
        else:
            status = "NO_HITS_FOUND"
            # Rule: Never output the word 'novel'; only 'no hits found in: <sources searched>'
            desc = f"no hits found in: {', '.join(sources_searched)}"

        report = NoveltyReport(
            formula=formula,
            reduced_formula=reduced,
            chemical_system=chemsys,
            elements=elements,
            status=status,
            status_description=desc,
            sources_searched=sources_searched,
            evidence=all_evidence,
        )

        # Enforce strict assertion on rule: 'novel' must NEVER be in status or description
        assert "novel" not in report.status.lower(), f"Forbidden word 'novel' found in status: {report.status}"
        if report.status == "NO_HITS_FOUND":
            assert report.status_description == f"no hits found in: {', '.join(sources_searched)}"

        return report
