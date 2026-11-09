"""
Unit tests for Layerwise Streaming LoRA Trainer, Disk Budget, Sequence Packing,
and Gating Suite (C2 Correctness and C3 Throughput).
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from training.layerwise_trainer import (
    DiskBudget,
    DiskBudgetManager,
    LayerShardManager,
    LayerwiseModel,
    MockLinearLoRA,
    SequencePacker,
    run_correctness_gate,
    run_throughput_gate,
)


class TestLayerwiseTrainer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_disk_budget_manager(self):
        budget = DiskBudget(max_disk_gb=90.0, base_weights_gb=45.0, safety_margin_gb=5.0)
        self.assertEqual(budget.max_activation_spill_gb, 40.0)

        manager = DiskBudgetManager(budget)
        max_tokens = budget.calculate_max_tokens_per_step(num_layers=80, hidden_dim=8192, bytes_per_elem=2)
        self.assertGreater(max_tokens, 10000)

        feasible, total_gb = manager.check_budget_feasibility(num_tokens=2048, num_layers=80, hidden_dim=8192)
        self.assertTrue(feasible)
        self.assertLess(total_gb, 90.0)

        # Excessively large tokens should fail budget
        feasible_big, total_gb_big = manager.check_budget_feasibility(num_tokens=100000, num_layers=80, hidden_dim=8192)
        self.assertFalse(feasible_big)
        self.assertGreater(total_gb_big, 90.0)

    def test_sequence_packer(self):
        packer = SequencePacker(max_tokens_per_step=10)
        seqs = [
            np.array([1, 2, 3]),
            np.array([4, 5]),
            np.array([6, 7, 8, 9]),
            np.array([10, 11]),
        ]
        packed = list(packer.pack(seqs))
        # Total tokens = 3 + 2 + 4 + 2 = 11.
        # Pack 1: [1,2,3,4,5,6,7,8,9] = length 9 <= 10
        # Pack 2: [10, 11] = length 2 <= 10
        self.assertEqual(len(packed), 2)
        self.assertEqual(len(packed[0]), 9)
        self.assertEqual(len(packed[1]), 2)
        self.assertTrue(np.array_equal(packed[0], np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])))
        self.assertTrue(np.array_equal(packed[1], np.array([10, 11])))

    def test_mock_linear_lora(self):
        np.random.seed(42)
        layer = MockLinearLoRA(in_dim=16, out_dim=16, r=4, alpha=8.0)
        x = np.random.randn(4, 16).astype(np.float32)

        out = layer.forward(x)
        self.assertEqual(out.shape, (4, 16))

        grad_out = np.ones((4, 16), dtype=np.float32)
        dx = layer.backward(x, grad_out)
        self.assertEqual(dx.shape, (4, 16))
        # With B initialized to zero (standard LoRA), grad_B is non-zero, grad_A is 0 on step 0
        self.assertFalse(np.all(layer.grad_B == 0))

        # Once B is non-zero, grad_A becomes non-zero
        layer.B += 0.05
        layer.grad_A.fill(0)
        layer.backward(x, grad_out)
        self.assertFalse(np.all(layer.grad_A == 0))

        # Test unloading error
        layer.unload()
        with self.assertRaises(RuntimeError):
            layer.forward(x)

    def test_layerwise_model_forward_backward(self):
        np.random.seed(42)
        model = LayerwiseModel(num_layers=3, hidden_dim=16, storage_dir=self.storage_dir, r=4)
        x = np.random.randn(2, 16).astype(np.float32)

        # Forward
        out = model.forward_layerwise(x)
        self.assertEqual(out.shape, (2, 16))

        # Backward
        grad_loss = np.ones_like(out)
        grad_norm = model.backward_layerwise(grad_loss)
        self.assertGreater(grad_norm, 0.0)

        # Optimizer step
        orig_B = model.lora_params[0]["B"].copy()
        model.optimizer_step(lr=1e-2)
        self.assertFalse(np.allclose(orig_B, model.lora_params[0]["B"]))
        # Gradients should be zeroed after optimizer step
        self.assertTrue(np.all(model.lora_params[0]["grad_A"] == 0))
        self.assertTrue(np.all(model.lora_params[0]["grad_B"] == 0))

    def test_layerwise_checkpoint_and_resume(self):
        np.random.seed(42)
        ckpt_dir = self.storage_dir / "checkpoints"
        model = LayerwiseModel(num_layers=2, hidden_dim=8, storage_dir=self.storage_dir, r=2)

        # Modify LoRA params to non-trivial values
        model.lora_params[0]["A"] += 0.5
        model.lora_params[1]["B"] += 0.75

        step_dir = model.save_lora_checkpoint(ckpt_dir, step=42)
        self.assertTrue(step_dir.exists())
        self.assertTrue((step_dir / "manifest.json").exists())
        self.assertTrue((step_dir / "lora_weights.npz").exists())

        # Create new model and load checkpoint
        model_resume = LayerwiseModel(num_layers=2, hidden_dim=8, storage_dir=self.storage_dir / "m2", r=2)
        restored_step = model_resume.load_lora_checkpoint(step_dir)

        self.assertEqual(restored_step, 42)
        self.assertTrue(np.allclose(model.lora_params[0]["A"], model_resume.lora_params[0]["A"]))
        self.assertTrue(np.allclose(model.lora_params[1]["B"], model_resume.lora_params[1]["B"]))

    def test_c2_correctness_gate(self):
        res = run_correctness_gate(steps=5, hidden_dim=32, num_layers=3)
        self.assertTrue(res["passed"])
        self.assertLess(res["max_loss_rel_error"], 1e-3)
        self.assertLess(res["max_grad_rel_error"], 1e-3)

    def test_c3_throughput_gate(self):
        res = run_throughput_gate()
        self.assertTrue(res["exceeds_24h_budget"])
        self.assertGreater(res["hours_for_2m_tokens"], 24.0)
        self.assertGreater(res["io_fraction_pct"], 90.0)


if __name__ == "__main__":
    unittest.main()
