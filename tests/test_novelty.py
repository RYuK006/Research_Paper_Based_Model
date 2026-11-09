"""
Unit tests for the Novelty Checker (candidate_pipeline/novelty.py).
Tests regression cases:
1. (La,Y)H10 must be KNOWN.
2. Co-doped BaFe2As2 must be KNOWN.
3. Word 'novel' must NEVER appear in output.
"""

import unittest
from candidate_pipeline.novelty import NoveltyChecker, NoveltyReport


class TestNoveltyChecker(unittest.TestCase):
    """Test suite for multi-source candidate novelty validation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = NoveltyChecker()

    def test_regression_lanthanum_yttrium_hydride_known(self) -> None:
        """Regression test 1: (La,Y)H10 was published by Semenok et al. 2021 and must evaluate to KNOWN."""
        report = self.checker.check_candidate("(La0.85Y0.15)H10")
        self.assertIsInstance(report, NoveltyReport)
        self.assertEqual(report.status, "KNOWN")
        self.assertIn("H", report.elements)
        self.assertIn("La", report.elements)
        self.assertIn("Y", report.elements)
        self.assertGreater(len(report.evidence), 0)
        # Ensure evidence cites Semenok et al. or ternary hydride literature
        evidence_texts = " ".join([e.title + " " + e.details for e in report.evidence]).lower()
        self.assertTrue(
            "lanthanum" in evidence_texts and ("yttrium" in evidence_texts or "hydride" in evidence_texts),
            f"Evidence missing key ternary hydride terms: {evidence_texts}"
        )

    def test_regression_cobalt_doped_bafe2as2_known(self) -> None:
        """Regression test 2: Co-doped BaFe2As2 is a hallmark iron-based superconductor and must evaluate to KNOWN."""
        report = self.checker.check_candidate("Ba(Fe0.9Co0.1)2As2")
        self.assertIsInstance(report, NoveltyReport)
        self.assertEqual(report.status, "KNOWN")
        self.assertIn("Ba", report.elements)
        self.assertIn("Fe", report.elements)
        self.assertIn("Co", report.elements)
        self.assertIn("As", report.elements)
        self.assertGreater(len(report.evidence), 0)

    def test_forbidden_word_novel_never_emitted(self) -> None:
        """Test rule: Never output the word 'novel'; only 'no hits found in: <sources searched>'."""
        # Query a completely synthetic hypothetical formula with obscure elements
        report = self.checker.check_candidate("AtFrOg")
        self.assertNotIn("novel", report.status.lower())
        self.assertNotIn("novel", report.status_description.lower())
        if report.status == "NO_HITS_FOUND":
            expected_prefix = "no hits found in:"
            self.assertTrue(
                report.status_description.startswith(expected_prefix),
                f"Description does not start with '{expected_prefix}': {report.status_description}"
            )

    def test_pymatgen_formula_parsing(self) -> None:
        """Test pymatgen composition parsing and reduced formula normalization."""
        comp, chemsys, elements = self.checker.parse_composition("(La0.85Y0.15)H10")
        self.assertEqual(chemsys, "H-La-Y")
        self.assertEqual(sorted(elements), ["H", "La", "Y"])
        self.assertAlmostEqual(float(comp["H"]), 10.0)


if __name__ == "__main__":
    unittest.main()
