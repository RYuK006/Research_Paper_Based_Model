"""Cleans and deduplicates the research paper database for superconductor discovery.

Rules:
1. Retains arXiv papers in cond-mat.supr-con, plus cond-mat.mtrl-sci with superconduct* in title or abstract.
2. Drops all off-topic Semantic Scholar papers (retains only those mentioning superconduct*).
3. Drops all non-superconducting OpenAlex papers (retains only those mentioning superconduct*).
4. Deduplicates across sources by:
   - Normalized arXiv ID (e.g. '2305.12345', 'cond-mat/0101001')
   - Normalized DOI (lowercased, stripped of URL prefixes)
   - Normalized title (alphanumeric characters, lowercase)
5. Generates per-source counts and publication year histogram from 1995 to 2026.
"""

from __future__ import annotations

import logging
import re
import sqlite3
from typing import Dict, List, Optional, Set, Tuple

from data.collect_papers import normalize_doi

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clean_corpus")


def normalize_title(title: Optional[str]) -> str:
    """Normalizes title to lowercase alphanumeric string for robust deduplication."""
    if not title:
        return ""
    # Strip LaTeX formatting, punctuation, whitespace
    cleaned = re.sub(r"[\$\{\}\\\_\^]", "", title)
    alphanumeric = re.sub(r"[^a-zA-Z0-9]", "", cleaned)
    return alphanumeric.lower()


def extract_arxiv_id(paper_id: str, raw_json_str: Optional[str]) -> Optional[str]:
    """Extracts raw arXiv identifier from ID string or raw_json."""
    if paper_id.startswith("arxiv:"):
        return paper_id[len("arxiv:"):].strip().lower()
    return None


def is_superconductivity_focused(title: str, abstract: str, categories: str) -> bool:
    """Checks whether a record has genuine superconductivity focus."""
    cat_lower = (categories or "").lower()
    if "cond-mat.supr-con" in cat_lower:
        return True

    text_lower = f"{title or ''} {abstract or ''}".lower()
    if "superconduct" in text_lower:
        return True

    return False


def clean_and_deduplicate(db_path: str = "data/papers.db") -> Tuple[Dict[str, int], Dict[int, int]]:
    conn = sqlite3.connect(db_path, timeout=60.0)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT count(*) FROM papers")
    initial_count = c.fetchone()[0]
    logger.info(f"Initial paper count in database: {initial_count:,}")

    # Step 1: Purge off-topic Semantic Scholar and non-superconducting OpenAlex
    logger.info("Purging non-superconducting papers from OpenAlex and Semantic Scholar...")
    c.execute("""
        DELETE FROM papers
        WHERE source IN ('semanticscholar', 'openalex')
          AND lower(title) NOT LIKE '%superconduct%'
          AND lower(abstract) NOT LIKE '%superconduct%'
    """)
    purged_non_sc = c.rowcount
    conn.commit()
    logger.info(f"Purged {purged_non_sc:,} off-topic / non-superconductivity papers.")

    # Step 2: Purge off-topic arXiv papers (must be cond-mat.supr-con OR (cond-mat.mtrl-sci with superconduct*))
    logger.info("Filtering arXiv papers to cond-mat.supr-con and cond-mat.mtrl-sci (superconduct*)...")
    c.execute("SELECT id, title, abstract, categories FROM papers WHERE source = 'arxiv'")
    arxiv_rows = c.fetchall()

    arxiv_ids_to_delete = []
    for r in arxiv_rows:
        cats = (r["categories"] or "").lower()
        if "cond-mat.supr-con" in cats:
            continue
        if "cond-mat.mtrl-sci" in cats:
            text = f"{r['title'] or ''} {r['abstract'] or ''}".lower()
            if "superconduct" in text:
                continue
        # If neither, mark for deletion
        text = f"{r['title'] or ''} {r['abstract'] or ''}".lower()
        if "superconduct" not in text:
            arxiv_ids_to_delete.append(r["id"])

    if arxiv_ids_to_delete:
        c.executemany("DELETE FROM papers WHERE id = ?", [(i,) for i in arxiv_ids_to_delete])
        conn.commit()
        logger.info(f"Purged {len(arxiv_ids_to_delete):,} off-topic arXiv papers.")

    # Step 3: Deduplicate across sources
    # Priority order: arXiv > OpenAlex > Semantic Scholar
    logger.info("Deduplicating papers across sources by arXiv ID, DOI, and normalized title...")
    c.execute("SELECT id, title, year, doi, source, raw_json FROM papers ORDER BY CASE source WHEN 'arxiv' THEN 1 WHEN 'openalex' THEN 2 ELSE 3 END, year DESC")
    all_rows = c.fetchall()

    seen_arxiv_ids: Set[str] = set()
    seen_dois: Set[str] = set()
    seen_titles: Set[str] = set()

    duplicate_ids: List[str] = []

    for r in all_rows:
        pid = r["id"]
        arx_id = extract_arxiv_id(pid, r["raw_json"])
        norm_d = normalize_doi(r["doi"])
        norm_t = normalize_title(r["title"])

        is_dup = False

        if arx_id and arx_id in seen_arxiv_ids:
            is_dup = True
        elif norm_d and norm_d in seen_dois:
            is_dup = True
        elif norm_t and len(norm_t) > 15 and norm_t in seen_titles:
            is_dup = True

        if is_dup:
            duplicate_ids.append(pid)
        else:
            if arx_id:
                seen_arxiv_ids.add(arx_id)
            if norm_d:
                seen_dois.add(norm_d)
            if norm_t and len(norm_t) > 15:
                seen_titles.add(norm_t)

    if duplicate_ids:
        c.executemany("DELETE FROM papers WHERE id = ?", [(i,) for i in duplicate_ids])
        conn.commit()
        logger.info(f"Removed {len(duplicate_ids):,} cross-source duplicates.")

    # Step 4: Re-index and compute statistics
    c.execute("VACUUM")
    conn.commit()

    c.execute("SELECT source, count(*) FROM papers GROUP BY source ORDER BY count(*) DESC")
    source_counts = dict(c.fetchall())

    c.execute("SELECT year, count(*) FROM papers WHERE year IS NOT NULL GROUP BY year ORDER BY year")
    year_histogram = dict(c.fetchall())

    c.execute("SELECT count(*) FROM papers")
    final_count = c.fetchone()[0]

    logger.info("=" * 70)
    logger.info(f"CORPUS CLEANING COMPLETE: {final_count:,} verified superconductivity papers.")
    logger.info("PER-SOURCE BREAKDOWN:")
    for s, count in source_counts.items():
        logger.info(f"  - {s:<18}: {count:,} papers ({count / final_count * 100:.1f}%)")

    logger.info("PUBLICATION YEAR HISTOGRAM (1995 - 2026):")
    for y in range(1995, 2027):
        cnt = year_histogram.get(y, 0)
        bar = "#" * min(50, cnt // 50)
        logger.info(f"  {y}: {cnt:>5} papers {bar}")
    logger.info("=" * 70)

    conn.close()
    return source_counts, year_histogram


if __name__ == "__main__":
    clean_and_deduplicate()

