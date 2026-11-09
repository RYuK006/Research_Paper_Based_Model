"""Generates detailed analytical reports on the 10,000 research paper dataset."""

from __future__ import annotations

import collections
import json
import logging
import re
import sqlite3
from pathlib import Path
from typing import Any, Counter, Dict, List, Tuple

from pipeline.storage import StorageManager

logger = logging.getLogger("report_generator")

# Common chemical elements
ELEMENTS = [
    "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen",
    "Fluorine", "Neon", "Sodium", "Magnesium", "Aluminum", "Silicon", "Phosphorus", "Sulfur",
    "Chlorine", "Argon", "Potassium", "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium",
    "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Gallium", "Germanium",
    "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium", "Strontium", "Yttrium", "Zirconium",
    "Niobium", "Molybdenum", "Ruthenium", "Rhodium", "Palladium", "Silver", "Cadmium", "Indium",
    "Tin", "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium", "Barium", "Lanthanum",
    "Cerium", "Praseodymium", "Neodymium", "Samarium", "Europium", "Gadolinium", "Terbium",
    "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium", "Hafnium", "Tantalum",
    "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury", "Thallium",
    "Lead", "Bismuth", "Thorium", "Uranium"
]

# Material and compound classes
COMPOUND_CLASSES = [
    ("Cuprates / High-Tc Superconductors", [r"\bcuprate", r"\byba?cu", r"\bbsc?co", r"\blaco", r"\bhgba?ca?cu"]),
    ("Iron-based Pnictides & Chalcogenides", [r"\bpnictide", r"\bchalcogenide", r"\bfeas", r"\bfe\w*se", r"\blao?fe"]),
    ("Perovskites & Oxides", [r"\bperovskite", r"\boxide", r"\btitanate", r"\bruthenate"]),
    ("Superhydrides & High-Pressure Phases", [r"\bhydride", r"\blahh", r"\byh", r"\bclathrate"]),
    ("2D Materials & Dichalcogenides", [r"\bgraphene", r"\btransition metal dichalcogenide", r"\btmd\b", r"\bmos2", r"\bwse2"]),
    ("Intermetallics & Heavy Fermions", [r"\bheavy fermion", r"\bkondo", r"\bintermetallic", r"\bheavily doped"]),
    ("Topological & Quantum Materials", [r"\btopological insulator", r"\bweyl", r"\bdirac semimetal", r"\bmajorana"]),
    ("Metal-Organic Frameworks (MOFs)", [r"\bmetal-organic framework", r"\bmof\b", r"\bcoordination polymer"]),
]


