"""
Validation harness for structured extractions.
Benchmarks automated extractions against a hand-checked gold-standard sample
to guarantee high data integrity before feeding into the candidate pipeline.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from extraction.extractor import StructuredExtractor
from extraction.models import ExtractedPaperRecord

logger = logging.getLogger("validator")

# Hand-checked benchmark papers with verified ground-truth values
GOLD_STANDARD_BENCHMARKS = [
    {
        "paper_id": "bench_001",
        "title": "Superconductivity at 250 K in lanthanum hydride under high pressure",
        "abstract": "Laser-heated diamond anvil cells were used to synthesize cubic LaH10 at 170 GPa. Electrical resistivity measurements confirm Tc of 250 K. Further experimental studies should investigate ternary hydrides with yttrium.",
        "year": 2019,
        "ground_truth": {
            "material": "LaH10",
            "elements": ["H", "La"],
            "structure_type": "Cubic",
            "tc_kelvin": 250.0,
            "pressure_gpa": 170.0,
            "synthesis_method": "Laser-heated diamond anvil cell",
        }
    },
    {
        "paper_id": "bench_002",
        "title": "High-temperature superconductivity in YBa2Cu3O7-delta perovskite films",
        "abstract": "Pulsed laser deposition was utilized to grow orthorhombic YBa2Cu3O7 thin films. SQUID magnetometry confirms zero resistance and Meissner effect with Tc of 92 K at ambient pressure.",
        "year": 2020,
        "ground_truth": {
            "material": "YBa2Cu3O7",
            "elements": ["Ba", "Cu", "O", "Y"],
            "structure_type": "Orthorhombic",
            "tc_kelvin": 92.0,
            "pressure_gpa": 0.0001,
            "synthesis_method": "Pulsed laser deposition",
        }
    },
    {
        "paper_id": "bench_003",
        "title": "Superconductivity at 39 K in magnesium diboride",
        "abstract": "Solid-state reaction between magnesium and boron powder at high temperature produces hexagonal MgB2 with Tc of 39 K. Four-probe electrical resistivity was measured.",
        "year": 2001,
        "ground_truth": {
            "material": "MgB2",
            "elements": ["B", "Mg"],
            "structure_type": "Hexagonal",
            "tc_kelvin": 39.0,
            "pressure_gpa": None,
            "synthesis_method": "Solid-state reaction",
        }
    }
]


class ExtractionValidator:
    """
    Validates StructuredExtractor output against hand-checked gold-standard benchmark records.
    """

    def __init__(self) -> None:
        self.extractor = StructuredExtractor(db_path=":memory:")

    def evaluate_benchmark_sample(
        self,
        benchmarks: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Runs automated extraction on gold-standard benchmarks and calculates field-level accuracy.
        """
        items = benchmarks or GOLD_STANDARD_BENCHMARKS
        total_fields = 0
        correct_fields = 0
        field_stats = {
            "elements": {"correct": 0, "total": 0},
            "tc": {"correct": 0, "total": 0},
            "pressure": {"correct": 0, "total": 0},
            "structure": {"correct": 0, "total": 0},
            "synthesis": {"correct": 0, "total": 0},
        }

        detailed_results = []

        for b in items:
            rec = self.extractor.extract_record(
                paper_id=b["paper_id"],
                title=b["title"],
                abstract=b["abstract"],
                year=b["year"],
            )
            gt = b["ground_truth"]

            # 1. Elements
            field_stats["elements"]["total"] += 1
            if set(rec.elements) == set(gt["elements"]):
                field_stats["elements"]["correct"] += 1
                correct_fields += 1
            total_fields += 1

            # 2. Tc
            field_stats["tc"]["total"] += 1
            if rec.tc_kelvin == gt["tc_kelvin"]:
                field_stats["tc"]["correct"] += 1
                correct_fields += 1
            total_fields += 1

            # 3. Pressure
            field_stats["pressure"]["total"] += 1
            if rec.pressure_gpa == gt["pressure_gpa"]:
                field_stats["pressure"]["correct"] += 1
                correct_fields += 1
            total_fields += 1

            # 4. Structure
            field_stats["structure"]["total"] += 1
            if rec.structure_type.lower() == gt["structure_type"].lower():
                field_stats["structure"]["correct"] += 1
                correct_fields += 1
            total_fields += 1

            # 5. Synthesis
            field_stats["synthesis"]["total"] += 1
            if rec.synthesis_method.lower() == gt["synthesis_method"].lower():
                field_stats["synthesis"]["correct"] += 1
                correct_fields += 1
            total_fields += 1

            detailed_results.append({
                "paper_id": b["paper_id"],
                "extracted_material": rec.material,
                "extracted_tc": rec.tc_kelvin,
                "expected_tc": gt["tc_kelvin"],
                "extracted_pressure": rec.pressure_gpa,
                "expected_pressure": gt["pressure_gpa"],
                "confidence": rec.confidence,
            })

        overall_accuracy = round(correct_fields / max(1, total_fields), 4)
        field_accuracies = {
            f: round(stats["correct"] / max(1, stats["total"]), 4)
            for f, stats in field_stats.items()
        }

        report = {
            "samples_evaluated": len(items),
            "total_field_comparisons": total_fields,
            "overall_accuracy": overall_accuracy,
            "error_rate": round(1.0 - overall_accuracy, 4),
            "field_accuracies": field_accuracies,
            "detailed_results": detailed_results,
            "validation_status": "PASSED" if overall_accuracy >= 0.85 else "NEEDS_TUNING",
        }

        logger.info(f"Validation completed on {len(items)} samples. Overall Accuracy: {overall_accuracy * 100:.1f}%")
        return report


def main() -> None:
    """CLI runner for Extraction Validator."""
    validator = ExtractionValidator()
    report = validator.evaluate_benchmark_sample()
    print("\n" + "=" * 60)
    print("EXTRACTION VALIDATION BENCHMARK REPORT")
    print("=" * 60)
    print(f"Overall Accuracy: {report['overall_accuracy'] * 100:.1f}%")
    print(f"Error Rate:       {report['error_rate'] * 100:.1f}%")
    print(f"Status:           {report['validation_status']}")
    print("-" * 60)
    for field, acc in report["field_accuracies"].items():
        print(f"  - {field.capitalize():<12}: {acc * 100:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
