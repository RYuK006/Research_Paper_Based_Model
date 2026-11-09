"""
Resumable Data Collector for Superconductivity and Materials Research Papers.
Collects up to 50,000 papers from open sources (arXiv and OpenAlex) into papers.db.

Features:
1. Open-access sources only (arXiv API, OpenAlex polite pool).
2. Strict politeness: polite User-Agent with contact email, rate-limit pauses (3.0s for arXiv, 0.25s for OpenAlex).
3. Resumable checkpointing: saves exact cursor, category, and offset to JSON and SQLite.
4. Robust deduplication by paper ID and normalized DOI.
5. Preserves publication year, authors, abstract, categories, open-access status, and license.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import signal
import sqlite3
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("collect_papers")

ARXIV_API_URL = "https://export.arxiv.org/api/query"
OPENALEX_API_URL = "https://api.openalex.org/works"

ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    """Normalize DOI string by stripping URL prefixes and lowercase conversion."""
    if not doi:
        return None
    d = doi.strip().lower()
    for prefix in ["https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/", "doi:"]:
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d.strip().strip("/")


def reconstruct_openalex_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Reconstruct plain abstract text from OpenAlex inverted index mapping."""
    if not inverted_index:
        return ""
    try:
        word_positions: List[Tuple[int, str]] = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(w for _, w in word_positions)
    except Exception:
        return ""


@dataclass
class PaperItem:
    id: str
    title: str
    abstract: str
    authors: List[str]
    year: Optional[int]
    doi: Optional[str]
    source: str
    categories: List[str]
    open_access_pdf_url: Optional[str] = None
    license: Optional[str] = None
    download_status: str = "metadata_only"
    raw_json: Dict[str, Any] = field(default_factory=dict)


