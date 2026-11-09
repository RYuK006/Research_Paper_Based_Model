"""
Section-based document chunker for scientific papers.
Splits papers by section (abstract, methods, results, discussion) into chunks of
roughly 300-800 tokens, maintaining sentence boundaries and rich bibliographic metadata.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

logger = logging.getLogger("chunker")


@dataclass
class PaperChunk:
    """Represents a discrete semantic chunk of a scientific paper."""
    chunk_id: str
    paper_id: str
    title: str
    authors: List[str]
    year: int
    doi: Optional[str]
    section: str
    chunk_index: int
    text: str
    token_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def citation_str(self) -> str:
        """Standard scholarly citation string."""
        first_author = self.authors[0] if self.authors else "Unknown"
        author_short = f"{first_author} et al." if len(self.authors) > 1 else first_author
        doi_suffix = f", DOI: {self.doi}" if self.doi else f", ID: {self.paper_id}"
        return f"[{author_short}, {self.year}{doi_suffix}]"


class SectionChunker:
    """
    Splits scientific documents into semantic chunks respecting section boundaries
    and target token size limits (default 300 to 800 tokens).
    """

    # Common scientific section headers
    SECTION_PATTERN = re.compile(
        r"^(?:#{1,4}\s+)?(?:\d+\.?\s+)?(abstract|introduction|materials\s+and\s+methods|methods|experimental|synthesis|results(?:\s+and\s+discussion)?|discussion|conclusion|future\s+work|acknowledgments|references)\b.*$",
        re.IGNORECASE | re.MULTILINE,
    )

    def __init__(
        self,
        min_tokens: int = 150,
        max_tokens: int = 800,
        target_tokens: int = 500,
        overlap_tokens: int = 50,
    ) -> None:
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens

    def estimate_tokens(self, text: str) -> int:
        """Heuristic token count estimation (~4 characters per token)."""
        return max(1, len(text.split()))

    def split_into_sections(self, content: str) -> List[Dict[str, str]]:
        """Splits full document text into major scientific sections."""
        lines = content.split("\n")
        sections: List[Dict[str, str]] = []
        current_section = "Header/Abstract"
        current_lines: List[str] = []

        for line in lines:
            match = self.SECTION_PATTERN.match(line.strip())
            if match and len(current_lines) > 0:
                sec_text = "\n".join(current_lines).strip()
                if sec_text:
                    sections.append({"section": current_section, "text": sec_text})
                current_section = match.group(1).title()
                current_lines = [line]
            else:
                current_lines.append(line)

        if current_lines:
            sec_text = "\n".join(current_lines).strip()
            if sec_text:
                sections.append({"section": current_section, "text": sec_text})

        return sections if sections else [{"section": "FullText", "text": content.strip()}]

    def split_section_into_chunks(self, text: str) -> List[str]:
        """Splits a section into chunks between min_tokens and max_tokens."""
        # Split on paragraph breaks first
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks: List[str] = []
        current_chunk_paras: List[str] = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = self.estimate_tokens(para)

            # If a single paragraph exceeds max_tokens, split on sentences
            if para_tokens > self.max_tokens:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                for sent in sentences:
                    sent_tokens = self.estimate_tokens(sent)
                    if current_tokens + sent_tokens > self.max_tokens and current_tokens >= self.min_tokens:
                        chunks.append("\n\n".join(current_chunk_paras))
                        current_chunk_paras = [sent]
                        current_tokens = sent_tokens
                    else:
                        current_chunk_paras.append(sent)
                        current_tokens += sent_tokens
            elif current_tokens + para_tokens > self.max_tokens and current_tokens >= self.min_tokens:
                chunks.append("\n\n".join(current_chunk_paras))
                current_chunk_paras = [para]
                current_tokens = para_tokens
            else:
                current_chunk_paras.append(para)
                current_tokens += para_tokens

        if current_chunk_paras:
            final_text = "\n\n".join(current_chunk_paras).strip()
            if final_text:
                chunks.append(final_text)

        return chunks if chunks else [text]

    def chunk_paper(
        self,
        paper_id: str,
        title: str,
        authors: List[str],
        year: int,
        content: str,
        doi: Optional[str] = None,
    ) -> List[PaperChunk]:
        """
        Chunks an entire research paper into section-aware semantic chunks.
        """
        sections = self.split_into_sections(content)
        all_chunks: List[PaperChunk] = []
        chunk_idx = 0

        for sec in sections:
            sec_name = sec["section"]
            sec_text = sec["text"]
            text_chunks = self.split_section_into_chunks(sec_text)

            for t in text_chunks:
                tokens = self.estimate_tokens(t)
                all_chunks.append(
                    PaperChunk(
                        chunk_id=f"{paper_id}_c{chunk_idx:03d}",
                        paper_id=paper_id,
                        title=title,
                        authors=authors,
                        year=year,
                        doi=doi,
                        section=sec_name,
                        chunk_index=chunk_idx,
                        text=t,
                        token_count=tokens,
                    )
                )
                chunk_idx += 1

        return all_chunks
