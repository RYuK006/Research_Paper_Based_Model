"""
Harvest Progress and Database Statistics Monitor.
Prints total papers, distribution by source, year histogram, and category counts.
"""

import json
import sqlite3
from collections import Counter
from pathlib import Path


def inspect_database(db_path: str = "data/papers.db"):
    db_file = Path(db_path)
    if not db_file.exists():
        print(f"Database not found at {db_file}")
        return

    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()

    # 1. Total papers
    cur.execute("SELECT COUNT(*) FROM papers")
    total_papers = cur.fetchone()[0]

    # 2. Source distribution
    cur.execute("SELECT source, COUNT(*) FROM papers GROUP BY source ORDER BY COUNT(*) DESC")
    source_counts = cur.fetchall()

    # 3. Year histogram
    cur.execute("SELECT year, COUNT(*) FROM papers WHERE year IS NOT NULL GROUP BY year ORDER BY year")
    year_counts = cur.fetchall()

    # 4. Superconductivity count
    cur.execute("SELECT title, abstract, categories, year FROM papers")
    rows = cur.fetchall()

    from evaluation.time_split_evaluator import TimeSplitEvaluator
    evaluator = TimeSplitEvaluator(db_path=db_path)

    sc_total = 0
    sc_by_cutoff = {"pre_2015": 0, "post_2015": 0, "post_2018": 0, "post_2020": 0}
    cat_counter = Counter()

    for title, abstract, cats_json, year in rows:
        # Category aggregation
        if cats_json:
            try:
                cats = json.loads(cats_json)
                if isinstance(cats, list):
                    for c in cats:
                        cat_counter[c] += 1
            except Exception:
                pass

        # Superconductivity filter
        if evaluator.is_superconductivity_research_paper(title, abstract, cats_json):
            sc_total += 1
            if year:
                if year <= 2015:
                    sc_by_cutoff["pre_2015"] += 1
                if year > 2015:
                    sc_by_cutoff["post_2015"] += 1
                if year > 2018:
                    sc_by_cutoff["post_2018"] += 1
                if year > 2020:
                    sc_by_cutoff["post_2020"] += 1

    conn.close()

    print("\n" + "=" * 70)
    print("PAPERS DATABASE PROGRESS & METRICS")
    print("=" * 70)
    print(f"Total Papers in papers.db:    {total_papers:,} / 50,000")
    print(f"Superconductivity Papers:     {sc_total:,}")
    print(f"  - Pre-2015:                 {sc_by_cutoff['pre_2015']:,}")
    print(f"  - Post-2015 (>2015):        {sc_by_cutoff['post_2015']:,}")
    print(f"  - Post-2018 (>2018):        {sc_by_cutoff['post_2018']:,}")
    print(f"  - Post-2020 (>2020):        {sc_by_cutoff['post_2020']:,}")
    print("-" * 70)
    print("Source Breakdown:")
    for src, cnt in source_counts:
        print(f"  {src:18s}: {cnt:,} ({cnt/total_papers*100:.1f}%)")
    print("-" * 70)
    print("Year Histogram (Recent Years 2010-2026):")
    recent_years = [y for y in year_counts if y[0] and y[0] >= 2010]
    for yr, cnt in recent_years:
        bar = "█" * min(50, int(cnt / 50))
        print(f"  {yr}: {cnt:5,d} {bar}")
    print("-" * 70)
    print("Top 15 Categories/Concepts:")
    for cat, cnt in cat_counter.most_common(15):
        print(f"  {cat:35s}: {cnt:,}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    inspect_database()
