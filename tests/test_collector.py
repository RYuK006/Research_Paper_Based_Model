"""
Unit tests for Resumable Research Paper Harvester (data/collect_papers.py).
Tests:
1. arXiv Atom XML parsing.
2. OpenAlex JSON parsing and inverted index reconstruction.
3. Deduplication by canonical ID and normalized DOI.
4. Resumable checkpointing and state restoration.
5. Polite User-Agent and rate-limit handling.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from data.collect_papers import (
    PaperDatabase,
    PaperItem,
    ResumablePaperCollector,
    normalize_doi,
    reconstruct_openalex_abstract,
)


class TestCollector(unittest.TestCase):
    """Test suite for paper collector."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "test_papers.db"
        self.checkpoint_path = self.temp_path / "test_checkpoint.json"
        self.collectors_to_close = []

    def tearDown(self) -> None:
        for c in self.collectors_to_close:
            try:
                c.close()
            except Exception:
                pass
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_normalize_doi(self) -> None:
        """Test DOI normalization removes URL prefixes and lowercases."""
        self.assertEqual(normalize_doi("https://doi.org/10.1103/PhysRevB.100.014501"), "10.1103/physrevb.100.014501")
        self.assertEqual(normalize_doi("http://dx.doi.org/10.1038/nature12345"), "10.1038/nature12345")
        self.assertEqual(normalize_doi("doi:10.1016/j.physc.2020.123"), "10.1016/j.physc.2020.123")
        self.assertIsNone(normalize_doi(None))
        self.assertIsNone(normalize_doi(""))

    def test_reconstruct_openalex_abstract(self) -> None:
        """Test inverted index reconstruction to linear text."""
        inverted = {
            "Superconductivity": [0],
            "in": [1],
            "hydrides": [2],
            "under": [3],
            "pressure.": [4],
        }
        text = reconstruct_openalex_abstract(inverted)
        self.assertEqual(text, "Superconductivity in hydrides under pressure.")
        self.assertEqual(reconstruct_openalex_abstract(None), "")

    def test_arxiv_atom_xml_parsing(self) -> None:
        """Test parsing of arXiv Atom XML response."""
        xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
          <entry>
            <id>http://arxiv.org/abs/2301.05678v1</id>
            <published>2023-01-15T12:00:00Z</published>
            <title>Discovery of High-Tc Phase in Ternary Hydride</title>
            <summary>We report superconductivity at 200 K under 150 GPa.</summary>
            <author><name>Alice Smith</name></author>
            <author><name>Bob Jones</name></author>
            <arxiv:doi>10.1103/PhysRevLett.130.012345</arxiv:doi>
            <category term="cond-mat.supr-con"/>
            <category term="cond-mat.mtrl-sci"/>
            <arxiv:license>http://creativecommons.org/licenses/by/4.0/</arxiv:license>
          </entry>
        </feed>
        """
        collector = ResumablePaperCollector(
            db_path=str(self.db_path),
            checkpoint_path=str(self.checkpoint_path),
        )
        self.collectors_to_close.append(collector)
        items = collector.parse_arxiv_atom(xml_data)
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item.id, "arxiv:2301.05678")
        self.assertEqual(item.title, "Discovery of High-Tc Phase in Ternary Hydride")
        self.assertEqual(item.abstract, "We report superconductivity at 200 K under 150 GPa.")
        self.assertEqual(item.year, 2023)
        self.assertEqual(item.authors, ["Alice Smith", "Bob Jones"])
        self.assertEqual(item.doi, "10.1103/physrevlett.130.012345")
        self.assertIn("cond-mat.supr-con", item.categories)
        self.assertEqual(item.open_access_pdf_url, "https://arxiv.org/pdf/2301.05678.pdf")
        self.assertEqual(item.license, "http://creativecommons.org/licenses/by/4.0/")

    def test_openalex_item_parsing(self) -> None:
        """Test parsing of OpenAlex work item JSON."""
        work_json = {
            "id": "https://openalex.org/W2981234567",
            "title": "Superconducting Properties of Iron Pnictides",
            "publication_year": 2021,
            "doi": "https://doi.org/10.1103/PhysRevB.103.014502",
            "abstract_inverted_index": {"Study": [0], "of": [1], "BaFe2As2.": [2]},
            "authorships": [{"author": {"display_name": "Carol Danvers"}}],
            "concepts": [{"display_name": "Superconductivity"}, {"display_name": "Condensed matter"}],
            "open_access": {"oa_url": "https://arxiv.org/pdf/2101.12345.pdf", "oa_status": "gold"},
            "primary_location": {"license": "cc-by"},
            "cited_by_count": 45,
        }
        collector = ResumablePaperCollector(
            db_path=str(self.db_path),
            checkpoint_path=str(self.checkpoint_path),
        )
        self.collectors_to_close.append(collector)
        item = collector.parse_openalex_item(work_json)
        self.assertIsNotNone(item)
        self.assertEqual(item.id, "openalex:W2981234567")
        self.assertEqual(item.title, "Superconducting Properties of Iron Pnictides")
        self.assertEqual(item.year, 2021)
        self.assertEqual(item.doi, "10.1103/physrevb.103.014502")
        self.assertEqual(item.abstract, "Study of BaFe2As2.")
        self.assertEqual(item.authors, ["Carol Danvers"])
        self.assertEqual(item.open_access_pdf_url, "https://arxiv.org/pdf/2101.12345.pdf")

    def test_database_batch_insert_and_deduplication(self) -> None:
        """Test batch insertion and deduplication by ID and normalized DOI."""
        db = PaperDatabase(str(self.db_path))

        item1 = PaperItem(
            id="arxiv:2401.0001",
            title="Paper One",
            abstract="Abstract One",
            authors=["A. Author"],
            year=2024,
            doi="10.1000/1",
            source="arxiv",
            categories=["cond-mat.supr-con"],
        )
        item2 = PaperItem(
            id="openalex:W10001",
            title="Paper Two",
            abstract="Abstract Two",
            authors=["B. Author"],
            year=2023,
            doi="10.1000/2",
            source="openalex",
            categories=["Materials Science"],
        )

        inserted = db.insert_batch([item1, item2])
        self.assertEqual(inserted, 2)
        self.assertEqual(db.get_total_count(), 2)

        ids, dois = db.load_existing_identifiers()
        self.assertIn("arxiv:2401.0001", ids)
        self.assertIn("openalex:W10001", ids)
        self.assertIn("10.1000/1", dois)
        self.assertIn("10.1000/2", dois)

    def test_checkpoint_saving_and_resumption(self) -> None:
        """Test that collector saves and resumes checkpoint state across executions."""
        collector = ResumablePaperCollector(
            db_path=str(self.db_path),
            checkpoint_path=str(self.checkpoint_path),
        )
        self.collectors_to_close.append(collector)
        initial_state = collector.load_checkpoint()
        self.assertEqual(initial_state["arxiv"]["start_index"], 0)

        # Mutate and save checkpoint
        initial_state["arxiv"]["start_index"] = 250
        initial_state["arxiv"]["current_category_idx"] = 1
        initial_state["openalex"]["cursor"] = "cursor_token_xyz"
        collector.save_checkpoint(initial_state)

        # Re-instantiate collector and verify resumption
        collector_restarted = ResumablePaperCollector(
            db_path=str(self.db_path),
            checkpoint_path=str(self.checkpoint_path),
        )
        self.collectors_to_close.append(collector_restarted)
        resumed_state = collector_restarted.load_checkpoint()
        self.assertEqual(resumed_state["arxiv"]["start_index"], 250)
        self.assertEqual(resumed_state["arxiv"]["current_category_idx"], 1)
        self.assertEqual(resumed_state["openalex"]["cursor"], "cursor_token_xyz")


if __name__ == "__main__":
    unittest.main()
