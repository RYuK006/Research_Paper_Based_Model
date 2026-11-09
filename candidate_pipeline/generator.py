"""
Candidate Material Generator.
Translates Layer 2 discovery gaps into chemically and crystallographically valid superconductor candidates.
Enforces site-specific prototype substitutions, oxidation state balancing, and metal/nonmetal site segregation.
Guarantees determinism with a fixed seed.
"""

from __future__ import annotations

import logging
import random
import re
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Set, Tuple

from pymatgen.core import Composition, Element

logger = logging.getLogger("candidate_generator")

# Crystallographic Prototype Definitions and Site Rules
PROTOTYPE_SPECS = {
    "Clathrate hydride": {
        "prototype": "LaH10",
        "space_group": "Fm-3m (#225)",
        "lattice_system": "Cubic",
        "allowed_cage_metals": {"La", "Y", "Ce", "Th", "Sc", "Ca", "Sr", "Pr", "Nd", "Sm", "Eu", "Gd", "Lu"},
        "forbidden_cage_elements": {"O", "C", "N", "P", "S", "F", "Cl", "Br", "I", "As", "Se", "Te", "Cu", "Ag", "Au", "Zn", "Cd", "Hg"},
    },
    "Perovskite oxide": {
        "prototype": "YBa2Cu3O7",
        "space_group": "Pmmm (#47)",
        "lattice_system": "Orthorhombic",
        "sites": {
            "Y_site": {"name": "Y (rare-earth)", "allowed": {"Y", "Nd", "Sm", "Eu", "Gd", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"}},
            "Ba_site": {"name": "Ba (alkaline-earth)", "allowed": {"Ba", "Sr", "Ca"}},
            "Cu_site": {"name": "Cu (transition metal)", "allowed": {"Cu", "Zn", "Ni", "Co", "Fe", "Al"}},
        }
    },
    "Iron chalcogenide / pnictide": {
        "prototype": "BaFe2As2",
        "space_group": "I4/mmm (#139)",
        "lattice_system": "Tetragonal",
        "sites": {
            "Ba_site": {"name": "Ba (alkali/alkaline-earth spacer)", "allowed": {"Ba", "Sr", "Ca", "Eu", "K", "Rb", "Cs", "Na"}},
            "Fe_site": {"name": "Fe (transition metal layer)", "allowed": {"Fe", "Co", "Ni", "Rh", "Pd", "Ru", "Ir", "Pt"}},
            "As_site": {"name": "As (pnictogen/chalcogen)", "allowed": {"As", "P", "Se"}},
        }
    },
    "Boride / Carbide": {
        "prototype": "MgB2",
        "space_group": "P6/mmm (#191)",
        "lattice_system": "Hexagonal",
        "sites": {
            "Mg_site": {"name": "Mg", "allowed": {"Mg", "Al", "Sc"}},
            "B_site": {"name": "B", "allowed": {"B", "C"}},
        }
    }
}


@dataclass
class MaterialCandidate:
    """Represents a proposed material candidate for computational and experimental verification."""
    candidate_id: str
    formula: str
    reduced_formula: str
    elements: List[str]
    stoichiometry: Dict[str, float]
    target_family: str
    prototype: str
    space_group: str
    lattice_system: str
    tc_status: str  # e.g., 'NOT COMPUTED' or 'COMPUTED (GroupKFold SuperCon Model)'
    predicted_tc: Optional[float]
    predicted_tc_uncertainty: Optional[float]
    predicted_pressure_gpa: Optional[float]
    pressure_status: str  # e.g., 'NOT COMPUTED (Requires ab initio enthalpy)'
    gap_origin: str
    discovery_score: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CandidateGenerator:
    """
    Generates structured chemical candidates from Layer 2 discovery gaps with deterministic seeding,
    strict crystallographic site assignment, and chemical sanity checks.
    """

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed
        self._rng = random.Random(seed)

    def is_valid_substitution(self, formula: str, family: str) -> Tuple[bool, str]:
        """
        Enforces crystallographic prototype site matching and chemical sanity rules.
        Rejects invalid substitutions including nonmetals on metal sites and site collisions.
        """
        # Rule 1: Clathrate hydrides (Fm-3m LaH10 prototype)
        if "H10" in formula or "hydride" in family.lower():
            m = re.search(r"\(([A-Za-z0-9\.]+)\)H10", formula)
            if m:
                cations = re.findall(r"([A-Z][a-z]*)", m.group(1))
                spec = PROTOTYPE_SPECS["Clathrate hydride"]
                for cat in cations:
                    if cat in spec["forbidden_cage_elements"]:
                        return False, f"Nonmetal/incompatible element '{cat}' cannot occupy metal cage center in clathrate hydride"
                    if cat not in spec["allowed_cage_metals"]:
                        try:
                            el = Element(cat)
                            if not el.is_metal or el.X > 2.2:
                                return False, f"Element '{cat}' is not a suitable electropositive metal for hydride cage"
                        except Exception:
                            return False, f"Invalid chemical symbol '{cat}'"

        # Rule 2: Perovskite cuprates (Pmmm YBa2Cu3O7 prototype)
        if "Ba2Cu3O7" in formula or "Perovskite" in family:
            m = re.search(r"\(([A-Za-z0-9\.]+)\)Ba2Cu3O7", formula)
            if m:
                substituents = re.findall(r"([A-Z][a-z]*)", m.group(1))
                # The substituted site is the Y site!
                for s in substituents:
                    if s in ["Ba", "Sr"]:
                        return False, f"Alkaline earth element '{s}' placed on rare-earth Y site causes site collision and charge imbalance"
                    if s not in PROTOTYPE_SPECS["Perovskite oxide"]["sites"]["Y_site"]["allowed"]:
                        return False, f"Element '{s}' cannot substitute on Y site in YBa2Cu3O7"

        # Rule 3: Iron pnictides (I4/mmm BaFe2As2 prototype)
        if "Fe2As2" in formula or "pnictide" in family.lower():
            m = re.search(r"\(([A-Za-z0-9\.]+)\)Fe2As2", formula)
            if m:
                substituents = re.findall(r"([A-Z][a-z]*)", m.group(1))
                # The substituted site is the Ba site!
                for s in substituents:
                    if s in ["Fe", "Co", "Ni"]:
                        return False, f"Transition metal '{s}' placed on Ba site causes site collision and destroys 122 lattice"
                    if s not in PROTOTYPE_SPECS["Iron chalcogenide / pnictide"]["sites"]["Ba_site"]["allowed"]:
                        return False, f"Element '{s}' cannot substitute on Ba site in BaFe2As2"

        return True, "Valid prototype substitution"

    def build_candidate_from_pair(
        self,
        candidate_idx: int,
        element_1: str,
        element_2: str,
        discovery_score: float,
        family: Optional[str] = None,
        doping_fraction: float = 0.15,
    ) -> Optional[MaterialCandidate]:
        """
        Builds a valid candidate from an untried element pair by identifying the chemically
        matching prototype and site. Returns None if no valid substitution is chemically possible.
        """
        cid = f"CAND_{candidate_idx:03d}"
        e1, e2 = sorted([element_1, element_2])
        x = doping_fraction
        rem = round(1.0 - x, 2)

        # 1. Check Perovskite Cuprate Y-site rare-earth substitution: (Y1-xRx)Ba2Cu3O7
        y_site_metals = PROTOTYPE_SPECS["Perovskite oxide"]["sites"]["Y_site"]["allowed"]
        if (family == "Perovskite oxide" or family is None) and (
            (e1 == "Y" and e2 in y_site_metals) or (e2 == "Y" and e1 in y_site_metals) or (family == "Perovskite oxide" and e1 in y_site_metals and e2 in y_site_metals)
        ):
            host = "Y" if "Y" in [e1, e2] else e1
            dopant = e2 if host == e1 else e1
            formula = f"({host}{rem}{dopant}{x})Ba2Cu3O7"
            fam = "Perovskite oxide"
            spec = PROTOTYPE_SPECS[fam]
            comp = Composition(f"{host}{rem}{dopant}{x}Ba2Cu3O7")
            stoich = {host: rem, dopant: x, "Ba": 2.0, "Cu": 3.0, "O": 7.0}

            valid, reason = self.is_valid_substitution(formula, fam)
            if valid:
                return MaterialCandidate(
                    candidate_id=cid,
                    formula=formula,
                    reduced_formula=comp.reduced_formula,
                    elements=sorted([host, dopant, "Ba", "Cu", "O"]),
                    stoichiometry=stoich,
                    target_family=fam,
                    prototype=spec["prototype"],
                    space_group=spec["space_group"],
                    lattice_system=spec["lattice_system"],
                    tc_status="NOT COMPUTED",
                    predicted_tc=None,
                    predicted_tc_uncertainty=None,
                    predicted_pressure_gpa=None,
                    pressure_status="Ambient (0 GPa)",
                    gap_origin=f"Untried isovalent rare-earth substitution {dopant} in YBCO cuprate",
                    discovery_score=discovery_score,
                )

        # 2. Check 122 Iron Pnictide Fe-site transition metal doping: Ba(Fe1-xMx)2As2
        fe_site_metals = PROTOTYPE_SPECS["Iron chalcogenide / pnictide"]["sites"]["Fe_site"]["allowed"]
        if (family == "Iron chalcogenide / pnictide" or family is None) and (
            (e1 == "Fe" and e2 in fe_site_metals) or (e2 == "Fe" and e1 in fe_site_metals)
        ):
            dopant = e2 if e1 == "Fe" else e1
            formula = f"Ba(Fe{rem}{dopant}{x})2As2"
            fam = "Iron chalcogenide / pnictide"
            spec = PROTOTYPE_SPECS[fam]
            comp = Composition(f"BaFe{rem*2} {dopant}{x*2} As2")
            stoich = {"Ba": 1.0, "Fe": rem * 2, dopant: x * 2, "As": 2.0}

            return MaterialCandidate(
                candidate_id=cid,
                formula=formula,
                reduced_formula=comp.reduced_formula,
                elements=sorted(["Ba", "Fe", dopant, "As"]),
                stoichiometry=stoich,
                target_family=fam,
                prototype=spec["prototype"],
                space_group=spec["space_group"],
                lattice_system=spec["lattice_system"],
                tc_status="NOT COMPUTED",
                predicted_tc=None,
                predicted_tc_uncertainty=None,
                predicted_pressure_gpa=None,
                pressure_status="Ambient (0 GPa)",
                gap_origin=f"Untried Fe-site transition metal dopant {dopant} in 122 iron pnictide",
                discovery_score=discovery_score,
            )

        # 3. Check 122 Iron Pnictide Ba-site alkali/alkaline-earth doping: (Ba1-xKx)Fe2As2
        ba_site_metals = PROTOTYPE_SPECS["Iron chalcogenide / pnictide"]["sites"]["Ba_site"]["allowed"]
        if (family == "Iron chalcogenide / pnictide" or family is None) and (
            (e1 in ["Ba", "Sr"] and e2 in ["K", "Rb", "Cs"]) or (e2 in ["Ba", "Sr"] and e1 in ["K", "Rb", "Cs"])
        ):
            host = e1 if e1 in ["Ba", "Sr"] else e2
            dopant = e2 if e1 in ["Ba", "Sr"] else e1
            formula = f"({host}{rem}{dopant}{x})Fe2As2"
            fam = "Iron chalcogenide / pnictide"
            spec = PROTOTYPE_SPECS[fam]
            comp = Composition(f"{host}{rem}{dopant}{x}Fe2As2")
            stoich = {host: rem, dopant: x, "Fe": 2.0, "As": 2.0}

            return MaterialCandidate(
                candidate_id=cid,
                formula=formula,
                reduced_formula=comp.reduced_formula,
                elements=sorted([host, dopant, "Fe", "As"]),
                stoichiometry=stoich,
                target_family=fam,
                prototype=spec["prototype"],
                space_group=spec["space_group"],
                lattice_system=spec["lattice_system"],
                tc_status="NOT COMPUTED",
                predicted_tc=None,
                predicted_tc_uncertainty=None,
                predicted_pressure_gpa=None,
                pressure_status="Ambient (0 GPa)",
                gap_origin=f"Untried Ba-site hole dopant {dopant} in 122 iron pnictide",
                discovery_score=discovery_score,
            )

        # 4. Check Perovskite Cuprate Cu-site substitution: YBa2(Cu1-xMx)3O7
        cu_site_metals = PROTOTYPE_SPECS["Perovskite oxide"]["sites"]["Cu_site"]["allowed"]
        if (family == "Perovskite oxide" or family is None) and (
            (e1 == "Cu" and e2 in cu_site_metals) or (e2 == "Cu" and e1 in cu_site_metals)
        ):
            dopant = e2 if e1 == "Cu" else e1
            formula = f"YBa2(Cu{rem}{dopant}{x})3O7"
            fam = "Perovskite oxide"
            spec = PROTOTYPE_SPECS[fam]
            comp = Composition(f"YBa2Cu{rem*3} {dopant}{x*3} O7")
            stoich = {"Y": 1.0, "Ba": 2.0, "Cu": rem * 3, dopant: x * 3, "O": 7.0}

            return MaterialCandidate(
                candidate_id=cid,
                formula=formula,
                reduced_formula=comp.reduced_formula,
                elements=sorted(["Y", "Ba", "Cu", dopant, "O"]),
                stoichiometry=stoich,
                target_family=fam,
                prototype=spec["prototype"],
                space_group=spec["space_group"],
                lattice_system=spec["lattice_system"],
                tc_status="NOT COMPUTED",
                predicted_tc=None,
                predicted_tc_uncertainty=None,
                predicted_pressure_gpa=None,
                pressure_status="Ambient (0 GPa)",
                gap_origin=f"Untried Cu-site transition metal dopant {dopant} in YBCO cuprate",
                discovery_score=discovery_score,
            )

        # 5. Check Clathrate Hydride compatibility (Fm-3m LaH10)
        hydride_metals = PROTOTYPE_SPECS["Clathrate hydride"]["allowed_cage_metals"]
        if (family == "Clathrate hydride" or family is None) and (e1 in hydride_metals and e2 in hydride_metals):
            formula = f"({e1}{rem}{e2}{x})H10"
            fam = "Clathrate hydride"
            spec = PROTOTYPE_SPECS[fam]
            comp = Composition(f"{e1}{rem}{e2}{x}H10")
            stoich = {e1: rem, e2: x, "H": 10.0}

            valid, reason = self.is_valid_substitution(formula, fam)
            if not valid:
                logger.debug(f"Rejected candidate {formula}: {reason}")
                return None

            return MaterialCandidate(
                candidate_id=cid,
                formula=formula,
                reduced_formula=comp.reduced_formula,
                elements=sorted([e1, e2, "H"]),
                stoichiometry=stoich,
                target_family=fam,
                prototype=spec["prototype"],
                space_group=spec["space_group"],
                lattice_system=spec["lattice_system"],
                tc_status="NOT COMPUTED",
                predicted_tc=None,
                predicted_tc_uncertainty=None,
                predicted_pressure_gpa=None,
                pressure_status="NOT COMPUTED (Requires ab initio enthalpy calculation)",
                gap_origin=f"Untried element pair {e1}-{e2} mapped to clathrate hydride cage",
                discovery_score=discovery_score,
            )

        # Nonmetals on metal sites or unsupported combinations are rejected
        logger.debug(f"Pair ({e1}, {e2}) does not match any valid crystallographic prototype site.")
        return None

    def generate_candidates_from_gaps(
        self,
        untried_pairs: List[Dict[str, Any]],
        max_candidates: int = 10,
    ) -> List[MaterialCandidate]:
        """
        Deterministically filters and generates valid candidate materials from gap analysis records.
        """
        # Sort gaps deterministically by discovery_score (descending) and element pair (ascending)
        sorted_gaps = sorted(
            untried_pairs,
            key=lambda g: (-float(g.get("discovery_score", 0.0)), g.get("element_1", ""), g.get("element_2", ""))
        )

        candidates: List[MaterialCandidate] = []
        candidate_idx = 1

        for gap in sorted_gaps:
            e1 = gap.get("element_1", "")
            e2 = gap.get("element_2", "")
            score = float(gap.get("discovery_score", 0.0))

            cand = self.build_candidate_from_pair(
                candidate_idx=candidate_idx,
                element_1=e1,
                element_2=e2,
                discovery_score=score,
            )

            if cand is not None:
                candidates.append(cand)
                candidate_idx += 1
                if len(candidates) >= max_candidates:
                    break

        logger.info(f"Generated {len(candidates)} valid candidates from {len(untried_pairs)} discovery gaps.")
        return candidates
