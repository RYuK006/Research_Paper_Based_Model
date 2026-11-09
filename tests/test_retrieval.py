"""
Unit tests for Layer 1 retrieval engine (chunker, vector store, reranker, and literature assistant).
"""

import tempfile
import unittest
from pathlib import Path
import numpy as np

from retrieval.chunker import SectionChunker, PaperChunk
from retrieval.vector_store import VectorStore
from retrieval.reranker import CrossEncoderReranker
from retrieval.assistant import LiteratureAssistant, simple_hash_embedding


class TestRetrieval(unittest.TestCase):
    """Test suite for literature retrieval and assistant components."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "test_vectors.db"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_section_chunker(self) -> None:
        """Test section-based splitting and token-bounded chunking."""
        chunker = SectionChunker(min_tokens=20, max_tokens=100, target_tokens=50)

        paper_text = """
# Abstract
Superconductivity in compressed hydrides has emerged as a promising route to room-temperature superconductivity.
We investigate lanthanum decahydride under megabar pressures.

# Methods
Samples were loaded into diamond anvil cells with ammonia borane as a hydrogen source.
Laser heating was applied at 170 GPa to synthesize the fcc phase.

# Results
Four-probe electrical resistivity measurements confirm zero resistance below Tc = 250 K.
Synchrotron X-ray diffraction confirms the clathrate structure with space group Fm-3m.
"""
        chunks = chunker.chunk_paper(
            paper_id="arxiv:1803.0001",
            title="Superconductivity in LaH10",
            authors=["M. Drozdov", "A. Eremets"],
            year=2019,
            content=paper_text,
            doi="10.1038/s41586-019-1201-8",
        )

        self.assertGreaterEqual(len(chunks), 3)
        sections = [c.section for c in chunks]
        self.assertIn("Abstract", sections)
        self.assertIn("Methods", sections)
        self.assertIn("Results", sections)

        # Check citation string format
        cit = chunks[0].citation_str
        self.assertIn("Drozdov et al.", cit)
        self.assertIn("2019", cit)
        self.assertIn("10.1038", cit)

    def test_vector_store_indexing_and_search(self) -> None:
        """Test adding chunks to VectorStore and running cosine similarity search."""
        store = VectorStore(str(self.db_path))

        c1 = PaperChunk(
            chunk_id="c1",
            paper_id="p1",
            title="Hydride Superconductors",
            authors=["Alice"],
            year=2020,
            doi=None,
            section="Abstract",
            chunk_index=0,
            text="High pressure hydrides like H3S and LaH10 exhibit high Tc.",
            token_count=10,
        )
        c2 = PaperChunk(
            chunk_id="c2",
            paper_id="p2",
            title="Cuprate Perovskites",
            authors=["Bob"],
            year=2015,
            doi=None,
            section="Methods",
            chunk_index=0,
            text="YBCO films grown via pulsed laser deposition on STO substrates.",
            token_count=10,
        )

        # Create distinct embeddings
        dim = 128
        emb1 = np.zeros(dim, dtype=np.float32)
        emb1[0:10] = 1.0
        emb2 = np.zeros(dim, dtype=np.float32)
        emb2[20:30] = 1.0

        store.add_chunks([c1, c2], [emb1, emb2])
        self.assertEqual(store.count(), 2)

        # Query matching c1
        q_vec = np.zeros(dim, dtype=np.float32)
        q_vec[0:5] = 1.0

        results = store.search(q_vec, top_k=2)
        self.assertEqual(len(results), 2)
        top_chunk, top_score = results[0]
        self.assertEqual(top_chunk.chunk_id, "c1")
        self.assertGreater(top_score, results[1][1])

    def test_cross_encoder_reranker(self) -> None:
        """Test reranking candidates based on query lexical and semantic match."""
        reranker = CrossEncoderReranker()

        c1 = PaperChunk(
            chunk_id="c1",
            paper_id="p1",
            title="Study on Cuprates",
            authors=["Smith"],
            year=2018,
            doi=None,
            section="Abstract",
            chunk_index=0,
            text="General semiconductor transport properties without mention of pressure.",
            token_count=10,
        )
        c2 = PaperChunk(
            chunk_id="c2",
            paper_id="p2",
            title="Superconducting Hydrides",
            authors=["Johnson"],
            year=2021,
            doi=None,
            section="Results",
            chunk_index=0,
            text="Superconducting transition temperature Tc reaches 250 K at 170 GPa pressure.",
            token_count=12,
        )

        candidates = [(c1, 0.8), (c2, 0.7)]
        reranked = reranker.rerank("superconducting Tc 250 K pressure", candidates, top_n=2)
        self.assertEqual(len(reranked), 2)
        # c2 has exact match for query terms, should be boosted
        self.assertEqual(reranked[0][0].chunk_id, "c2")

    def test_literature_assistant_e2e(self) -> None:
        """Test LiteratureAssistant end-to-end question answering pipeline."""
        assistant = LiteratureAssistant(vector_store_path=str(self.db_path), embed_dim=128)

        chunk = PaperChunk(
            chunk_id="c_lah10",
            paper_id="arxiv:1812.01560",
            title="Observation of Superconductivity at 250 K in LaH10",
            authors=["M. Somayazulu", "R. Hemley"],
            year=2019,
            doi="10.1103/PhysRevLett.122.027001",
            section="Results",
            chunk_index=0,
            text="Electrical resistance measurements of lanthanum hydride under megabar pressures show a sharp drop to zero at 250 K at 170 GPa.",
            token_count=25,
        )
        emb = simple_hash_embedding(chunk.text, dim=128)
        assistant.store.add_chunks([chunk], [emb])

        res = assistant.answer_query("What is the Tc and pressure of lanthanum hydride?")
        self.assertEqual(res["sources_used"], 1)
        self.assertIn("Somayazulu et al.", res["citations"][0]["citation"])
        self.assertIn("250 K", res["prompt"])
        self.assertIn("Strictly", res["prompt"], "Grounding instructions must be present")


if __name__ == "__main__":
    unittest.main()