class ReportGenerator:
    """Analyzes papers in SQLite and writes REPORT.md and summary JSON."""

    def __init__(self, base_dir: Optional[str | Path] = None):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.storage = StorageManager(base_dir=self.base_dir / "data")
        self.report_path = self.base_dir / "REPORT.md"
        self.summary_json_path = self.base_dir / "data" / "analysis_summary.json"

    def analyze(self) -> Dict[str, Any]:
        """Perform full analytical scan across all stored papers."""
        counts = self.storage.get_counts_by_source()
        total_papers = sum(counts.values())

        year_counter: Counter[int] = collections.Counter()
        element_counter: Counter[str] = collections.Counter()
        compound_counter: Counter[str] = collections.Counter()
        citation_list: List[Tuple[str, str, int, str]] = []  # (title, source, citations, doi/url)

        with sqlite3.connect(str(self.storage.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, abstract, year, citation_count, source, doi, open_access_pdf_url FROM papers"
            )
            rows = cursor.fetchall()

        for row in rows:
            p_id, title, abstract, year, citations, source, doi, oa_url = row
            text = f"{title or ''} {abstract or ''}".lower()

            if year:
                year_counter[year] += 1

            if citations:
                citation_list.append((title or "Untitled", source, citations or 0, doi or oa_url or ""))

            # Count elements
            for elem in ELEMENTS:
                if re.search(r"\b" + elem.lower() + r"\b", text):
                    element_counter[elem] += 1

            # Count compound classes
            for class_name, regexes in COMPOUND_CLASSES:
                if any(re.search(pattern, text) for pattern in regexes):
                    compound_counter[class_name] += 1

        citation_list.sort(key=lambda x: x[2], reverse=True)
        top_cited = citation_list[:25]

        summary = {
            "total_papers": total_papers,
            "source_distribution": counts,
            "year_distribution": dict(sorted(year_counter.items())),
            "top_elements": element_counter.most_common(20),
            "compound_classes": compound_counter.most_common(),
            "top_cited_papers": [
                {"title": t, "source": s, "citations": c, "link": l}
                for t, s, c, l in top_cited
            ],
        }

        self.summary_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.summary_json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        return summary

    def generate_report(self) -> Path:
        """Generate markdown REPORT.md."""
        data = self.analyze()
        total = data["total_papers"]
        sources = data["source_distribution"]
        years = data["year_distribution"]
        elements = data["top_elements"]
        compounds = data["compound_classes"]
        top_cited = data["top_cited_papers"]

        md: List[str] = [
            "# Comprehensive Corpus Report: 10,000 Scientific Research Papers",
            "",
            "> Automated synthesis and domain analysis of scientific literature harvested from **arXiv**, **OpenAlex**, and **Semantic Scholar** / Open Academic Graph.",
            "",
            "## 1. Executive Summary",
            "",
            f"- **Total Papers Collected**: **{total:,}**",
            f"- **Target Milestone**: 10,000 papers",
            f"- **Database Index**: SQLite (`data/papers.db`) with full JSONL stream (`data/manifests/papers_manifest.jsonl`)",
            f"- **Target Google Drive Storage**: `https://drive.google.com/drive/folders/1kYS059jeKZsFENUvd7ClgeIBlwAJibdL`",
            "",
            "### Source Distribution",
            "",
            "| Data Source | Collected Count | Percentage | Focus Domains |",
            "| :--- | :---: | :---: | :--- |",
        ]

        for src, cnt in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            pct = (cnt / total * 100) if total > 0 else 0
            focus = {
                "arxiv": "Superconductivity (`cond-mat.supr-con`), Materials Science (`cond-mat.mtrl-sci`)",
                "openalex": "Chemistry, Chemical Elements, Novel Compounds, Open-Access Works",
                "semanticscholar": "Chemical Compounds, Materials Synthesis, Crossref Open Graph",
            }.get(src, "Scientific Literature")
            md.append(f"| **{src.upper()}** | {cnt:,} | {pct:.1f}% | {focus} |")

        md.extend([
            f"| **TOTAL** | **{total:,}** | **100.0%** | Comprehensive Physical Sciences Corpus |",
            "",
            "---",
            "",
            "## 2. Chemical Elements Frequency",
            "",
            "Most prominently studied chemical elements identified in paper titles and abstracts across the corpus:",
            "",
            "| Rank | Element | Frequency (Papers) | Percentage of Corpus |",
            "| :---: | :--- | :---: | :---: |",
        ])

        for idx, (elem, freq) in enumerate(elements, 1):
            pct = (freq / total * 100) if total > 0 else 0
            md.append(f"| {idx} | **{elem}** | {freq:,} | {pct:.1f}% |")

        md.extend([
            "",
            "---",
            "",
            "## 3. Compound & Materials Class Distribution",
            "",
            "Distribution of papers across key material families, superconducting structures, and novel chemical compounds:",
            "",
            "| Material / Compound Class | Paper Count | Proportion |",
            "| :--- | :---: | :---: |",
        ])

        for cls_name, cnt in compounds:
            pct = (cnt / total * 100) if total > 0 else 0
            md.append(f"| {cls_name} | {cnt:,} | {pct:.1f}% |")

        md.extend([
            "",
            "---",
            "",
            "## 4. Publication Timeline",
            "",
            "Distribution of publications by year across the corpus:",
            "",
            "| Year Span | Number of Papers | Proportion |",
            "| :--- | :---: | :---: |",
        ])

        # Group years into decades/recent buckets
        decade_counts: Counter[str] = collections.Counter()
        for y, c in years.items():
            if y >= 2024:
                decade_counts["2024 - 2026 (Recent Frontiers)"] += c
            elif y >= 2020:
                decade_counts["2020 - 2023"] += c
            elif y >= 2010:
                decade_counts["2010 - 2019"] += c
            elif y >= 2000:
                decade_counts["2000 - 2009"] += c
            else:
                decade_counts["Pre-2000 (Foundational)"] += c

        for span, cnt in decade_counts.items():
            pct = (cnt / total * 100) if total > 0 else 0
            md.append(f"| {span} | {cnt:,} | {pct:.1f}% |")

        md.extend([
            "",
            "---",
            "",
            "## 5. Top Highly-Cited Landmark Papers in Corpus",
            "",
            "| Citations | Title | Source | Link / DOI |",
            "| :---: | :--- | :---: | :--- |",
        ])

        for p in top_cited[:15]:
            title = p["title"][:90] + ("..." if len(p["title"]) > 90 else "")
            link = p["link"] or "N/A"
            md.append(f"| **{p['citations']:,}** | {title} | {p['source'].upper()} | `{link}` |")

        md.extend([
            "",
            "---",
            "",
            "## 6. Pipeline Artifacts & Local Manifests",
            "",
            "- **SQLite Database**: `data/papers.db` (indexes, schema, full text and citation counts)",
            "- **JSONL Stream Manifest**: `data/manifests/papers_manifest.jsonl`",
            "- **Raw Payloads**: `data/papers/arxiv/`, `data/papers/openalex/`, `data/papers/semanticscholar/`",
            "- **Google Drive Uploader**: `drive_sync/gdrive_uploader.py`",
            f"- **Target Google Drive**: `https://drive.google.com/drive/folders/1kYS059jeKZsFENUvd7ClgeIBlwAJibdL`",
            "",
            "_Report generated autonomously by Antigravity Pipeline under author RYuK006._",
        ])

        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")

        logger.info("Report written to %s", self.report_path)
        return self.report_path


def main() -> None:
    gen = ReportGenerator()
    gen.generate_report()
    print(f"Report successfully generated at: {gen.report_path}")


if __name__ == "__main__":
    main()
