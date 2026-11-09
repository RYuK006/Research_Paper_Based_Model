"""Master Orchestrator for the Research Paper Collection Pipeline."""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeRemainingColumn
from rich.table import Table

from collectors.arxiv_collector import ArxivCollector
from collectors.openalex_collector import OpenAlexCollector
from collectors.semanticscholar_collector import SemanticScholarCollector
from pipeline.storage import StorageManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("orchestrator")
console = Console()


class CollectionOrchestrator:
    """Coordinates multi-source harvesting across arXiv, OpenAlex, and Semantic Scholar."""

    def __init__(
        self,
        base_dir: Optional[str | Path] = None,
        arxiv_target: int = 4000,
        openalex_target: int = 3000,
        s2_target: int = 3000,
    ):
        self.storage = StorageManager(base_dir=base_dir)
        self.arxiv_target = arxiv_target
        self.openalex_target = openalex_target
        self.s2_target = s2_target

        self.arxiv_collector = ArxivCollector(self.storage)
        self.openalex_collector = OpenAlexCollector(self.storage)
        self.s2_collector = SemanticScholarCollector(self.storage)

    def print_status(self) -> Dict[str, int]:
        """Print current collection status table."""
        counts = self.storage.get_counts_by_source()
        total = sum(counts.values())

        table = Table(title="[bold green]Research Paper Corpus Status[/bold green]")
        table.add_column("Data Source", style="cyan", no_wrap=True)
        table.add_column("Target", style="magenta", justify="right")
        table.add_column("Collected", style="green", justify="right")
        table.add_column("Completion", style="yellow", justify="right")

        sources = [
            ("arxiv", self.arxiv_target),
            ("openalex", self.openalex_target),
            ("semanticscholar", self.s2_target),
        ]

        for src, target in sources:
            cnt = counts.get(src, 0)
            pct = (cnt / target * 100) if target > 0 else 0
            table.add_row(src.upper(), f"{target:,}", f"{cnt:,}", f"{pct:.1f}%")

        overall_target = self.arxiv_target + self.openalex_target + self.s2_target
        overall_pct = (total / overall_target * 100) if overall_target > 0 else 0
        table.add_section()
        table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]{overall_target:,}[/bold]",
            f"[bold]{total:,}[/bold]",
            f"[bold]{overall_pct:.1f}%[/bold]",
        )

        console.print(table)
        return counts

    def run(self, active_sources: Optional[List[str]] = None) -> None:
        """Run all collectors to reach 10,000 papers."""
        if active_sources is None:
            active_sources = ["openalex", "semanticscholar", "arxiv"]

        console.print(
            Panel(
                f"[bold cyan]Launching 10,000 Research Paper Collection Pipeline[/bold cyan]\n"
                f"Targets: arXiv: {self.arxiv_target:,} | OpenAlex: {self.openalex_target:,} | S2/OpenCorpus: {self.s2_target:,}",
                title="Pipeline Initialization",
            )
        )

        self.print_status()

        # Run OpenAlex
        if "openalex" in active_sources:
            console.print("\n[bold yellow]>>> Harvesting OpenAlex (Chemistry, Elements, Compounds)...[/bold yellow]")
            self.openalex_collector.harvest(target_count=self.openalex_target)
            self.print_status()

        # Run Semantic Scholar / Open Corpus
        if "semanticscholar" in active_sources:
            console.print("\n[bold yellow]>>> Harvesting Semantic Scholar & Open Corpus (Chemistry & Synthesis)...[/bold yellow]")
            self.s2_collector.harvest(target_count=self.s2_target)
            self.print_status()

        # Run arXiv
        if "arxiv" in active_sources:
            console.print("\n[bold yellow]>>> Harvesting arXiv (cond-mat.supr-con & cond-mat.mtrl-sci)...[/bold yellow]")
            self.arxiv_collector.harvest(target_count=self.arxiv_target)
            self.print_status()

        console.print("\n[bold green]Collection Pipeline Complete![/bold green]")
        self.print_status()


def main() -> None:
    parser = argparse.ArgumentParser(description="10,000 Research Paper Harvester")
    parser.add_argument("--arxiv", type=int, default=4000, help="arXiv paper target (default: 4000)")
    parser.add_argument("--openalex", type=int, default=3000, help="OpenAlex target (default: 3000)")
    parser.add_argument("--s2", type=int, default=3000, help="Semantic Scholar target (default: 3000)")
    parser.add_argument("--sources", type=str, default="openalex,semanticscholar,arxiv", help="Comma-separated sources")
    parser.add_argument("--verify-only", action="store_true", help="Print database counts and exit")

    args = parser.parse_args()

    orchestrator = CollectionOrchestrator(
        arxiv_target=args.arxiv,
        openalex_target=args.openalex,
        s2_target=args.s2,
    )

    if args.verify_only:
        orchestrator.print_status()
        return

    active_sources = [s.strip().lower() for s in args.sources.split(",") if s.strip()]
    orchestrator.run(active_sources=active_sources)


if __name__ == "__main__":
    main()
