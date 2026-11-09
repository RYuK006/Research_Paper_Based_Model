"""arXiv LaTeX Source Downloader and Parser."""

from __future__ import annotations

import gzip
import io
import logging
import re
import tarfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx

from parsers.models import ParsedDocument
from pipeline.models import PaperRecord

logger = logging.getLogger("latex_parser")


class ArxivLatexParser:
    """Downloads arXiv LaTeX source bundles and extracts clean Markdown with equations and tables."""

    def __init__(
        self,
        user_agent: str = "ResearchCollector/1.0 (mailto:RYuK006@users.noreply.github.com)",
        timeout: float = 30.0,
    ):
        self.headers = {"User-Agent": user_agent}
        self.timeout = timeout

    def fetch_source_archive(self, arxiv_id: str) -> Optional[bytes]:
        """Download source bundle from arXiv src endpoint."""
        clean_id = arxiv_id.replace("arxiv:", "").strip()
        url = f"https://arxiv.org/src/{clean_id}"

        with httpx.Client(headers=self.headers, timeout=self.timeout, follow_redirects=True) as client:
            try:
                resp = client.get(url)
                if resp.status_code == 200 and len(resp.content) > 100:
                    return resp.content
                else:
                    logger.warning("arXiv source download returned HTTP %d for %s", resp.status_code, arxiv_id)
            except Exception as e:
                logger.error("Failed to download arXiv source for %s: %s", arxiv_id, e)

        return None

    def extract_tex_files(self, content_bytes: bytes) -> Dict[str, str]:
        """Extract .tex files from tar.gz or gzip compressed buffer."""
        tex_files: Dict[str, str] = {}

        # 1. Try tarfile
        try:
            with tarfile.open(fileobj=io.BytesIO(content_bytes)) as tar:
                for member in tar.getmembers():
                    if member.name.lower().endswith((".tex", ".latex")):
                        extracted = tar.extractfile(member)
                        if extracted:
                            tex_files[member.name] = extracted.read().decode("utf-8", errors="ignore")
                if tex_files:
                    return tex_files
        except Exception:
            pass

        # 2. Try single gzip decompressed tex file
        try:
            decompressed = gzip.decompress(content_bytes)
            text = decompressed.decode("utf-8", errors="ignore")
            if "\\document" in text or "\\section" in text or "\\begin" in text:
                tex_files["main.tex"] = text
                return tex_files
        except Exception:
            pass

        # 3. Raw text check
        try:
            raw_text = content_bytes.decode("utf-8", errors="ignore")
            if "\\document" in raw_text or "\\begin" in raw_text:
                tex_files["main.tex"] = raw_text
                return tex_files
        except Exception:
            pass

        return tex_files

    def _select_main_tex(self, tex_dict: Dict[str, str]) -> str:
        """Identify primary TeX document among extracted files."""
        if not tex_dict:
            return ""

        # Score files by document markers
        best_name = None
        best_score = -1
        for name, text in tex_dict.items():
            score = 0
            if "\\documentclass" in text or "\\documentstyle" in text:
                score += 10
            if "\\begin{document}" in text:
                score += 10
            if "\\title" in text:
                score += 5
            score += min(len(text) // 1000, 5)

            if score > best_score:
                best_score = score
                best_name = name

        return tex_dict[best_name] if best_name else next(iter(tex_dict.values()))

    def parse_tex_to_markdown(self, raw_tex: str) -> Tuple[str, List[str], List[str], Dict[str, str]]:
        """Parse raw LaTeX string into clean Markdown, extracting equations, tables, and sections."""
        # 1. Strip comments while preserving \%
        lines: List[str] = []
        for line in raw_tex.splitlines():
            line_no_comment = re.sub(r"(?<!\\)%.*$", "", line).rstrip()
            if line_no_comment:
                lines.append(line_no_comment)
        tex = "\n".join(lines)

        # 2. Extract equations
        equations: List[str] = []
        eq_patterns = [
            r"\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}",
            r"\\begin\{align\*?\}(.*?)\\end\{align\*?\}",
            r"\\begin\{eqnarray\*?\}(.*?)\\end\{eqnarray\*?\}",
            r"\\\[(.*?)\\\]",
            r"\$\$(.*?)\$\$",
        ]

        for pat in eq_patterns:
            for match in re.finditer(pat, tex, re.DOTALL):
                eq_text = match.group(1).strip()
                if eq_text:
                    equations.append(eq_text)

        # 3. Extract tables
        tables: List[str] = []
        table_pattern = r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}"
        for match in re.finditer(table_pattern, tex, re.DOTALL):
            tbl = match.group(1).strip()
            if tbl:
                tables.append(tbl)

        tabular_pattern = r"\\begin\{tabular\*?\}(.*?)\\end\{tabular\*?\}"
        for match in re.finditer(tabular_pattern, tex, re.DOTALL):
            tbl = match.group(1).strip()
            if tbl and tbl not in "".join(tables):
                tables.append(tbl)

        # 4. Extract sections
        sections: Dict[str, str] = {}
        section_pattern = r"\\section\*?\{([^}]+)\}"
        parts = re.split(section_pattern, tex)
        if len(parts) > 1:
            for i in range(1, len(parts), 2):
                sec_title = parts[i].strip()
                sec_body = parts[i + 1].strip() if (i + 1) < len(parts) else ""
                sections[sec_title] = sec_body

        # 5. Clean LaTeX markup into Markdown
        md = tex

        # Strip preamble
        if "\\begin{document}" in md:
            md = md.split("\\begin{document}", 1)[-1]
        if "\\end{document}" in md:
            md = md.split("\\end{document}", 1)[0]

        # Convert section headers
        md = re.sub(r"\\section\*?\{([^}]+)\}", r"\n\n## \1\n", md)
        md = re.sub(r"\\subsection\*?\{([^}]+)\}", r"\n\n### \1\n", md)
        md = re.sub(r"\\subsubsection\*?\{([^}]+)\}", r"\n\n#### \1\n", md)

        # Clean font styles
        md = re.sub(r"\\textbf\{([^}]+)\}", r"**\1**", md)
        md = re.sub(r"\\textit\{([^}]+)\}", r"*\1*", md)
        md = re.sub(r"\\emph\{([^}]+)\}", r"*\1*", md)
        md = re.sub(r"\\texttt\{([^}]+)\}", r"`\1`", md)

        # Standardize equation blocks
        md = re.sub(r"\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}", r"\n\n$$\n\1\n$$\n\n", md, flags=re.DOTALL)
        md = re.sub(r"\\begin\{align\*?\}(.*?)\\end\{align\*?\}", r"\n\n$$\n\1\n$$\n\n", md, flags=re.DOTALL)
        md = re.sub(r"\\begin\{eqnarray\*?\}(.*?)\\end\{eqnarray\*?\}", r"\n\n$$\n\1\n$$\n\n", md, flags=re.DOTALL)

        # Remove common TeX noise macros
        md = re.sub(r"\\label\{[^}]+\}", "", md)
        md = re.sub(r"\\cite\{([^}]+)\}", r"[\1]", md)
        md = re.sub(r"\\ref\{([^}]+)\}", r"\1", md)
        md = re.sub(r"\\[a-zA-Z]+\*?\{?\}?", "", md)  # generic macros
        md = re.sub(r"\n{3,}", "\n\n", md).strip()

        return md, equations, tables, sections

    def parse(self, paper: PaperRecord) -> Optional[ParsedDocument]:
        """Fetch and parse paper from arXiv LaTeX source."""
        arxiv_id = paper.id.replace("arxiv:", "").strip()
        archive_bytes = self.fetch_source_archive(arxiv_id)
        if not archive_bytes:
            return None

        tex_dict = self.extract_tex_files(archive_bytes)
        if not tex_dict:
            return None

        main_tex = self._select_main_tex(tex_dict)
        if not main_tex:
            return None

        md, eqs, tables, secs = self.parse_tex_to_markdown(main_tex)

        return ParsedDocument(
            paper_id=paper.id,
            title=paper.title,
            authors=paper.authors,
            year=paper.year,
            doi=paper.doi,
            source="arxiv",
            abstract=paper.abstract,
            parser_used="arxiv_latex",
            text_markdown=md,
            equations=eqs,
            tables=tables,
            sections=secs,
        )
