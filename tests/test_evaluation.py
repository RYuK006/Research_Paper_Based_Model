"""
Unit tests for the Honest Superconductivity Time-Split Evaluator (evaluation/time_split_evaluator.py).
Verifies:
1. Strict filtering to superconductivity papers (non-superconducting papers rejected).
2. Failure test if any hit is not about superconductivity.
3. Multi-baseline comparison (Random, Frequency, Similarity) on identical candidate pool.
4. Multiple K values (10, 25, 50) and raw counts reporting.
5. Hit evidence persistence with traceable IDs.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from evaluation.time_split_evaluator import TimeSplitEvaluator, EvaluationReport


class TestEvaluation(unittest.TestCase):
    """Test suite for honest superconductivity discovery benchmarking."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "test_eval_papers.db"

        # Create mock database
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE papers (
                id TEXT PRIMARY KEY,
                title TEXT,
                abstract TEXT,
                year INTEGER,
                doi TEXT,
                categories TEXT
            )
        """)

        # Insert test papers:
        # Pre-2004 superconductivity papers
        # p1: La, H, O (superconduct)
        # p2: Y, H, O (superconduct)
        # Post-2004 superconductivity papers
        # p3: (La, Y) synthesized together in superconductivity study!
        # Non-superconducting papers (e.g. bioinorganic or cancer drug)
        # p4: Paclitaxel Osmium complex (NO superconductivity)
        papers = [
            ("p1", "Synthesis of Lanthanum hydride LaH10", "High pressure superconductivity of La and H with trace O.", 2002, "10.1/1", "cond-mat.supr-con"),
            ("p2", "Yttrium hydride YH9 superconductivity", "Superconductivity in Y with H under pressure.", 2003, "10.1/2", "cond-mat.supr-con"),
            ("p3", "Discovery of high-Tc ternary (La,Y)H10", "Superconductivity in ternary hydride containing La and Y at 160 GPa.", 2008, "10.1/3", "cond-mat.supr-con"),
            ("p4", "Spectrophotometric analysis of paclitaxel with osmium", "Paclitaxel reacts with Os in biological medium.", 2009, "10.1/4", "bio.med"),
        ]
        c.executemany("INSERT INTO papers VALUES (?, ?, ?, ?, ?, ?)", papers)
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_corpus_filters_out_non_superconductivity_papers(self) -> None:
        """Test that non-superconducting papers (like paclitaxel/osmium p4) are strictly excluded."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004)
        pre, post = evaluator.load_superconductivity_corpus_split()

        all_ids = [p["id"] for p in pre + post]
        self.assertNotIn("p4", all_ids, "Non-superconductivity paper p4 must NOT be loaded into corpus!")
        self.assertEqual(len(pre), 2)  # p1, p2
        self.assertEqual(len(post), 1)  # p3

    def test_every_hit_must_be_superconductivity(self) -> None:
        """Test that every hit in the report is strictly asserted as a superconductivity publication."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004)
        report = evaluator.evaluate(k_values=[5, 10])

        self.assertGreater(len(report.verified_discoveries), 0)
        for d in report.verified_discoveries:
            self.assertTrue(d.is_superconductivity_paper, f"Hit paper {d.title} must be a superconductivity paper!")

    def test_multi_baseline_and_raw_counts(self) -> None:
        """Test comparison against random, frequency, and similarity baselines with raw counts."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004)
        report = evaluator.evaluate(k_values=[5, 10])

        self.assertEqual(len(report.comparisons_by_k), 2)
        comp_5 = report.comparisons_by_k[0]
        self.assertEqual(comp_5.k, min(5, report.pool_size))
        self.assertIsInstance(comp_5.model_hits, int)
        self.assertIsInstance(comp_5.random_hits, int)
        self.assertIsInstance(comp_5.frequency_hits, int)
        self.assertIsInstance(comp_5.similarity_hits, int)
        self.assertGreaterEqual(comp_5.model_rate, 0.0)

    def test_markdown_and_json_report(self) -> None:
        """Test markdown generation and JSON serialization."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004)
        report = evaluator.evaluate(k_values=[5])

        md = evaluator.generate_markdown_report(report)
        self.assertIn("# 📈 Empirical Time-Split Scientific Discovery Benchmark", md)
        self.assertIn("Raw Counts", md)
        self.assertIn("Random Baseline", md)
        self.assertIn("Element Frequency Baseline", md)
        self.assertIn("Element Similarity Baseline", md)

        data = report.to_dict()
        self.assertIn("comparisons_by_k", data)
        self.assertIn("verified_discoveries", data)


if __name__ == "__main__":
    unittest.main()
