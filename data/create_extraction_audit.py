"""Generates 50 random abstracts stratified by year for human extraction auditing.

Outputs: data/extraction_audit.csv

Columns:
- sample_id: Sequential integer 1..50
- paper_id: Database paper ID
- year: Publication year
- title: Paper title
- abstract: Full paper abstract text
- extracted_compounds: Semicolon-separated list of compound formulas detected by extractor
- extracted_elements: Semicolon-separated sorted list of periodic elements detected
- extracted_pairs: Semicolon-separated sorted list of co-occurring element pairs (E1-E2)
- human_verified_compounds: (Blank for human annotator)
- human_verified_elements: (Blank for human annotator)
- human_verified_pairs: (Blank for human annotator)
- extraction_error_type: (Blank for annotator, e.g. False Positive, Missed Compound, Acronym)
- human_notes: (Blank for annotator notes)
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
import random
import sqlite3
from typing import Any, Dict, List

from extraction.formula_extractor import extract_compounds_and_elements

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("create_extraction_audit")

DB_PATH = Path("data/papers.db")
OUTPUT_CSV = Path("data/extraction_audit.csv")


def sample_stratified_abstracts(
    db_path: Path = DB_PATH,
    total_samples: int = 50,
    seed: int = 42
) -> List[Dict[str, Any]]:
    """Selects total_samples papers stratified across available publication years."""
    random.seed(seed)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get years and paper counts
    c.execute("""
        SELECT year, count(*)
        FROM papers
        WHERE abstract IS NOT NULL AND length(abstract) > 50
          AND year BETWEEN 1995 AND 2026
        GROUP BY year
        ORDER BY year ASC
    """)
    year_rows = c.fetchall()
    years = [row["year"] for row in year_rows]
    if not years:
        conn.close()
        return []

    # Allocate samples per year: base 1 sample per year (for 31 years = 31), remainder distributed
    samples_per_year: Dict[int, int] = {y: 1 for y in years}
    remainder = total_samples - len(years)

    # Distribute remaining samples across years with highest paper density
    # Fetch paper density
    c.execute("""
        SELECT year, count(*) as cnt
        FROM papers
        WHERE abstract IS NOT NULL AND length(abstract) > 50
          AND year BETWEEN 1995 AND 2026
        GROUP BY year
        ORDER BY cnt DESC
    """)
    dense_years = [row["year"] for row in c.fetchall()]

    idx = 0
    while remainder > 0:
        y = dense_years[idx % len(dense_years)]
        samples_per_year[y] += 1
        remainder -= 1
        idx += 1

    selected_papers: List[Dict[str, Any]] = []
    for y in sorted(years):
        n = samples_per_year[y]
        c.execute("""
            SELECT id, year, title, abstract
            FROM papers
            WHERE year = ? AND abstract IS NOT NULL AND length(abstract) > 50
            ORDER BY RANDOM()
            LIMIT ?
        """, (y, n))
        for row in c.fetchall():
            selected_papers.append({
                "paper_id": row["id"],
                "year": row["year"],
                "title": row["title"],
                "abstract": row["abstract"]
            })

    conn.close()
    return selected_papers[:total_samples]


def generate_audit_csv(output_csv: Path = OUTPUT_CSV) -> Path:
    papers = sample_stratified_abstracts(total_samples=50, seed=42)
    logger.info(f"Sampled {len(papers)} abstracts stratified across publication years.")

    fieldnames = [
        "sample_id",
        "paper_id",
        "year",
        "title",
        "abstract",
        "extracted_compounds",
        "extracted_elements",
        "extracted_pairs",
        "human_verified_compounds",
        "human_verified_elements",
        "human_verified_pairs",
        "extraction_error_type",
        "human_notes"
    ]

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, paper in enumerate(papers, start=1):
            text = f"{paper['title'] or ''} {paper['abstract'] or ''}"
            compounds_info = extract_compounds_and_elements(text)

            compounds_list = [c["formula"] for c in compounds_info]
            elements_set = set()
            pairs_set = set()

            for c in compounds_info:
                c_elems = sorted(list(c["elements"]))
                elements_set.update(c_elems)
                for j in range(len(c_elems)):
                    for k in range(j + 1, len(c_elems)):
                        pairs_set.add(f"{c_elems[j]}-{c_elems[k]}")

            writer.writerow({
                "sample_id": i,
                "paper_id": paper["paper_id"],
                "year": paper["year"],
                "title": paper["title"],
                "abstract": paper["abstract"],
                "extracted_compounds": "; ".join(compounds_list),
                "extracted_elements": "; ".join(sorted(elements_set)),
                "extracted_pairs": "; ".join(sorted(pairs_set)),
                "human_verified_compounds": "",
                "human_verified_elements": "",
                "human_verified_pairs": "",
                "extraction_error_type": "",
                "human_notes": ""
            })

    logger.info(f"Successfully generated extraction audit sheet: {output_csv}")
    return output_csv


if __name__ == "__main__":
    generate_audit_csv()
