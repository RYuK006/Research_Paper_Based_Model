"""
Candidate Material Generator.
Translates Layer 2 discovery gaps (untried element combinations & unfollowed hypotheses)
into concrete chemical candidates with balanced stoichiometries and crystal lattice assignments.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("candidate_generator")

# Known structural archetypes for materials discovery
CRYSTAL_ARCHETYPES = {
    "Clathrate hydride": {
        "prototype": "LaH10",
        "space_group": "Fm-3m (#225)",
        "lattice_system": "Cubic",
        "base_pressure_gpa": 170.0,
        "base_tc_range": (240.0, 265.0),
        "stoichiometry_pattern": "A1-x Bx H10",
    },
    "Perovskite oxide": {
        "prototype": "YBa2Cu3O7",
        "space_group": "Pmmm (#47)",
        "lattice_system": "Orthorhombic",
        "base_pressure_gpa": 0.0001,
        "base_tc_range": (90.0, 105.0),
        "stoichiometry_pattern": "A Ba2 (Cu1-x Bx)3 O7",
    },
    "Iron chalcogenide / pnictide": {
        "prototype": "FeSe / BaFe2As2",
        "space_group": "P4/nmm (#129)",
        "lattice_system": "Tetragonal",
        "base_pressure_gpa": 2.0,
        "base_tc_range": (35.0, 55.0),
        "stoichiometry_pattern": "A1-x Bx Fe2 As2",
    },
    "Boride / Carbide": {
        "prototype": "MgB2",
        "space_group": "P6/mmm (#191)",
        "lattice_system": "Hexagonal",
        "base_pressure_gpa": 0.0001,
        "base_tc_range": (35.0, 48.0),
        "stoichiometry_pattern": "(M1-x Bx) B2",
    },
}


@dataclass
class MaterialCandidate:
    """Represents a proposed novel material candidate for computational and experimental verification."""
    candidate_id: str
    formula: str
    elements: List[str]
    stoichiometry: Dict[str, float]
    target_family: str
    space_group: str
    lattice_system: str
    predicted_tc_range: Tuple[float, float]
    predicted_pressure_gpa: float
    gap_origin: str
    discovery_score: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CandidateGenerator:
    """
    Generates structured chemical candidates from Layer 2 discovery gaps.
    """

    def __init__(self) -> None:
        pass

    def generate_candidate_from_element_gap(
        self,
        candidate_idx: int,
        element_1: str,
        element_2: str,
        discovery_score: float,
        family: str = "Clathrate hydride",
        doping_fraction: float = 0.15,
    ) -> MaterialCandidate:
        """
        Builds a candidate formula by co-doping the untried element pair into a structural archetype.
        """
        cid = f"CAND_{candidate_idx:03d}"
        archetype = CRYSTAL_ARCHETYPES.get(family, CRYSTAL_ARCHETYPES["Clathrate hydride"])

        # Determine host vs dopant
        x = doping_fraction
        rem = round(1.0 - x, 2)

        if family == "Clathrate hydride":
            formula = f"({element_1}{rem}{element_2}{x})H10"
            stoich = {element_1: rem, element_2: x, "H": 10.0}
            elems = sorted([element_1, element_2, "H"])
            # Pressure reduction heuristic from chemical precompression
            pred_pressure = max(50.0, archetype["base_pressure_gpa"] * (1.0 - (doping_fraction * 0.4)))
            pred_tc = (archetype["base_tc_range"][0] + 5.0, archetype["base_tc_range"][1] + 15.0)

        elif family == "Perovskite oxide":
            formula = f"({element_1}{rem}{element_2}{x})Ba2Cu3O7"
            stoich = {element_1: rem, element_2: x, "Ba": 2.0, "Cu": 3.0, "O": 7.0}
            elems = sorted([element_1, element_2, "Ba", "Cu", "O"])
            pred_pressure = 0.0001
            pred_tc = (archetype["base_tc_range"][0] - 2.0, archetype["base_tc_range"][1] + 8.0)

        else:
            formula = f"({element_1}{rem}{element_2}{x})Fe2As2"
            stoich = {element_1: rem, element_2: x, "Fe": 2.0, "As": 2.0}
            elems = sorted([element_1, element_2, "Fe", "As"])
            pred_pressure = archetype["base_pressure_gpa"]
            pred_tc = archetype["base_tc_range"]

        return MaterialCandidate(
            candidate_id=cid,
            formula=formula,
            elements=elems,
            stoichiometry=stoich,
            target_family=family,
            space_group=archetype["space_group"],
            lattice_system=archetype["lattice_system"],
            predicted_tc_range=pred_tc,
            predicted_pressure_gpa=round(pred_pressure, 1),
            gap_origin=f"Untried element pair {element_1}-{element_2} from literature co-occurrence analysis",
            discovery_score=discovery_score,
        )

    def generate_candidates_from_gaps(
        self,
        untried_pairs: List[Dict[str, Any]],
        max_candidates: int = 10,
    ) -> List[MaterialCandidate]:
        """Batch generates candidates from Layer 2 discovery gaps."""
        candidates = []
        for idx, gap in enumerate(untried_pairs[:max_candidates], 1):
            e1 = gap.get("element_1", "La")
            e2 = gap.get("element_2", "Y")
            score = float(gap.get("discovery_score", 100.0))

            # Select family based on elements
            if "H" in gap.get("shared_partner_elements", []) or e1 in ["La", "Y", "Ce", "Th", "Ca"]:
                family = "Clathrate hydride"
            elif "Cu" in gap.get("shared_partner_elements", []) or "O" in gap.get("shared_partner_elements", []):
                family = "Perovskite oxide"
            else:
                family = "Iron chalcogenide / pnictide"

            cand = self.generate_candidate_from_element_gap(
                candidate_idx=idx,
                element_1=e1,
                element_2=e2,
                discovery_score=score,
                family=family,
            )
            candidates.append(cand)

        logger.info(f"Generated {len(candidates)} material candidates from discovery gaps.")
        return candidates
