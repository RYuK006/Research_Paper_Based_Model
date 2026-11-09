"""Loader and stream-filter for Cornell University arXiv bulk metadata dataset.

Dataset: Cornell University arXiv Dataset (data/arxiv-metadata-oai-snapshot.json)
Kaggle source: https://www.kaggle.com/datasets/Cornell-University/arxiv

Filtering rules:
1. Retains all papers with category 'cond-mat.supr-con'.
2. Retains papers with category 'cond-mat.mtrl-sci' IF AND ONLY IF their title or abstract
   explicitly mentions 'superconduct*'.
3. Excludes all other arXiv categories.
4. If data/arxiv-metadata-oai-snapshot.json is missing, prints detailed download instructions
   and immediately halts without substituting another source.
5. Reports year-by-year counts compared against the current database corpus.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any, Dict, Iterator, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("load_arxiv_kaggle")

DEFAULT_SNAPSHOT_PATH = Path("data/arxiv-metadata-oai-snapshot.json")
DEFAULT_DB_PATH = Path("data/papers.db")


def print_missing_file_instructions(snapshot_path: Path) -> None:
    """Prints instructions for obtaining the Cornell arXiv dataset and halts execution."""
    msg = f"""
================================================================================
CORNELL arXiv METADATA SNAPSHOT MISSING
================================================================================
Expected file location:
  {snapshot_path.resolve()}

The Cornell University arXiv bulk metadata snapshot was not found.
To acquire the authoritative dataset:

1. Web Download:
   Visit Kaggle: https://www.kaggle.com/datasets/Cornell-University/arxiv
   Download 'arxiv-metadata-oai-snapshot.json' (~3.8 GB uncompressed JSON Lines).

2. Kaggle CLI Download:
   Run:
     kaggle datasets download -d Cornell-University/arxiv -f arxiv-metadata-oai-snapshot.json -p data/
   If downloaded as a zip archive, extract arxiv-metadata-oai-snapshot.json into data/.

3. Placement:
   Ensure the file is located exactly at:
     {snapshot_path}

