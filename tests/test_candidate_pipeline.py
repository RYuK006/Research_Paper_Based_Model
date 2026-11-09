"""
Unit tests for the Candidate Discovery Pipeline (generator, verifier, protocol designer, and orchestrator).
"""

import tempfile
import unittest
from pathlib import Path

from candidate_pipeline.generator import CandidateGenerator, MaterialCandidate
from candidate_pipeline.protocol_designer import ProtocolDesigner
from candidate_pipeline.verifier import CandidateVerifier
from candidate_pipeline.orchestrator import CandidatePipelineOrchestrator


class TestCandidatePipeline(unittest.TestCase):
    """Test suite for candidate materials pipeline."""

    def setUp(self) -> None:
        self.generator = CandidateGenerator()
        self.verifier = CandidateVerifier()
        self.designer = ProtocolDesigner()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_candidate_generator(self) -> None:
        """Test formula and stoichiometry generation from element discovery gaps."""
        cand = self.generator.generate_candidate_from_element_gap(
            candidate_idx=1,
            element_1="La",
            element_2="Y",
            discovery_score=450.0,
            family="Clathrate hydride",
            doping_fraction=0.15,
        )
        self.assertEqual(cand.candidate_id, "CAND_001")
        self.assertEqual(cand.formula, "(La0.85Y0.15)H10")
        self.assertIn("H", cand.elements)
        self.assertIn("La", cand.elements)
        self.assertIn("Y", cand.elements)
        self.assertEqual(cand.stoichiometry["H"], 10.0)
        self.assertEqual(cand.stoichiometry["La"], 0.85)
        self.assertEqual(cand.stoichiometry["Y"], 0.15)
        self.assertEqual(cand.space_group, "Fm-3m (#225)")

    def test_candidate_verifier(self) -> None:
        """Test physical verification heuristics (electronegativity spread & precompression)."""
        cand = self.generator.generate_candidate_from_element_gap(
            candidate_idx=1,
            element_1="La",
            element_2="Y",
            discovery_score=450.0,
            family="Clathrate hydride",
        )
        res = self.verifier.verify_candidate(cand)
        self.assertIn(res.plausibility_status, ["HIGHLY_PROMISING", "VIABLE"])
        self.assertGreaterEqual(res.stability_score, 0.70)
        self.assertGreater(res.chemical_precompression_index, 0.80)

        # Test Perovskite tolerance calculation
        perov_cand = self.generator.generate_candidate_from_element_gap(
            candidate_idx=2,
            element_1="Y",
            element_2="Ba",
            discovery_score=300.0,
            family="Perovskite oxide",
        )
        res_perov = self.verifier.verify_candidate(perov_cand)
        self.assertIsNotNone(res_perov.goldschmidt_tolerance)
        self.assertGreater(res_perov.goldschmidt_tolerance, 0.7)

    def test_protocol_designer(self) -> None:
        """Test generating lab-ready synthesis recipes."""
        cand = self.generator.generate_candidate_from_element_gap(
            candidate_idx=1,
            element_1="La",
            element_2="Y",
            discovery_score=450.0,
            family="Clathrate hydride",
        )
        protocol = self.designer.design_protocol(cand)
        self.assertIn("diamond anvil", protocol.recommended_synthesis_method.lower())
        self.assertTrue(any("Ammonia borane" in p or "H2" in p for p in protocol.starting_precursors))
        self.assertTrue(any("Synchrotron" in c for c in protocol.characterization_plan))
        md = protocol.to_markdown()
        self.assertIn("### Protocol for Candidate CAND_001", md)

    def test_pipeline_orchestrator(self) -> None:
        """Test end-to-end orchestrator execution."""
        mock_db = self.temp_path / "mock.db"
        orchestrator = CandidatePipelineOrchestrator(
            db_path=str(mock_db),
            output_dir=str(self.temp_path),
        )
        res = orchestrator.run_pipeline(max_candidates=3)
        self.assertEqual(res["candidates_count"], 3)
        self.assertTrue((self.temp_path / "candidates.json").exists())


if __name__ == "__main__":
    unittest.main()

