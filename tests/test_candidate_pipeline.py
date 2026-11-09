"""
Unit tests for the Candidate Discovery Pipeline (candidate_pipeline/).
Verifies:
1. Rejection of invalid formulas: (O,As)H10, (C,Cu)H10, (Ba,Sr)Ba2Cu3O7, (Fe,Co)Fe2As2.
2. Determinism across repeated runs with fixed seed.
3. Correct prototype site assignments and pymatgen compositions.
"""

import tempfile
import unittest
from pathlib import Path

from candidate_pipeline.generator import CandidateGenerator, MaterialCandidate
from candidate_pipeline.verifier import CandidateVerifier
from candidate_pipeline.protocol_designer import ProtocolDesigner
from candidate_pipeline.orchestrator import CandidatePipelineOrchestrator


class TestCandidatePipeline(unittest.TestCase):
    """Test suite for candidate materials pipeline."""

    def setUp(self) -> None:
        self.generator = CandidateGenerator(seed=42)
        self.verifier = CandidateVerifier()
        self.designer = ProtocolDesigner()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_reject_invalid_formulas(self) -> None:
        """
        Tests that the generator strictly rejects the 4 hallmark invalid formulas:
        1. (O,As)H10 (nonmetal/metalloid on metal cage site)
        2. (C,Cu)H10 (nonmetal/late transition metal on hydride cage)
        3. (Ba,Sr)Ba2Cu3O7 (Ba placed on the Y site in YBa2Cu3O7)
        4. (Fe,Co)Fe2As2 (Fe placed on the Ba site in BaFe2As2)
        """
        # 1. (O,As)H10
        valid_1, reason_1 = self.generator.is_valid_substitution("(O0.85As0.15)H10", "Clathrate hydride")
        self.assertFalse(valid_1, "Expected (O,As)H10 to be rejected")
        self.assertIn("Nonmetal", reason_1)

        # 2. (C,Cu)H10
        valid_2, reason_2 = self.generator.is_valid_substitution("(C0.85Cu0.15)H10", "Clathrate hydride")
        self.assertFalse(valid_2, "Expected (C,Cu)H10 to be rejected")
        self.assertIn("Nonmetal", reason_2)

        # 3. (Ba,Sr)Ba2Cu3O7
        valid_3, reason_3 = self.generator.is_valid_substitution("(Ba0.85Sr0.15)Ba2Cu3O7", "Perovskite oxide")
        self.assertFalse(valid_3, "Expected (Ba,Sr)Ba2Cu3O7 to be rejected")
        self.assertIn("Alkaline earth", reason_3)

        # 4. (Fe,Co)Fe2As2
        valid_4, reason_4 = self.generator.is_valid_substitution("(Fe0.85Co0.15)Fe2As2", "Iron chalcogenide / pnictide")
        self.assertFalse(valid_4, "Expected (Fe,Co)Fe2As2 to be rejected")
        self.assertIn("Transition metal", reason_4)

        # Also test rejection when calling build_candidate_from_pair
        self.assertIsNone(self.generator.build_candidate_from_pair(1, "O", "As", 100.0))
        self.assertIsNone(self.generator.build_candidate_from_pair(2, "C", "Cu", 100.0))

    def test_valid_prototype_generation(self) -> None:
        """Test valid prototype-grounded candidate generation."""
        # Valid hydride: La-Y
        cand_hydride = self.generator.build_candidate_from_pair(1, "La", "Y", 450.0)
        self.assertIsNotNone(cand_hydride)
        self.assertEqual(cand_hydride.formula, "(La0.85Y0.15)H10")
        self.assertEqual(cand_hydride.target_family, "Clathrate hydride")
        self.assertEqual(cand_hydride.space_group, "Fm-3m (#225)")
        self.assertEqual(cand_hydride.tc_status, "NOT COMPUTED")
        self.assertIsNone(cand_hydride.predicted_tc)

        # Valid 122 iron pnictide Fe-site doping: Fe-Co
        cand_pnictide = self.generator.build_candidate_from_pair(2, "Fe", "Co", 350.0)
        self.assertIsNotNone(cand_pnictide)
        self.assertEqual(cand_pnictide.formula, "Ba(Fe0.85Co0.15)2As2")
        self.assertEqual(cand_pnictide.target_family, "Iron chalcogenide / pnictide")
        self.assertEqual(cand_pnictide.space_group, "I4/mmm (#139)")

        # Valid YBCO rare-earth substitution: Y-Gd
        cand_cuprate = self.generator.build_candidate_from_pair(3, "Y", "Gd", 300.0)
        self.assertIsNotNone(cand_cuprate)
        self.assertEqual(cand_cuprate.formula, "(Y0.85Gd0.15)Ba2Cu3O7")
        self.assertEqual(cand_cuprate.target_family, "Perovskite oxide")

    def test_deterministic_generation_with_seed(self) -> None:
        """Test that candidate generation is 100% reproducible with fixed seed."""
        gaps = [
            {"element_1": "La", "element_2": "Y", "discovery_score": 450.0},
            {"element_1": "Fe", "element_2": "Co", "discovery_score": 380.0},
            {"element_1": "O", "element_2": "As", "discovery_score": 350.0},  # Invalid gap
            {"element_1": "Y", "element_2": "Gd", "discovery_score": 300.0},
            {"element_1": "Ba", "element_2": "K", "discovery_score": 250.0},
        ]

        gen1 = CandidateGenerator(seed=42)
        gen2 = CandidateGenerator(seed=42)

        res1 = gen1.generate_candidates_from_gaps(gaps, max_candidates=5)
        res2 = gen2.generate_candidates_from_gaps(gaps, max_candidates=5)

        self.assertEqual(len(res1), len(res2))
        for c1, c2 in zip(res1, res2):
            self.assertEqual(c1.formula, c2.formula)
            self.assertEqual(c1.target_family, c2.target_family)
            self.assertEqual(c1.discovery_score, c2.discovery_score)


if __name__ == "__main__":
    unittest.main()
