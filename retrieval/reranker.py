"""
Cross-Encoder Reranker for scientific literature retrieval.
Re-scores candidate chunks retrieved from vector search using cross-attention relevance.
"""

from __future__ import annotations

import logging
import math
import re
from typing import List, Tuple

from retrieval.chunker import PaperChunk

logger = logging.getLogger("reranker")


class CrossEncoderReranker:
    """
    Reranks top candidate chunks using cross-encoder relevance scoring.
    Supports neural cross-encoders (e.g., cross-encoder/ms-marco-MiniLM-L-6-v2)
    with robust semantic-lexical fallback for CPU/fast environments.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        self.model_name = model_name
        self._model = None
        self._init_model()

    def _init_model(self) -> None:
        """Attempts to load sentence_transformers CrossEncoder if available."""
        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name)
            logger.info(f"Loaded neural CrossEncoder: {self.model_name}")
        except Exception:
            logger.debug("Operating with semantic-lexical hybrid reranker.")

    def _lexical_relevance_score(self, query: str, text: str) -> float:
        """Calculates BM25-style lexical matching score with term proximity bonuses."""
        query_terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
        if not query_terms:
            return 0.0

        text_lower = text.lower()
        score = 0.0

        for term in query_terms:
            count = text_lower.count(term)
            if count > 0:
                tf = count / (count + 1.2)
                score += tf

        # Phrase bonus
        if query.lower() in text_lower:
            score += 2.0

        return score

    def rerank(
        self,
        query: str,
        candidates: List[Tuple[PaperChunk, float]],
        top_n: int = 5,
    ) -> List[Tuple[PaperChunk, float]]:
        """
        Reranks a list of (PaperChunk, initial_vector_score) tuples and returns the top_n.
        """
        if not candidates:
            return []

        if self._model is not None:
            try:
                pairs = [[query, chunk.text] for chunk, _ in candidates]
                scores = self._model.predict(pairs)
                reranked = [
                    (chunk, float(score))
                    for (chunk, _), score in zip(candidates, scores)
                ]
                reranked.sort(key=lambda x: x[1], reverse=True)
                return reranked[:top_n]
            except Exception as e:
                logger.warning(f"Neural reranker prediction failed: {e}. Fallback to hybrid scoring.")

        # Hybrid re-scoring: combines normalized vector score with lexical precision
        reranked = []
        for chunk, vec_score in candidates:
            lex_score = self._lexical_relevance_score(query, chunk.text)
            combined_score = (vec_score * 0.6) + (min(lex_score, 3.0) * 0.4)
            reranked.append((chunk, float(combined_score)))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_n]