Per benchmark integrity guidelines, NO SUBSTITUTE SOURCE will be used.
Halting operation.
================================================================================
"""
    print(msg, file=sys.stderr)


def extract_year_from_arxiv_record(record: Dict[str, Any]) -> Optional[int]:
    """Extracts publication/submission year from an arXiv record.

    Checks:
    1. First version submission date in versions list ('created': 'Mon, 2 Apr 2007...')
    2. arXiv ID pattern (YYMM.NNNNN or category/YYMMNNN)
    3. update_date field (YYYY-MM-DD)
    """
    versions = record.get("versions")
    if versions and isinstance(versions, list) and len(versions) > 0:
        first_created = versions[0].get("created", "")
        # e.g., 'Mon, 2 Apr 2007 19:18:42 GMT'
        match = re.search(r"\b(19\d\d|20\d\d)\b", first_created)
        if match:
            return int(match.group(1))

    arxiv_id = str(record.get("id", "")).strip()
    # New format: YYMM.NNNNN
    match_new = re.match(r"^(\d{2})(\d{2})\.\d+", arxiv_id)
    if match_new:
        yy = int(match_new.group(1))
        return 1900 + yy if yy >= 90 else 2000 + yy

    # Old format: arch-ive/YYMMNNN
    match_old = re.search(r"/(\d{2})(\d{2})\d{3}", arxiv_id)
    if match_old:
        yy = int(match_old.group(1))
        return 1900 + yy if yy >= 90 else 2000 + yy

    update_date = str(record.get("update_date", "")).strip()
    match_up = re.match(r"^(19\d\d|20\d\d)", update_date)
    if match_up:
        return int(match_up.group(1))

    return None


def is_relevant_arxiv_paper(categories_str: str, title: str, abstract: str) -> bool:
    """Applies strict category and superconductivity keyword filter."""
    cats = (categories_str or "").lower().split()
    if "cond-mat.supr-con" in cats:
        return True

    if "cond-mat.mtrl-sci" in cats:
        combined_text = f"{title or ''} {abstract or ''}".lower()
        if "superconduct" in combined_text:
            return True

    return False


def stream_arxiv_snapshot(snapshot_path: Path) -> Iterator[Dict[str, Any]]:
    """Yields parsed records matching filtering criteria from snapshot file."""
    with open(snapshot_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            cats = record.get("categories", "")
            title = record.get("title", "")
            abstract = record.get("abstract", "")

            if is_relevant_arxiv_paper(cats, title, abstract):
                record["_extracted_year"] = extract_year_from_arxiv_record(record)
                yield record


def get_current_corpus_year_histogram(db_path: Path) -> Dict[int, int]:
    """Retrieves year histogram from current database."""
    if not db_path.exists():
        return {}
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("""
        SELECT year, count(*)
        FROM papers
        WHERE year IS NOT NULL AND year BETWEEN 1990 AND 2026
        GROUP BY year
        ORDER BY year ASC
    """)
    hist = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return hist


def report_coverage_comparison(
    snapshot_hist: Dict[int, int],
    corpus_hist: Dict[int, int]
) -> str:
    """Generates comparison table of papers per year."""
    all_years = sorted(set(list(snapshot_hist.keys()) + list(corpus_hist.keys())))
    lines = [
        "==========================================================================",
        "SUPERCONDUCTIVITY PAPERS PER YEAR: KAGGLE SNAPSHOT VS CURRENT CORPUS",
        "==========================================================================",
        f"{'Year':<8} | {'Kaggle Snapshot':<18} | {'Current Database':<18} | {'Delta':<10}",
        "---------+--------------------+--------------------+-----------"
    ]
    tot_snap = sum(snapshot_hist.values())
    tot_corp = sum(corpus_hist.values())

    for yr in all_years:
        snap_count = snapshot_hist.get(yr, 0)
        corp_count = corpus_hist.get(yr, 0)
        delta = snap_count - corp_count
        delta_str = f"{delta:+d}" if delta != 0 else "0"
        lines.append(f"{yr:<8} | {snap_count:<18} | {corp_count:<18} | {delta_str:<10}")

    lines.append("---------+--------------------+--------------------+-----------")
    tot_delta = tot_snap - tot_corp
    lines.append(f"{'TOTAL':<8} | {tot_snap:<18} | {tot_corp:<18} | {tot_delta:+d}")
    lines.append("==========================================================================")
    return "\n".join(lines)


def process_arxiv_snapshot(
    snapshot_path: Path = DEFAULT_SNAPSHOT_PATH,
    db_path: Path = DEFAULT_DB_PATH,
    insert_to_db: bool = False
) -> Optional[Dict[str, Any]]:
    """Validates existence of snapshot file, filters records, and outputs comparison."""
    if not snapshot_path.exists():
        print_missing_file_instructions(snapshot_path)
        return None

    logger.info(f"Scanning Cornell arXiv snapshot from: {snapshot_path}")
    snapshot_hist: Dict[int, int] = {}
    total_matched = 0

    for rec in stream_arxiv_snapshot(snapshot_path):
        total_matched += 1
        yr = rec.get("_extracted_year")
        if yr:
            snapshot_hist[yr] = snapshot_hist.get(yr, 0) + 1

    current_corpus_hist = get_current_corpus_year_histogram(db_path)
    report_text = report_coverage_comparison(snapshot_hist, current_corpus_hist)
    print(report_text)

    return {
        "total_matched": total_matched,
        "snapshot_histogram": snapshot_hist,
        "corpus_histogram": current_corpus_hist
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Stream-filter Cornell arXiv snapshot metadata.")
    parser.add_argument(
        "--snapshot-path",
        type=Path,
        default=DEFAULT_SNAPSHOT_PATH,
        help="Path to arxiv-metadata-oai-snapshot.json"
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to SQLite database"
    )
    args = parser.parse_args()

    res = process_arxiv_snapshot(args.snapshot_path, args.db_path)
    if res is None:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

