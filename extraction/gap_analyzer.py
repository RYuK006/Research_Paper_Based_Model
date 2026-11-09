"""
Discovery Gap Analyzer (Layer 2 Idea Generator).
Analyzes the structured materials database to uncover:
1. Untried element combinations that appear in similar compounds but were never co-doped.
2. Cross-family synthesis methods used for one structural family but never applied to another.
3. Authors' stated 'future work' and unconfirmed hypotheses that nobody followed up on.
"""

from __future__ import annotations

import itertools
import json
import logging
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("gap_analyzer")


class DiscoveryGapAnalyzer:
    """
    Uncovers hidden research directions and novel candidate materials
    by querying the structured materials extraction database.
    """

    def __init__(self, db_path: str = "data/papers.db") -> None:
        self.db_path = Path(db_path)

    def _get_records(self) -> List[Dict[str, Any]]:
        """Fetches all structured material rows from SQLite."""
        if not self.db_path.exists():
            return []

        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        try:
            c.execute("""
                SELECT paper_id, doi, year, material, composition, elements_json,
                       structure_type, tc_kelvin, pressure_gpa, synthesis_method,
                       measurement_type, future_work, confidence
                FROM structured_materials
            """)
            rows = c.fetchall()
            records = []
            for r in rows:
                records.append({
                    "paper_id": r["paper_id"],
                    "doi": r["doi"],
                    "year": r["year"],
                    "material": r["material"],
                    "composition": r["composition"],
                    "elements": json.loads(r["elements_json"]) if r["elements_json"] else [],
                    "structure_type": r["structure_type"],
                    "tc_kelvin": r["tc_kelvin"],
                    "pressure_gpa": r["pressure_gpa"],
                    "synthesis_method": r["synthesis_method"],
                    "measurement_type": r["measurement_type"],
                    "future_work": r["future_work"],
                    "confidence": r["confidence"],
                })
            return records
        except sqlite3.OperationalError:
            logger.warning(f"structured_materials table not found in {self.db_path}")
            return []
        finally:
            conn.close()

    def find_untried_element_combinations(
        self,
        family: Optional[str] = None,
        min_element_freq: int = 2,
        top_n: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Discovers element pairs (E1, E2) that frequently appear with common elements
        in known compounds but have NEVER been synthesized together in the corpus.
        """
        records = self._get_records()
        if family:
            records = [r for r in records if family.lower() in r["structure_type"].lower()]

        # Track existing combinations and element frequencies
        tested_pairs: Set[Tuple[str, str]] = set()
        element_counts: Counter[str] = Counter()
        co_occurrence: Dict[str, Set[str]] = defaultdict(set)

        for r in records:
            elems = r["elements"]
            for e in elems:
                element_counts[e] += 1
            for e1, e2 in itertools.combinations(elems, 2):
                pair = tuple(sorted([e1, e2]))
                tested_pairs.add(pair)
                co_occurrence[e1].add(e2)
                co_occurrence[e2].add(e1)

        candidate_elements = [e for e, count in element_counts.items() if count >= min_element_freq]
        untried_candidates = []

        for e1, e2 in itertools.combinations(candidate_elements, 2):
            pair = tuple(sorted([e1, e2]))
            if pair not in tested_pairs:
                # Calculate shared partner elements (Jaccard similarity of neighborhoods)
                shared_partners = co_occurrence[e1].intersection(co_occurrence[e2])
                if shared_partners:
                    score = len(shared_partners) * (element_counts[e1] + element_counts[e2])
                    untried_candidates.append({
                        "element_1": e1,
                        "element_2": e2,
                        "shared_partner_elements": sorted(list(shared_partners)),
                        "shared_partners_count": len(shared_partners),
                        "discovery_score": score,
                        "target_family": family or "General crystal lattice",
                        "rationale": (
                            f"Both {e1} and {e2} frequently co-dope with {', '.join(sorted(list(shared_partners))[:4])} "
                            f"in active studies, but {e1}-{e2} co-doping has zero occurrences in the corpus."
                        ),
                    })

        untried_candidates.sort(key=lambda x: x["discovery_score"], reverse=True)
        return untried_candidates[:top_n]

    def find_cross_family_synthesis_methods(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Identifies synthesis methods widely established in one structural family
        that have never been applied to another related structural family.
        """
        records = self._get_records()
        family_methods: Dict[str, Counter[str]] = defaultdict(Counter)

        for r in records:
            struct = r["structure_type"]
            method = r["synthesis_method"]
            if method != "Standard synthesis" and struct != "Crystalline lattice":
                family_methods[struct][method] += 1

        all_structures = list(family_methods.keys())
        opportunities = []

        for s1, s2 in itertools.permutations(all_structures, 2):
            s1_methods = family_methods[s1]
            s2_methods = family_methods[s2]

            for method, count in s1_methods.items():
                if count >= 2 and s2_methods[method] == 0:
                    score = count * sum(s2_methods.values())
                    opportunities.append({
                        "established_family": s1,
                        "target_family": s2,
                        "synthesis_method": method,
                        "established_papers_count": count,
                        "opportunity_score": score,
                        "hypothesis": (
                            f"Method '{method}' is established in {s1} ({count} papers) "
                            f"but has 0 reported applications in {s2}. Adapting '{method}' to {s2} "
                            f"could unlock higher purity, stabilized metastable phases, or thin-film epitaxial growth."
                        ),
                    })

        opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return opportunities[:top_n]

    def collect_unfollowed_future_work(
        self,
        cutoff_year: int = 2021,
        top_n: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Collects authors' stated future work and hypotheses from pre-cutoff papers
        that were never subsequently followed up in later papers.
        """
        records = self._get_records()
        pre_papers = [r for r in records if r["year"] <= cutoff_year]
        post_papers = [r for r in records if r["year"] > cutoff_year]

        post_corpus_text = " ".join([f"{p['material']} {p['future_work']}" for p in post_papers]).lower()

        unfollowed = []
        for r in pre_papers:
            fw = r["future_work"]
            if len(fw) < 30 or "Further chemical" in fw:
                continue

            # Check if key material or specific dopant was mentioned in post papers
            mat = r["material"].lower()
            is_followed = mat in post_corpus_text and len(mat) > 3

            if not is_followed:
                unfollowed.append({
                    "original_paper_id": r["paper_id"],
                    "year": r["year"],
                    "doi": r["doi"],
                    "material": r["material"],
                    "structure_type": r["structure_type"],
                    "stated_future_work": fw,
                    "status": "UNFOLLOWED_LEAD",
                    "opportunity": (
                        f"Authors in {r['year']} stated: '{fw}'. "
                        f"No subsequent papers in the post-{cutoff_year} corpus pursued this direction."
                    ),
                })

        unfollowed.sort(key=lambda x: x["year"], reverse=True)
        return unfollowed[:top_n]

    def generate_discovery_report(self) -> str:
        """Assembles all three gap analyses into a comprehensive markdown summary."""
        untried = self.find_untried_element_combinations(top_n=5)
        cross_methods = self.find_cross_family_synthesis_methods(top_n=5)
        unfollowed = self.collect_unfollowed_future_work(top_n=5)

        lines = [
            "# 💡 Layer 2: Scientific Discovery Gap Analysis Report",
            "",
            "Generated by analyzing structured extractions across the 10,000 papers database.",
            "",
            "---",
            "",
            "## 1. Untried Element Combinations (High-Probability Discovery)",
            "These element pairs co-occur frequently with shared partner elements in known compounds, but have never been co-doped together:",
            "",
            "| Element 1 | Element 2 | Shared Partners | Target Family | Score |",
            "| :--- | :--- | :--- | :--- | :---: |",
        ]

        for u in untried:
            partners = ", ".join(u["shared_partner_elements"][:4])
            lines.append(f"| **{u['element_1']}** | **{u['element_2']}** | {partners} | {u['target_family']} | {u['discovery_score']} |")

        lines.extend([
            "",
            "---",
            "",
            "## 2. Cross-Family Synthesis Opportunities",
            "Synthesis methods widely proven in one structural family with zero reported applications in another:",
            "",
            "| Established In | Target Family | Synthesis Method | Papers in Est. | Opportunity Hypothesis |",
            "| :--- | :--- | :--- | :---: | :--- |",
        ])

        for c in cross_methods:
            lines.append(f"| **{c['established_family']}** | **{c['target_family']}** | `{c['synthesis_method']}` | {c['established_papers_count']} | {c['hypothesis'][:80]}... |")

        lines.extend([
            "",
            "---",
            "",
            "## 3. Authors' Stated 'Future Work' Nobody Followed Up On",
            "Unconfirmed hypotheses and proposed follow-up experiments from historical papers with no subsequent publications:",
            "",
        ])

        for idx, unf in enumerate(unfollowed, 1):
            lines.append(f"### {idx}. {unf['material']} ({unf['year']}, ID: {unf['original_paper_id']})")
            lines.append(f"- **Structure**: {unf['structure_type']}")
            lines.append(f"- **Stated Future Work**: *\"{unf['stated_future_work']}\"*")
            lines.append(f"- **Discovery Gap**: {unf['opportunity']}")
            lines.append("")

        return "\n".join(lines)


def main() -> None:
    """CLI runner for Discovery Gap Analyzer."""
    analyzer = DiscoveryGapAnalyzer()
    report = analyzer.generate_discovery_report()
    print(report)


if __name__ == "__main__":
    main()
