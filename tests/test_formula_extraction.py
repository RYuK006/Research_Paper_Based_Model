"""Tests for formula-only element extraction and benchmarking on 30 hand-labeled abstracts."""

import json
import logging
import os
import unittest
from typing import Dict, List, Set

from extraction.formula_extractor import (
    extract_all_elements,
    extract_compound_element_pairs,
    extract_compounds_and_elements,
)

logger = logging.getLogger(__name__)


class TestFormulaExtraction(unittest.TestCase):
    """Evaluates strict formula-level extraction, negative control rejection, and gold benchmark."""

    @classmethod
    def setUpClass(cls) -> None:
        gold_path = os.path.join(os.path.dirname(__file__), "..", "data", "labeled_abstracts_30.json")
        with open(gold_path, "r", encoding="utf-8") as f:
            cls.gold_abstracts = json.load(f)

    def test_benchmark_precision_and_recall_on_30_abstracts(self) -> None:
        """Evaluates extraction Precision and Recall against 30 hand-labeled gold abstracts."""
        total_tp = 0
        total_fp = 0
        total_fn = 0

        for item in self.gold_abstracts:
            gold_set: Set[str] = set(item["gold_elements"])
            text = f"{item['title']} {item['abstract']}"
            extracted_set: Set[str] = extract_all_elements(text)

            tp = len(extracted_set.intersection(gold_set))
            fp = len(extracted_set - gold_set)
            fn = len(gold_set - extracted_set)

            total_tp += tp
            total_fp += fp
            total_fn += fn

        precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        logger.info(
            f"Hand-labeled 30 Abstract Benchmark Results: "
            f"Precision = {precision * 100:.1f}%, Recall = {recall * 100:.1f}%, F1 = {f1 * 100:.1f}% "
            f"(TP={total_tp}, FP={total_fp}, FN={total_fn})"
        )

        # Assert strict performance requirements (>= 90% Precision and Recall)
        self.assertGreaterEqual(precision, 0.90, f"Precision {precision:.2f} fell below 0.90")
        self.assertGreaterEqual(recall, 0.90, f"Recall {recall:.2f} fell below 0.90")

    def test_negative_controls_strictly_zero_extracted(self) -> None:
        """Negative controls: English words (In, As, Be, At, K), units (Ne FIB, 39 K), and acronyms."""
        negative_texts = [
            "Ne FIB milling was applied to etch sapphire substrates.",
            "In this study, As was used as a comparative reagent for Be thin films.",
            "Measurements of the critical temperature Tc = 39 K were performed in a SQUID magnetometer.",
            "At ambient pressure, no superconductivity was observed above 1.8 K in K-band microwave cavities.",
            "Pm and Am radioisotopes were examined using XPS and EDX spectroscopy.",
            "The BCS theory explains electron-phonon pairing; however, DFT calculations indicate an instability.",
        ]

        for text in negative_texts:
            elems = extract_all_elements(text)
            self.assertEqual(
                elems,
                set(),
                f"Negative control leak! Extracted {elems} from non-formula text: '{text}'"
            )

    def test_technetium_in_formula_vs_critical_temperature(self) -> None:
        """Tc is technetium only when inside an inorganic formula; Tc as critical temperature is masked."""
        # Critical temperature (must NOT extract Tc)
        tc_temp_text = "The sample exhibits a sharp superconducting transition with Tc = 25 K and Tc ~ 30 K."
        self.assertEqual(extract_all_elements(tc_temp_text), set())

        # Technetium diboride (MUST extract Tc and B)
        tc_formula_text = "Technetium diboride TcB2 shows high hardness and phonon-mediated superconductivity."
        extracted = extract_all_elements(tc_formula_text)
        self.assertIn("Tc", extracted)
        self.assertIn("B", extracted)

    def test_complex_doped_formulas(self) -> None:
        """Tests extraction from complex doped and algebraic solid solutions."""
        cases = [
            ("(Dy1-xErx)Rh3.8Ru0.2B4", {"Dy", "Er", "Rh", "Ru", "B"}),
            ("Ba(Fe0.92Co0.08)2As2", {"Ba", "Fe", "Co", "As"}),
            ("(La0.85Y0.15)H10", {"La", "Y", "H"}),
            ("YBa2Cu3O7-d", {"Y", "Ba", "Cu", "O"}),
            ("Bi2Sr2CaCu2O8+x", {"Bi", "Sr", "Ca", "Cu", "O"}),
        ]
        for formula, expected_elements in cases:
            extracted = extract_all_elements(formula)
            self.assertEqual(
                extracted,
                expected_elements,
                f"Failed for formula '{formula}': expected {expected_elements}, got {extracted}"
            )

    def test_transuranic_elements_excluded(self) -> None:
        """Elements with Z > 94 (Am, Cm, Bk, Cf, etc.) are strictly excluded."""
        text = "Fictional compound AmH10 and CfB2 were modeled theoretically."
        extracted = extract_all_elements(text)
        self.assertNotIn("Am", extracted)
        self.assertNotIn("Cf", extracted)

    def test_compound_element_pairs_generation(self) -> None:
        """Tests that extract_compound_element_pairs produces pairs exclusively within the same formula."""
        text = "We compare LaNiGa2 with YScH8."
        pairs = extract_compound_element_pairs(text)

        # Within LaNiGa2: (Ga, La), (Ga, Ni), (La, Ni)
        self.assertIn(("Ga", "La"), pairs)
        self.assertIn(("Ga", "Ni"), pairs)
        self.assertIn(("La", "Ni"), pairs)

        # Within YScH8: (H, Sc), (H, Y), (Sc, Y)
        self.assertIn(("H", "Sc"), pairs)
        self.assertIn(("H", "Y"), pairs)
        self.assertIn(("Sc", "Y"), pairs)

        # Across compounds (La and Y are NOT in the same compound here!)
        self.assertNotIn(("La", "Y"), pairs)
        self.assertNotIn(("Ga", "H"), pairs)


if __name__ == "__main__":
    unittest.main()
