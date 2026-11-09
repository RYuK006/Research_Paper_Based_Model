"""
Vector store for scientific paper chunks with SQLite persistence and cosine similarity search.
Supports dense vector retrieval, metadata filtering, and fast in-memory indexing.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from retrieval.chunker import PaperChunk

logger = logging.getLogger("vector_store")


class VectorStore:
    """
    Persistent vector store using SQLite for chunk metadata and numpy for vectorized search.
    Supports top-k cosine similarity retrieval with section, year, and author filters.
    """

    def __init__(self, db_path: str = "data/vectors/vector_index.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

        self._chunk_ids: List[str] = []
        self._embeddings_matrix: Optional[np.ndarray] = None
        self._load_index_to_memory()

    def _init_db(self) -> None:
        """Initializes database schema for chunks and embeddings."""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                title TEXT,
                authors_json TEXT,
                year INTEGER,
                doi TEXT,
                section TEXT,
                chunk_index INTEGER,
                text TEXT,
                token_count INTEGER,
                embedding_blob BLOB
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_chunks_paper_id ON chunks (paper_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_chunks_year ON chunks (year)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_chunks_section ON chunks (section)")
        conn.commit()
        conn.close()

    def _load_index_to_memory(self) -> None:
        """Loads all vector embeddings from SQLite into contiguous numpy array for rapid search."""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT chunk_id, embedding_blob FROM chunks WHERE embedding_blob IS NOT NULL")
        rows = c.fetchall()
        conn.close()

        if not rows:
            self._chunk_ids = []
            self._embeddings_matrix = None
            return

        chunk_ids = []
        vecs = []
        for cid, blob in rows:
            arr = np.frombuffer(blob, dtype=np.float32)
            chunk_ids.append(cid)
            vecs.append(arr)

        self._chunk_ids = chunk_ids
        matrix = np.vstack(vecs)
        # Normalize for cosine similarity via dot product
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self._embeddings_matrix = matrix / norms

    def add_chunks(
        self,
        chunks: List[PaperChunk],
        embeddings: List[np.ndarray],
    ) -> int:
        """Inserts paper chunks and their dense embeddings into the store."""
        if len(chunks) != len(embeddings):
            raise ValueError(f"Chunks count ({len(chunks)}) != embeddings count ({len(embeddings)})")

        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()

        records = []
        for chunk, emb in zip(chunks, embeddings):
            emb_norm = emb.astype(np.float32)
            blob = emb_norm.tobytes()
            records.append((
                chunk.chunk_id,
                chunk.paper_id,
                chunk.title,
                json.dumps(chunk.authors),
                chunk.year,
                chunk.doi,
                chunk.section,
                chunk.chunk_index,
                chunk.text,
                chunk.token_count,
                blob,
            ))

        c.executemany("""
            INSERT OR REPLACE INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, records)
        conn.commit()
        conn.close()

        self._load_index_to_memory()
        logger.info(f"Added {len(chunks)} chunks to vector store. Total index size: {len(self._chunk_ids)}")
        return len(chunks)

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 30,
        section_filter: Optional[str] = None,
        year_filter: Optional[int] = None,
    ) -> List[Tuple[PaperChunk, float]]:
        """
        Retrieves top_k chunks by cosine similarity to query_vector.
        Returns list of (PaperChunk, similarity_score).
        """
        if self._embeddings_matrix is None or len(self._chunk_ids) == 0:
            return []

        q = query_vector.astype(np.float32).flatten()
        q_norm = np.linalg.norm(q)
        if q_norm > 0:
            q = q / q_norm

        scores = np.dot(self._embeddings_matrix, q)
        top_indices = np.argsort(scores)[::-1][:min(top_k * 2, len(scores))]

        # Fetch chunk records
        matched_chunk_ids = [self._chunk_ids[idx] for idx in top_indices]
        id_to_score = {self._chunk_ids[idx]: float(scores[idx]) for idx in top_indices}

        placeholders = ",".join("?" for _ in matched_chunk_ids)
        query = f"SELECT chunk_id, paper_id, title, authors_json, year, doi, section, chunk_index, text, token_count FROM chunks WHERE chunk_id IN ({placeholders})"
        params: List[Any] = list(matched_chunk_ids)

        if section_filter:
            query += " AND section = ?"
            params.append(section_filter)
        if year_filter:
            query += " AND year = ?"
            params.append(year_filter)

        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()

        results = []
        for row in rows:
            cid, pid, title, auth_json, yr, doi, sec, cidx, text, tokens = row
            chunk = PaperChunk(
                chunk_id=cid,
                paper_id=pid,
                title=title,
                authors=json.loads(auth_json) if auth_json else [],
                year=yr,
                doi=doi,
                section=sec,
                chunk_index=cidx,
                text=text,
                token_count=tokens,
            )
            score = id_to_score.get(cid, 0.0)
            results.append((chunk, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def count(self) -> int:
        """Returns total number of indexed chunks."""
        return len(self._chunk_ids)
