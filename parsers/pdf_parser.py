"""PDF Parser using PyMuPDF4LLM and layout analysis for Markdown, equations, and tables."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pymupdf
import pymupdf4llm

from parsers.models import ParsedDocument
from pipeline.models import PaperRecord

logger = logging.getLogger("pdf_parser")


class PDFParser:
    """Converts scientific PDF papers into clean Markdown preserving equations, tables, and metadata."""

    def __init__(self):
        pass

    def extract_equations_and_tables(self, md_text: str) -> Tuple[List[str], List[str]]:
        """Identify LaTeX math expressions and Markdown tables from extracted document text."""
        equations: List[str] = []
        tables: List[str] = []
        seen_eqs = set()

        # Find display equations: $$ ... $$, \[ ... \], or lines with formulas
        eq_patterns = [
            r"\$\$(.*?)\$\$",
            r"\\\[(.*?)\\\]",
            r"(?:^|\n)\s*([a-zA-Z\d\s\+\-\*\/=><\(\)\{\}\^_\\]{5,}\s*=\s*[a-zA-Z\d\s\+\-\*\/=><\(\)\{\}\^_\\]{5,})(?:\n|$)",
        ]
        for pat in eq_patterns:
            for m in re.finditer(pat, md_text, re.DOTALL):
                eq = m.group(1).strip()
                normalized = re.sub(r"\s+", " ", eq)
                if eq and len(eq) > 3 and normalized not in seen_eqs:
                    equations.append(eq)
                    seen_eqs.add(normalized)

        # Find Markdown tables: lines with | --- |
        table_pattern = r"((?:[ \t]*\|[^\n]+\|\n?)+)"
        for m in re.finditer(table_pattern, md_text):
            tbl = m.group(1).strip()
            if "---" in tbl:
                tables.append(tbl)

        return equations, tables

    def extract_sections(self, md_text: str) -> Dict[str, str]:
        """Extract structured sections based on Markdown headers."""
        sections: Dict[str, str] = {}
        header_pattern = r"(?:^|\n)(#{1,3}\s+[^\n]+)"
        parts = re.split(header_pattern, md_text)
        if len(parts) > 1:
            for i in range(1, len(parts), 2):
                h = parts[i].strip().lstrip("#").strip()
                b = parts[i + 1].strip() if (i + 1) < len(parts) else ""
                sections[h] = b
        return sections

    def parse_pdf_file(
        self,
        pdf_path: str | Path,
        metadata: Optional[PaperRecord | Dict[str, Any]] = None,
    ) -> ParsedDocument:
        """Convert a local PDF file into a ParsedDocument."""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Convert PDF to structured Markdown using pymupdf4llm
        md_text = pymupdf4llm.to_markdown(str(path))

        equations, tables = self.extract_equations_and_tables(md_text)
        sections = self.extract_sections(md_text)

        # Extract or inherit metadata
        paper_id = path.stem
        title = path.stem.replace("_", " ")
        authors: List[str] = []
        year = None
        doi = None
        source = "pdf"
        abstract = ""

        if isinstance(metadata, PaperRecord):
            paper_id = metadata.id
            title = metadata.title or title
            authors = metadata.authors or []
            year = metadata.year
            doi = metadata.doi
            source = metadata.source or source
            abstract = metadata.abstract or ""
        elif isinstance(metadata, dict):
            paper_id = metadata.get("id", paper_id)
            title = metadata.get("title", title)
            authors = metadata.get("authors", [])
            year = metadata.get("year")
            doi = metadata.get("doi")
            source = metadata.get("source", source)
            abstract = metadata.get("abstract", "")

        return ParsedDocument(
            paper_id=paper_id,
            title=title,
            authors=authors,
            year=year,
            doi=doi,
            source=source,
            abstract=abstract,
            parser_used="pymupdf_marker",
            text_markdown=md_text,
            equations=equations,
            tables=tables,
            sections=sections,
        )
