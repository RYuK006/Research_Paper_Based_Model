"""Master Paper Parser Orchestrator integrating arXiv LaTeX source, GROBID, and PyMuPDF/Marker."""

from __future__ import annotations

import argparse
import logging
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.table import Table

from parsers.grobid_parser import GrobidParser
from parsers.latex_parser import ArxivLatexParser
from parsers.models import ParsedDocument
from parsers.pdf_parser import PDFParser
from pipeline.models import PaperRecord
from pipeline.storage import StorageManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("paper_parser")
console = Console()


class PaperParser:
    """Master document parser prioritizing arXiv LaTeX source, GROBID, and PyMuPDF-Marker."""

    def __init__(self, base_dir: Optional[str | Path] = None):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent / "data"
        else:
            self.base_dir = Path(base_dir)

        self.storage = StorageManager(base_dir=self.base_dir)
        self.parsed_dir = self.base_dir / "parsed"
        for sub in ["arxiv", "openalex", "semanticscholar"]:
            (self.parsed_dir / sub).mkdir(parents=True, exist_ok=True)

        self.latex_parser = ArxivLatexParser()
        self.pdf_parser = PDFParser()
        self.grobid_parser = GrobidParser()

        self._init_parsed_db()

    def _init_parsed_db(self) -> None:
        """Create table for tracking parsed papers."""
        conn = sqlite3.connect(str(self.storage.db_path))
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS parsed_documents (
                    paper_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    year INTEGER,
                    authors TEXT,
                    doi TEXT,
                    source TEXT NOT NULL,
                    parser_used TEXT NOT NULL,
                    markdown_path TEXT NOT NULL,
                    equation_count INTEGER DEFAULT 0,
                    table_count INTEGER DEFAULT 0,
                    parsed_at TEXT NOT NULL
                )
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_parsed_source ON parsed_documents(source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_parsed_parser ON parsed_documents(parser_used)")
            conn.commit()
        finally:
            conn.close()

    def parse_paper(self, paper: PaperRecord, local_pdf_path: Optional[str | Path] = None) -> Optional[ParsedDocument]:
        """Parse a single paper using the best available parser."""
        doc: Optional[ParsedDocument] = None

        # 1. If arXiv paper, attempt LaTeX source first
        if paper.source == "arxiv" or "arxiv" in paper.id:
            logger.info("Attempting arXiv LaTeX source extraction for %s...", paper.id)
            try:
                doc = self.latex_parser.parse(paper)
                if doc:
                    logger.info("Successfully parsed arXiv LaTeX source: %d equations, %d tables", len(doc.equations), len(doc.tables))
            except Exception as e:
                logger.warning("LaTeX parsing error for %s: %s", paper.id, e)

        # 2. If PDF available or downloaded, try GROBID then PDFParser
        pdf_path = None
        if local_pdf_path and Path(local_pdf_path).exists():
            pdf_path = Path(local_pdf_path)
        elif paper.local_file_path and Path(paper.local_file_path).suffix.lower() == ".pdf" and Path(paper.local_file_path).exists():
            pdf_path = Path(paper.local_file_path)

        if not doc and pdf_path:
            # Check GROBID
            if self.grobid_parser.is_alive():
                logger.info("Parsing with GROBID server for %s...", paper.id)
                try:
                    doc = self.grobid_parser.parse_pdf(pdf_path, fallback_record=paper)
                except Exception as e:
                    logger.warning("GROBID processing failed for %s: %s", paper.id, e)

            # Fallback to PyMuPDF / Marker layout parser
            if not doc:
                logger.info("Parsing with PyMuPDF-Marker layout engine for %s...", paper.id)
                doc = self.pdf_parser.parse_pdf_file(pdf_path, metadata=paper)

        # 3. If neither source nor PDF, generate rich metadata document
        if not doc:
            clean_md = (
                f"{paper.abstract}\n\n"
                f"**Keywords / Categories**: {', '.join(paper.categories)}\n\n"
                f"**Citations**: {paper.citation_count}\n"
                f"**Open Access Link**: [{paper.open_access_pdf_url}]({paper.open_access_pdf_url})\n"
            )
            doc = ParsedDocument(
                paper_id=paper.id,
                title=paper.title,
                authors=paper.authors,
                year=paper.year,
                doi=paper.doi,
                source=paper.source,
                abstract=paper.abstract,
                parser_used="metadata_abstract",
                text_markdown=clean_md,
            )

        # Save to disk
        clean_name = paper.id.replace(":", "_").replace("/", "_").replace(".", "_")
        dest_md = self.parsed_dir / paper.source / f"{clean_name}.md"
        doc.save_markdown(dest_md)

        # Save record in parsed_documents SQLite
        self._record_parsed(doc, str(dest_md))
        return doc

    def _record_parsed(self, doc: ParsedDocument, md_path: str) -> None:
        """Record parsing details in SQLite database."""
        import json

        conn = sqlite3.connect(str(self.storage.db_path))
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO parsed_documents (
                    paper_id, title, year, authors, doi, source, parser_used,
                    markdown_path, equation_count, table_count, parsed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(paper_id) DO UPDATE SET
                    title = excluded.title,
                    year = excluded.year,
                    authors = excluded.authors,
                    doi = excluded.doi,
                    source = excluded.source,
                    parser_used = excluded.parser_used,
                    markdown_path = excluded.markdown_path,
                    equation_count = excluded.equation_count,
                    table_count = excluded.table_count,
                    parsed_at = excluded.parsed_at
                """,
                (
                    doc.paper_id,
                    doc.title,
                    doc.year,
                    json.dumps(doc.authors, ensure_ascii=False),
                    doc.doi,
                    doc.source,
                    doc.parser_used,
                    md_path,
                    len(doc.equations),
                    len(doc.tables),
                    doc.parsed_at,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def get_parsed_stats(self) -> Dict[str, Any]:
        """Retrieve statistics of parsed papers."""
        conn = sqlite3.connect(str(self.storage.db_path))
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT parser_used, COUNT(*), SUM(equation_count), SUM(table_count) FROM parsed_documents GROUP BY parser_used")
            rows = cursor.fetchall()
            stats = {}
            for r in rows:
                stats[r[0]] = {
                    "count": r[1],
                    "total_equations": r[2] or 0,
                    "total_tables": r[3] or 0,
                }
            return stats
        finally:
            conn.close()

    def print_parsed_table(self) -> None:
        """Display summary table of parsed papers."""
        stats = self.get_parsed_stats()
        table = Table(title="[bold green]Parsed Scientific Documents Summary[/bold green]")
        table.add_column("Parser Engine", style="cyan")
        table.add_column("Documents Parsed", style="green", justify="right")
        table.add_column("Equations Extracted", style="magenta", justify="right")
        table.add_column("Tables Extracted", style="yellow", justify="right")

        total_docs = sum(s["count"] for s in stats.values())
        total_eqs = sum(s["total_equations"] for s in stats.values())
        total_tbls = sum(s["total_tables"] for s in stats.values())

        for p_name, s in stats.items():
            table.add_row(
                p_name,
                f"{s['count']:,}",
                f"{s['total_equations']:,}",
                f"{s['total_tables']:,}",
            )

        table.add_section()
        table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]{total_docs:,}[/bold]",
            f"[bold]{total_eqs:,}[/bold]",
            f"[bold]{total_tbls:,}[/bold]",
        )
        console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse research papers into clean Markdown preserving equations and tables")
    parser.add_argument("--limit", type=int, default=10, help="Number of papers to parse (default: 10)")
    parser.add_argument("--source", type=str, default=None, help="Filter by source (arxiv, openalex, semanticscholar)")
    parser.add_argument("--stats", action="store_true", help="Print parsed documents summary")

    args = parser.parse_args()
    paper_parser = PaperParser()

    if args.stats:
        paper_parser.print_parsed_table()
        return

    # Fetch papers from SQLite
    conn = sqlite3.connect(str(paper_parser.storage.db_path))
    try:
        cursor = conn.cursor()
        query = "SELECT id, title, abstract, authors, year, doi, source, categories, citation_count, open_access_pdf_url, local_file_path FROM papers"
        params = []
        if args.source:
            query += " WHERE source = ?"
            params.append(args.source)
        query += f" LIMIT {args.limit}"
        cursor.execute(query, params)
        rows = cursor.fetchall()
    finally:
        conn.close()

    import json
    for r in rows:
        rec = PaperRecord(
            id=r[0],
            title=r[1],
            abstract=r[2] or "",
            authors=json.loads(r[3]) if r[3] else [],
            year=r[4],
            doi=r[5],
            source=r[6],
            categories=json.loads(r[7]) if r[7] else [],
            citation_count=r[8] or 0,
            open_access_pdf_url=r[9],
            local_file_path=r[10],
        )
        doc = paper_parser.parse_paper(rec)
        if doc:
            console.print(f"[green]Parsed {rec.id}[/green] -> {doc.parser_used} (Eqs: {len(doc.equations)}, Tables: {len(doc.tables)})")

    paper_parser.print_parsed_table()


if __name__ == "__main__":
    main()
