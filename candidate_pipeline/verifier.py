"""
Computational Verification Harness for Candidate Materials.
Evaluates chemical plausibility, Pauling electronegativities, Goldschmidt tolerance factors,
and chemical precompression to score thermodynamic viability.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from candidate_pipeline.generator import MaterialCandidate

logger = logging.getLogger("candidate_verifier")

# Pauling Electronegativities
ELECTRONEGATIVITIES = {
    "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "K": 0.82, "Ca": 1.00, "Sc": 1.36, "Ti": 1.54, "V": 1.63, "Cr": 1.66, "Mn": 1.55,
    "Fe": 1.83, "Co": 1.88, "Ni": 1.91, "Cu": 1.90, "Zn": 1.65, "Ga": 1.81, "Ge": 2.01,
    "As": 2.18, "Se": 2.55, "Br": 2.96, "Rb": 0.82, "Sr": 0.95, "Y": 1.22, "Zr": 1.33,
    "Nb": 1.60, "Mo": 2.16, "Tc": 1.90, "Ru": 2.20, "Rh": 2.28, "Pd": 2.20, "Ag": 1.93,
    "Cd": 1.69, "In": 1.78, "Sn": 1.96, "Sb": 2.05, "Te": 2.10, "I": 2.66, "Cs": 0.79,
    "Ba": 0.89, "La": 1.10, "Ce": 1.12, "Pr": 1.13, "Nd": 1.14, "Th": 1.30, "U": 1.38,
}

# Shannon Ionic Radii (in Angstroms, coordination ~6/8/12)
IONIC_RADII = {
    "H": 0.25, "O": 1.40, "F": 1.33, "Cl": 1.81, "S": 1.84, "Se": 1.98,
    "La": 1.16, "Y": 1.02, "Ba": 1.42, "Sr": 1.26, "Ca": 1.12, "Cu": 0.73,
    "Fe": 0.65, "Co": 0.65, "Ni": 0.69, "As": 0.58, "Mg": 0.72, "B": 0.27,
    "Th": 1.05, "Ce": 1.01, "K": 1.38, "In": 0.80, "Cs": 1.67, "V": 0.54,
}


@dataclass
class VerificationResult:
    """Evaluation metrics for candidate physical viability."""
    candidate_id: str
    formula: str
    plausibility_status: str  # 'HIGHLY_PROMISING', 'VIABLE', 'METASTABLE'
    stability_score: float  # 0.0 to 1.0
    goldschmidt_tolerance: Optional[float]
    electronegativity_diff: float
    chemical_precompression_index: float
    verification_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CandidateVerifier:
    """
    Evaluates physical plausibility and stability heuristics for proposed material candidates.
    """

    def __init__(self) -> None:
        pass

    def calculate_goldschmidt_tolerance(self, candidate: MaterialCandidate) -> Optional[float]:
        """Calculates Goldschmidt tolerance factor for perovskite-type materials: t = (rA + rX) / (sqrt(2) * (rB + rX))."""
        if "Perovskite" not in candidate.target_family:
            return None

        # Approximate cation A as host rare-earth/alkaline earth, B as Cu/transition metal, X as O
        r_A = IONIC_RADII.get(candidate.elements[0], 1.15)
        r_B = IONIC_RADII.get("Cu", 0.73)
        r_X = IONIC_RADII.get("O", 1.40)

        t = (r_A + r_X) / (math.sqrt(2.0) * (r_B + r_X))
        return round(t, 4)

    def calculate_electronegativity_spread(self, elements: List[str]) -> float:
        """Calculates max electronegativity difference across constituents."""
        vals = [ELECTRONEGATIVITIES.get(e, 1.5) for e in elements]
        if not vals:
            return 0.0
        return round(max(vals) - min(vals), 3)

    def calculate_precompression_index(self, candidate: MaterialCandidate) -> float:
        """Heuristic for chemical precompression in hydride clathrate cages."""
        if "hydride" not in candidate.target_family.lower():
            return 1.0

        # Heavier cations shrink hydrogen cage volume
        cations = [e for e in candidate.elements if e != "H"]
        radii = [IONIC_RADII.get(c, 1.1) for c in cations]
        avg_radius = sum(radii) / max(1, len(radii))
        # Optimal clathrate cage radius ~ 1.05 - 1.15 A
        optimality = 1.0 - abs(avg_radius - 1.10)
        return max(0.5, min(round(optimality, 3), 1.0))

    def verify_candidate(self, candidate: MaterialCandidate) -> VerificationResult:
        """Runs full computational verification suite on a single candidate."""
        notes = []
        score = 0.5

        # 1. Electronegativity Check
        en_diff = self.calculate_electronegativity_spread(candidate.elements)
        if 0.5 <= en_diff <= 2.5:
            score += 0.2
            notes.append("Favorable polar-covalent / metallic hybridization for electronic transport.")
        else:
            notes.append(f"High electronegativity delta ({en_diff}); potential ionic insulating tendency.")

        # 2. Tolerance / Packing
        tol = self.calculate_goldschmidt_tolerance(candidate)
        if tol is not None:
            if 0.85 <= tol <= 1.02:
                score += 0.25
                notes.append(f"Goldschmidt tolerance factor t={tol:.3f} within optimal cubic/orthorhombic perovskite stability window.")
            else:
                score += 0.1
                notes.append(f"Tolerance factor t={tol:.3f} indicates significant Jahn-Teller or octahedral tilt distortion.")

        # 3. Chemical Precompression (for Hydrides)
        precomp = self.calculate_precompression_index(candidate)
        if "hydride" in candidate.target_family.lower():
            if precomp >= 0.85:
                score += 0.25
                notes.append(f"High precompression index ({precomp:.2f}): Dopant cations induce steric pressure, stabilizing H-clathrate cage at reduced external pressure.")
            else:
                notes.append(f"Moderate precompression index ({precomp:.2f}).")

        # Status
        final_score = min(round(score, 3), 1.0)
        if final_score >= 0.80:
            status = "HIGHLY_PROMISING"
        elif final_score >= 0.60:
            status = "VIABLE"
        else:
            status = "METASTABLE"

        return VerificationResult(
            candidate_id=candidate.candidate_id,
            formula=candidate.formula,
            plausibility_status=status,
            stability_score=final_score,
            goldschmidt_tolerance=tol,
            electronegativity_diff=en_diff,
            chemical_precompression_index=precomp,
            verification_notes=notes,
        )

    def verify_candidates_batch(
        self,
        candidates: List[MaterialCandidate],
    ) -> List[VerificationResult]:
        """Batch verifies a list of candidate materials."""
        results = [self.verify_candidate(c) for c in candidates]
        results.sort(key=lambda x: x.stability_score, reverse=True)
        return results
