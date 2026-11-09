"""
Multi-Cutoff Time-Split Benchmark Runner.
Executes empirical evaluations across cutoff years 2015, 2018, and 2020.
Evaluates Model vs Random vs Frequency vs Similarity baselines with 95% bootstrap CIs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from evaluation.time_split_evaluator import (
    TimeSplitEvaluator,
    EvaluationReport,
)


def run_benchmark_for_cutoff(
    cutoff_year: int,
    db_path: str = "data/papers.db",
    k_values: List[int] = [10, 25, 50],
) -> EvaluationReport:
    print("\n" + "=" * 80)
    print(f"RUNNING TIME-SPLIT BENCHMARK: CUTOFF YEAR {cutoff_year}")
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
    print(f"Pre-Cutoff Corpus:  {report.pre_cutoff_papers:,} papers")
    print(f"Post-Cutoff Corpus: {report.post_cutoff_papers:,} papers")
    print(f"Untried Pool Size:  {report.pool_size:,} candidate element pairs")
    print(f"Metric Validity:    {'PASSED (<20% random)' if report.random_baseline_valid else 'FAILED (>20% random)'}")
    print(f"Mean Rank:          {report.mean_rank:.1f}")
    print(f"ROC AUC:            {report.roc_auc:.4f}")
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
    cutoff_years = [2015, 2018, 2020]
    summary = {}

    for cutoff in cutoff_years:
        rep = run_benchmark_for_cutoff(cutoff_year=cutoff)
        summary[cutoff] = {
            "pre_cutoff": rep.pre_cutoff_papers,
            "post_cutoff": rep.post_cutoff_papers,
            "pool_size": rep.pool_size,
            "random_baseline_valid": rep.random_baseline_valid,
            "mean_rank": rep.mean_rank,
            "roc_auc": rep.roc_auc,
            "comparisons": [c.to_dict() for c in rep.comparisons_by_k],
            "discoveries_count": len(rep.verified_discoveries),
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

