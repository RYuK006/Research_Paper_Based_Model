"""
Unit tests for the Novelty Checker (candidate_pipeline/novelty.py).
Tests:
1. Negative controls: an absurd system (Ar-Kr-Rn-H10) must return NO_HITS_FOUND.
2. Positive regression cases: (La,Y)H10 and Co-doped BaFe2As2 must evaluate to KNOWN.
3. Match type classification: EXACT_FORMULA | FULL_ELEMENT_SYSTEM | PARTIAL_SYSTEM | SINGLE_ELEMENT.
4. Single-element or partial matches must never produce KNOWN.
5. Word 'novel' must NEVER appear in output.
"""

import unittest
from candidate_pipeline.novelty import MatchType, NoveltyChecker, NoveltyReport


class TestNoveltyChecker(unittest.TestCase):
    """Test suite for multi-source candidate novelty validation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = NoveltyChecker()

    def test_negative_control_absurd_noble_gas_hydride_returns_no_hits_found(self) -> None:
        """Negative control: an absurd noble gas hydride (Ar-Kr-Rn-H10) must return NO_HITS_FOUND."""
        report = self.checker.check_candidate("(Ar0.5Kr0.5)H10")
        self.assertIsInstance(report, NoveltyReport)
        self.assertEqual(report.status, "NO_HITS_FOUND")
        expected_prefix = "no hits found in:"
        self.assertTrue(
            report.status_description.startswith(expected_prefix),
            f"Description must start with '{expected_prefix}': {report.status_description}"
        )
        # Any evidence items gathered must never have EXACT_FORMULA or FULL_ELEMENT_SYSTEM with sc_verified=True
        for ev in report.evidence:
            self.assertNotIn(
                ev.match_type,
                [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value],
                f"Absurd system produced spurious full match: {ev}"
            )

    def test_regression_lanthanum_yttrium_hydride_known(self) -> None:
        """Regression test 1: (La,Y)H10 was published by Semenok et al. 2021 and must evaluate to KNOWN."""
        report = self.checker.check_candidate("(La0.85Y0.15)H10")
        self.assertIsInstance(report, NoveltyReport)
        self.assertEqual(report.status, "KNOWN")
        self.assertIn("H", report.elements)
        self.assertIn("La", report.elements)
        self.assertIn("Y", report.elements)
        self.assertGreater(len(report.evidence), 0)

        # Must have qualifying match_type (EXACT_FORMULA or FULL_ELEMENT_SYSTEM) about superconductivity
        qualifying = [
            e for e in report.evidence
            if e.match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value]
            and e.is_superconductivity
        ]
        self.assertGreater(
            len(qualifying), 0,
            "Expected at least one qualifying EXACT_FORMULA or FULL_ELEMENT_SYSTEM evidence item for (La,Y)H10"
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

        qualifying = [
            e for e in report.evidence
            if e.match_type in [MatchType.EXACT_FORMULA.value, MatchType.FULL_ELEMENT_SYSTEM.value]
            and e.is_superconductivity
        ]
        self.assertGreater(
            len(qualifying), 0,
            "Expected qualifying EXACT_FORMULA or FULL_ELEMENT_SYSTEM evidence item for Ba(Fe,Co)2As2"
        )

    def test_single_element_or_partial_never_produces_known(self) -> None:
        """
        Rule test: CAND_001 (Ce0.85Sr0.15)H10 previously had false KNOWN from single-element matches (Sr in SrFe2As2).
        Assert that PARTIAL or SINGLE_ELEMENT matches must never produce KNOWN.
        """
        report = self.checker.check_candidate("(Ce0.85Sr0.15)H10")
        self.assertIsInstance(report, NoveltyReport)
        # Ce-Sr-H has never been reported as a superconducting hydride, so it must NOT be KNOWN
        self.assertNotEqual(
            report.status, "KNOWN",
            f"(Ce,Sr)H10 was falsely marked KNOWN. Status: {report.status}, description: {report.status_description}"
        )
        self.assertEqual(report.status, "NO_HITS_FOUND")

        # Every evidence item must possess a valid match_type
        valid_match_types = {m.value for m in MatchType}
        for ev in report.evidence:
            self.assertIn(ev.match_type, valid_match_types)
            # If any evidence is SINGLE_ELEMENT or PARTIAL_SYSTEM, verify it did not produce KNOWN
            if ev.match_type in [MatchType.SINGLE_ELEMENT.value, MatchType.PARTIAL_SYSTEM.value]:
                self.assertNotEqual(report.status, "KNOWN")

    def test_forbidden_word_novel_never_emitted(self) -> None:
        """Test rule: Never output the word 'novel'; only 'no hits found in: <sources searched>'."""
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


    def test_positive_controls_hallmark_superconductors_and_fn_rate(self) -> None:
        r"""
        Tests $\ge 5$ hallmark positive controls across distinct superconductor families:
        1. (La0.8Ce0.2)H10 (ternary clathrate hydride)
        2. (Ca0.5Y0.5)H12 (ternary clathrate hydride)
        3. (Ba0.6K0.4)Fe2As2 (hole-doped 122 iron pnictide)
        4. SmFeAs(O0.85F0.15) (fluorine-doped 1111 iron oxypnictide)
        5. Fe(Se0.5Te0.5) (iron chalcogenide)
        6. La1.85Sr0.15CuO4 (hallmark LSCO cuprate)
        7. Sr2RuO4 (hallmark ruthenate)
        8. MgB2 (hallmark binary boride)
        
        Asserts that every hallmark known superconductor evaluates strictly to KNOWN.
        Calculates and verifies that the False Negative Rate (FNR) is exactly 0.0%.
        """
        positive_controls = [
            ("(La0.85Y0.15)H10", "Ternary hydride (La-Y-H)"),
            ("Ba(Fe0.9Co0.1)2As2", "Electron-doped 122 pnictide (Ba-Fe-Co-As)"),
            ("(La0.8Ce0.2)H10", "Ternary hydride (La-Ce-H)"),
            ("(Ca0.5Y0.5)H12", "Ternary hydride (Ca-Y-H)"),
            ("(Ba0.6K0.4)Fe2As2", "Hole-doped 122 pnictide (Ba-K-Fe-As)"),
            ("SmFeAs(O0.85F0.15)", "Fluorine-doped oxypnictide (Sm-Fe-As-O-F)"),
            ("Fe(Se0.5Te0.5)", "Iron chalcogenide (Fe-Se-Te)"),
            ("La1.85Sr0.15CuO4", "Hallmark LSCO cuprate (La-Sr-Cu-O)"),
            ("Sr2RuO4", "Layered ruthenate (Sr-Ru-O)"),
            ("MgB2", "Conventional binary boride (Mg-B)"),
        ]

        false_negatives = []
        for formula, desc in positive_controls:
            report = self.checker.check_candidate(formula)
            if report.status != "KNOWN":
                false_negatives.append((formula, desc, report.status, report.status_description))

        fnr = len(false_negatives) / len(positive_controls)
        print(f"\n[Positive Control Audit] Tested: {len(positive_controls)}, False Negatives: {len(false_negatives)}, FNR: {fnr:.1%}")
        for fn in false_negatives:
            print(f"  FAILED: {fn[0]} ({fn[1]}) -> {fn[2]}: {fn[3]}")

        self.assertEqual(
            len(false_negatives), 0,
            f"Expected 0.0% false negative rate on hallmark positive controls, got {len(false_negatives)} failures: {false_negatives}"
        )
        self.assertEqual(fnr, 0.0)


if __name__ == "__main__":
    unittest.main()
