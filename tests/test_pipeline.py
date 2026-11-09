"""Unit tests for models, storage, parsing, and reporting."""

import tempfile
import unittest
from pathlib import Path

from analytics.report_generator import ReportGenerator
from collectors.openalex_collector import reconstruct_abstract
from pipeline.models import PaperRecord
from pipeline.storage import StorageManager


class TestPipeline(unittest.TestCase):
    """Test suite for research paper pipeline components."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.storage = StorageManager(base_dir=self.base_dir / "data")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_paper_record_serialization(self):
        """Test PaperRecord serialization and roundtrip conversion."""
        record = PaperRecord(
            id="arxiv:2305.00001",
            title="Observation of Superconductivity in High Pressure Hydrides",
            abstract="We report the synthesis and crystal structure of new hydride compounds.",
            authors=["A. Physicist", "B. Chemist"],
            year=2024,
            doi="10.1000/182",
            source="arxiv",
            categories=["cond-mat.supr-con", "cond-mat.mtrl-sci"],
            citation_count=42,
            open_access_pdf_url="https://arxiv.org/pdf/2305.00001.pdf",
        )

        d = record.to_dict()
        self.assertEqual(d["id"], "arxiv:2305.00001")
        self.assertEqual(len(d["authors"]), 2)

        restored = PaperRecord.from_dict(d)
        self.assertEqual(restored.id, record.id)
        self.assertEqual(restored.title, record.title)
        self.assertEqual(restored.citation_count, 42)

    def test_storage_batch_upsert_and_deduplication(self):
        """Test storage engine SQLite upsert and deduplication."""
        rec1 = PaperRecord(
            id="openalex:W1001",
            title="Synthesis of Novel Perovskite Cuprate Compounds",
            abstract="Study of copper, oxygen and barium elements in superconducting lattices.",
            authors=["Dr. Synthesis"],
            year=2023,
            source="openalex",
            citation_count=10,
        )
        rec2 = PaperRecord(
            id="openalex:W1002",
            title="Iron Pnictide Transition Temperature Analysis",
            abstract="Investigation into iron, arsenic and lanthanum superconducting compounds.",
            authors=["Dr. Pnictide"],
            year=2022,
            source="openalex",
            citation_count=25,
        )

        count = self.storage.upsert_papers_batch([rec1, rec2])
        self.assertEqual(count, 2)
        self.assertTrue(self.storage.paper_exists("openalex:W1001"))
        self.assertTrue(self.storage.paper_exists("openalex:W1002"))
        self.assertFalse(self.storage.paper_exists("openalex:W9999"))

        # Test duplicate upsert updates instead of failing
        rec1_updated = PaperRecord(
            id="openalex:W1001",
            title="Synthesis of Novel Perovskite Cuprate Compounds (Updated)",
            abstract="Updated abstract text.",
            authors=["Dr. Synthesis"],
            year=2023,
            source="openalex",
            citation_count=15,
        )
        self.storage.upsert_paper(rec1_updated)
        counts = self.storage.get_counts_by_source()
        self.assertEqual(counts.get("openalex"), 2)

    def test_checkpointing(self):
        """Test pipeline checkpoint save and load."""
        self.storage.save_checkpoint("openalex", "cursor_xyz_123", 500)
        cursor, count = self.storage.get_checkpoint("openalex")
        self.assertEqual(cursor, "cursor_xyz_123")
        self.assertEqual(count, 500)

    def test_openalex_abstract_reconstruction(self):
        """Test inverted index abstract reconstruction."""
        inverted = {
            "Novel": [0],
            "synthesis": [1],
            "of": [2],
            "superconducting": [3],
            "materials.": [4],
        }
        text = reconstruct_abstract(inverted)
        self.assertEqual(text, "Novel synthesis of superconducting materials.")

    def test_report_generation(self):
        """Test report generation on mock database."""
        rec = PaperRecord(
            id="arxiv:2401.0001",
            title="Discovery of Superconducting Hydrides Containing Yttrium and Hydrogen",
            abstract="High pressure synthesis reveals new compound phases of yttrium hydrides.",
            authors=["C. Researcher"],
            year=2024,
            source="arxiv",
            categories=["cond-mat.supr-con"],
            citation_count=50,
        )
        self.storage.upsert_paper(rec)

        gen = ReportGenerator(base_dir=self.base_dir)
        report_file = gen.generate_report()
        self.assertTrue(report_file.exists())
        content = report_file.read_text(encoding="utf-8")
        self.assertIn("10,000 Scientific Research Papers", content)
        self.assertIn("Yttrium", content)
        self.assertIn("Hydride", content)


if __name__ == "__main__":
    unittest.main()
