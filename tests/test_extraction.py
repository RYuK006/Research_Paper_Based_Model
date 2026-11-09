"""
Unit tests for Layer 2 structured extraction and discovery gap analysis.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from extraction.extractor import StructuredExtractor
from extraction.gap_analyzer import DiscoveryGapAnalyzer
from extraction.models import ExtractedPaperRecord
from extraction.validator import ExtractionValidator


class TestExtraction(unittest.TestCase):
    """Test suite for Layer 2 extraction and discovery gap engine."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "test_extract.db"

        # Create mock database with structured_materials table
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE structured_materials (
                paper_id TEXT PRIMARY KEY,
                doi TEXT,
                year INTEGER,
                material TEXT,
                composition TEXT,
                elements_json TEXT,
                structure_type TEXT,
                tc_kelvin REAL,
                pressure_gpa REAL,
                synthesis_method TEXT,
                measurement_type TEXT,
                future_work TEXT,
                confidence REAL
            )
        """)
        # Insert records illustrating gap discovery:
        # e.g., Cuprate perovskites (La, Cu, O) and (Y, Cu, O) - both have Cu and O as shared partners,
        # but La and Y co-doping was not synthesized.
        records = [
            (
                "p1", "10.1/1", 2018, "La2CuO4", "La2CuO4", json.dumps(["Cu", "La", "O"]),
                "Perovskite", 40.0, 0.0001, "Solid-state reaction", "Electrical resistivity",
                "Further study of alternative rare-earth substitution is warranted.", 0.9
            ),
            (
                "p2", "10.1/2", 2019, "YBa2Cu3O7", "YBa2Cu3O7", json.dumps(["Ba", "Cu", "O", "Y"]),
                "Perovskite", 92.0, 0.0001, "Pulsed laser deposition", "SQUID",
                "High pressure studies could reveal competing electronic phases.", 0.95
            ),
            (
                "p3", "10.1/3", 2020, "LaH10", "LaH10", json.dumps(["H", "La"]),
                "Clathrate", 250.0, 170.0, "Laser-heated diamond anvil cell", "Synchrotron XRD",
                "Ternary hydride synthesis with cerium or yttrium remains an open question.", 0.95
            ),
        ]
        c.executemany("INSERT INTO structured_materials VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", records)
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_extractor_property_parsing(self) -> None:
        """Test extraction of formula, elements, Tc, and pressure."""
        extractor = StructuredExtractor(db_path=str(self.db_path))
        sample_text = (
            "We synthesize cubic LaH10 with laser-heated diamond anvil cell at 170 GPa. "
            "Superconducting transition temperature Tc reaches 250 K. "
            "Electrical resistivity and synchrotron X-ray diffraction were measured. "
            "Future work should explore lower pressure stabilization."
        )

        rec = extractor.extract_record("test_id", "High Pressure LaH10", sample_text, 2019)
        self.assertEqual(rec.material, "LaH10")
        self.assertIn("La", rec.elements)
        self.assertIn("H", rec.elements)
        self.assertEqual(rec.structure_type, "Cubic")
        self.assertEqual(rec.tc_kelvin, 250.0)
        self.assertEqual(rec.pressure_gpa, 170.0)
        self.assertEqual(rec.synthesis_method, "Laser-heated diamond anvil cell")
        self.assertGreaterEqual(rec.confidence, 0.8)

    def test_gap_analyzer_untried_elements(self) -> None:
        """Test finding element combinations that share partners but were never co-doped."""
        analyzer = DiscoveryGapAnalyzer(db_path=str(self.db_path))
        untried = analyzer.find_untried_element_combinations(min_element_freq=1, top_n=5)

        self.assertGreater(len(untried), 0)
        # Look for pairs sharing Cu or O
        pair_elems = [(u["element_1"], u["element_2"]) for u in untried]
        # In our records: La has Cu, O, H. Y has Ba, Cu, O.
        # So (La, Y) share Cu and O, but (La, Y) was never co-doped!
        self.assertTrue(
            any(("La" in p and "Y" in p) for p in pair_elems),
            f"Expected (La, Y) in untried candidates, got {pair_elems}"
        )

    def test_gap_analyzer_cross_family_synthesis(self) -> None:
        """Test identifying cross-family synthesis opportunities."""
        analyzer = DiscoveryGapAnalyzer(db_path=str(self.db_path))
        # Add another record so count >= 2
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            INSERT INTO structured_materials VALUES (
                'p4', '10.1/4', 2021, 'YH9', 'YH9', '["H", "Y"]',
                'Clathrate', 240.0, 160.0, 'Laser-heated diamond anvil cell',
                'Electrical resistivity', 'Open lead', 0.9
            )
        """)
        conn.commit()
        conn.close()

        cross_methods = analyzer.find_cross_family_synthesis_methods(top_n=5)
        self.assertGreater(len(cross_methods), 0)
        # Laser-heated diamond anvil cell is used in Clathrate (2 papers), but 0 in Perovskite
        clathrate_to_perov = [
            c for c in cross_methods
            if c["established_family"] == "Clathrate" and c["target_family"] == "Perovskite"
        ]
        self.assertEqual(len(clathrate_to_perov), 1)
        self.assertEqual(clathrate_to_perov[0]["synthesis_method"], "Laser-heated diamond anvil cell")

    def test_extraction_validator_accuracy(self) -> None:
        """Test validation harness against hand-checked gold standard benchmarks."""
        validator = ExtractionValidator()
        report = validator.evaluate_benchmark_sample()
        self.assertGreaterEqual(report["overall_accuracy"], 0.85)
        self.assertEqual(report["validation_status"], "PASSED")


if __name__ == "__main__":
    unittest.main()
