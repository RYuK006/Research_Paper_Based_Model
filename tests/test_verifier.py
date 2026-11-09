"""
Unit tests for Candidate Verifier and Thermodynamic Stability (candidate_pipeline/verifier.py).
Verifies:
1. Real stability calculation (E_above_hull in meV/atom, method, reference data version).
2. Prefilter heuristics are labeled strictly as prefilter, never stability status.
3. Tc policy: template values purged, returns 'Tc: NOT COMPUTED'.
4. Hydrides generate Quantum ESPRESSO decks clearly marked 'NOT RUN'.
"""

import tempfile
import unittest
from pathlib import Path

from candidate_pipeline.generator import CandidateGenerator
from candidate_pipeline.verifier import CandidateVerifier, VerificationResult


class TestCandidateVerifier(unittest.TestCase):
    """Test suite for thermodynamic stability, prefilters, and Tc policy."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.qe_dir = Path(self.temp_dir.name) / "dft_decks"
        self.generator = CandidateGenerator(seed=42)
        self.verifier = CandidateVerifier(qe_output_dir=str(self.qe_dir))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_stability_and_prefilter_separation(self) -> None:
        """Test that heuristic prefilters and thermodynamic stability are strictly separated."""
        cand = self.generator.build_candidate_from_pair(1, "Fe", "Co", 350.0)
        self.assertIsNotNone(cand)

        res = self.verifier.verify_candidate(cand)
        self.assertIsInstance(res, VerificationResult)

        # Prefilter assertions
        self.assertIn(res.prefilter.prefilter_status, ["PASS", "FLAGGED"])
        self.assertIsInstance(res.prefilter.electronegativity_spread, float)

        # Stability assertions
        self.assertIsNotNone(res.stability.stability_status)
        self.assertIn("Materials Project", res.stability.method)
        self.assertEqual(res.stability.reference_data_version, "MP API v0.88.1")

    def test_tc_template_purged(self) -> None:
        """Test that all hardcoded family templates are purged and Tc is reported as NOT COMPUTED."""
        cand = self.generator.build_candidate_from_pair(1, "La", "Y", 450.0)
        self.assertIsNotNone(cand)

        res = self.verifier.verify_candidate(cand)
        self.assertIsNone(res.predicted_tc, "Predicted Tc must be None when not empirically computed")
        self.assertIn("NOT COMPUTED", res.tc_source)
        self.assertIn("NOT COMPUTED", res.pressure_source)

    def test_hydride_qe_input_generation_marked_not_run(self) -> None:
        """Test that Quantum ESPRESSO decks are generated for hydrides with explicit NOT RUN watermark."""
        cand = self.generator.build_candidate_from_pair(1, "La", "Y", 450.0)
        self.assertIsNotNone(cand)

        res = self.verifier.verify_candidate(cand)
        self.assertIsNotNone(res.qe_input_files)
        self.assertIn("pw_in", res.qe_input_files)
        self.assertIn("ph_in", res.qe_input_files)

        pw_file = Path(res.qe_input_files["pw_in"])
        self.assertTrue(pw_file.exists())
        content = pw_file.read_text(encoding="utf-8")
        self.assertIn("STATUS: NOT RUN (DFT input generated for HPC execution)", content)
        self.assertIn("Eliashberg", content)


if __name__ == "__main__":
    unittest.main()
