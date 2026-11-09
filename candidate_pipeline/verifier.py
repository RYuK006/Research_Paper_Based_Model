"""
Computational Verification and Stability Harness for Candidate Superconductors.
Evaluates:
1. Prefilter heuristics (tolerance factor, electronegativity spread) - strictly labeled as prefilters.
2. Real thermodynamic stability: Energy Above Hull (E_above_hull) in meV/atom against Materials Project phase diagrams.
3. Tc & Pressure policy: Removes all hardcoded templates; reports 'NOT COMPUTED' unless empirically/theoretically calculated.
4. Generates marked 'NOT RUN' Quantum ESPRESSO electron-phonon input decks for hydrides.
"""

from __future__ import annotations

import logging
import math
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
from pymatgen.core import Composition, Element

from candidate_pipeline.generator import MaterialCandidate
from candidate_pipeline.qe_input_generator import generate_qe_input_decks

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

# Shannon Ionic Radii (Angstroms)
IONIC_RADII = {
    "H": 0.25, "O": 1.40, "F": 1.33, "Cl": 1.81, "S": 1.84, "Se": 1.98,
    "La": 1.16, "Y": 1.02, "Ba": 1.42, "Sr": 1.26, "Ca": 1.12, "Cu": 0.73,
    "Fe": 0.65, "Co": 0.65, "Ni": 0.69, "As": 0.58, "Mg": 0.72, "B": 0.27,
    "Th": 1.05, "Ce": 1.01, "K": 1.38, "In": 0.80, "Cs": 1.67, "V": 0.54,
    "Gd": 1.05, "Nd": 1.11, "Sm": 1.08, "Eu": 1.07,
}


@dataclass
class PrefilterMetrics:
    """Heuristic sanity prefilter (explicitly not a thermodynamic stability score)."""
    goldschmidt_tolerance: Optional[float]
    electronegativity_spread: float
    precompression_index: float
    prefilter_status: str  # 'PASS', 'FLAGGED'

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ThermodynamicStability:
    """Rigorous thermodynamic stability evaluated against convex hull."""
    energy_above_hull_mev: Optional[float]
    stability_status: str  # 'ON_CONVEX_HULL (0 meV)', 'METASTABLE (< 50 meV/atom)', 'UNSTABLE (> 50 meV/atom)', 'NOT COMPUTED'
    method: str  # e.g., 'Materials Project Phase Diagram v0.88.1'
    reference_data_version: str
    competing_phases: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VerificationResult:
    """Comprehensive verification outcome for candidate material."""
    candidate_id: str
    formula: str
    prefilter: PrefilterMetrics
    stability: ThermodynamicStability
    tc_source: str  # 'NOT COMPUTED' or 'GroupKFold Regressor (OOD / Uncertainty)'
    predicted_tc: Optional[float]
    predicted_tc_uncertainty: Optional[float]
    pressure_source: str
    predicted_pressure_gpa: Optional[float]
    qe_input_files: Optional[Dict[str, str]]
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "formula": self.formula,
            "prefilter": self.prefilter.to_dict(),
            "stability": self.stability.to_dict(),
            "tc_source": self.tc_source,
            "predicted_tc": self.predicted_tc,
            "predicted_tc_uncertainty": self.predicted_tc_uncertainty,
            "pressure_source": self.pressure_source,
            "predicted_pressure_gpa": self.predicted_pressure_gpa,
            "qe_input_files": self.qe_input_files,
            "notes": self.notes,
        }


