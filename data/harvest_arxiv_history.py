"""Harvests historical arXiv papers for cond-mat.supr-con (1995-2021) to ensure continuous year coverage."""

import logging
import sqlite3
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

import httpx

from data.collect_papers import PaperDatabase, PaperItem, normalize_doi

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("arxiv_history")

ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def parse_atom_entries(xml_text: str) -> List[PaperItem]:
    items: List[PaperItem] = []
    try:
        root = ET.fromstring(xml_text)
    except Exception as e:
        logger.error(f"Failed to parse XML: {e}")
        return items

    for entry in root.findall("atom:entry", ATOM_NS):
        id_elem = entry.find("atom:id", ATOM_NS)
        if id_elem is None or not id_elem.text:
            continue

        raw_url = id_elem.text.strip()
        arxiv_id = raw_url.split("/abs/")[-1]
        paper_id = f"arxiv:{arxiv_id}"

        title_elem = entry.find("atom:title", ATOM_NS)
        title = " ".join(title_elem.text.split()) if (title_elem is not None and title_elem.text) else "Untitled"

        summary_elem = entry.find("atom:summary", ATOM_NS)
        abstract = " ".join(summary_elem.text.split()) if (summary_elem is not None and summary_elem.text) else ""

        published_elem = entry.find("atom:published", ATOM_NS)
        year: Optional[int] = None
        if published_elem is not None and published_elem.text:
            try:
                dt = datetime.fromisoformat(published_elem.text.strip().replace("Z", "+00:00"))
                year = dt.year
            except Exception:
                pass

        doi_elem = entry.find("arxiv:doi", ATOM_NS)
        doi = normalize_doi(doi_elem.text.strip()) if (doi_elem is not None and doi_elem.text) else None

        authors: List[str] = []
        for author in entry.findall("atom:author", ATOM_NS):
            name_elem = author.find("atom:name", ATOM_NS)
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text.strip())

        categories: List[str] = []
        primary_cat = entry.find("arxiv:primary_category", ATOM_NS)
        if primary_cat is not None and primary_cat.get("term"):
            categories.append(primary_cat.get("term", ""))
        for cat in entry.findall("atom:category", ATOM_NS):
            term = cat.get("term")
            if term and term not in categories:
                categories.append(term)

        pdf_url: Optional[str] = None
        for link in entry.findall("atom:link", ATOM_NS):
            if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                pdf_url = link.get("href")
                break

        items.append(PaperItem(
            id=paper_id,
            title=title,
            abstract=abstract,
            authors=authors,
            year=year,
            doi=doi,
            source="arxiv",
            categories=categories,
            open_access_pdf_url=pdf_url,
            download_status="metadata_only",
            raw_json={"arxiv_id": arxiv_id, "categories": categories}
        ))

    return items


def harvest_historical_years(db_path: str = "data/papers.db", max_per_year: int = 500) -> None:
    db = PaperDatabase(db_path)
    existing_ids, existing_dois = db.load_existing_identifiers()
    logger.info(f"Existing DB has {len(existing_ids):,} IDs and {len(existing_dois):,} DOIs.")

    client = httpx.Client(headers={"User-Agent": "ResearchCollector/1.0 (mailto:RYuK006@users.noreply.github.com)"}, timeout=45.0)

    # Years to fill
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT year, count(*) FROM papers WHERE source = 'arxiv' GROUP BY year")
    existing_counts = dict(c.fetchall())

    years_to_harvest = [y for y in range(1995, 2022) if existing_counts.get(y, 0) < 100]
    logger.info(f"Targeting {len(years_to_harvest)} years with < 100 papers: {years_to_harvest}")

    total_added = 0
    for y in years_to_harvest:
        start_date = f"{y}01010000"
        end_date = f"{y}12312359"
        query_url = (
            f"https://export.arxiv.org/api/query?"
            f"search_query=cat:cond-mat.supr-con+AND+submittedDate:[{start_date}+TO+{end_date}]"
            f"&start=0&max_results={max_per_year}"
        )
        logger.info(f"Harvesting year {y} from arXiv...")
        try:
            r = client.get(query_url)
            if r.status_code == 429:
                logger.warning("Rate limit 429 received. Backing off 10s...")
                time.sleep(10.0)
                r = client.get(query_url)
            if r.status_code != 200:
                logger.error(f"HTTP {r.status_code} for year {y}")
                time.sleep(3.0)
                continue

            items = parse_atom_entries(r.text)
            new_items = []
            for item in items:
                # Ensure year is set correctly if parsed as None
                if item.year is None:
                    item.year = y
                if item.id not in existing_ids and (not item.doi or item.doi not in existing_dois):
                    new_items.append(item)
                    existing_ids.add(item.id)
                    if item.doi:
                        existing_dois.add(item.doi)

            if new_items:
                inserted = db.insert_batch(new_items)
                total_added += inserted
                logger.info(f"Year {y}: inserted {inserted} papers (Total added: {total_added}).")
            else:
                logger.info(f"Year {y}: 0 new papers found.")

            # Polite pause for arXiv API guidelines
            time.sleep(3.0)

        except Exception as e:
            logger.error(f"Error harvesting year {y}: {e}")
            time.sleep(3.0)

    logger.info(f"Completed historical harvest! Total added: {total_added} papers.")


if __name__ == "__main__":
    harvest_historical_years()