class PaperDatabase:
    """Interface to SQLite papers.db schema."""

    def __init__(self, db_path: str = "data/papers.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        conn = self.get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    abstract TEXT,
                    authors TEXT,
                    year INTEGER,
                    doi TEXT,
                    source TEXT NOT NULL,
                    categories TEXT,
                    citation_count INTEGER DEFAULT 0,
                    open_access_pdf_url TEXT,
                    local_file_path TEXT,
                    download_status TEXT DEFAULT 'metadata_only',
                    collected_at TEXT NOT NULL,
                    raw_json TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    source TEXT PRIMARY KEY,
                    last_cursor TEXT,
                    collected_count INTEGER DEFAULT 0,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_papers_source ON papers(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi)")
            conn.commit()
        finally:
            conn.close()

    def load_existing_identifiers(self) -> Tuple[Set[str], Set[str]]:
        """Returns existing (ids, normalized_dois)."""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, doi FROM papers")
            rows = cur.fetchall()
            ids = {r["id"] for r in rows if r["id"]}
            dois = {normalize_doi(r["doi"]) for r in rows if r["doi"]}
            dois.discard(None)
            return ids, dois
        finally:
            conn.close()

    def insert_batch(self, items: List[PaperItem]) -> int:
        """Batch insert papers into database."""
        if not items:
            return 0
        now_iso = datetime.now(timezone.utc).isoformat()
        records = []
        for p in items:
            records.append((
                p.id,
                p.title,
                p.abstract,
                json.dumps(p.authors, ensure_ascii=False),
                p.year,
                p.doi,
                p.source,
                json.dumps(p.categories, ensure_ascii=False),
                p.raw_json.get("citation_count", 0),
                p.open_access_pdf_url,
                p.raw_json.get("local_file_path"),
                p.download_status,
                now_iso,
                json.dumps(p.raw_json, ensure_ascii=False),
            ))
        conn = self.get_connection()
        try:
            conn.executemany("""
                INSERT OR REPLACE INTO papers (
                    id, title, abstract, authors, year, doi, source, categories,
                    citation_count, open_access_pdf_url, local_file_path,
                    download_status, collected_at, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, records)
            conn.commit()
        finally:
            conn.close()
        return len(records)

    def get_total_count(self) -> int:
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM papers")
            return cur.fetchone()[0]
        finally:
            conn.close()


class ResumablePaperCollector:
    """Orchestrates collection across arXiv and OpenAlex with resumability."""

    def __init__(
        self,
        db_path: str = "data/papers.db",
        checkpoint_path: str = "data/collection_checkpoint.json",
        email: str = "RYuK006@users.noreply.github.com",
        user_agent: Optional[str] = None,
        arxiv_rate_limit: float = 3.0,
        openalex_rate_limit: float = 0.3,
        http_client: Optional[httpx.Client] = None,
    ):
        self.db = PaperDatabase(db_path)
        self.checkpoint_path = Path(checkpoint_path)
        self.email = email
        self.user_agent = user_agent or f"ModelSuperconductor/1.0 (mailto:{self.email})"
        self.arxiv_rate_limit = arxiv_rate_limit
        self.openalex_rate_limit = openalex_rate_limit
        self.client = http_client or httpx.Client(
            headers={"User-Agent": self.user_agent},
            timeout=30.0,
            follow_redirects=True,
        )

        self.existing_ids, self.existing_dois = self.db.load_existing_identifiers()
        logger.info(f"Loaded existing database: {len(self.existing_ids):,} IDs, {len(self.existing_dois):,} DOIs.")

        self.interrupted = False
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum: Any, frame: Any) -> None:
        logger.warning("Interrupt signal received. Gracefully saving checkpoint and exiting...")
        self.interrupted = True

    def load_checkpoint(self) -> Dict[str, Any]:
        """Loads state checkpoint from disk or initializes fresh structure."""
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.info(f"Loaded existing checkpoint from {self.checkpoint_path}")
                    return data
            except Exception as e:
                logger.warning(f"Error loading checkpoint {self.checkpoint_path}: {e}. Initializing fresh.")

        return {
            "arxiv": {
                "categories": ["cond-mat.supr-con", "cond-mat.mtrl-sci", "physics.chem-ph"],
                "current_category_idx": 0,
                "start_index": 0,
                "completed": False,
            },
            "openalex": {
                "cursor": "*",
                "completed": False,
            },
            "total_collected_in_session": 0,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    def close(self) -> None:
        """Close resources and connections."""
        try:
            self.client.close()
        except Exception:
            pass

    def save_checkpoint(self, state: Dict[str, Any]) -> None:
        """Atomically saves checkpoint to disk."""
        state["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_file = self.checkpoint_path.with_suffix(".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        tmp_file.replace(self.checkpoint_path)
        logger.debug(f"Saved checkpoint to {self.checkpoint_path}")

    # ==========================================
    # arXiv Harvester
    # ==========================================
    def parse_arxiv_atom(self, xml_text: str) -> List[PaperItem]:
        """Parses arXiv API Atom XML feed into PaperItem models."""
        items: List[PaperItem] = []
        try:
            root = ET.fromstring(xml_text)
        except Exception as e:
            logger.error(f"XML parse error: {e}")
            return items

        for entry in root.findall("atom:entry", ATOM_NS):
            id_elem = entry.find("atom:id", ATOM_NS)
            if id_elem is None or not id_elem.text:
                continue

            raw_url = id_elem.text.strip()
            # Extract clean arXiv ID, e.g., '2305.12345'
            arxiv_id = raw_url.split("/abs/")[-1].split("v")[0]
            canonical_id = f"arxiv:{arxiv_id}"

            title_elem = entry.find("atom:title", ATOM_NS)
            title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else ""

            summary_elem = entry.find("atom:summary", ATOM_NS)
            abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""

            pub_elem = entry.find("atom:published", ATOM_NS)
            year = None
            if pub_elem is not None and pub_elem.text:
                try:
                    year = int(pub_elem.text[:4])
                except ValueError:
                    pass

            authors = []
            for a in entry.findall("atom:author", ATOM_NS):
                name_el = a.find("atom:name", ATOM_NS)
                if name_el is not None and name_el.text:
                    authors.append(name_el.text.strip())

            doi_elem = entry.find("arxiv:doi", ATOM_NS)
            doi = normalize_doi(doi_elem.text) if doi_elem is not None and doi_elem.text else None

            categories = []
            for c in entry.findall("atom:category", ATOM_NS):
                term = c.get("term")
                if term:
                    categories.append(term)

            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            license_elem = entry.find("arxiv:license", ATOM_NS)
            license_url = license_elem.text.strip() if license_elem is not None and license_elem.text else None

            items.append(PaperItem(
                id=canonical_id,
                title=title,
                abstract=abstract,
                authors=authors,
                year=year,
                doi=doi,
                source="arxiv",
                categories=categories,
                open_access_pdf_url=pdf_url,
                license=license_url,
                download_status="metadata_only",
                raw_json={
                    "arxiv_id": arxiv_id,
                    "published": pub_elem.text if pub_elem is not None else None,
                    "license": license_url,
                    "categories": categories,
                }
            ))

        return items

    def harvest_arxiv(
        self,
        target_count: int,
        checkpoint: Dict[str, Any],
        max_batch_size: int = 100,
    ) -> int:
        """Harvest papers from arXiv with category iteration and resumability."""
        arxiv_state = checkpoint.get("arxiv", {})
        categories = arxiv_state.get("categories", ["cond-mat.supr-con", "cond-mat.mtrl-sci", "physics.chem-ph"])
        cat_idx = arxiv_state.get("current_category_idx", 0)
        start_idx = arxiv_state.get("start_index", 0)

        collected = 0

        while cat_idx < len(categories) and not self.interrupted:
            current_cat = categories[cat_idx]
            logger.info(f"[arXiv] Querying category '{current_cat}' starting at index {start_idx}...")

            query_url = (
                f"{ARXIV_API_URL}?search_query=cat:{current_cat}"
                f"&start={start_idx}&max_results={max_batch_size}"
                f"&sortBy=submittedDate&sortOrder=descending"
            )

            try:
                r = self.client.get(query_url)
                if r.status_code == 429:
                    logger.warning("[arXiv] Rate limited (429). Sleeping 10s...")
                    time.sleep(10.0)
                    continue
                elif r.status_code != 200:
                    logger.warning(f"[arXiv] HTTP {r.status_code}. Sleeping 5s...")
                    time.sleep(5.0)
                    continue

                records = self.parse_arxiv_atom(r.text)
                if not records:
                    logger.info(f"[arXiv] No more records in category '{current_cat}'. Moving to next.")
                    cat_idx += 1
                    start_idx = 0
                    arxiv_state["current_category_idx"] = cat_idx
                    arxiv_state["start_index"] = start_idx
                    self.save_checkpoint(checkpoint)
                    continue

                # Deduplicate
                unique_records = []
                for rec in records:
                    if rec.id in self.existing_ids:
                        continue
                    if rec.doi and rec.doi in self.existing_dois:
                        continue
                    unique_records.append(rec)
                    self.existing_ids.add(rec.id)
                    if rec.doi:
                        self.existing_dois.add(rec.doi)

                if unique_records:
                    inserted = self.db.insert_batch(unique_records)
                    collected += inserted
                    checkpoint["total_collected_in_session"] = checkpoint.get("total_collected_in_session", 0) + inserted
                    logger.info(f"[arXiv] Saved {inserted} new papers from '{current_cat}' (Total in DB: {self.db.get_total_count():,}).")

                start_idx += len(records)
                arxiv_state["start_index"] = start_idx
                self.save_checkpoint(checkpoint)

                if collected >= target_count:
                    logger.info(f"[arXiv] Target count of {target_count} reached for this run.")
                    break

                time.sleep(self.arxiv_rate_limit)

            except Exception as e:
                logger.error(f"[arXiv] Fetch error: {e}")
                time.sleep(5.0)

        if cat_idx >= len(categories):
            arxiv_state["completed"] = True
            self.save_checkpoint(checkpoint)
            logger.info("[arXiv] Completed all target categories.")

        return collected

    # ==========================================
    # OpenAlex Harvester
    # ==========================================
    def parse_openalex_item(self, item: Dict[str, Any]) -> Optional[PaperItem]:
        """Parses OpenAlex work JSON into PaperItem."""
        raw_id = item.get("id", "").split("/")[-1]
        title = item.get("title")
        if not raw_id or not title:
            return None

        paper_id = f"openalex:{raw_id}"
        abstract = reconstruct_openalex_abstract(item.get("abstract_inverted_index"))
        year = item.get("publication_year")

        doi = normalize_doi(item.get("doi"))

        authors = []
        for a in item.get("authorships", []):
            name = a.get("author", {}).get("display_name")
            if name:
                authors.append(name)

        categories = []
        for c in item.get("concepts", []):
            c_name = c.get("display_name")
            if c_name:
                categories.append(c_name)

        oa = item.get("open_access", {})
        oa_url = oa.get("oa_url")
        if not oa_url:
            oa_url = (item.get("primary_location") or {}).get("pdf_url")

        license_name = (item.get("primary_location") or {}).get("license")

        return PaperItem(
            id=paper_id,
            title=title.strip().replace("\n", " "),
            abstract=abstract.strip().replace("\n", " "),
            authors=authors,
            year=year,
            doi=doi,
            source="openalex",
            categories=categories,
            open_access_pdf_url=oa_url,
            license=license_name,
            download_status="metadata_only",
            raw_json={
                "openalex_id": raw_id,
                "oa_status": oa.get("oa_status"),
                "license": license_name,
                "citation_count": item.get("cited_by_count", 0),
            }
        )

    def harvest_openalex(
        self,
        target_count: int,
        checkpoint: Dict[str, Any],
        per_page: int = 50,
    ) -> int:
        """Harvest papers from OpenAlex with cursor paging and polite pool."""
        oa_state = checkpoint.get("openalex", {})
        cursor = oa_state.get("cursor", "*")
        collected = 0

        # Query for superconductivity and materials chemistry
        query = "superconductivity OR 'condensed matter' OR 'materials chemistry'"

        while cursor and not self.interrupted:
            logger.info(f"[OpenAlex] Fetching works with cursor: {cursor[:15]}...")

            params = {
                "search": query,
                "per-page": per_page,
                "cursor": cursor,
                "mailto": self.email,
            }

            try:
                r = self.client.get(OPENALEX_API_URL, params=params)
                if r.status_code == 429:
                    logger.warning("[OpenAlex] Rate limit (429) hit. Pausing for 5 seconds...")
                    time.sleep(5.0)
                    continue
                elif r.status_code != 200:
                    logger.warning(f"[OpenAlex] HTTP {r.status_code}. Pausing 3s...")
                    time.sleep(3.0)
                    continue

                data = r.json()
                results = data.get("results", [])
                next_cursor = data.get("meta", {}).get("next_cursor")

                if not results or not next_cursor or next_cursor == cursor:
                    logger.info("[OpenAlex] Reached end of cursor pagination.")
                    oa_state["completed"] = True
                    break

                records = [self.parse_openalex_item(item) for item in results]
                records = [rec for rec in records if rec is not None]

                unique_records = []
                for rec in records:
                    if rec.id in self.existing_ids:
                        continue
                    if rec.doi and rec.doi in self.existing_dois:
                        continue
                    unique_records.append(rec)
                    self.existing_ids.add(rec.id)
                    if rec.doi:
                        self.existing_dois.add(rec.doi)

                if unique_records:
                    inserted = self.db.insert_batch(unique_records)
                    collected += inserted
                    checkpoint["total_collected_in_session"] = checkpoint.get("total_collected_in_session", 0) + inserted
                    logger.info(f"[OpenAlex] Saved {inserted} new papers (Total in DB: {self.db.get_total_count():,}).")

                cursor = next_cursor
                oa_state["cursor"] = cursor
                self.save_checkpoint(checkpoint)

                if collected >= target_count:
                    logger.info(f"[OpenAlex] Target count of {target_count} reached for this run.")
                    break

                time.sleep(self.openalex_rate_limit)

            except Exception as e:
                logger.error(f"[OpenAlex] Request error: {e}")
                time.sleep(5.0)

        return collected

    def collect(
        self,
        target_papers: int = 50000,
        sources: Optional[List[str]] = None,
        run_limit: Optional[int] = None,
    ) -> int:
        """Main execution orchestrator."""
        sources = sources or ["arxiv", "openalex"]
        checkpoint = self.load_checkpoint()
        total_in_db = self.db.get_total_count()

        logger.info("=" * 70)
        logger.info(f"RESUMABLE RESEARCH PAPER HARVESTER")
        logger.info(f"Current DB Count: {total_in_db:,} papers | Global Target: {target_papers:,}")
        if run_limit:
            logger.info(f"Run Limit Cap: {run_limit} papers")
        logger.info(f"Sources Enabled: {', '.join(sources)}")
        logger.info(f"Checkpoint File: {self.checkpoint_path}")
        logger.info("=" * 70)

        remaining_global = max(0, target_papers - total_in_db)
        if remaining_global == 0:
            logger.info("Database has already reached or exceeded target count.")
            return 0

        target_this_session = min(remaining_global, run_limit) if run_limit else remaining_global
        total_collected = 0

        for src in sources:
            if self.interrupted or total_collected >= target_this_session:
                break
            quota = target_this_session - total_collected

            if src.lower() == "arxiv":
                collected = self.harvest_arxiv(target_count=quota, checkpoint=checkpoint)
                total_collected += collected
            elif src.lower() == "openalex":
                collected = self.harvest_openalex(target_count=quota, checkpoint=checkpoint)
                total_collected += collected

        final_count = self.db.get_total_count()
        logger.info("=" * 70)
        logger.info(f"HARVEST SESSION COMPLETE: Collected {total_collected} new papers.")
        logger.info(f"Final Total Papers in papers.db: {final_count:,}")
        logger.info("=" * 70)
        return total_collected


def main() -> None:
    parser = argparse.ArgumentParser(description="Resumable Superconductor Paper Harvester")
    parser.add_argument("--db-path", default="data/papers.db", help="Path to SQLite database")
    parser.add_argument("--checkpoint", default="data/collection_checkpoint.json", help="Path to checkpoint file")
    parser.add_argument("--target", type=int, default=50000, help="Global paper target count")
    parser.add_argument("--limit", type=int, default=None, help="Max papers to collect in this run")
    parser.add_argument("--sources", nargs="+", default=["arxiv", "openalex"], help="Sources to query")
    parser.add_argument("--email", default="RYuK006@users.noreply.github.com", help="Polite pool contact email")
    args = parser.parse_args()

    collector = ResumablePaperCollector(
        db_path=args.db_path,
        checkpoint_path=args.checkpoint,
        email=args.email,
    )
    collector.collect(
        target_papers=args.target,
        sources=args.sources,
        run_limit=args.limit,
    )


if __name__ == "__main__":
    main()