class CandidateVerifier:
    """
    Evaluates candidate materials with rigorous thermodynamic stability checks,
    labeled heuristic prefilters, and strict removal of template Tc values.
    """

    def __init__(
        self,
        mp_api_key: Optional[str] = None,
        qe_output_dir: str = "data/dft_inputs",
        timeout_seconds: float = 12.0,
    ) -> None:
        self.mp_api_key = mp_api_key or os.environ.get("MP_API_KEY", "h8yUPGpRyq8vEc8u5Ks5DH7KcA6YaX6S")
        self.qe_output_dir = Path(qe_output_dir)
        self.timeout = timeout_seconds

    def evaluate_prefilter(self, candidate: MaterialCandidate) -> PrefilterMetrics:
        """Evaluates heuristic prefilter (tolerance factor, electronegativity spread)."""
        elements = candidate.elements
        vals = [ELECTRONEGATIVITIES.get(e, 1.5) for e in elements]
        en_spread = round(max(vals) - min(vals), 3) if vals else 0.0

        tolerance = None
        if "Perovskite" in candidate.target_family:
            r_A = IONIC_RADII.get(candidate.elements[0], 1.15)
            r_B = IONIC_RADII.get("Cu", 0.73)
            r_X = IONIC_RADII.get("O", 1.40)
            tolerance = round((r_A + r_X) / (math.sqrt(2.0) * (r_B + r_X)), 4)

        precomp = 1.0
        if "hydride" in candidate.target_family.lower():
            cations = [e for e in candidate.elements if e != "H"]
            radii = [IONIC_RADII.get(c, 1.1) for c in cations]
            mean_r = sum(radii) / max(1, len(radii))
            precomp = round(1.0 + (1.20 - mean_r) * 0.4, 3)

        status = "PASS"
        if tolerance is not None and (tolerance < 0.75 or tolerance > 1.05):
            status = "FLAGGED"
        if en_spread > 2.8:
            status = "FLAGGED"

        return PrefilterMetrics(
            goldschmidt_tolerance=tolerance,
            electronegativity_spread=en_spread,
            precompression_index=precomp,
            prefilter_status=status,
        )

    def compute_thermodynamic_stability(self, candidate: MaterialCandidate) -> ThermodynamicStability:
        """
        Computes energy above hull vs Materials Project phase diagram.
        Reports exact number in meV/atom, method, and reference version.
        """
        if not self.mp_api_key:
            return ThermodynamicStability(
                energy_above_hull_mev=None,
                stability_status="NOT COMPUTED (Materials Project API key not configured)",
                method="None",
                reference_data_version="None",
                competing_phases=[],
            )

        chemsys = "-".join(sorted(candidate.elements))
        headers = {"X-API-KEY": self.mp_api_key}
        url = f"https://api.materialsproject.org/materials/summary/?chemsys={chemsys}&_limit=10&_fields=material_id,formula_pretty,energy_above_hull,formation_energy_per_atom"

        try:
            r = httpx.get(url, headers=headers, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()
                entries = data.get("data", [])
                if not entries:
                    # System not in ambient MP database (common for high-pressure hydrides or novel dopings)
                    return ThermodynamicStability(
                        energy_above_hull_mev=None,
                        stability_status="NOT COMPUTED (No ambient MP phase diagram entry for chemsys; requires high-pressure DFT relaxation)",
                        method="Materials Project Phase Diagram (chemsys query)",
                        reference_data_version="MP API v0.88.1",
                        competing_phases=[],
                    )

                # Check if exact reduced formula is in MP entries
                comp = Composition(candidate.formula.replace("(", "").replace(")", ""))
                matching_entry = None
                for entry in entries:
                    if entry.get("formula_pretty") == comp.reduced_formula:
                        matching_entry = entry
                        break

                competing = [f"{e.get('formula_pretty')} ({e.get('material_id')})" for e in entries[:3]]

                if matching_entry is not None and matching_entry.get("energy_above_hull") is not None:
                    e_hull_ev = float(matching_entry["energy_above_hull"])
                    e_hull_mev = round(e_hull_ev * 1000.0, 1)
                    if e_hull_mev <= 0.05:
                        stat = "ON_CONVEX_HULL (0.0 meV/atom - Ground State)"
                    elif e_hull_mev < 50.0:
                        stat = f"METASTABLE ({e_hull_mev:.1f} meV/atom above hull)"
                    else:
                        stat = f"UNSTABLE ({e_hull_mev:.1f} meV/atom above hull)"

                    return ThermodynamicStability(
                        energy_above_hull_mev=e_hull_mev,
                        stability_status=stat,
                        method="Materials Project DFT Convex Hull (exact formula match)",
                        reference_data_version="MP API v0.88.1",
                        competing_phases=competing,
                    )
                else:
                    # Endmember phases exist; proposed doped solution requires relaxation
                    min_hull_ev = min((e.get("energy_above_hull") or 0.0) for e in entries)
                    min_hull_mev = round(min_hull_ev * 1000.0, 1)
                    return ThermodynamicStability(
                        energy_above_hull_mev=None,
                        stability_status=f"NOT COMPUTED (Solid solution in {chemsys}; competing phases present, lowest ground state E_hull={min_hull_mev:.1f} meV/atom)",
                        method="Materials Project Phase Diagram (solid solution interpolation required)",
                        reference_data_version="MP API v0.88.1",
                        competing_phases=competing,
                    )
            else:
                return ThermodynamicStability(
                    energy_above_hull_mev=None,
                    stability_status=f"NOT COMPUTED (Materials Project API returned HTTP {r.status_code})",
                    method="Materials Project Phase Diagram",
                    reference_data_version="MP API v0.88.1",
                    competing_phases=[],
                )
        except Exception as e:
            return ThermodynamicStability(
                energy_above_hull_mev=None,
                stability_status=f"NOT COMPUTED (Materials Project query error: {str(e)[:80]})",
                method="Materials Project Phase Diagram",
                reference_data_version="MP API v0.88.1",
                competing_phases=[],
            )

    def verify_candidate(self, candidate: MaterialCandidate) -> VerificationResult:
        """
        Runs comprehensive verification on candidate material:
        - Prefilter checks
        - Real thermodynamic stability
        - Strict Tc policy: NOT COMPUTED unless empirically trained model is provided
        - Generates watermarked Quantum ESPRESSO decks for hydrides
        """
        prefilter = self.evaluate_prefilter(candidate)
        stability = self.compute_thermodynamic_stability(candidate)

        # Tc Policy: All templates removed! Output 'NOT COMPUTED'
        tc_source = "Tc: NOT COMPUTED (Template values purged; requires ab initio electron-phonon calculation or calibrated model)"
        predicted_tc = None
        predicted_tc_unc = None

        # Pressure Policy: Output 'NOT COMPUTED' unless determined by enthalpy curve
        if "hydride" in candidate.target_family.lower():
            pressure_source = "Pressure: NOT COMPUTED (Requires ab initio H(P) enthalpy calculation vs decomposition products)"
            pred_pressure = None
            # Generate Quantum ESPRESSO input decks clearly marked as NOT RUN
            decks = generate_qe_input_decks(
                formula=candidate.formula,
                space_group=candidate.space_group,
                output_dir=self.qe_output_dir,
                pressure_gpa=150.0,
            )
            qe_files = {k: str(v) for k, v in decks.items()}
        else:
            pressure_source = "Ambient Pressure (0 GPa)"
            pred_pressure = 0.0001
            qe_files = None

        notes = [
            f"Prefilter status: {prefilter.prefilter_status}",
            f"Thermodynamic stability: {stability.stability_status}",
            f"Method: {stability.method} (Data version: {stability.reference_data_version})",
        ]
        if stability.energy_above_hull_mev is not None:
            notes.append(f"Energy above convex hull: {stability.energy_above_hull_mev:.1f} meV/atom")

        return VerificationResult(
            candidate_id=candidate.candidate_id,
            formula=candidate.formula,
            prefilter=prefilter,
            stability=stability,
            tc_source=tc_source,
            predicted_tc=predicted_tc,
            predicted_tc_uncertainty=predicted_tc_unc,
            pressure_source=pressure_source,
            predicted_pressure_gpa=pred_pressure,
            qe_input_files=qe_files,
            notes=notes,
        )

    def verify_candidates(self, candidates: List[MaterialCandidate]) -> List[VerificationResult]:
        """Runs verification across a batch of candidates."""
        return [self.verify_candidate(c) for c in candidates]
