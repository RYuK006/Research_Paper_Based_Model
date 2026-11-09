"""
Evaluation package for rigorous scientific discovery benchmarking.
Implements the time-split evaluation methodology (pre-2021 training vs post-2021 future literature)
comparing discovery signal against random and frequency baselines.
"""

from evaluation.time_split_evaluator import TimeSplitEvaluator, EvaluationReport

__all__ = ["TimeSplitEvaluator", "EvaluationReport"]
