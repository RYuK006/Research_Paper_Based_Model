"""Storage engine for SQLite indexing and JSONL manifests."""

from __future__ import annotations

import json
import os
import sqlite3
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pipeline.models import PaperRecord


class StorageManager:
    """Manages persistent paper records in SQLite and JSONL manifests."""

    def __init__(self, base_dir: Optional[str | Path] = None):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent / "data"
        else:
            self.base_dir = Path(base_dir)

        self.papers_dir = self.base_dir / "papers"
        self.arxiv_dir = self.papers_dir / "arxiv"
        self.openalex_dir = self.papers_dir / "openalex"
        self.s2_dir = self.papers_dir / "semanticscholar"
        self.manifest_dir = self.base_dir / "manifests"

        self.db_path = self.base_dir / "papers.db"
        self.manifest_path = self.manifest_dir / "papers_manifest.jsonl"

        self._lock = threading.Lock()
        self._ensure_directories()
        self._init_db()

    def _ensure_directories(self) -> None:
        """Create storage directories if they do not exist."""
        for path in [
            self.base_dir,
            self.papers_dir,
            self.arxiv_dir,
            self.openalex_dir,
            self.s2_dir,
            self.manifest_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get a thread-safe connection to the SQLite database."""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Initialize database schema with indexes."""
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
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
                        download_status TEXT DEFAULT 'pending',
                        collected_at TEXT NOT NULL,
                        raw_json TEXT
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS checkpoints (
                        source TEXT PRIMARY KEY,
                        last_cursor TEXT,
                        collected_count INTEGER DEFAULT 0,
                        updated_at TEXT NOT NULL
                    )
                    """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_papers_source ON papers(source)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(download_status)"
                )
                conn.commit()

    def paper_exists(self, paper_id: str) -> bool:
        """Check if a paper ID already exists in storage."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM papers WHERE id = ? LIMIT 1", (paper_id,))
            return cursor.fetchone() is not None

    def upsert_paper(self, record: PaperRecord) -> None:
        """Insert or update a single paper record."""
        self.upsert_papers_batch([record])

    def upsert_papers_batch(self, records: List[PaperRecord]) -> int:
        """Batch insert or update paper records in SQLite and append to manifest."""
        if not records:
            return 0

        rows = []
        for r in records:
            rows.append(
                (
                    r.id,
                    r.title,
                    r.abstract,
                    json.dumps(r.authors, ensure_ascii=False),
                    r.year,
                    r.doi,
                    r.source,
                    json.dumps(r.categories, ensure_ascii=False),
                    r.citation_count,
                    r.open_access_pdf_url,
                    r.local_file_path,
                    r.download_status,
                    r.collected_at,
                    json.dumps(r.raw_metadata, ensure_ascii=False),
                )
            )

        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(
                    """
                    INSERT INTO papers (
                        id, title, abstract, authors, year, doi, source,
                        categories, citation_count, open_access_pdf_url,
                        local_file_path, download_status, collected_at, raw_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        title = excluded.title,
                        abstract = excluded.abstract,
                        authors = excluded.authors,
                        year = excluded.year,
                        doi = excluded.doi,
                        source = excluded.source,
                        categories = excluded.categories,
                        citation_count = excluded.citation_count,
                        open_access_pdf_url = excluded.open_access_pdf_url,
                        local_file_path = excluded.local_file_path,
                        download_status = excluded.download_status,
                        collected_at = excluded.collected_at,
                        raw_json = excluded.raw_json
                    """,
                    rows,
                )
                conn.commit()

            # Append to JSONL manifest
            with open(self.manifest_path, "a", encoding="utf-8") as f:
                for r in records:
                    f.write(r.to_json() + "\n")

        return len(records)

    def get_counts_by_source(self) -> Dict[str, int]:
        """Get count of collected papers grouped by source."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT source, COUNT(*) FROM papers GROUP BY source")
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_total_count(self) -> int:
        """Get total count of collected papers."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM papers")
            row = cursor.fetchone()
            return row[0] if row else 0

    def save_checkpoint(self, source: str, cursor_val: str, count: int) -> None:
        """Save pipeline checkpoint for resume support."""
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO checkpoints (source, last_cursor, collected_count, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(source) DO UPDATE SET
                        last_cursor = excluded.last_cursor,
                        collected_count = excluded.collected_count,
                        updated_at = excluded.updated_at
                    """,
                    (source, cursor_val, count, now),
                )
                conn.commit()

    def get_checkpoint(self, source: str) -> Tuple[Optional[str], int]:
        """Retrieve last saved cursor and count for a source."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT last_cursor, collected_count FROM checkpoints WHERE source = ?",
                (source,),
            )
            row = cursor.fetchone()
            if row:
                return row[0], row[1]
            return None, 0
