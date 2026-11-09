"""
Training package for Layer 3 research paper fine-tuning and instruction dataset building.
Supports AirLLM layer-streaming LoRA training on ultra-high parameter models (70B, 405B),
Unsloth QLoRA, and time-split scientific discovery evaluation.
"""

from training.dataset_builder import ScientificDatasetBuilder

__all__ = ["ScientificDatasetBuilder"]
