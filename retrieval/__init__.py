"""
Layer 1: Scientific Literature Retrieval and Verification Engine.
Provides section-based paper chunking, dense embedding, vector retrieval,
cross-encoder reranking, and cite-strictly literature assistant.
"""

from retrieval.chunker import SectionChunker, PaperChunk
from retrieval.vector_store import VectorStore
from retrieval.reranker import CrossEncoderReranker
from retrieval.assistant import LiteratureAssistant

__all__ = [
    "SectionChunker",
    "PaperChunk",
    "VectorStore",
    "CrossEncoderReranker",
    "LiteratureAssistant",
]
