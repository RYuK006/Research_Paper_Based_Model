"""arXiv Bulk Collector using OAI-PMH and arXiv API."""

from __future__ import annotations

import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import httpx

from pipeline.models import PaperRecord
from pipeline.storage import StorageManager

logger = logging.getLogger(__name__)

OAI_ENDPOINT = "https://export.arxiv.org/oai2"
API_ENDPOINT = "https://export.arxiv.org/api/query"

OAI_NAMESPACES = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "arxiv": "http://arxiv.org/OAI/arXiv/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
}


class ArxivCollector:
    """Collects bulk research papers from arXiv (cond-mat.supr-con & cond-mat.mtrl-sci)."""

    def __init__(
        self,
        storage: StorageManager,
        user_agent: str = "ResearchCollector/1.0 (mailto:RYuK006@users.noreply.github.com)",
        download_pdfs: bool = False,
    ):
        self.storage = storage
        self.download_pdfs = download_pdfs
        self.headers = {"User-Agent": user_agent}
        self.target_categories = {"cond-mat.supr-con", "cond-mat.mtrl-sci"}

    def _parse_arxiv_record(self, record_elem: ET.Element) -> Optional[PaperRecord]:
        """Parse an arXiv OAI XML record into a PaperRecord."""
        header = record_elem.find("oai:header", OAI_NAMESPACES)
        if header is None or header.get("status") == "deleted":
            return None

        metadata = record_elem.find("oai:metadata", OAI_NAMESPACES)
        if metadata is None:
            return None

        arxiv_elem = metadata.find("arxiv:arXiv", OAI_NAMESPACES)
        if arxiv_elem is not None:
            # Full arXiv format
            raw_id = arxiv_elem.findtext("arxiv:id", "", OAI_NAMESPACES).strip()
            title = (
                arxiv_elem.findtext("arxiv:title", "", OAI_NAMESPACES)
                .replace("\n", " ")
                .strip()
            )
            abstract = (
                arxiv_elem.findtext("arxiv:abstract", "", OAI_NAMESPACES)
                .replace("\n", " ")
                .strip()
            )
            categories_str = arxiv_elem.findtext(
                "arxiv:categories", "", OAI_NAMESPACES
            ).strip()
            categories = categories_str.split() if categories_str else []
            doi = arxiv_elem.findtext("arxiv:doi", None, OAI_NAMESPACES)
            if doi:
                doi = doi.strip()

            authors: List[str] = []
            authors_elem = arxiv_elem.find("arxiv:authors", OAI_NAMESPACES)
            if authors_elem is not None:
                for author in authors_elem.findall("arxiv:author", OAI_NAMESPACES):
                    keyname = author.findtext("arxiv:keyname", "", OAI_NAMESPACES)
                    forenames = author.findtext("arxiv:forenames", "", OAI_NAMESPACES)
                    name = f"{forenames} {keyname}".strip() if forenames else keyname
                    if name:
                        authors.append(name)

            created_date = arxiv_elem.findtext("arxiv:created", "", OAI_NAMESPACES)
            year = None
            if created_date and len(created_date) >= 4:
                try:
                    year = int(created_date[:4])
                except ValueError:
                    pass

        else:
            # Fallback to Dublin Core (oai_dc)
            dc_elem = metadata.find("oai_dc:dc", OAI_NAMESPACES)
            if dc_elem is None:
                return None

            raw_id_elem = header.findtext("oai:identifier", "", OAI_NAMESPACES)
            raw_id = raw_id_elem.replace("oai:arXiv.org:", "").strip()
            title = (
                dc_elem.findtext("dc:title", "", OAI_NAMESPACES)
                .replace("\n", " ")
                .strip()
            )
            abstract = (
                dc_elem.findtext("dc:description", "", OAI_NAMESPACES)
                .replace("\n", " ")
                .strip()
            )
            categories = [
                subj.text.strip()
                for subj in dc_elem.findall("dc:subject", OAI_NAMESPACES)
                if subj.text
            ]
            authors = [
                creator.text.strip()
                for creator in dc_elem.findall("dc:creator", OAI_NAMESPACES)
                if creator.text
            ]
            date_str = dc_elem.findtext("dc:date", "", OAI_NAMESPACES)
            year = (
                int(date_str[:4])
                if date_str and len(date_str) >= 4 and date_str[:4].isdigit()
                else None
            )
            doi = None
            for ident in dc_elem.findall("dc:identifier", OAI_NAMESPACES):
                if ident.text and "doi:" in ident.text.lower():
                    doi = ident.text.split("doi:")[-1].strip()

        if not raw_id or not title:
            return None

        # Check relevance to cond-mat.supr-con or cond-mat.mtrl-sci
        is_relevant = any(
            any(
                cat.lower() in c.lower() or c.lower() in cat.lower()
                for cat in self.target_categories
            )
            for c in categories
        )
        # Also check title/abstract keywords for chemistry/superconductivity/materials
        keywords = [
            "superconduct",
            "crystal",
            "compound",
            "material",
            "transition temperature",
            "cuprate",
            "pnictide",
            "hydride",
            "perovskite",
            "chemical",
            "ferromagnet",
        ]
        text_lower = f"{title.lower()} {abstract.lower()}"
        if not is_relevant:
            is_relevant = any(kw in text_lower for kw in keywords)

        if not is_relevant:
            return None

        paper_id = f"arxiv:{raw_id}"
        clean_id = re.sub(r"[^\w\-.]", "_", raw_id)
        pdf_url = f"https://arxiv.org/pdf/{raw_id}.pdf"

        # Save metadata payload file
        local_payload_path = self.storage.arxiv_dir / f"{clean_id}.json"

        record = PaperRecord(
            id=paper_id,
            title=title,
            abstract=abstract,
            authors=authors,
            year=year,
            doi=doi,
            source="arxiv",
            categories=categories,
            citation_count=0,
            open_access_pdf_url=pdf_url,
            local_file_path=str(local_payload_path),
            download_status="metadata_only",
            raw_metadata={"raw_arxiv_id": raw_id, "categories": categories},
        )

        with open(local_payload_path, "w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)

        return record

    def harvest(
        self,
        target_count: int = 4000,
        batch_callback: Optional[Any] = None,
    ) -> int:
        """Harvest up to target_count papers from arXiv."""
        resumption_token, collected = self.storage.get_checkpoint("arxiv")
        if collected >= target_count:
            logger.info("arXiv collector already reached target of %d", target_count)
            return collected

        logger.info(
            "Starting arXiv harvest: target=%d, resume_count=%d",
            target_count,
            collected,
        )

        with httpx.Client(
            headers=self.headers, timeout=60.0, follow_redirects=True
        ) as client:
            token = resumption_token
            # Try specific sets first: cond-mat, physics:cond-mat
            while collected < target_count:
                if token:
                    params = {"verb": "ListRecords", "resumptionToken": token}
                else:
                    params = {
                        "verb": "ListRecords",
                        "metadataPrefix": "arXiv",
                        "set": "physics:cond-mat",
                    }

                try:
                    resp = client.get(OAI_ENDPOINT, params=params)
                    if resp.status_code == 503:
                        retry_after = int(resp.headers.get("Retry-After", 20))
                        logger.warning(
                            "arXiv rate limit (503). Backing off %d seconds...",
                            retry_after,
                        )
                        time.sleep(retry_after)
                        continue

                    if resp.status_code != 200:
                        logger.error(
                            "arXiv OAI returned HTTP %d: %s",
                            resp.status_code,
                            resp.text[:200],
                        )
                        # Fallback to arXiv API
                        break

                    root = ET.fromstring(resp.content)
                    list_records = root.find("oai:ListRecords", OAI_NAMESPACES)
                    if list_records is None:
                        logger.warning("No ListRecords element found in response.")
                        break

                    new_records: List[PaperRecord] = []
                    for rec_elem in list_records.findall(
                        "oai:record", OAI_NAMESPACES
                    ):
                        paper = self._parse_arxiv_record(rec_elem)
                        if paper and not self.storage.paper_exists(paper.id):
                            new_records.append(paper)
                            collected += 1
                            if collected >= target_count:
                                break

                    if new_records:
                        self.storage.upsert_papers_batch(new_records)
                        logger.info(
                            "Saved %d arXiv papers (Total: %d / %d)",
                            len(new_records),
                            collected,
                            target_count,
                        )
                        if batch_callback:
                            batch_callback(len(new_records), collected)

                    token_elem = list_records.find(
                        "oai:resumptionToken", OAI_NAMESPACES
                    )
                    if (
                        token_elem is not None
                        and token_elem.text
                        and token_elem.text.strip()
                    ):
                        token = token_elem.text.strip()
                        self.storage.save_checkpoint("arxiv", token, collected)
                    else:
                        logger.info("arXiv OAI harvest reached end of set.")
                        break

                    # Respect polite crawl rate
                    time.sleep(3.0)

                except Exception as e:
                    logger.error("Error during arXiv harvest: %s", e)
                    time.sleep(5.0)
                    break

            # If still need more, use the arXiv Search API
            if collected < target_count:
                logger.info(
                    "Continuing via arXiv Search API (cond-mat.supr-con OR cond-mat.mtrl-sci)..."
                )
                collected = self._harvest_via_api(
                    client,
                    target_count=target_count,
                    collected=collected,
                    batch_callback=batch_callback,
                )

        return collected

    def _harvest_via_api(
        self,
        client: httpx.Client,
        target_count: int,
        collected: int,
        batch_callback: Optional[Any] = None,
    ) -> int:
        """Fetch papers via the arXiv Query API."""
        start = collected
        batch_size = 100
        queries = [
            "cat:cond-mat.supr-con",
            "cat:cond-mat.mtrl-sci",
            "all:superconductivity AND all:compound",
            "all:chemistry AND all:crystals",
        ]

        atom_ns = {"atom": "http://www.w3.org/2005/Atom"}

        for query in queries:
            if collected >= target_count:
                break

            query_start = 0
            while collected < target_count:
                params = {
                    "search_query": query,
                    "start": query_start,
                    "max_results": batch_size,
                    "sortBy": "submittedDate",
                    "sortOrder": "descending",
                }
                try:
                    resp = client.get(API_ENDPOINT, params=params)
                    if resp.status_code == 503:
                        logger.warning("arXiv API 503 backoff...")
                        time.sleep(15.0)
                        continue
                    if resp.status_code != 200:
                        logger.warning("arXiv API error %d", resp.status_code)
                        break

                    root = ET.fromstring(resp.content)
                    entries = root.findall("atom:entry", atom_ns)
                    if not entries:
                        break

                    batch_records: List[PaperRecord] = []
                    for entry in entries:
                        id_url = entry.findtext("atom:id", "", atom_ns).strip()
                        raw_id = id_url.split("/abs/")[-1].strip()
                        title = (
                            entry.findtext("atom:title", "", atom_ns)
                            .replace("\n", " ")
                            .strip()
                        )
                        abstract = (
                            entry.findtext("atom:summary", "", atom_ns)
                            .replace("\n", " ")
                            .strip()
                        )
                        published = entry.findtext("atom:published", "", atom_ns)
                        year = int(published[:4]) if published and len(published) >= 4 else None

                        authors = [
                            a.findtext("atom:name", "", atom_ns).strip()
                            for a in entry.findall("atom:author", atom_ns)
                            if a.findtext("atom:name", "", atom_ns)
                        ]
                        categories = [
                            c.attrib.get("term", "").strip()
                            for c in entry.findall("atom:category", atom_ns)
                            if c.attrib.get("term")
                        ]

                        doi = None
                        pdf_url = f"https://arxiv.org/pdf/{raw_id}.pdf"
                        for link in entry.findall("atom:link", atom_ns):
                            if link.attrib.get("title") == "doi":
                                doi = link.attrib.get("href", "").replace(
                                    "http://dx.doi.org/", ""
                                )
                            elif link.attrib.get("title") == "pdf":
                                pdf_url = link.attrib.get("href", pdf_url)

                        paper_id = f"arxiv:{raw_id}"
                        if self.storage.paper_exists(paper_id):
                            continue

                        clean_id = re.sub(r"[^\w\-.]", "_", raw_id)
                        local_path = self.storage.arxiv_dir / f"{clean_id}.json"

                        rec = PaperRecord(
                            id=paper_id,
                            title=title,
                            abstract=abstract,
                            authors=authors,
                            year=year,
                            doi=doi,
                            source="arxiv",
                            categories=categories,
                            citation_count=0,
                            open_access_pdf_url=pdf_url,
                            local_file_path=str(local_path),
                            download_status="metadata_only",
                            raw_metadata={"raw_arxiv_id": raw_id, "categories": categories},
                        )

                        with open(local_path, "w", encoding="utf-8") as f:
                            json.dump(rec.to_dict(), f, ensure_ascii=False, indent=2)

                        batch_records.append(rec)
                        collected += 1
                        if collected >= target_count:
                            break

                    if batch_records:
                        self.storage.upsert_papers_batch(batch_records)
                        logger.info(
                            "arXiv API: Saved %d papers (Total: %d / %d)",
                            len(batch_records),
                            collected,
                            target_count,
                        )
                        if batch_callback:
                            batch_callback(len(batch_records), collected)

                    query_start += batch_size
                    time.sleep(3.0)

                except Exception as e:
                    logger.error("arXiv API request error: %s", e)
                    time.sleep(5.0)
                    break

        self.storage.save_checkpoint("arxiv", str(collected), collected)
        return collected
