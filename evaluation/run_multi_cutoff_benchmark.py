"""Multi-Cutoff Time-Split Benchmark Runner.

Executes frozen empirical evaluations across cutoff years:
- Previously unexamined: 2012, 2022
- Core historical cutoffs: 2015, 2018, 2020

Evaluates Model vs Random vs Frequency vs Similarity baselines with:
- Top-K hit rates and Wilson 95% CIs
- Paired bootstrap 95% CIs on Top-K (Model - Frequency)
- Full-pool ROC AUC and Mean Rank for all 4 baselines
- Paired bootstrap 95% CIs on Δ(Model - Frequency) ROC AUC
- Temporal publication rate tracking and loud imbalance warnings
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from evaluation.time_split_evaluator import (
    EvaluationReport,
    TimeSplitEvaluator,
)


def run_benchmark_for_cutoff(
    cutoff_year: int,
    db_path: str = "data/papers.db",
    k_values: List[int] = [10, 25, 50],
) -> EvaluationReport:
    print("\n" + "=" * 80)
    print(f"RUNNING FROZEN TIME-SPLIT BENCHMARK: CUTOFF YEAR {cutoff_year}")
    print("=" * 80)

    evaluator = TimeSplitEvaluator(
        db_path=db_path,
        cutoff_year=cutoff_year,
    )
    report = evaluator.evaluate(k_values=k_values)

    json_path = f"data/time_split_results_{cutoff_year}.json"
    md_path = f"TIME_SPLIT_EVALUATION_{cutoff_year}.md"

    evaluator.save_report_json(report, output_path=json_path)
    evaluator.generate_markdown_report(report, output_path=md_path)

    # If cutoff is 2018 (primary benchmark), also update default paths
    if cutoff_year == 2018:
        evaluator.save_report_json(report, output_path="data/time_split_results.json")
        evaluator.generate_markdown_report(report, output_path="TIME_SPLIT_EVALUATION.md")

    print(f"Cutoff Year:        {report.cutoff_year}")
    print(f"Pre-Cutoff Corpus:  {report.pre_cutoff_papers:,} papers ({report.pre_rate_per_year:.1f} papers/yr)")
    print(f"Post-Cutoff Corpus: {report.post_cutoff_papers:,} papers ({report.post_rate_per_year:.1f} papers/yr)")
    print(f"Rate Ratio:         {report.temporal_rate_ratio:.2f}x ({'⚠️ IMBALANCE > 2x' if report.temporal_imbalance_warning else 'NORMAL'})")
    print(f"Untried Pool Size:  {report.pool_size:,} candidate element pairs")
    print(f"Metric Validity:    {'PASSED (<20% random)' if report.random_baseline_valid else 'FAILED (>20% random)'}")
    print(f"Model AUC:          {report.auc_model:.4f} (Mean Rank: {report.mean_rank_model:.1f})")
    print(f"Freq  AUC:          {report.auc_frequency:.4f} (Mean Rank: {report.mean_rank_frequency:.1f})")
    print(f"Sim   AUC:          {report.auc_similarity:.4f} (Mean Rank: {report.mean_rank_similarity:.1f})")
    print(f"Rand  AUC:          {report.auc_random:.4f} (Mean Rank: {report.mean_rank_random:.1f})")
    print(f"ΔAUC (M - F) 95% CI: [{report.paired_auc_diff_ci_95[0]:+.4f}, {report.paired_auc_diff_ci_95[1]:+.4f}]")
    print(f"Bootstrap Trials:   {report.bootstrap_iterations:,}")
    print("-" * 80)

    # Power status check
    is_underpowered = report.post_cutoff_papers < 200
    if is_underpowered:
        print(f"⚠️ STATISTICAL POWER: UNDERPOWERED (< 200 post-cutoff papers: {report.post_cutoff_papers:,})")
    else:
        print(f"✅ STATISTICAL POWER: ADEQUATELY POWERED (>= 200 post-cutoff papers: {report.post_cutoff_papers:,})")

    print("-" * 80)
    print("METRICS BY K CUTOFF:")
    for c in report.comparisons_by_k:
        model_str = f"Model: {c.model_hits:2d}/{c.k} ({c.model_rate:5.1f}%, 95% CI: [{c.model_ci_95[0]:.1f}, {c.model_ci_95[1]:.1f}]%)"
        freq_str  = f"Freq:  {c.frequency_hits:2d}/{c.k} ({c.frequency_rate:5.1f}%, 95% CI: [{c.frequency_ci_95[0]:.1f}, {c.frequency_ci_95[1]:.1f}]%)"
        rand_str  = f"Rand:  {c.random_hits:2d}/{c.k} ({c.random_rate:5.1f}%, 95% CI: [{c.random_ci_95[0]:.1f}, {c.random_ci_95[1]:.1f}]%)"
        sim_str   = f"Sim:   {c.similarity_hits:2d}/{c.k} ({c.similarity_rate:5.1f}%, 95% CI: [{c.similarity_ci_95[0]:.1f}, {c.similarity_ci_95[1]:.1f}]%)"
        diff_str  = f"Diff CI: [{c.paired_diff_ci_95[0]:+.1f}, {c.paired_diff_ci_95[1]:+.1f}]"

        if c.paired_diff_ci_95[0] > 0.0:
            verdict = "MODEL BEATS FREQUENCY (STAT SIG)"
        elif c.model_hits > c.frequency_hits:
            verdict = "MODEL BEATS FREQ (CI CROSSES 0)"
        elif c.model_hits == c.frequency_hits:
            verdict = "MODEL TIES FREQUENCY (=)"
        else:
            verdict = "FREQUENCY BEATS MODEL (-)"

        print(f"  K={c.k:2d} -> {verdict:32s} | {model_str} | {freq_str} | {rand_str} | {sim_str} | {diff_str}")

    print("-" * 80)
    print(f"VERIFIED POST-CUTOFF DISCOVERIES IN TOP PREDICTIONS ({len(report.verified_discoveries)}):")
    for i, d in enumerate(report.verified_discoveries[:10], 1):
        pair_str = f"[{d.element_pair[0]}-{d.element_pair[1]}]"
        doi_str = d.doi or d.paper_id
        print(f"  {i:2d}. {pair_str:10s} '{d.title}' ({d.year}, DOI: {doi_str})")

    print("=" * 80 + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run multi-cutoff time-split benchmark")
    parser.add_argument(
        "--cutoffs",
        nargs="+",
        type=int,
        default=[2012, 2015, 2018, 2020, 2022],
        help="List of cutoff years to evaluate"
    )
    parser.add_argument("--db-path", default="data/papers.db", help="Path to papers.db")
    args = parser.parse_args()

    summary: Dict[int, Any] = {}

    for cutoff in args.cutoffs:
        rep = run_benchmark_for_cutoff(cutoff_year=cutoff, db_path=args.db_path)
        summary[cutoff] = {
            "pre_cutoff": rep.pre_cutoff_papers,
            "post_cutoff": rep.post_cutoff_papers,
            "pre_rate_per_year": rep.pre_rate_per_year,
            "post_rate_per_year": rep.post_rate_per_year,
            "temporal_rate_ratio": rep.temporal_rate_ratio,
            "temporal_imbalance_warning": rep.temporal_imbalance_warning,
            "pool_size": rep.pool_size,
            "random_baseline_valid": rep.random_baseline_valid,
            "mean_rank": rep.mean_rank_model,
            "roc_auc": rep.auc_model,
            "auc_model": rep.auc_model,
            "auc_frequency": rep.auc_frequency,
            "auc_similarity": rep.auc_similarity,
            "auc_random": rep.auc_random,
            "mean_rank_model": rep.mean_rank_model,
            "mean_rank_frequency": rep.mean_rank_frequency,
            "mean_rank_similarity": rep.mean_rank_similarity,
            "mean_rank_random": rep.mean_rank_random,
            "paired_auc_diff_ci_95": rep.paired_auc_diff_ci_95,
            "comparisons": [c.to_dict() for c in rep.comparisons_by_k],
            "discoveries_count": len(report_discoveries := rep.verified_discoveries),
        }

    # Save aggregated summary
    summary_path = Path("data/multi_cutoff_benchmark_summary.json")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Sync REPORT.md Section 2.D
    from evaluation.update_report_benchmark import update_report_benchmark
    update_report_benchmark(summary_json_path=str(summary_path))


if __name__ == "__main__":
    main()
