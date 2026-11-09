"""Unit tests for document parsers (arXiv LaTeX, GROBID, and PDF)."""

import unittest
from pathlib import Path

from parsers.grobid_parser import GrobidParser
from parsers.latex_parser import ArxivLatexParser
from parsers.models import ParsedDocument
from parsers.pdf_parser import PDFParser


class TestParsers(unittest.TestCase):
    """Test suite for document parsing and metadata preservation."""

    def test_parsed_document_frontmatter(self):
        """Test YAML frontmatter serialization preserving title, year, authors, DOI."""
        doc = ParsedDocument(
            paper_id="arxiv:2401.0001",
            title="Discovery of Superconducting Hydrides",
            authors=["A. Physicist", "B. Chemist"],
            year=2024,
            doi="10.1038/s41586-024-0001",
            source="arxiv",
            abstract="Study of hydride lattices under high pressure.",
            parser_used="arxiv_latex",
            text_markdown="## Introduction\n\nContent here.",
            equations=["H \\psi = E \\psi"],
            tables=["| Pressure | Tc |\n| --- | --- |\n| 150 GPa | 250 K |"],
        )

        md = doc.to_markdown_with_frontmatter()
        self.assertIn("paper_id: \"arxiv:2401.0001\"", md)
        self.assertIn("title: \"Discovery of Superconducting Hydrides\"", md)
        self.assertIn("doi: \"10.1038/s41586-024-0001\"", md)
        self.assertIn("year: 2024", md)
        self.assertIn("- A. Physicist", md)
        self.assertIn("- B. Chemist", md)
        self.assertIn("equation_count: 1", md)
        self.assertIn("table_count: 1", md)
        self.assertIn("## Introduction", md)

    def test_latex_tex_parsing(self):
        """Test LaTeX parser extracting equations, tables, sections, and font styles."""
        raw_tex = r"""
        \documentclass{article}
        \title{Superconducting Transition in Novel Cuprate Phases}
        \author{Jane Doe}
        \begin{document}
        \section{Introduction}
        High-temperature superconductivity in \textbf{cuprates} remains an active topic.
        \begin{equation}
        H = -t \sum_{\langle i,j \rangle, \sigma} c_{i\sigma}^\dagger c_{j\sigma} + U \sum_i n_{i\uparrow} n_{i\downarrow}
        \end{equation}
        \section{Results}
        We summarize the parameters in Table \ref{tab:params}:
        \begin{table}
        \begin{tabular}{|c|c|}
        \hline
        Compound & Tc (K) \\
        \hline
        YBa2Cu3O7 & 93 \\
        \hline
        \end{tabular}
        \end{table}
        \end{document}
        """

        parser = ArxivLatexParser()
        md, equations, tables, sections = parser.parse_tex_to_markdown(raw_tex)

        self.assertEqual(len(equations), 1)
        self.assertIn(r"c_{i\sigma}^\dagger", equations[0])

        self.assertEqual(len(tables), 1)
        self.assertIn("YBa2Cu3O7", tables[0])

        self.assertIn("Introduction", sections)
        self.assertIn("Results", sections)
        self.assertIn("**cuprates**", md)
        self.assertIn("$$", md)

    def test_pdf_parser_equations_and_tables(self):
        """Test PDF markdown table and equation detection."""
        sample_md = """
        # Results

        The relationship is given by:
        $$
        E = m c^2 + \frac{p^2}{2m}
        $$

        | Element | Superconducting Tc (K) |
        | --- | --- |
        | Niobium | 9.2 |
        | Lead | 7.2 |
        """

        pdf_parser = PDFParser()
        eqs, tbls = pdf_parser.extract_equations_and_tables(sample_md)

        self.assertEqual(len(eqs), 1)
        self.assertIn("E = m c^2", eqs[0])

        self.assertEqual(len(tbls), 1)
        self.assertIn("Niobium", tbls[0])

    def test_grobid_tei_xml_parsing(self):
        """Test GROBID TEI-XML parser extracting metadata, formulas, and tables."""
        tei_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Crystal Growth of Rare-Earth Borides</title>
                    </titleStmt>
                    <publicationStmt>
                        <date when="2023-05-15"/>
                    </publicationStmt>
                    <sourceDesc>
                        <biblStruct>
                            <idno type="DOI">10.1016/j.jcrysgro.2023.01.002</idno>
                            <analytic>
                                <author>
                                    <persName>
                                        <forename>Marie</forename>
                                        <surname>Curie</surname>
                                    </persName>
                                </author>
                            </analytic>
                        </biblStruct>
                    </sourceDesc>
                </fileDesc>
                <profileDesc>
                    <abstract>
                        <p>We present the synthesis of high-purity single crystals.</p>
                    </abstract>
                </profileDesc>
            </teiHeader>
            <text>
                <body>
                    <div>
                        <head>Synthesis Method</head>
                        <p>The floating zone method was applied under argon atmosphere.</p>
                        <formula>\\lambda = \\frac{h}{p}</formula>
                        <figure type="table">
                            <head>Lattice Constants</head>
                            <p>a = 4.15 Angstroms</p>
                        </figure>
                    </div>
                </body>
            </text>
        </TEI>
        """

        parser = GrobidParser()
        doc = parser.parse_tei_xml(tei_xml, paper_id="test:boride_01")

        self.assertEqual(doc.title, "Crystal Growth of Rare-Earth Borides")
        self.assertEqual(doc.year, 2023)
        self.assertEqual(doc.doi, "10.1016/j.jcrysgro.2023.01.002")
        self.assertIn("Marie Curie", doc.authors)
        self.assertEqual(len(doc.equations), 1)
        self.assertIn("\\lambda", doc.equations[0])
        self.assertEqual(len(doc.tables), 1)
        self.assertIn("Synthesis Method", doc.sections)


if __name__ == "__main__":
    unittest.main()
