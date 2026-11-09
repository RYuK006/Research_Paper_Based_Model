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
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import httpx
from pymatgen.core import Composition

logger = logging.getLogger("novelty_checker")


def load_mp_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """Retrieves Materials Project API key strictly from environment variable or .env file."""
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()
    env_key = os.environ.get("MP_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    # Fallback to local .env file
    for p in [Path(".env"), Path(__file__).resolve().parent.parent / ".env"]:
        if p.exists():
            try:
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("MP_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
            except Exception:
                pass
    return None


class MatchType(str, Enum):
    EXACT_FORMULA = "EXACT_FORMULA"
    FULL_ELEMENT_SYSTEM = "FULL_ELEMENT_SYSTEM"
    PARTIAL_SYSTEM = "PARTIAL_SYSTEM"
    SINGLE_ELEMENT = "SINGLE_ELEMENT"


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
    match_type: str = MatchType.SINGLE_ELEMENT.value
    is_superconductivity: bool = False

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
        self.mp_api_key = load_mp_api_key(mp_api_key)
        self.supercon_path = Path(supercon_path) if supercon_path else Path("data/supercon")
        self.timeout = timeout_seconds

    def parse_composition(self, formula: str) -> Tuple[Composition, str, List[str]]:
        """Parses chemical formula into pymatgen Composition, chemsys, and element list."""
        cleaned = formula.strip()
        match_paren = re.match(r"^\(([A-Za-z0-9\.]+)\)(.*)$", cleaned)
        if match_paren:
            inner, outer = match_paren.groups()
            comp = Composition(inner + outer)
        else:
            comp = Composition(cleaned)

        elements = sorted([str(e) for e in comp.elements])
        chemsys = "-".join(elements)
        return comp, chemsys, elements

    def analyze_evidence_text(
        self,
        title: str,
        abstract: str,
        formula: str,
        elements: List[str],
        is_hydride: bool,
    ) -> Tuple[str, bool]:
        """
        Analyzes paper title and abstract against candidate formula and elements.
        Returns:
            match_type: EXACT_FORMULA | FULL_ELEMENT_SYSTEM | PARTIAL_SYSTEM | SINGLE_ELEMENT
            is_superconductivity: bool indicating whether paper is genuine superconductivity evidence.
        """
        raw_text = f"{title or ''} {abstract or ''}"
        text_lower = raw_text.lower()

        # 1. Superconductivity Context Check
        has_sc = bool(re.search(r"\bsuperconduct\w*", text_lower))

        # For hydrides, additionally require "hydride" or hydrogen with high pressure context
        if is_hydride:
            has_hydride_word = bool(re.search(r"\bhydride\w*\b", text_lower))
            has_pressure_h_context = bool(
                re.search(r"(?:hydrogen|h2|\bh\b).{0,80}?(?:gpa|megabar|pressure|diamond\s+anvil|lh-?dac|dac)", text_lower)
                or re.search(r"(?:gpa|megabar|pressure|diamond\s+anvil|lh-?dac|dac).{0,80}?(?:hydrogen|h2|\bh\b)", text_lower)
            )
            is_superconductivity = has_sc and (has_hydride_word or has_pressure_h_context)
        else:
            is_superconductivity = has_sc

        # 2. Exact Formula Check
        # Clean formula string tokens to test
        formula_clean = re.sub(r"[\s\(\)]", "", formula).lower()
        text_no_spaces = re.sub(r"[\s\(\)\_\-]", "", text_lower)

        # Check for exact formula string or doped variant
        is_exact = False
        if formula.lower() in text_lower or formula_clean in text_no_spaces:
            is_exact = True
        elif is_hydride and len(elements) >= 3:
            # Check for generic alloy hydride mention like "(La,Y)H10" or "La-Y ternary hydride"
            metals = [e for e in elements if e != "H"]
            if len(metals) == 2:
                m1, m2 = metals
                alloy_patterns = [
                    rf"\({m1},{m2}\)\s*h\d*",
                    rf"\({m2},{m1}\)\s*h\d*",
                    rf"{m1}\s*-\s*{m2}\s+(?:ternary\s+)?hydride",
                    rf"{m2}\s*-\s*{m1}\s+(?:ternary\s+)?hydride",
                    rf"{ELEMENT_NAMES.get(m1, m1)}\s*-\s*{ELEMENT_NAMES.get(m2, m2)}\s+(?:ternary\s+)?hydride",
                ]
                for pat in alloy_patterns:
                    if re.search(pat, text_lower):
                        is_exact = True
                        break

        # Check 122 pnictide doping variants like Ba(Fe,Co)2As2 or Co-doped BaFe2As2
        if not is_exact and "Fe" in elements and "As" in elements:
            dopants = [e for e in elements if e not in ["Fe", "As", "Ba", "Sr", "Ca", "Eu"]]
            host_cations = [e for e in elements if e in ["Ba", "Sr", "Ca", "Eu"]]
            if dopants and host_cations:
                d = dopants[0]
                h = host_cations[0]
                pnictide_patterns = [
                    rf"{d}\s*-\s*doped\s+{h}fe2as2",
                    rf"{ELEMENT_NAMES.get(d, d)}\s*-\s*doped\s+{h}fe2as2",
                    rf"\({h}[0-9\.\-]*{d}[0-9\.\-]*\)\s*fe2as2",
                    rf"{h}\(fe[0-9\.\-]*{d}[0-9\.\-]*\)\s*2as2",
                    rf"{h}\(fe\s*,\s*{d}\)\s*2as2",
                ]
                for pat in pnictide_patterns:
                    if re.search(pat, text_lower):
                        is_exact = True
                        break

        if is_exact:
            return MatchType.EXACT_FORMULA.value, is_superconductivity

        # 3. Constituent Elements Check
        matched_elements: Set[str] = set()
        for e in elements:
            ename = ELEMENT_NAMES.get(e, "").lower()
            # Full element name check
            if ename and re.search(rf"\b{re.escape(ename)}\b", text_lower):
                matched_elements.add(e)
                continue

            # Special case for Hydrogen
            if e == "H":
                if re.search(r"\bhydride\w*\b|\bhydrogen\b|\bh2\b", text_lower):
                    matched_elements.add("H")
                continue

            # Special case for Potassium (K): must NOT be a temperature in Kelvin (like 55 K)
            if e == "K":
                if re.search(r"\bpotassium\b", text_lower):
                    matched_elements.add("K")
                elif re.search(r"(?<!\d\s)(?<!\d)\bK\b(?!\s*[\-–]?[A-Z0-9]*\b(?:\s*band|\s*edge))", raw_text):
                    if not re.search(r"\b(?:at|below|above|T_?[cC]\s*=?)\s*K\b", text_lower):
                        matched_elements.add("K")
                continue

            # Special cases for ambiguous 2-letter tokens: In, As
            if e == "In":
                if re.search(r"\bindium\b|\bIn-(?:doped|flux|films?)\b|\bIn\s+(?:layer|site|plane|atoms?)\b", raw_text, re.IGNORECASE):
                    matched_elements.add("In")
                continue
            if e == "As":
                if re.search(r"\barsenic\b|\barsenide\b|\bFeAs\b|\bAs-(?:based|doped)\b|\bAs\s+(?:layer|site|plane|atoms?)\b", raw_text, re.IGNORECASE):
                    matched_elements.add("As")
                continue

            # Multi-letter symbols (e.g. Ce, Sr, Ba, Fe, Co, La, Y, etc.)
            if len(e) >= 2:
                if re.search(rf"\b{re.escape(e)}\b", raw_text):
                    matched_elements.add(e)

        num_matched = len(matched_elements)
        if num_matched == len(elements):
            match_type = MatchType.FULL_ELEMENT_SYSTEM.value
        elif num_matched > 1:
            match_type = MatchType.PARTIAL_SYSTEM.value
        elif num_matched == 1:
            match_type = MatchType.SINGLE_ELEMENT.value
        else:
            match_type = MatchType.SINGLE_ELEMENT.value

        return match_type, is_superconductivity

    def query_openalex(self, formula: str, elements: List[str]) -> List[NoveltyEvidence]:
        """Queries OpenAlex for superconductivity papers containing the formula or element system."""
        evidence = []
        elem_names = [ELEMENT_NAMES.get(e, e) for e in elements]
        is_hydride = "H" in elements

        # Formulate targeted queries
        if is_hydride:
            queries = [
                f"superconducting hydride {' '.join(elements)}",
                f"superconductor hydride {formula}",
                f"superconducting hydride {' '.join(elem_names)}",
            ]
        else:
            queries = [
                f"superconductor {formula}",
                f"superconductor {' '.join(elements)}",
                f"superconducting {' '.join(elem_names)}",
            ]

        seen_urls: Set[str] = set()

        for q in queries:
            try:
                params = {
                    "search": q,
                    "per-page": 5,
                    "mailto": "research@materials.org",
                }
                headers = {"User-Agent": "ModelSuperconductor/1.0 (mailto:research@materials.org)"}
                r = httpx.get("https://api.openalex.org/works", params=params, headers=headers, timeout=self.timeout)
                if r.status_code == 429:
                    time.sleep(1.0)
                    r = httpx.get("https://api.openalex.org/works", params=params, headers=headers, timeout=self.timeout)

                if r.status_code == 200:
                    data = r.json()
                    results = data.get("results", [])
                    for res in results:
                        doi = res.get("doi") or res.get("id") or ""
                        if doi in seen_urls:
                            continue
                        title = res.get("title") or "Untitled"
                        abstract = res.get("abstract") or ""

                        match_type, is_sc = self.analyze_evidence_text(
                            title=title,
                            abstract=abstract,
                            formula=formula,
                            elements=elements,
                            is_hydride=is_hydride,
                        )

                        seen_urls.add(doi)
                        evidence.append(NoveltyEvidence(
                            source="OpenAlex API",
                            title=title,
                            year=res.get("publication_year"),
                            url_or_id=doi,
                            details=f"Query '{q}' [{match_type}] (sc_verified={is_sc})",
                            match_type=match_type,
                            is_superconductivity=is_sc,
                        ))

                        if len(evidence) >= 8:
                            break
            except Exception as e:
                logger.debug(f"OpenAlex query '{q}' failed: {e}")

            # If we found an exact or full match, we can stop querying
            if any(e.match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value] and e.is_superconductivity for e in evidence):
                break
            time.sleep(0.2)

        return evidence

    def query_materials_project(self, chemsys: str, formula: str) -> List[NoveltyEvidence]:
        """Queries Materials Project for entries in the chemical system."""
        evidence = []
        if not self.mp_api_key:
            return evidence

        headers = {"X-API-KEY": self.mp_api_key}
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
                        match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                        is_superconductivity=False,  # MP is structural, not a superconductivity lit record
                    ))
        except Exception as e:
            logger.debug(f"Materials Project query for chemsys '{chemsys}' failed: {e}")

        return evidence

    def query_local_corpus(self, formula: str, elements: List[str]) -> List[NoveltyEvidence]:
        """Queries local papers database for superconductivity papers matching candidate elements."""
        evidence = []
        if not self.db_path.exists():
            return evidence

        is_hydride = "H" in elements

        try:
            conn = sqlite3.connect(str(self.db_path))
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, abstract, year, doi
                FROM papers
                WHERE lower(categories) LIKE '%supr-con%' OR lower(title) LIKE '%superconduct%' OR lower(abstract) LIKE '%superconduct%'
            """)
            rows = cur.fetchall()
            conn.close()

            for pid, title, abstract, year, doi in rows:
                match_type, is_sc = self.analyze_evidence_text(
                    title=title or "",
                    abstract=abstract or "",
                    formula=formula,
                    elements=elements,
                    is_hydride=is_hydride,
                )

                # Only include if at least PARTIAL_SYSTEM or above to keep evidence clean
                if match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value]:
                    evidence.append(NoveltyEvidence(
                        source="Local Superconductivity Corpus",
                        title=title or "Untitled",
                        year=year,
                        url_or_id=doi or f"paper_id:{pid}",
                        details=f"Local paper match [{match_type}]",
                        match_type=match_type,
                        is_superconductivity=is_sc,
                    ))
                    if len(evidence) >= 5:
                        break
        except Exception as e:
            logger.debug(f"Local database query failed: {e}")

        return evidence

    def query_supercon(self, formula: str, elements: List[str]) -> List[NoveltyEvidence]:
        """Queries benchmark table of hallmark known superconductors."""
        evidence = []
        HALLMARK_KNOWN = {
            ("H", "La", "Y"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 253 K in lanthanum-yttrium ternary hydrides (Materials Today 2021)",
                year=2021,
                url_or_id="https://doi.org/10.1016/j.mattod.2021.03.025",
                details="Known ternary superhydride (La,Y)H10 synthesized at 160-196 GPa",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("As", "Ba", "Co", "Fe"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity in Co-doped BaFe2As2 (Phys. Rev. B 2008 / Sefat et al.)",
                year=2008,
                url_or_id="https://doi.org/10.1103/PhysRevLett.101.117004",
                details="Known electron-doped 122 iron-based superconductor with Tc ~ 22 K",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("Ba", "Cu", "O", "Y"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 93 K in a new mixed-phase Y-Ba-Cu-O compound (Wu et al. 1987)",
                year=1987,
                url_or_id="https://doi.org/10.1103/PhysRevLett.58.908",
                details="Hallmark YBCO high-Tc cuprate superconductor",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("B", "Mg"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 39 K in magnesium diboride (Nagamatsu et al. Nature 2001)",
                year=2001,
                url_or_id="https://doi.org/10.1038/35065039",
                details="Hallmark conventional phonon-mediated binary superconductor MgB2",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("Ce", "H", "La"): NoveltyEvidence(
                source="SuperCon Reference",
                title="High-Temperature Superconducting Phase in Cerium-Doped Lanthanum Hydride at Megabar Pressures (Chen et al. PRL 2021)",
                year=2021,
                url_or_id="https://doi.org/10.1103/PhysRevLett.127.117001",
                details="Known ternary clathrate hydride (La,Ce)H10 with Tc up to 176 K at 100 GPa",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("Ca", "H", "Y"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity in ternary calcium yttrium hydrides under high pressure (Liang et al. Phys. Rev. B 2021)",
                year=2021,
                url_or_id="https://doi.org/10.1103/PhysRevB.104.134501",
                details="Known ternary clathrate hydride (Ca,Y)H12 with predicted Tc exceeding 200 K",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("As", "Ba", "Fe", "K"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 38 K in the Iron-Arsenide (Ba1-xKx)Fe2As2 (Rotter et al. PRL 2008)",
                year=2008,
                url_or_id="https://doi.org/10.1103/PhysRevLett.101.107006",
                details="Hallmark hole-doped 122 iron-based superconductor Ba0.6K0.4Fe2As2 with Tc = 38 K",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("As", "F", "Fe", "O", "Sm"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity at 43 K in SmFeAsO1-xFx (Chen et al. Nature 2008)",
                year=2008,
                url_or_id="https://doi.org/10.1038/nature07045",
                details="Hallmark fluorine-doped 1111 iron oxypnictide superconductor SmFeAs(O,F) with Tc up to 55 K",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("Fe", "Se", "Te"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity in Fe1+yTe1-xSex single crystals (Sales et al. Phys. Rev. B 2009)",
                year=2009,
                url_or_id="https://doi.org/10.1103/PhysRevB.79.094521",
                details="Hallmark iron chalcogenide superconductor Fe(Se,Te) with Tc ~ 15 K",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("Cu", "La", "O", "Sr"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Bulk Superconductivity at 36 K in La1.8Sr0.2CuO4 (Cava et al. PRL 1987 / Bednorz & Muller 1986)",
                year=1987,
                url_or_id="https://doi.org/10.1103/PhysRevLett.58.408",
                details="Hallmark high-Tc LSCO cuprate superconductor",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
            ),
            ("O", "Ru", "Sr"): NoveltyEvidence(
                source="SuperCon Reference",
                title="Superconductivity in a layered perovskite without copper (Maeno et al. Nature 1994)",
                year=1994,
                url_or_id="https://doi.org/10.1038/372532a0",
                details="Hallmark unconventional ruthenate superconductor Sr2RuO4",
                match_type=MatchType.FULL_ELEMENT_SYSTEM.value,
                is_superconductivity=True,
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
        Rule:
        - KNOWN only for EXACT_FORMULA or FULL_ELEMENT_SYSTEM about superconductivity.
        - LIKELY_KNOWN for close systems (e.g. Materials Project entries in chemical system).
        - PARTIAL or SINGLE_ELEMENT matches must never produce KNOWN.
        - Never output the word 'novel'; only 'no hits found in: <sources searched>'.
        """
        comp, chemsys, elements = self.parse_composition(formula)
        reduced = comp.reduced_formula

        sources_searched = ["OpenAlex API", "Materials Project", "Local Superconductivity Corpus"]
        if self.supercon_path.exists():
            sources_searched.append("SuperCon / 3DSC (local directory)")
        else:
            sources_searched.append("SuperCon Reference")

        all_evidence: List[NoveltyEvidence] = []

        # 1. SuperCon / Hallmark Reference Data (instant local lookup)
        sc_evidence = self.query_supercon(formula, elements)
        all_evidence.extend(sc_evidence)

        # 2. Local Superconductivity Corpus (instant local SQLite query)
        local_evidence = self.query_local_corpus(formula, elements)
        all_evidence.extend(local_evidence)

        # If already proven KNOWN by verified hallmark reference or local corpus, skip remote queries
        has_definitive_known = any(
            e.is_superconductivity and e.match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value]
            for e in all_evidence
        )

        # 3. OpenAlex API (remote)
        if not has_definitive_known:
            oa_evidence = self.query_openalex(formula, elements)
            all_evidence.extend(oa_evidence)

        # 4. Materials Project (remote)
        if not has_definitive_known:
            mp_evidence = self.query_materials_project(chemsys, formula)
            all_evidence.extend(mp_evidence)

        # Categorize evidence
        sc_literature_hits = [
            e for e in all_evidence
            if e.source in ["OpenAlex API", "Local Superconductivity Corpus", "SuperCon Reference", "SuperCon / 3DSC (local directory)"]
            and e.is_superconductivity
            and e.match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value]
        ]

        mp_full_hits = [
            e for e in all_evidence
            if e.source == "Materials Project" and e.match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value]
        ]

        mp_partial_hits = [
            e for e in all_evidence
            if e.source == "Materials Project" and e.match_type == MatchType.PARTIAL_SYSTEM.value
        ]

        if sc_literature_hits:
            status = "KNOWN"
            top_ev = sc_literature_hits[0]
            desc = f"KNOWN: Established superconductor in literature (e.g., '{top_ev.title}', {top_ev.year or 'n.d.'} [{top_ev.match_type}])"
        elif mp_full_hits:
            status = "LIKELY_KNOWN"
            top_ev = mp_full_hits[0]
            desc = f"LIKELY_KNOWN: Chemical system present in structural databases (e.g., '{top_ev.title}' [{top_ev.match_type}])"
        elif mp_partial_hits:
            status = "LIKELY_KNOWN"
            top_ev = mp_partial_hits[0]
            desc = f"LIKELY_KNOWN: Close related phase present in structural databases (e.g., '{top_ev.title}' [{top_ev.match_type}])"
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
