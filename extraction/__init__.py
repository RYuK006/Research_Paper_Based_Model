"""
Layer 2: Structured Scientific Extraction and Discovery Gap Analysis Engine.
Extracts fixed-schema materials tables (material, composition, structure, Tc, pressure, synthesis, future work)
and identifies unseen element combinations, cross-family synthesis methods, and unfollowed research leads.
"""

from extraction.models import ExtractedPaperRecord
from extraction.extractor import StructuredExtractor
from extraction.gap_analyzer import DiscoveryGapAnalyzer
from extraction.validator import ExtractionValidator

__all__ = [
    "ExtractedPaperRecord",
    "StructuredExtractor",
    "DiscoveryGapAnalyzer",
    "ExtractionValidator",
]
