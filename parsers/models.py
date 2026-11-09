"""Data models for parsed document representations."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ParsedDocument:
    """Representation of a parsed research paper with preserved metadata, equations, and tables."""

    paper_id: str
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    doi: Optional[str] = None
    source: str = ""  # 'arxiv', 'openalex', 'semanticscholar'
    abstract: str = ""
    parser_used: str = ""  # 'arxiv_latex', 'grobid', 'pymupdf_marker'
    text_markdown: str = ""
    equations: List[str] = field(default_factory=list)
    tables: List[str] = field(default_factory=list)
    sections: Dict[str, str] = field(default_factory=dict)
    parsed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_markdown_with_frontmatter(self) -> str:
        """Serialize document with YAML frontmatter containing all metadata."""
        authors_yaml = "\n".join(f"  - {a}" for a in self.authors) if self.authors else "  []"
        doi_val = f'"{self.doi}"' if self.doi else "null"
        year_val = str(self.year) if self.year else "null"

        lines = [
            "---",
            f"paper_id: \"{self.paper_id}\"",
            f"title: \"{self.title}\"",
            "authors:",
            authors_yaml,
            f"year: {year_val}",
            f"doi: {doi_val}",
            f"source: \"{self.source}\"",
            f"parser_used: \"{self.parser_used}\"",
            f"parsed_at: \"{self.parsed_at}\"",
            f"equation_count: {len(self.equations)}",
            f"table_count: {len(self.tables)}",
            "---",
            "",
            f"# {self.title}",
            "",
        ]

        if self.abstract:
            lines.extend([
                "## Abstract",
                "",
                self.abstract,
                "",
            ])

        lines.extend([
            "## Document Content",
            "",
            self.text_markdown,
            "",
        ])

        return "\n".join(lines)

    def save_markdown(self, dest_path: str | Path) -> Path:
        """Write serialized document to disk."""
        target = Path(dest_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.to_markdown_with_frontmatter(), encoding="utf-8")
        return target
