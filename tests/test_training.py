"""
Unit tests for Layer 3 training package, dataset builder, and AirLLM adapter saving.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from training.dataset_builder import InstructionSample, ScientificDatasetBuilder
from training.train_airllm import AirLLMTrainer, format_chatml_prompt


class TestTraining(unittest.TestCase):
    """Test suite for research paper training pipelines."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Setup mock database
        self.db_path = self.temp_path / "mock_papers.db"
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE papers (
                id TEXT PRIMARY KEY,
                title TEXT,
                abstract TEXT,
                year INTEGER,
                source TEXT
            )
        """)
        # Insert papers: 2 pre-2021, 1 post-2021
        papers = [
            (
                "arxiv:1803.0001",
                "Superconductivity in LaH10 under high pressure",
                "We synthesize LaH10 with cubic structure at 170 GPa. The compound exhibits superconductivity with Tc around 250 K. Further experimental studies with yttrium substitution could stabilize higher critical temperatures.",
                2018,
                "arxiv",
            ),
            (
                "openalex:W10002",
                "Synthesis of YBa2Cu3O7-delta perovskite thin films",
                "Orthorhombic YBa2Cu3O7-delta thin films were fabricated using pulsed laser deposition. Zero resistance was achieved with Tc of 92 K at ambient pressure. Dopant tuning remains an important open direction.",
                2020,
                "openalex",
            ),
            (
                "s2:2023.0003",
                "Novel hydride phases and room temperature hypotheses",
                "Recent explorations into ternary hydrides reveal superconducting transitions above 260 K at 180 GPa. Chemical precompression via nitrogen inclusion warrants immediate synchrotron investigation.",
                2023,
                "semanticscholar",
            ),
        ]
        c.executemany("INSERT INTO papers VALUES (?, ?, ?, ?, ?)", papers)
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_property_and_structure_extraction(self) -> None:
        """Test heuristic extraction of Tc, pressure, chemical formula, and crystal structure."""
        builder = ScientificDatasetBuilder(db_path=str(self.db_path), output_dir=str(self.temp_path))

        sample_text = "We synthesize cubic LaH10 with Tc around 250 K at pressure of 170 GPa."
        tc_press = builder.extract_tc_and_pressure(sample_text)
        self.assertIsNotNone(tc_press)
        self.assertIn("250 K", tc_press[0])
        self.assertIn("170 GPa", tc_press[1])

        mat_struct = builder.extract_material_and_structure(sample_text)
        self.assertIsNotNone(mat_struct)
        self.assertEqual(mat_struct[0], "LaH10")
        self.assertEqual(mat_struct[1], "Cubic")

    def test_segment_abstract_for_hypothesis(self) -> None:
        """Test splitting abstract into background context and concluding proposal."""
        builder = ScientificDatasetBuilder(db_path=str(self.db_path), output_dir=str(self.temp_path))
        abstract = (
            "Cuprate superconductors demonstrate anomalous normal state behavior. "
            "Angle-resolved photoemission spectroscopy reveals pseudogap phenomena. "
            "High magnetic field NMR studies should be conducted to probe spin fluctuations."
        )
        context, target = builder.segment_abstract_for_hypothesis(abstract)
        self.assertIn("Cuprate superconductors", context)
        self.assertIn("High magnetic field NMR", target)

    def test_sample_serialization(self) -> None:
        """Test Alpaca and ChatML format conversions."""
        sample = InstructionSample(
            sample_id="test_001",
            paper_id="paper_123",
            year=2020,
            task_type="extraction",
            instruction="Extract the critical temperature.",
            input_text="Sample text reporting Tc of 39 K in MgB2.",
            target_output="Tc is 39 K.",
            split="train_pre2021",
        )
        alpaca = sample.to_alpaca()
        self.assertEqual(alpaca["instruction"], "Extract the critical temperature.")
        self.assertEqual(alpaca["output"], "Tc is 39 K.")

        chatml = sample.to_chatml()
        self.assertEqual(len(chatml["messages"]), 3)
        self.assertEqual(chatml["messages"][0]["role"], "system")
        self.assertEqual(chatml["messages"][1]["role"], "user")
        self.assertEqual(chatml["messages"][2]["role"], "assistant")

    def test_time_split_dataset_building(self) -> None:
        """Test dataset generation correctly partitions pre-2021 and post-2021 papers."""
        output_dir = self.temp_path / "dataset"
        builder = ScientificDatasetBuilder(
            db_path=str(self.db_path),
            cutoff_year=2021,
            output_dir=str(output_dir),
        )
        stats = builder.build_dataset()

        # We had 2 pre-2021 papers (each gives 2 samples: extract + hypothesis = 4 train samples)
        # And 1 post-2021 paper (2 eval samples)
        self.assertEqual(stats["train_samples_pre2021"], 4)
        self.assertEqual(stats["eval_samples_post2021"], 2)
        self.assertTrue((output_dir / "train_pre2021_chatml.jsonl").exists())
        self.assertTrue((output_dir / "eval_post2021_chatml.jsonl").exists())

    def test_chatml_formatting_and_trainer_checkpoint(self) -> None:
        """Test ChatML prompt formatting and AirLLMTrainer checkpoint saving."""
        messages = [
            {"role": "user", "content": "What is the crystal structure of FeSe?"},
            {"role": "assistant", "content": "FeSe has a tetragonal PbO-type structure at ambient conditions."},
        ]
        formatted = format_chatml_prompt(messages)
        self.assertIn("<|start_header_id|>user<|end_header_id|>", formatted)
        self.assertIn("FeSe", formatted)

        trainer_dir = self.temp_path / "test_trainer"
        trainer = AirLLMTrainer(
            model_id="meta-llama/Llama-3.3-70B-Instruct",
            output_dir=str(trainer_dir),
            lora_r=16,
            lora_alpha=32,
        )
        ckpt_path = trainer.save_checkpoint(1, {"loss": 1.95})
        self.assertTrue(Path(ckpt_path).exists())
        self.assertTrue((Path(ckpt_path) / "adapter_config.json").exists())


if __name__ == "__main__":
    unittest.main()
