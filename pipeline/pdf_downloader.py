"""Asynchronous high-throughput PDF downloader for collected open-access papers."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeRemainingColumn

from pipeline.storage import StorageManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("pdf_downloader")
console = Console()


class PDFDownloader:
    """Downloads full-text PDFs for papers in the SQLite database with open-access links."""

    def __init__(
        self,
        base_dir: Optional[str | Path] = None,
        concurrency: int = 5,
        user_agent: str = "ResearchCollector/1.0 (mailto:RYuK006@users.noreply.github.com)",
    ):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent / "data"
        else:
            self.base_dir = Path(base_dir)

        self.storage = StorageManager(base_dir=self.base_dir)
        self.pdf_dir = self.base_dir / "papers" / "pdfs"
        self.concurrency = concurrency
        self.headers = {"User-Agent": user_agent}

        for sub in ["arxiv", "openalex", "semanticscholar"]:
            (self.pdf_dir / sub).mkdir(parents=True, exist_ok=True)

    def get_pending_downloads(self, limit: Optional[int] = None) -> List[Tuple[str, str, str]]:
        """Retrieve papers that have an open_access_pdf_url and are not yet downloaded."""
        conn = sqlite3.connect(str(self.storage.db_path))
        try:
            cursor = conn.cursor()
            query = """
                SELECT id, source, open_access_pdf_url
                FROM papers
                WHERE open_access_pdf_url IS NOT NULL
                  AND open_access_pdf_url != ''
                  AND (download_status != 'completed' OR download_status IS NULL)
            """
            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

    def update_download_status(self, paper_id: str, file_path: str, status: str) -> None:
        """Update paper status in SQLite."""
        conn = sqlite3.connect(str(self.storage.db_path))
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE papers
                SET local_file_path = ?, download_status = ?
                WHERE id = ?
                """,
                (file_path, status, paper_id),
            )
            conn.commit()
        finally:
            conn.close()

    async def _download_one(
        self,
        client: httpx.AsyncClient,
        semaphore: asyncio.Semaphore,
        paper_id: str,
        source: str,
        pdf_url: str,
        progress: Progress,
        task_id: Any,
    ) -> bool:
        """Download a single paper PDF."""
        clean_id = paper_id.replace(":", "_").replace("/", "_").replace(".", "_")
        dest_path = self.pdf_dir / source / f"{clean_id}.pdf"

        if dest_path.exists() and dest_path.stat().st_size > 1024:
            self.update_download_status(paper_id, str(dest_path), "completed")
            progress.advance(task_id)
            return True

        async with semaphore:
            for attempt in range(3):
                try:
                    resp = await client.get(pdf_url)
                    if resp.status_code == 200 and len(resp.content) > 1024:
                        # Verify PDF header
                        if resp.content[:4] == b"%PDF" or "pdf" in resp.headers.get("content-type", "").lower():
                            dest_path.write_bytes(resp.content)
                            self.update_download_status(paper_id, str(dest_path), "completed")
                            progress.advance(task_id)
                            return True
                    elif resp.status_code == 429:
                        await asyncio.sleep(2.0 * (attempt + 1))
                        continue
                    else:
                        break
                except Exception as e:
                    await asyncio.sleep(1.0)

            self.update_download_status(paper_id, "", "failed")
            progress.advance(task_id)
            return False

    async def download_all(self, limit: Optional[int] = None) -> int:
        """Download PDFs asynchronously with progress bar."""
        papers = self.get_pending_downloads(limit=limit)
        if not papers:
            console.print("[yellow]No pending PDF downloads found.[/yellow]")
            return 0

        console.print(f"[bold cyan]Starting download of {len(papers):,} open-access PDFs...[/bold cyan]")
        semaphore = asyncio.Semaphore(self.concurrency)

        limits = httpx.Limits(max_keepalive_connections=self.concurrency, max_connections=self.concurrency * 2)
        async with httpx.AsyncClient(headers=self.headers, limits=limits, timeout=30.0, follow_redirects=True) as client:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task_id = progress.add_task("[cyan]Downloading papers...", total=len(papers))
                tasks = [
                    self._download_one(client, semaphore, p_id, src, url, progress, task_id)
                    for p_id, src, url in papers
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

        success_count = sum(1 for r in results if r is True)
        console.print(f"[bold green]Successfully downloaded {success_count:,} PDFs![/bold green]")
        return success_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Download full-text PDFs for open-access papers")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of PDFs to download")
    parser.add_argument("--concurrency", type=int, default=5, help="Concurrent downloads (default: 5)")
    args = parser.parse_args()

    downloader = PDFDownloader(concurrency=args.concurrency)
    asyncio.run(downloader.download_all(limit=args.limit))


if __name__ == "__main__":
    main()
