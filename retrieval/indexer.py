"""
High-throughput batch indexer for scientific papers.
Reads papers from data/papers.db or parsed Markdown files, runs section-aware chunking,
computes dense vector embeddings, and stores into VectorStore.
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import List, Optional

import numpy as np
from retrieval.assistant import simple_hash_embedding
from retrieval.chunker import PaperChunk, SectionChunker
from retrieval.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("indexer")


class PaperIndexer:
    """
    Indexes research papers into the VectorStore for fast similarity retrieval.
    """

    def __init__(
        self,
        papers_db_path: str = "data/papers.db",
        vector_db_path: str = "data/vectors/vector_index.db",
        embed_dim: int = 384,
    ) -> None:
        self.papers_db_path = Path(papers_db_path)
        self.vector_store = VectorStore(vector_db_path)
        self.chunker = SectionChunker(min_tokens=100, max_tokens=600, target_tokens=350)
        self.embed_dim = embed_dim
        self._embedder_model = None
        self._init_embedder()

    def _init_embedder(self) -> None:
        """Initializes dense sentence transformer if installed."""
        try:
            from sentence_transformers import SentenceTransformer
            self._embedder_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
            logger.info("Using neural dense embedder: BAAI/bge-small-en-v1.5")
        except Exception:
            logger.info("Using fast hash-based dense embedding fallback.")

    def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Embeds a batch of chunk texts."""
        if self._embedder_model is not None:
            try:
                embeddings = self._embedder_model.encode(texts, normalize_embeddings=True)
                return [np.array(e, dtype=np.float32) for e in embeddings]
            except Exception as e:
                logger.warning(f"Dense embedder failed: {e}. Fallback to fast hash embedding.")

        return [simple_hash_embedding(t, dim=self.embed_dim) for t in texts]

    def index_papers_from_db(
        self,
        limit: int = 500,
        batch_size: int = 50,
    ) -> int:
        """Reads papers from SQLite, chunks them, embeds them, and inserts into VectorStore."""
        if not self.papers_db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.papers_db_path}")

        conn = sqlite3.connect(str(self.papers_db_path))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("""
            SELECT id, title, authors, abstract, year, doi
            FROM papers
            WHERE abstract IS NOT NULL AND length(abstract) > 80
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
        conn.close()

        logger.info(f"Loaded {len(rows)} papers for chunking and vector indexing...")
        start_time = time.time()
        total_chunks_indexed = 0

        current_chunks: List[PaperChunk] = []
        for r in rows:
            authors = []
            if r["authors"]:
                try:
                    authors = json.loads(r["authors"])
                except Exception:
                    authors = [a.strip() for a in r["authors"].split(",") if a.strip()]

            content = f"# Abstract\n{r['abstract']}"
            chunks = self.chunker.chunk_paper(
                paper_id=r["id"],
                title=r["title"] or "Untitled",
                authors=authors,
                year=r["year"] or 2020,
                content=content,
                doi=r["doi"],
            )
            current_chunks.extend(chunks)

            if len(current_chunks) >= batch_size:
                texts = [c.text for c in current_chunks]
                embeddings = self.embed_texts(texts)
                self.vector_store.add_chunks(current_chunks, embeddings)
                total_chunks_indexed += len(current_chunks)
                current_chunks = []

        if current_chunks:
            texts = [c.text for c in current_chunks]
            embeddings = self.embed_texts(texts)
            self.vector_store.add_chunks(current_chunks, embeddings)
            total_chunks_indexed += len(current_chunks)

        elapsed = time.time() - start_time
        logger.info(f"Indexing complete! Indexed {total_chunks_indexed} chunks from {len(rows)} papers in {elapsed:.2f}s.")
        logger.info(f"Vector store now contains {self.vector_store.count()} searchable chunks.")
        return total_chunks_indexed


def main() -> None:
    """CLI runner for paper indexer."""
    parser = argparse.ArgumentParser(description="Scientific Paper Vector Indexer")
    parser.add_argument("--limit", type=int, default=300, help="Number of papers to index")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for embedding")
    parser.add_argument("--papers-db", default="data/papers.db", help="Path to papers database")
    parser.add_argument("--vector-db", default="data/vectors/vector_index.db", help="Path to vector index")

    args = parser.parse_args()
    indexer = PaperIndexer(
        papers_db_path=args.papers_db,
        vector_db_path=args.vector_db,
    )
    indexer.index_papers_from_db(limit=args.limit, batch_size=args.batch_size)


if __name__ == "__main__":
    main()
