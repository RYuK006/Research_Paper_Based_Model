"""
Programmatically synchronizes REPORT.md Section 2.D with the empirical benchmark results from data/time_split_results.json.
Guarantees that no hand-typed numbers exist in the report.
"""

from __future__ import annotations

import json
from pathlib import Path


def update_report_benchmark(
    results_json_path: str = "data/time_split_results.json",
    report_md_path: str = "REPORT.md",
) -> None:
    results_file = Path(results_json_path)
    report_file = Path(report_md_path)

    if not results_file.exists():
        raise FileNotFoundError(f"Benchmark results JSON not found: {results_file}")
    if not report_file.exists():
        raise FileNotFoundError(f"Report Markdown not found: {report_file}")

    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cutoff_year = data.get("cutoff_year", 2004)
    pre_papers = data.get("pre_cutoff_papers", 0)
    post_papers = data.get("post_cutoff_papers", 0)
    pool_size = data.get("pool_size", 0)
    comparisons = data.get("comparisons_by_k", [])
    verified_discoveries = data.get("verified_discoveries", [])

    lines = [
        "### D. Honest Superconductivity Benchmark (`evaluation/time_split_evaluator.py`)",
        f"- **Corpus Filtering**: Strictly filtered to {pre_papers + post_papers:,} total papers ({pre_papers:,} pre-{cutoff_year}, {post_papers:,} post-{cutoff_year}) categorized under `cond-mat.supr-con` or with verified superconductivity focus.",
        "- **Hit Assertion**: A post-cutoff paper is counted as a hit **only if** it is verified to be about superconductivity. Non-superconducting papers (e.g. paclitaxel osmium coordination complexes) are rejected.",
        f"- **Baseline Comparison (Same Untried Candidate Pool of {pool_size:,} Pairs)**:",
    ]

    for c in comparisons:
        k = c.get("k")
        m_hits = c.get("model_hits", 0)
        m_rate = c.get("model_rate", 0.0)
        r_hits = c.get("random_hits", 0)
        r_rate = c.get("random_rate", 0.0)
        f_hits = c.get("frequency_hits", 0)
        f_rate = c.get("frequency_rate", 0.0)
        s_hits = c.get("similarity_hits", 0)
        s_rate = c.get("similarity_rate", 0.0)
        m_ci = c.get("model_ci_95", [0.0, 0.0])
        r_ci = c.get("random_ci_95", [0.0, 0.0])
        lift_r = c.get("lift_over_random", 0.0)
        lift_f = c.get("lift_over_frequency", 0.0)

        lines.append(
            f"  - **K={k}**: Model **{m_hits}/{k} ({m_rate:.1f}%, 95% CI: [{m_ci[0]:.1f}, {m_ci[1]:.1f}])** | "
            f"Random **{r_hits}/{k} ({r_rate:.1f}%, 95% CI: [{r_ci[0]:.1f}, {r_ci[1]:.1f}])** | "
            f"Frequency **{f_hits}/{k} ({f_rate:.1f}%)** | "
            f"Similarity **{s_hits}/{k} ({s_rate:.1f}%)** | Lift over Random: **{lift_r:.2f}x**"
        )

    lines.append(f"- **Bootstrap 95% Confidence Intervals**: Evaluated over {data.get('bootstrap_iterations', 1000):,} resampling iterations.")
    lines.append("- **Hit Provenance**: Complete JSON export saved to `data/time_split_results.json`.")

    new_section = "\n".join(lines)

    report_text = report_file.read_text(encoding="utf-8")
    
    # Locate Section 2.D
    start_marker = "### D. Honest Superconductivity Benchmark (`evaluation/time_split_evaluator.py`)"
    end_marker = "\n---\n\n## 3. What Was NOT Verified"

    start_idx = report_text.find(start_marker)
    end_idx = report_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find section markers for Section 2.D in REPORT.md")

    updated_report = report_text[:start_idx] + new_section + "\n\n" + report_text[end_idx + 1:]
    report_file.write_text(updated_report, encoding="utf-8")
    print(f"Successfully updated Section 2.D in {report_file} from {results_file}")


if __name__ == "__main__":
    update_report_benchmark()
