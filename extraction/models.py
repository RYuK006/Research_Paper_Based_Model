"""
Data models for Layer 2 structured extraction table.
Stores material, composition, crystal structure, Tc, pressure, synthesis method,
measurement techniques, and author stated future work.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ExtractedPaperRecord:
    """Fixed-schema materials record extracted from a research paper."""
    paper_id: str
    doi: Optional[str]
    year: int
    material: str
    composition: str
    elements: List[str]
    structure_type: str
    tc_kelvin: Optional[float]
    pressure_gpa: Optional[float]
    synthesis_method: str
    measurement_type: str
    future_work: str
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_sql_row(self) -> tuple:
        """Converts to SQLite row tuple."""
        return (
            self.paper_id,
            self.doi,
            self.year,
            self.material,
            self.composition,
            json.dumps(self.elements),
            self.structure_type,
            self.tc_kelvin,
            self.pressure_gpa,
            self.synthesis_method,
            self.measurement_type,
            self.future_work,
            self.confidence,
        )

    @classmethod
    def from_sql_row(cls, row: tuple) -> ExtractedPaperRecord:
        """Constructs instance from SQLite row tuple."""
        return cls(
            paper_id=row[0],
            doi=row[1],
            year=row[2],
            material=row[3],
            composition=row[4],
            elements=json.loads(row[5]) if row[5] else [],
            structure_type=row[6],
            tc_kelvin=row[7],
            pressure_gpa=row[8],
            synthesis_method=row[9],
            measurement_type=row[10],
            future_work=row[11],
            confidence=row[12],
        )
