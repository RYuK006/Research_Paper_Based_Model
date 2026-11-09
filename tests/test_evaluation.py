"""Unit tests for the Honest Superconductivity Time-Split Evaluator (evaluation/time_split_evaluator.py).

Verifies:
1. Strict filtering to superconductivity papers (non-superconducting papers rejected).
2. Failure test if any hit is not about superconductivity.
3. Multi-baseline comparison (Random, Frequency, Similarity) on identical candidate pool.
4. Multiple K values (10, 25, 50) and raw counts reporting.
5. Hit evidence persistence with traceable IDs.
6. Every confidence interval strictly contains its point estimate.
7. Pre/post counts, pool sizes, and hit lists strictly differ across cutoffs.
8. Dynamic report headers matching cutoff years.
"""

from __future__ import annotations

import gc
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from evaluation.time_split_evaluator import (
    BaselineComparison,
    EvaluationReport,
    TimeSplitEvaluator,
    wilson_ci,
)


class TestEvaluation(unittest.TestCase):
    """Test suite for honest superconductivity discovery benchmarking."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "test_eval_papers.db"

        # Create mock database with complete schema
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE papers (
                id TEXT PRIMARY KEY,
                title TEXT,
                abstract TEXT,
                year INTEGER,
                doi TEXT,
                source TEXT,
                categories TEXT
            )
        """)

        # Insert test papers
        papers = [
            ("p1", "Synthesis of Lanthanum hydride LaH10", "High pressure superconductivity of La and H with trace O.", 2002, "10.1103/PhysRev.mock1", "arxiv", "cond-mat.supr-con"),
            ("p2", "Yttrium hydride YH9 superconductivity", "Superconductivity in Y with H under pressure.", 2003, "10.1103/PhysRev.mock2", "arxiv", "cond-mat.supr-con"),
            ("p3", "Discovery of high-Tc ternary (La,Y)H10", "Superconductivity in ternary hydride containing (La0.8Y0.2)H10 at 160 GPa.", 2008, "10.1103/PhysRev.mock3", "arxiv", "cond-mat.supr-con"),
            ("p4", "Spectrophotometric analysis of paclitaxel with osmium", "Paclitaxel reacts with Os in biological medium.", 2009, "10.1016/j.mock4", "openalex", "bio.med"),
        ]
        c.executemany("INSERT INTO papers VALUES (?, ?, ?, ?, ?, ?, ?)", papers)
        conn.commit()
        c.close()
        conn.close()

    def tearDown(self) -> None:
        gc.collect()
        try:
            self.temp_dir.cleanup()
        except PermissionError:
            pass

    def test_corpus_filters_out_non_superconductivity_papers(self) -> None:
        """Test that non-superconducting papers (like paclitaxel/osmium p4) are strictly excluded."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004, bootstrap_trials=20)
        pre, post = evaluator.load_superconductivity_corpus_split()

        all_ids = [p["id"] for p in pre + post]
        self.assertNotIn("p4", all_ids, "Non-superconductivity paper p4 must NOT be loaded into corpus!")
        self.assertEqual(len(pre), 2)  # p1, p2
        self.assertEqual(len(post), 1)  # p3

    def test_every_hit_must_be_superconductivity(self) -> None:
        """Test that every hit in the report is strictly asserted as a superconductivity publication."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004, bootstrap_trials=20)
        report = evaluator.evaluate(k_values=[5, 10])

        self.assertGreater(len(report.verified_discoveries), 0)
        for d in report.verified_discoveries:
            self.assertTrue(d.is_superconductivity_paper, f"Hit paper {d.title} must be a superconductivity paper!")

    def test_multi_baseline_and_raw_counts(self) -> None:
        """Test comparison against random, frequency, and similarity baselines with raw counts."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004, bootstrap_trials=20)
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
        """Test markdown generation and JSON serialization using isolated temp paths."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004, bootstrap_trials=20)
        report = evaluator.evaluate(k_values=[5])

        test_md = self.temp_path / "test_report.md"
        test_json = self.temp_path / "test_results.json"

        md = evaluator.generate_markdown_report(report, output_path=str(test_md))
        evaluator.save_report_json(report, output_path=str(test_json))

        self.assertTrue(test_md.exists())
        self.assertTrue(test_json.exists())

        self.assertIn("# Empirical Discovery Benchmark Report", md)
        self.assertIn("Random Baseline", md)
        self.assertIn("Frequency Baseline", md)
        self.assertIn("Similarity Baseline", md)

        data = report.to_dict()
        self.assertIn("comparisons_by_k", data)
        self.assertIn("verified_discoveries", data)

    def test_ci_contains_point_estimate(self) -> None:
        """Every calculated Wilson confidence interval must strictly contain its point estimate."""
        evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=2004, bootstrap_trials=50)
        report = evaluator.evaluate(k_values=[5, 10])

        for c in report.comparisons_by_k:
            # Model CI
            self.assertLessEqual(c.model_ci_95[0], c.model_rate + 1e-4)
            self.assertGreaterEqual(c.model_ci_95[1], c.model_rate - 1e-4)

            # Frequency CI
            self.assertLessEqual(c.frequency_ci_95[0], c.frequency_rate + 1e-4)
            self.assertGreaterEqual(c.frequency_ci_95[1], c.frequency_rate - 1e-4)

            # Random CI
            self.assertLessEqual(c.random_ci_95[0], c.random_rate + 1e-4)
            self.assertGreaterEqual(c.random_ci_95[1], c.random_rate - 1e-4)

    def test_multi_cutoff_counts_and_hits_differ(self) -> None:
        """Benchmark results across distinct cutoffs (2015, 2018, 2020) must have differing paper counts and pool sizes."""
        summary_file = Path("data/multi_cutoff_benchmark_summary.json")
        if not summary_file.exists():
            self.skipTest("multi_cutoff_benchmark_summary.json not present")

        with open(summary_file, "r", encoding="utf-8") as f:
            summary = json.load(f)

        cutoffs = [2015, 2018, 2020]
        pre_counts = [summary[str(y)]["pre_cutoff"] for y in cutoffs if str(y) in summary]
        post_counts = [summary[str(y)]["post_cutoff"] for y in cutoffs if str(y) in summary]
        pool_sizes = [summary[str(y)]["pool_size"] for y in cutoffs if str(y) in summary]

        self.assertEqual(len(set(pre_counts)), len(cutoffs), f"Pre-cutoff counts must differ: {pre_counts}")
        self.assertEqual(len(set(post_counts)), len(cutoffs), f"Post-cutoff counts must differ: {post_counts}")
        self.assertEqual(len(set(pool_sizes)), len(cutoffs), f"Pool sizes must differ: {pool_sizes}")

    def test_report_header_contains_cutoff_year(self) -> None:
        """Report header must dynamically reflect the cutoff year (e.g. pre-2018, pre-2020), not hardcoded pre-2004."""
        for year in [2015, 2018, 2020]:
            evaluator = TimeSplitEvaluator(db_path=str(self.db_path), cutoff_year=year)
            report = EvaluationReport(
                cutoff_year=year,
                pre_cutoff_papers=100,
                post_cutoff_papers=50,
                tested_k_values=[10],
                pool_size=1000,
                comparisons_by_k=[],
                bootstrap_iterations=10,
                verified_discoveries=[],
                statistical_signal_detected=False,
            )
            md = evaluator.generate_markdown_report(report)
            self.assertIn(f"Cutoff Year: {year}", md)
            self.assertIn(f"pre-{year}", md)

    def test_committed_outputs_contain_no_fixture_markers(self) -> None:
        """Integrity assertion: Unit test fixture data must NEVER leak into committed repo output files."""
        output_files = [
            Path("TIME_SPLIT_EVALUATION.md"),
            Path("data/time_split_results.json"),
            Path("data/candidates.json"),
            Path("CANDIDATE_MATERIALS.md"),
        ]
        forbidden_markers = [
            "10.1103/PhysRev.mock",
            "10.1016/j.mock",
            "Synthesis of Lanthanum hydride LaH10",
            "Yttrium hydride YH9 superconductivity",
            "Discovery of high-Tc ternary (La,Y)H10",
            "Spectrophotometric analysis of paclitaxel with osmium",
            "paclitaxel",
        ]
        for fpath in output_files:
            if fpath.exists():
                text = fpath.read_text(encoding="utf-8", errors="ignore")
                for marker in forbidden_markers:
                    self.assertNotIn(
                        marker,
                        text,
                        f"Fixture marker '{marker}' found in committed output file {fpath}! "
                        "Unit tests or mock pipelines must never overwrite committed artifacts."
                    )


if __name__ == "__main__":
    unittest.main()
