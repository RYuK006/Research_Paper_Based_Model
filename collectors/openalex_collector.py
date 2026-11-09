"""OpenAlex Collector for Chemistry, Elements, Compounds, and Materials."""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

from pipeline.models import PaperRecord
from pipeline.storage import StorageManager

logger = logging.getLogger(__name__)

OPENALEX_ENDPOINT = "https://api.openalex.org/works"


def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Reconstruct continuous abstract string from OpenAlex inverted index."""
    if not inverted_index:
        return ""
    try:
        word_positions: List[Tuple[int, str]] = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(w for _, w in word_positions)
    except Exception:
        return ""


class OpenAlexCollector:
    """Collects papers on Chemistry, Elements, Compounds, and Materials Science from OpenAlex."""

    def __init__(
        self,
        storage: StorageManager,
        email: str = "RYuK006@users.noreply.github.com",
    ):
        self.storage = storage
        self.headers = {
            "User-Agent": f"ResearchCollector/1.0 (mailto:{email})",
            "Accept": "application/json",
        }

    def _parse_work(self, item: Dict[str, Any]) -> Optional[PaperRecord]:
        """Convert OpenAlex work object to PaperRecord."""
        raw_id = item.get("id", "").split("/")[-1]
        title = item.get("title")
        if not raw_id or not title:
            return None

        paper_id = f"openalex:{raw_id}"
        abstract = reconstruct_abstract(item.get("abstract_inverted_index"))

        authors: List[str] = []
        for auth in item.get("authorships", []):
            author_obj = auth.get("author", {})
            name = author_obj.get("display_name")
            if name:
                authors.append(name)

        year = item.get("publication_year")
        doi = item.get("doi")
        if doi and "doi.org/" in doi:
            doi = doi.split("doi.org/")[-1]

        categories: List[str] = []
        for concept in item.get("concepts", []):
            c_name = concept.get("display_name")
            if c_name:
                categories.append(c_name)

        citation_count = item.get("cited_by_count", 0) or 0

        # Open access URL
        oa = item.get("open_access", {})
        oa_pdf_url = oa.get("oa_url")
        if not oa_pdf_url:
            prim_loc = item.get("primary_location") or {}
            oa_pdf_url = prim_loc.get("pdf_url") or prim_loc.get("landing_page_url")

        clean_id = re.sub(r"[^\w\-.]", "_", raw_id)
        local_path = self.storage.openalex_dir / f"{clean_id}.json"

        record = PaperRecord(
            id=paper_id,
            title=title.replace("\n", " ").strip(),
            abstract=abstract.replace("\n", " ").strip(),
            authors=authors,
            year=year,
            doi=doi,
            source="openalex",
            categories=categories,
            citation_count=citation_count,
            open_access_pdf_url=oa_pdf_url,
            local_file_path=str(local_path),
            download_status="metadata_only",
            raw_metadata={
                "openalex_id": raw_id,
                "concepts": categories[:5],
                "oa_status": oa.get("oa_status"),
            },
        )

        with open(local_path, "w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)

        return record

    def harvest(
        self,
        target_count: int = 3000,
        batch_callback: Optional[Any] = None,
    ) -> int:
        """Harvest up to target_count papers from OpenAlex."""
        saved_cursor, collected = self.storage.get_checkpoint("openalex")
        if collected >= target_count:
            logger.info("OpenAlex collector already reached target of %d", target_count)
            return collected

        # Multi-concept filters for broad chemistry & novel compound discovery
        concept_queries = [
            "concepts.id:C185592680",  # Chemistry
            "concepts.id:C192562407",  # Materials science
            "concepts.id:C2779777834", # Superconductor
        ]

        logger.info(
            "Starting OpenAlex harvest: target=%d, resume_count=%d",
            target_count,
            collected,
        )

        with httpx.Client(
            headers=self.headers, timeout=40.0, follow_redirects=True
        ) as client:
            per_page = 100
            for concept_filter in concept_queries:
                if collected >= target_count:
                    break

                filter_str = f"{concept_filter},has_abstract:true,has_fulltext:true"
                page = 1
                max_pages = 50

                while collected < target_count and page <= max_pages:
                    params = {
                        "filter": filter_str,
                        "per_page": per_page,
                        "page": page,
                        "select": "id,title,publication_year,abstract_inverted_index,authorships,concepts,cited_by_count,open_access,doi,primary_location",
                    }

                    try:
                        resp = client.get(OPENALEX_ENDPOINT, params=params)
                        if resp.status_code == 429:
                            logger.warning("OpenAlex 429 rate limit. Backing off 3 seconds...")
                            time.sleep(3.0)
                            continue

                        if resp.status_code != 200:
                            logger.error(
                                "OpenAlex API returned %d: %s",
                                resp.status_code,
                                resp.text[:200],
                            )
                            break

                        data = resp.json()
                        results = data.get("results", [])
                        if not results:
                            break

                        new_records: List[PaperRecord] = []
                        for item in results:
                            paper = self._parse_work(item)
                            if paper and not self.storage.paper_exists(paper.id):
                                new_records.append(paper)
                                collected += 1
                                if collected >= target_count:
                                    break

                        if new_records:
                            self.storage.upsert_papers_batch(new_records)
                            logger.info(
                                "Saved %d OpenAlex papers (Total: %d / %d)",
                                len(new_records),
                                collected,
                                target_count,
                            )
                            if batch_callback:
                                batch_callback(len(new_records), collected)

                        page += 1
                        self.storage.save_checkpoint("openalex", f"{concept_filter}:{page}", collected)
                        time.sleep(0.1)

                    except Exception as e:
                        logger.error("Error during OpenAlex harvest: %s", e)
                        time.sleep(2.0)
                        break

        return collected
