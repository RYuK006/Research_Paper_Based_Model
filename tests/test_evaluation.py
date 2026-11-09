"""
Unit tests for the Time-Split Scientific Discovery Benchmark Evaluator.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from evaluation.time_split_evaluator import TimeSplitEvaluator, EvaluationReport


class TestEvaluation(unittest.TestCase):
    """Test suite for time-split discovery benchmarking."""

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
                doi TEXT
            )
        """)

        # Insert historical pre-2021 papers:
        # p1: La, H, O
        # p2: Y, H, O
        # Both La and Y frequently co-occur with H and O, but (La, Y) has no pre-2021 co-occurrence!
        # Insert modern post-2021 papers:
        # p3: (La, Y) synthesized together! (Ground-truth future hit)
        papers = [
            ("p1", "Synthesis of Lanthanum hydride LaH10", "High pressure La and H react with trace O.", 2019, "10.1/1"),
            ("p2", "Yttrium hydride YH9 superconductivity", "Laser heating of Y with H in presence of O.", 2020, "10.1/2"),
            ("p3", "Discovery of high-Tc ternary (La,Y)H10", "Ternary hydride containing both La and Y synthesized at 160 GPa.", 2023, "10.1/3"),
            ("p4", "Iron selenide FeSe films", "Tetragonal FeSe thin films grown on STO.", 2017, "10.1/4"),
            ("p5", "Cobalt doped FeSe", "Transport properties of Co doped FeSe.", 2022, "10.1/5"),
        ]
        c.executemany("INSERT INTO papers VALUES (?, ?, ?, ?, ?)", papers)
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_corpus_split(self) -> None:
        """Test splitting corpus into pre-cutoff training and post-cutoff evaluation."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2021)
        pre, post = evaluator.load_corpus_split()
        self.assertEqual(len(pre), 3)  # p1 (2019), p2 (2020), p4 (2017)
        self.assertEqual(len(post), 2)  # p3 (2023), p5 (2022)

    def test_discovery_signal_evaluation(self) -> None:
        """Test evaluating discovery predictions against future ground truth."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2021)
        report = evaluator.evaluate_discovery_signal(top_k=5)

        self.assertIsInstance(report, EvaluationReport)
        self.assertEqual(report.cutoff_year, 2021)
        self.assertGreaterEqual(report.model_hit_rate, 0.0)
        self.assertGreaterEqual(report.lift_over_random, 1.0)
        self.assertIsInstance(report.verified_future_discoveries, list)

    def test_markdown_report_generation(self) -> None:
        """Test generating markdown evaluation report."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2021)
        report = evaluator.evaluate_discovery_signal(top_k=5)
        md = evaluator.generate_markdown_report(report)

        self.assertIn("# 📈 Empirical Time-Split Scientific Discovery Benchmark", md)
        self.assertIn("Hit Rate", md)
        self.assertIn("Relative Lift", md)


if __name__ == "__main__":
    unittest.main()
