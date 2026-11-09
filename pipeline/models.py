"""Data models for research paper records."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class PaperRecord:
    """Standardized representation of a scientific paper across all sources."""

    id: str  # Unique identifier, e.g. 'arxiv:2305.12345', 'openalex:W12345', 's2:12345'
    title: str
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    doi: Optional[str] = None
    source: str = ""  # 'arxiv', 'openalex', 'semanticscholar'
    categories: List[str] = field(default_factory=list)
    citation_count: int = 0
    open_access_pdf_url: Optional[str] = None
    local_file_path: Optional[str] = None
    download_status: str = "pending"  # 'pending', 'completed', 'metadata_only', 'failed'
    collected_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        data = asdict(self)
        return data

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PaperRecord:
        """Instantiate PaperRecord from dictionary."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            abstract=data.get("abstract", "") or "",
            authors=data.get("authors", []) or [],
            year=data.get("year"),
            doi=data.get("doi"),
            source=data.get("source", ""),
            categories=data.get("categories", []) or [],
            citation_count=data.get("citation_count", 0) or 0,
            open_access_pdf_url=data.get("open_access_pdf_url"),
            local_file_path=data.get("local_file_path"),
            download_status=data.get("download_status", "pending"),
            collected_at=data.get(
                "collected_at", datetime.now(timezone.utc).isoformat()
            ),
            raw_metadata=data.get("raw_metadata", {}) or {},
        )
