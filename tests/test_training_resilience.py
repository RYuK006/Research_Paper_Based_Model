"""
Unit tests for Guaranteed Baseline Training Resilience and Resumption (colab/train.py).
Tests:
1. Manifest atomic save and byte-level copy verification.
2. Simulated mid-run kill: verifies exact restoration of step, shard index, dataloader position, and RNG state.
3. CPU smoke-test execution on small sample.
4. Held-out evaluation and 10 discovery prompt completions.
"""

import json
import random
import tempfile
import unittest
from pathlib import Path

from colab.train import (
    CheckpointMeta,
    ManifestManager,
    ResearchLMTrainer,
    ShardManager,
    DISCOVERY_PROMPTS_POST_CUTOFF,
)


class TestTrainingResilience(unittest.TestCase):
    """Test suite for checkpoint resilience, shard streaming, and resumption."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.temp_path = Path(self.temp_dir.name)
        self.drive_root = self.temp_path / "mock_drive"
        self.local_root = self.temp_path / "mock_local"
        self.db_path = self.temp_path / "test_papers.db"

        # Initialize mock database with sample papers
        import sqlite3
        conn = sqlite3.connect(str(self.db_path))
        try:
            conn.execute("""
                CREATE TABLE papers (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    abstract TEXT,
                    authors TEXT,
                    year INTEGER,
                    doi TEXT,
                    source TEXT,
                    categories TEXT,
                    citation_count INTEGER,
                    open_access_pdf_url TEXT,
                    local_file_path TEXT,
                    download_status TEXT,
                    collected_at TEXT,
                    raw_json TEXT
                )
            """)
            papers = []
            for i in range(120):
                papers.append((
                    f"p_{i}",
                    f"Superconductivity Paper {i}",
                    f"High-temperature study of superconducting hydride {i} under pressure.",
                    json.dumps(["A. Physicist"]),
                    2002 if i < 100 else 2015,
                    f"10.1000/{i}",
                    "arxiv",
                    json.dumps(["cond-mat.supr-con"]),
                    10,
                    None,
                    None,
                    "metadata_only",
                    "2026-11-09T00:00:00Z",
                    json.dumps({}),
                ))
            conn.executemany("INSERT INTO papers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", papers)
            conn.commit()
        finally:
            conn.close()

    def tearDown(self) -> None:
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_manifest_verification_and_sync(self) -> None:
        """Test that checkpoint files are verified byte-for-byte and manifest is atomically updated."""
        manifest_mgr = ManifestManager(self.drive_root, self.local_root)
        local_ckpt = self.local_root / "checkpoints" / "ckpt-001"
        local_ckpt.mkdir(parents=True, exist_ok=True)
        (local_ckpt / "weights.bin").write_bytes(b"TEST_WEIGHTS_BYTES_12345")

        meta = CheckpointMeta(
            checkpoint_name="ckpt-001",
            global_step=50,
            shard_index=1,
            dataloader_position=120,
            loss=1.234,
            verified_at="2026-11-09T00:00:00Z",
        )

        success = manifest_mgr.save_and_verify_checkpoint(local_ckpt, meta)
        self.assertTrue(success)

        # Verify Drive contents
        drive_file = self.drive_root / "checkpoints" / "ckpt-001" / "weights.bin"
        self.assertTrue(drive_file.exists())
        self.assertEqual(drive_file.read_bytes(), b"TEST_WEIGHTS_BYTES_12345")

        # Verify Manifest
        loaded_manifest = manifest_mgr.load_manifest()
        self.assertIsNotNone(loaded_manifest["latest_checkpoint"])
        self.assertEqual(loaded_manifest["latest_checkpoint"]["global_step"], 50)
        self.assertEqual(loaded_manifest["latest_checkpoint"]["shard_index"], 1)

    def test_simulated_mid_run_kill_and_exact_resumption(self) -> None:
        """
        Simulates mid-run session kill:
        1. Run training to step 10 with checkpoint_interval=5.
        2. Verify checkpoint saved at step 10 with exact dataloader pos and RNG state.
        3. Delete the trainer object (simulating Colab session drop).
        4. Instantiate a new trainer pointing to Drive.
        5. Verify auto_resume_from_manifest restores exact step (10), shard, dataloader pos, and RNG state.
        6. Continue training to step 20 without repeating steps 1-10.
        """
        random.seed(12345)
        trainer_run1 = ResearchLMTrainer(
            drive_root=str(self.drive_root),
            local_root=str(self.local_root),
            db_path=str(self.db_path),
            cutoff_year=2004,
            smoke_test=True,
            checkpoint_interval=5,
            max_steps=10,
        )

        res1 = trainer_run1.run_training_loop()
        self.assertEqual(res1["final_step"], 10)

        # Inspect checkpoint state
        manifest = trainer_run1.manifest_mgr.load_manifest()
        latest = manifest["latest_checkpoint"]
        self.assertEqual(latest["global_step"], 10)
        saved_shard = latest["shard_index"]
        saved_pos = latest["dataloader_position"]
        saved_rng = latest["rng_state"]
        self.assertIsNotNone(saved_rng)

        # Simulate kill by deleting trainer_run1
        del trainer_run1

        # Start fresh session (e.g. user hits 'Run all' after reconnect)
        trainer_run2 = ResearchLMTrainer(
            drive_root=str(self.drive_root),
            local_root=str(self.local_root),
            db_path=str(self.db_path),
            cutoff_year=2004,
            smoke_test=True,
            checkpoint_interval=5,
            max_steps=20,  # Extend to 20
        )

        trainer_run2.auto_resume_from_manifest()

        # Strict equality assertions on restored state
        self.assertEqual(trainer_run2.global_step, 10, "Global step must be restored exactly.")
        self.assertEqual(trainer_run2.current_shard_idx, saved_shard, "Shard index must be restored exactly.")
        self.assertEqual(trainer_run2.dataloader_pos, saved_pos, "Dataloader position must be restored exactly.")
        self.assertEqual(trainer_run2.rng_state, saved_rng, "RNG state must be restored exactly.")

        # Continue training
        res2 = trainer_run2.run_training_loop()
        self.assertEqual(res2["final_step"], 20, "Should continue from step 10 to step 20.")

    def test_held_out_evaluation_and_discovery_prompts(self) -> None:
        """Test held-out evaluation on post-cutoff papers and prompt completions."""
        trainer = ResearchLMTrainer(
            drive_root=str(self.drive_root),
            local_root=str(self.local_root),
            db_path=str(self.db_path),
            smoke_test=True,
        )
        eval_res = trainer.evaluate_held_out()
        self.assertIn("base_perplexity", eval_res)
        self.assertIn("finetuned_perplexity", eval_res)
        self.assertIn("perplexity_reduction_pct", eval_res)
        self.assertEqual(len(eval_res["completions"]), 10)
        self.assertEqual(len(DISCOVERY_PROMPTS_POST_CUTOFF), 10)

        # Verify output json written
        self.assertTrue((self.local_root / "held_out_eval_results.json").exists())


if __name__ == "__main__":
    unittest.main()
