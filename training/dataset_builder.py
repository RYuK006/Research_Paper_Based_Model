"""
Scientific instruction tuning dataset builder for research papers.
Transforms 10,000 collected papers into instruction-tuning datasets for LLMs.
Implements the time-split evaluation methodology (pre-2021 training vs post-2021 evaluation)
to benchmark genuine unseen scientific discovery signal.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("dataset_builder")


SYSTEM_PROMPT = (
    "You are an expert scientific researcher in condensed matter physics, materials science, "
    "and inorganic chemistry. You reason strictly from experimental evidence, extract precise "
    "material compositions, synthesis protocols, and physical properties (Tc, pressure, crystal structure), "
    "and propose rigorous, chemically plausible follow-up experiments based on observed gaps."
)


@dataclass
class InstructionSample:
    """Represents a single instruction-tuning sample."""
    sample_id: str
    paper_id: str
    year: int
    task_type: str  # 'extraction', 'property_claim', 'hypothesis_proposal'
    instruction: str
    input_text: str
    target_output: str
    split: str  # 'train_pre2021' or 'eval_post2021'

    def to_alpaca(self) -> Dict[str, Any]:
        """Convert to standard Alpaca instruction-input-output format."""
        return {
            "id": self.sample_id,
            "instruction": self.instruction,
            "input": self.input_text,
            "output": self.target_output,
            "metadata": {
                "paper_id": self.paper_id,
                "year": self.year,
                "task_type": self.task_type,
                "split": self.split,
            },
        }

    def to_chatml(self) -> Dict[str, Any]:
        """Convert to Llama-3 / ChatML messages format."""
        user_content = self.instruction
        if self.input_text.strip():
            user_content = f"{self.instruction}\n\n### Context:\n{self.input_text}"

        return {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": self.target_output},
            ],
            "metadata": {
                "sample_id": self.sample_id,
                "paper_id": self.paper_id,
                "year": self.year,
                "task_type": self.task_type,
                "split": self.split,
            },
        }


class ScientificDatasetBuilder:
    """
    Builds instruction-tuning datasets from SQLite research paper database.
    Formats multi-task scientific training data and partitions by time-split cutoff.
    """

    def __init__(
        self,
        db_path: str = "data/papers.db",
        cutoff_year: int = 2021,
        output_dir: str = "data/training",
    ) -> None:
        self.db_path = Path(db_path)
        self.cutoff_year = cutoff_year
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_tc_and_pressure(self, text: str) -> Optional[Tuple[str, str]]:
        """Heuristic extractor for Tc and pressure claims in text."""
        tc_match = re.search(r"T_?[cC]\s*(?:=|of|around|up to|~)?\s*([0-9]+(?:\.[0-9]+)?\s*K)", text, re.IGNORECASE)
        press_match = re.search(r"(?:pressure|at)\s*(?:of|around|~)?\s*([0-9]+(?:\.[0-9]+)?\s*(?:GPa|bar|kbar|MPa|atm))", text, re.IGNORECASE)

        tc_val = tc_match.group(1) if tc_match else "Unspecified in abstract"
        press_val = press_match.group(1) if press_match else "Ambient pressure"

        if tc_match or press_match:
            return tc_val, press_val
        return None

    def extract_material_and_structure(self, text: str) -> Optional[Tuple[str, str]]:
        """Heuristic extractor for chemical formula and crystal structure."""
        formula_match = re.search(r"\b([A-Z][a-z]?[0-9]*(?:\.[0-9]+)?(?:[A-Z][a-z]?[0-9]*(?:\.[0-9]+)?)+)\b", text)
        struct_match = re.search(r"\b(tetragonal|orthorhombic|cubic|hexagonal|monoclinic|triclinic|perovskite|spinel|rutile|pyrochlore|fluorite)\b", text, re.IGNORECASE)

        formula = formula_match.group(1) if formula_match else "Target compound system"
        structure = struct_match.group(1).capitalize() if struct_match else "Unspecified lattice"

        if formula_match or struct_match:
            return formula, structure
        return None

    def segment_abstract_for_hypothesis(self, abstract: str) -> Tuple[str, str]:
        """
        Splits abstract into background/evidence context and author's concluding future work / implication.
        Used to train models on proposing the next experiment or discovery direction.
        """
        sentences = re.split(r"(?<=[.!?])\s+", abstract.strip())
        if len(sentences) <= 2:
            return abstract, "Further experimental characterization and chemical doping needed to elucidate the mechanism."

        # Take first 70-80% as context, last sentence(s) as the target proposal / future direction
        split_idx = max(1, len(sentences) - 2)
        context = " ".join(sentences[:split_idx])
        target = " ".join(sentences[split_idx:])
        return context, target

    def generate_samples_from_paper(self, row: sqlite3.Row) -> List[InstructionSample]:
        """Convert a paper database row into instruction tuning samples."""
        paper_id = row["id"]
        title = row["title"] or ""
        abstract = row["abstract"] or ""
        year = int(row["year"]) if row["year"] else 2020
        split = "train_pre2021" if year <= self.cutoff_year else "eval_post2021"

        if len(abstract.strip()) < 80:
            return []

        samples: List[InstructionSample] = []

        # Task 1: Structured Extraction (Layer 2 Table extraction)
        mat_struct = self.extract_material_and_structure(abstract)
        tc_press = self.extract_tc_and_pressure(abstract)

        ext_output = (
            f"**Structured Extraction Table**:\n"
            f"- **Target Material / Composition**: {mat_struct[0] if mat_struct else 'Materials system discussed in study'}\n"
            f"- **Crystal Structure**: {mat_struct[1] if mat_struct else 'Not specified'}\n"
            f"- **Superconducting Tc**: {tc_press[0] if tc_press else 'Not reported / Non-superconducting'}\n"
            f"- **Pressure Conditions**: {tc_press[1] if tc_press else 'Ambient'}\n"
            f"- **Core Finding**: {abstract[:200]}..."
        )

        samples.append(InstructionSample(
            sample_id=f"{paper_id}_extract",
            paper_id=paper_id,
            year=year,
            task_type="extraction",
            instruction=(
                "Extract the material composition, crystal structure, superconducting critical "
                "temperature (Tc), pressure conditions, and core finding from the following research abstract."
            ),
            input_text=f"Title: {title}\n\nAbstract:\n{abstract}",
            target_output=ext_output,
            split=split,
        ))

        # Task 2: Hypothesis Proposal / Next Experiment Generation (Layer 3 Core)
        context, future_work = self.segment_abstract_for_hypothesis(abstract)
        samples.append(InstructionSample(
            sample_id=f"{paper_id}_hypothesis",
            paper_id=paper_id,
            year=year,
            task_type="hypothesis_proposal",
            instruction=(
                "Based on the following experimental background, synthesis findings, and observed "
                "limitations, what follow-up experiment, dopant substitution, or next research direction "
                "should be pursued?"
            ),
            input_text=f"Title: {title}\n\nObserved Background & Results:\n{context}",
            target_output=(
                f"**Proposed Follow-Up Experiment & Research Direction**:\n\n"
                f"{future_work}\n\n"
                f"**Rationale**: Addressing these remaining open questions allows verifying "
                f"whether the phase stability and electronic transport persist under altered chemical pressure."
            ),
            split=split,
        ))

        return samples

    def build_dataset(
        self,
        limit_train: Optional[int] = None,
        limit_eval: Optional[int] = None,
    ) -> Dict[str, int]:
        """
        Queries papers database, generates instruction pairs, and exports to train and eval JSONL files.
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")

        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        train_file_alpaca = self.output_dir / "train_pre2021_alpaca.jsonl"
        train_file_chatml = self.output_dir / "train_pre2021_chatml.jsonl"
        eval_file_alpaca = self.output_dir / "eval_post2021_alpaca.jsonl"
        eval_file_chatml = self.output_dir / "eval_post2021_chatml.jsonl"

        train_count = 0
        eval_count = 0

        logger.info(f"Connecting to {self.db_path}, partitioning on cutoff year {self.cutoff_year}...")

        with (
            open(train_file_alpaca, "w", encoding="utf-8") as f_tr_alpaca,
            open(train_file_chatml, "w", encoding="utf-8") as f_tr_chatml,
            open(eval_file_alpaca, "w", encoding="utf-8") as f_ev_alpaca,
            open(eval_file_chatml, "w", encoding="utf-8") as f_ev_chatml,
        ):
            cursor.execute("SELECT id, title, abstract, year, source FROM papers ORDER BY year ASC")
            for row in cursor:
                samples = self.generate_samples_from_paper(row)
                for s in samples:
                    if s.split == "train_pre2021":
                        if limit_train and train_count >= limit_train:
                            continue
                        f_tr_alpaca.write(json.dumps(s.to_alpaca()) + "\n")
                        f_tr_chatml.write(json.dumps(s.to_chatml()) + "\n")
                        train_count += 1
                    else:
                        if limit_eval and eval_count >= limit_eval:
                            continue
                        f_ev_alpaca.write(json.dumps(s.to_alpaca()) + "\n")
                        f_ev_chatml.write(json.dumps(s.to_chatml()) + "\n")
                        eval_count += 1

        conn.close()

        stats = {
            "cutoff_year": self.cutoff_year,
            "train_samples_pre2021": train_count,
            "eval_samples_post2021": eval_count,
            "total_samples": train_count + eval_count,
            "files": {
                "train_alpaca": str(train_file_alpaca),
                "train_chatml": str(train_file_chatml),
                "eval_alpaca": str(eval_file_alpaca),
                "eval_chatml": str(eval_file_chatml),
            },
        }

        stats_path = self.output_dir / "dataset_stats.json"
        with open(stats_path, "w", encoding="utf-8") as f_stats:
            json.dump(stats, f_stats, indent=2)

        logger.info(f"Dataset build complete: {train_count} train samples, {eval_count} eval samples.")
        logger.info(f"Saved stats to {stats_path}")
        return stats


def main() -> None:
    """CLI runner for dataset builder."""
    import argparse

    parser = argparse.ArgumentParser(description="Build scientific instruction dataset from papers database")
    parser.add_argument("--db-path", default="data/papers.db", help="Path to SQLite papers database")
    parser.add_argument("--cutoff-year", type=int, default=2021, help="Cutoff year for time-split evaluation")
    parser.add_argument("--output-dir", default="data/training", help="Output directory for JSONL files")
    parser.add_argument("--limit-train", type=int, default=None, help="Limit number of train samples")
    parser.add_argument("--limit-eval", type=int, default=None, help="Limit number of eval samples")

    args = parser.parse_args()
    builder = ScientificDatasetBuilder(
        db_path=args.db_path,
        cutoff_year=args.cutoff_year,
        output_dir=args.output_dir,
    )
    stats = builder.build_dataset(limit_train=args.limit_train, limit_eval=args.limit_eval)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
