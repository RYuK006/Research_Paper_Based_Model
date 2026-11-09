"""GROBID REST Client and TEI-XML Parser for Scientific Papers."""

from __future__ import annotations

import logging
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx

from parsers.models import ParsedDocument
from pipeline.models import PaperRecord

logger = logging.getLogger("grobid_parser")

DEFAULT_GROBID_HOST = os.environ.get("GROBID_URL", "http://localhost:8070")
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


class GrobidParser:
    """Client for GROBID server to parse full-text scientific PDFs into structured Markdown."""

    def __init__(self, host: str = DEFAULT_GROBID_HOST, timeout: float = 60.0):
        self.host = host.rstrip("/")
        self.timeout = timeout

    def is_alive(self) -> bool:
        """Check if GROBID service is running and accessible."""
        try:
            with httpx.Client(timeout=5.0) as client:
                r = client.get(f"{self.host}/api/isalive")
                return r.status_code == 200
        except Exception:
            return False

    def process_fulltext_pdf(self, pdf_path: str | Path) -> Optional[str]:
        """Send PDF to GROBID /api/processFulltextDocument and return TEI-XML."""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        url = f"{self.host}/api/processFulltextDocument"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                with open(path, "rb") as f:
                    files = {"input": (path.name, f, "application/pdf")}
                    data = {
                        "consolidateHeader": "1",
                        "consolidateCitations": "1",
                        "includeRawAffiliations": "1",
                        "teiCoordinates": ["persName", "figure", "formula", "biblStruct"],
                    }
                    resp = client.post(url, files=files, data=data)
                    if resp.status_code == 200:
                        return resp.text
                    else:
                        logger.warning("GROBID returned HTTP %d: %s", resp.status_code, resp.text[:150])
        except Exception as e:
            logger.error("Error communicating with GROBID at %s: %s", self.host, e)

        return None

    def parse_tei_xml(
        self,
        tei_xml: str,
        paper_id: str = "",
        fallback_record: Optional[PaperRecord] = None,
    ) -> ParsedDocument:
        """Convert GROBID TEI-XML output into a ParsedDocument."""
        root = ET.fromstring(tei_xml)

        # 1. Metadata
        title_elem = root.find(".//tei:titleStmt/tei:title", TEI_NS)
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

        authors: List[str] = []
        for author in root.findall(".//tei:sourceDesc//tei:author", TEI_NS):
            first = author.findtext(".//tei:forename", "", TEI_NS)
            last = author.findtext(".//tei:surname", "", TEI_NS)
            full = f"{first} {last}".strip()
            if full:
                authors.append(full)

        doi_elem = root.find(".//tei:idno[@type='DOI']", TEI_NS)
        doi = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else None

        year = None
        date_elem = root.find(".//tei:publicationStmt//tei:date", TEI_NS)
        if date_elem is not None and date_elem.attrib.get("when"):
            when_val = date_elem.attrib["when"]
            if len(when_val) >= 4 and when_val[:4].isdigit():
                year = int(when_val[:4])

        abstract_elem = root.find(".//tei:profileDesc/tei:abstract", TEI_NS)
        abstract = ""
        if abstract_elem is not None:
            abstract = "".join(abstract_elem.itertext()).strip()

        # Fallback to existing record if GROBID header is missing details
        if fallback_record:
            paper_id = paper_id or fallback_record.id
            title = title or fallback_record.title
            authors = authors or fallback_record.authors
            year = year or fallback_record.year
            doi = doi or fallback_record.doi
            abstract = abstract or fallback_record.abstract

        # 2. Equations
        equations: List[str] = []
        for formula in root.findall(".//tei:formula", TEI_NS):
            eq_text = "".join(formula.itertext()).strip()
            if eq_text:
                equations.append(eq_text)

        # 3. Tables
        tables: List[str] = []
        for table in root.findall(".//tei:figure[@type='table']", TEI_NS):
            tbl_head = table.findtext("tei:head", "", TEI_NS).strip()
            tbl_body = "".join(table.itertext()).strip()
            tables.append(f"### Table: {tbl_head}\n\n{tbl_body}")

        # 4. Sections & Body
        sections: Dict[str, str] = {}
        body_lines: List[str] = []

        for div in root.findall(".//tei:body/tei:div", TEI_NS):
            head_elem = div.find("tei:head", TEI_NS)
            sec_title = head_elem.text.strip() if head_elem is not None and head_elem.text else "Section"
            paras: List[str] = []
            for p in div.findall("tei:p", TEI_NS):
                text = "".join(p.itertext()).strip()
                if text:
                    paras.append(text)
            sec_content = "\n\n".join(paras)
            sections[sec_title] = sec_content
            body_lines.append(f"## {sec_title}\n\n{sec_content}")

        text_markdown = "\n\n".join(body_lines)

        return ParsedDocument(
            paper_id=paper_id,
            title=title,
            authors=authors,
            year=year,
            doi=doi,
            source="grobid",
            abstract=abstract,
            parser_used="grobid",
            text_markdown=text_markdown,
            equations=equations,
            tables=tables,
            sections=sections,
        )

    def parse_pdf(
        self,
        pdf_path: str | Path,
        fallback_record: Optional[PaperRecord] = None,
    ) -> Optional[ParsedDocument]:
        """Process a PDF with GROBID."""
        tei_xml = self.process_fulltext_pdf(pdf_path)
        if not tei_xml:
            return None
        return self.parse_tei_xml(
            tei_xml,
            paper_id=fallback_record.id if fallback_record else Path(pdf_path).stem,
            fallback_record=fallback_record,
        )
