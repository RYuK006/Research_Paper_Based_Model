"""
Experimental Synthesis Protocol Designer.
Generates lab-ready synthesis protocols, precursor specifications, pressure-temperature profiles,
and characterization sequences for computationally verified material candidates.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from candidate_pipeline.generator import MaterialCandidate
from candidate_pipeline.verifier import VerificationResult

logger = logging.getLogger("protocol_designer")


@dataclass
class ExperimentalProtocol:
    """Detailed laboratory synthesis and characterization protocol for a candidate material."""
    candidate_id: str
    formula: str
    target_family: str
    recommended_synthesis_method: str
    starting_precursors: List[str]
    synthesis_conditions: Dict[str, Any]  # Pressure, temperature, duration, atmosphere
    characterization_plan: List[str]
    safety_notes: List[str]
    template_status: str = "UNVALIDATED HEURISTIC TEMPLATE (NOT EXPERIMENTALLY CERTIFIED)"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines = [
            f"### Protocol for Candidate {self.candidate_id}: `{self.formula}`",
            "> [!WARNING]",
            "> **UNVALIDATED HEURISTIC TEMPLATE**: This synthesis recipe is an uncalibrated heuristic template derived from structural archetypes. It has NOT been experimentally validated in a wet lab and must be verified before execution.",
            "",
            f"- **Protocol Status**: `{self.template_status}`",
            f"- **Target Structural Family**: {self.target_family}",
            f"- **Recommended Method**: **{self.recommended_synthesis_method}**",
            "",
            "#### 1. Starting Precursors & Reagents",
        ]
        for p in self.starting_precursors:
            lines.append(f"  - {p}")

        lines.extend([
            "",
            "#### 2. Synthesis Parameters & Conditions",
            f"  - **Target Pressure**: {self.synthesis_conditions.get('pressure', 'Ambient')}",
            f"  - **Reaction Temperature**: {self.synthesis_conditions.get('temperature', 'Room temperature')}",
            f"  - **Reaction Duration**: {self.synthesis_conditions.get('duration', 'Standard')}",
            f"  - **Atmosphere / Cell Medium**: {self.synthesis_conditions.get('atmosphere', 'Inert Ar')}",
            "",
            "#### 3. Diagnostic Characterization Sequence",
        ])
        for c in self.characterization_plan:
            lines.append(f"  - {c}")

        lines.extend([
            "",
            "#### 4. Safety & Handling",
        ])
        for s in self.safety_notes:
            lines.append(f"  - ⚠️ {s}")

        return "\n".join(lines)


class ProtocolDesigner:
    """
    Designs tailored experimental synthesis protocols for material candidates.
    """

    def __init__(self) -> None:
        pass

    def design_protocol(
        self,
        candidate: MaterialCandidate,
        verification: Optional[VerificationResult] = None,
    ) -> ExperimentalProtocol:
        """Constructs an experimental recipe tailored to candidate family and composition."""
        fam = candidate.target_family.lower()
        non_h_elems = [e for e in candidate.elements if e != "H"]

        if "hydride" in fam:
            method = "Laser-heated diamond anvil cell (LH-DAC)"
            precursors = [
                f"High-purity ({', '.join(non_h_elems)}) metal foil or powder (purity $\\ge 99.99\\%$), stoichiometrically weighed.",
                "Ammonia borane (NH3BH3) or pure molecular H2 gas loading as clean hydrogen donor.",
                "Rhenium or tungsten gasket pre-indented to 25-35 $\\mu$m thickness with 100 $\\mu$m sample chamber.",
            ]
            conditions = {
                "pressure": f"{candidate.predicted_pressure_gpa or 'Target megabar'} GPa (monitored via diamond anvil Raman / ruby fluorescence)",
                "temperature": "1800 - 2200 K (double-sided pulsed Nd:YAG laser heating at $\\lambda=1064$ nm)",
                "duration": "10 - 20 minutes laser annealing to induce cage phase nucleation",
                "atmosphere": "Cryogenic or pressurized hydrogen environment inside sealed DAC",
            }
            charact = [
                f"In-situ Synchrotron Powder X-ray Diffraction ($\\lambda=0.434$ Å) to confirm {candidate.space_group} clathrate lattice formation.",
                "Four-probe electrical resistance using sputtered Pt/Ti microelectrodes deposited on diamond culet.",
                "Measure resistance transition: verify zero-resistance state and critical transition down to 2 K.",
                "Magnetic susceptibility / AC susceptibility to confirm Meissner diamagnetic shielding.",
            ]
            safety = [
                "Extreme pressure risk: Diamond anvil culet cleavage during laser pulsing; operate behind blast shielding.",
                "Pressurized hydrogen embrittlement: Inspect gasket seal integrity prior to heating.",
            ]

        elif "perovskite" in fam:
            method = "Pulsed Laser Deposition (PLD) & Solid-State Reaction"
            precursors = [
                f"Stoichiometric oxides/carbonates of {', '.join(candidate.elements)} (e.g. BaCO3, CuO, Y2O3).",
                "Single-crystal substrate: SrTiO3 (001) or LaAlO3 (001) for epitaxial film growth.",
            ]
            conditions = {
                "pressure": "0.2 - 0.4 mbar dynamic O2 partial pressure during ablation; 1 atm post-anneal",
                "temperature": "780 - 820 °C deposition; 450 °C for 10 hours oxygenation anneal",
                "duration": "45 minutes ablation at 2-5 Hz KrF excimer laser ($\\lambda=248$ nm)",
                "atmosphere": "Pure oxygen (O2) environment to eliminate oxygen vacancies",
            }
            charact = [
                f"High-resolution XRD $\\theta-2\\theta$ scans to verify c-axis epitaxial orientation and space group {candidate.space_group}.",
                "Four-point probe electrical resistivity from 300 K down to 4.2 K in cryostat.",
                "SQUID vibrating sample magnetometry (VSM) to quantify superconducting volume fraction.",
            ]
            safety = [
                "UV Excimer Laser radiation hazard: Class 4 laser safety goggles required during PLD ablation.",
                "Fine oxide/carbonate particulate inhalation risk during stoichiometric powder grinding.",
            ]

        else:
            method = "High-Temperature Flux Growth & Arc Melting"
            precursors = [
                f"High-purity elemental ingots of {', '.join(candidate.elements)}.",
                "Self-flux medium (e.g. excess FeAs or Sn flux) inside evacuated quartz/alumina ampoule.",
            ]
            conditions = {
                "pressure": f"{candidate.predicted_pressure_gpa or 'Ambient (0 GPa)'} (or sealed evacuated tube)",
                "temperature": "1150 °C for 24h, followed by slow cooling at 2-4 °C/hour down to 750 °C",
                "duration": "7 to 10 days crystal growth cycle",
                "atmosphere": "High vacuum ($< 10^{-4}$ mbar) sealed in silica ampoule with Ta foil getter",
            }
            charact = [
                f"Single-crystal X-ray diffraction (SC-XRD) to refine tetragonal structure ({candidate.space_group}).",
                "Energy-dispersive X-ray spectroscopy (EDX/SEM) to confirm stoichiometric element ratio.",
                "Temperature-dependent electrical resistivity and Hall effect to probe carrier density.",
            ]
            safety = [
                "Toxic volatile vapors (e.g. As / Se sublimation) if ampoule ruptures at 1150 °C: Handle strictly in negative-pressure fume hood.",
                "Thermal stress ampoule explosion risk during furnace ramp-down.",
            ]

        return ExperimentalProtocol(
            candidate_id=candidate.candidate_id,
            formula=candidate.formula,
            target_family=candidate.target_family,
            recommended_synthesis_method=method,
            starting_precursors=precursors,
            synthesis_conditions=conditions,
            characterization_plan=charact,
            safety_notes=safety,
        )

    def design_protocols_batch(
        self,
        candidates: List[MaterialCandidate],
    ) -> List[ExperimentalProtocol]:
        """Designs protocols for a batch of candidate materials."""
        return [self.design_protocol(c) for c in candidates]

