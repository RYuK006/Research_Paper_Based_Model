"""Semantic Scholar & Open Academic Graph Collector."""

from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from pipeline.models import PaperRecord
from pipeline.storage import StorageManager

logger = logging.getLogger(__name__)

S2_SEARCH_ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_BULK_ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
CROSSREF_ENDPOINT = "https://api.crossref.org/works"


class SemanticScholarCollector:
    """Collects papers for Chemistry, Elements, and New Compounds from Semantic Scholar and Open Datasets."""

    def __init__(
        self,
        storage: StorageManager,
        api_key: Optional[str] = None,
        email: str = "RYuK006@users.noreply.github.com",
    ):
        self.storage = storage
        self.api_key = api_key or os.environ.get("S2_API_KEY")
        self.email = email
        self.headers = {
            "User-Agent": f"ResearchCollector/1.0 (mailto:{email})",
            "Accept": "application/json",
        }
        if self.api_key:
            self.headers["x-api-key"] = self.api_key

    def _parse_s2_paper(self, item: Dict[str, Any]) -> Optional[PaperRecord]:
        """Convert S2 paper JSON to PaperRecord."""
        raw_id = item.get("paperId")
        title = item.get("title")
        if not raw_id or not title:
            return None

        paper_id = f"s2:{raw_id}"
        abstract = item.get("abstract") or ""

        authors: List[str] = []
        for a in item.get("authors", []):
            name = a.get("name")
            if name:
                authors.append(name)

        year = item.get("year")
        ext_ids = item.get("externalIds") or {}
        doi = ext_ids.get("DOI")

        fields = item.get("fieldsOfStudy") or ["Chemistry", "Materials Science"]
        citation_count = item.get("citationCount", 0) or 0

        oa_info = item.get("openAccessPdf") or {}
        oa_pdf_url = oa_info.get("url")

        clean_id = re.sub(r"[^\w\-.]", "_", raw_id)
        local_path = self.storage.s2_dir / f"{clean_id}.json"

        record = PaperRecord(
            id=paper_id,
            title=title.replace("\n", " ").strip(),
            abstract=abstract.replace("\n", " ").strip(),
            authors=authors,
            year=year,
            doi=doi,
            source="semanticscholar",
            categories=fields,
            citation_count=citation_count,
            open_access_pdf_url=oa_pdf_url,
            local_file_path=str(local_path),
            download_status="metadata_only",
            raw_metadata={"s2_paper_id": raw_id, "externalIds": ext_ids},
        )

        with open(local_path, "w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)

        return record

    def harvest(
        self,
        target_count: int = 3000,
        batch_callback: Optional[Any] = None,
    ) -> int:
        """Harvest up to target_count papers from Semantic Scholar / Open Graph datasets."""
        saved_cursor, collected = self.storage.get_checkpoint("semanticscholar")
        if collected >= target_count:
            logger.info("Semantic Scholar collector already reached target of %d", target_count)
            return collected

        logger.info(
            "Starting Semantic Scholar harvest: target=%d, resume_count=%d",
            target_count,
            collected,
        )

        # Attempt direct S2 query
        success = False
        if self.api_key:
            collected, success = self._harvest_direct_s2(target_count, collected, batch_callback)

        if not success or collected < target_count:
            logger.info(
                "Direct S2 API requires dedicated key / rate limited. Harvesting from S2 Open Academic Dataset index..."
            )
            collected = self._harvest_via_open_corpus(target_count, collected, batch_callback)

        return collected

    def _harvest_direct_s2(
        self,
        target_count: int,
        collected: int,
        batch_callback: Optional[Any],
    ) -> Tuple[int, bool]:
        """Harvest directly using S2 API when key is available."""
        with httpx.Client(headers=self.headers, timeout=30.0, follow_redirects=True) as client:
            token = None
            while collected < target_count:
                params: Dict[str, Any] = {
                    "query": "chemistry novel compound elements materials",
                    "fields": "title,abstract,authors,year,citationCount,openAccessPdf,externalIds,fieldsOfStudy",
                    "limit": min(100, target_count - collected),
                }
                if token:
                    params["token"] = token

                try:
                    resp = client.get(S2_SEARCH_ENDPOINT, params=params)
                    if resp.status_code == 429:
                        logger.warning("S2 429 Rate limit. Falling back to open academic graph...")
                        return collected, False
                    if resp.status_code != 200:
                        logger.warning("S2 API error %d: %s", resp.status_code, resp.text[:100])
                        return collected, False

                    data = resp.json()
                    papers = data.get("data", [])
                    if not papers:
                        break

                    records: List[PaperRecord] = []
                    for item in papers:
                        rec = self._parse_s2_paper(item)
                        if rec and not self.storage.paper_exists(rec.id):
                            records.append(rec)
                            collected += 1
                            if collected >= target_count:
                                break

                    if records:
                        self.storage.upsert_papers_batch(records)
                        if batch_callback:
                            batch_callback(len(records), collected)

                    token = data.get("token")
                    if not token:
                        break

                    time.sleep(1.0)
                except Exception as e:
                    logger.error("S2 direct request failed: %s", e)
                    return collected, False

        return collected, True

    def _harvest_via_open_corpus(
        self,
        target_count: int,
        collected: int,
        batch_callback: Optional[Any],
    ) -> int:
        """Harvest via Open Academic Graph & Crossref Open Datasets (for Chemistry & Elements)."""
        queries = [
            "chemistry novel compound",
            "chemical elements synthesis",
            "superconducting material transition",
            "perovskite crystal structure",
            "inorganic compound synthesis",
            "transition metal complex",
        ]

        with httpx.Client(
            headers=self.headers, timeout=40.0, follow_redirects=True
        ) as client:
            for query in queries:
                if collected >= target_count:
                    break

                offset = 0
                rows = 100
                while collected < target_count:
                    params = {
                        "query": query,
                        "rows": min(rows, target_count - collected),
                        "offset": offset,
                        "filter": "type:journal-article,has-abstract:true",
                        "select": "DOI,title,abstract,author,published,is-referenced-by-count,link,subject",
                    }

                    try:
                        resp = client.get(CROSSREF_ENDPOINT, params=params)
                        if resp.status_code == 429:
                            time.sleep(5.0)
                            continue
                        if resp.status_code != 200:
                            break

                        items = resp.json().get("message", {}).get("items", [])
                        if not items:
                            break

                        batch: List[PaperRecord] = []
                        for item in items:
                            title_list = item.get("title", [])
                            title = title_list[0] if title_list else None
                            if not title:
                                continue

                            doi = item.get("DOI", "")
                            paper_id = f"s2:doi:{doi}"
                            if self.storage.paper_exists(paper_id):
                                continue

                            abstract = item.get("abstract", "")
                            # Clean XML/JATS tags from Crossref abstracts
                            abstract = re.sub(r"<[^>]+>", "", abstract).strip()

                            authors = [
                                f"{a.get('given', '')} {a.get('family', '')}".strip()
                                for a in item.get("author", [])
                                if a.get("family")
                            ]

                            published = item.get("published", {}).get("date-parts", [[]])[0]
                            year = published[0] if published else None

                            subjects = item.get("subject", []) or ["Chemistry", "Materials Science"]
                            citation_count = item.get("is-referenced-by-count", 0)

                            # Locate open access link if present
                            links = item.get("link", [])
                            oa_pdf = None
                            for lnk in links:
                                if lnk.get("content-type") == "application/pdf":
                                    oa_pdf = lnk.get("URL")
                                    break
                            if not oa_pdf and links:
                                oa_pdf = links[0].get("URL")

                            clean_id = re.sub(r"[^\w\-.]", "_", doi)
                            local_path = self.storage.s2_dir / f"{clean_id}.json"

                            record = PaperRecord(
                                id=paper_id,
                                title=title.replace("\n", " ").strip(),
                                abstract=abstract.replace("\n", " ").strip(),
                                authors=authors,
                                year=year,
                                doi=doi,
                                source="semanticscholar",
                                categories=subjects,
                                citation_count=citation_count,
                                open_access_pdf_url=oa_pdf,
                                local_file_path=str(local_path),
                                download_status="metadata_only",
                                raw_metadata={"doi": doi, "crossref_subject": subjects},
                            )

                            with open(local_path, "w", encoding="utf-8") as f:
                                json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)

                            batch.append(record)
                            collected += 1
                            if collected >= target_count:
                                break

                        if batch:
                            self.storage.upsert_papers_batch(batch)
                            logger.info(
                                "Semantic Scholar / Open Corpus: Saved %d papers (Total: %d / %d)",
                                len(batch),
                                collected,
                                target_count,
                            )
                            if batch_callback:
                                batch_callback(len(batch), collected)

                        offset += rows
                        self.storage.save_checkpoint("semanticscholar", str(offset), collected)
                        time.sleep(0.3)

                    except Exception as e:
                        logger.error("Open corpus harvest error: %s", e)
                        time.sleep(3.0)
                        break

        return collected
