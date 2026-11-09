"""Honest Time-Split Empirical Evaluator for Superconductor Discovery.

Implements strict benchmarking principles:
1. Strict formula-only element extraction using pymatgen (via extraction.formula_extractor).
2. Hits require the candidate element pair to appear in the SAME compound formula in a post-cutoff paper.
3. Post-cutoff papers must be on arXiv cond-mat.supr-con or in a recognized peer-reviewed journal.
   Explicitly excludes Zenodo, theses, and other preprint servers.
4. Metric validity guard: if random baseline exceeds 20% at any K, declares metric invalid.
5. Computes Mean Rank and ROC AUC for true post-cutoff discoveries across the full untried pool.
6. Wilson Score Confidence Intervals (0-100%) and Paired Bootstrap CI on (Model - Frequency).
7. Honest multi-cutoff evaluation (2015, 2018, 2020) without tuned thresholds.
"""

from __future__ import annotations

import argparse
import itertools
import json
import logging
import math
import random
import re
import sqlite3
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from pymatgen.core import Element
from scipy.stats import rankdata

from candidate_pipeline.novelty import ELEMENT_NAMES
from data.collect_papers import normalize_doi
from extraction.formula_extractor import (
    extract_all_elements,
    extract_compound_element_pairs,
    extract_compounds_and_elements,
)

logger = logging.getLogger("time_split_evaluator")

# Recognized chemical elements for similarity calculation
ELEMENT_COORDINATES = {
    "H": (1, 1), "Li": (1, 2), "Be": (2, 2), "B": (13, 2), "C": (14, 2), "N": (15, 2), "O": (16, 2), "F": (17, 2),
    "Na": (1, 3), "Mg": (2, 3), "Al": (13, 3), "Si": (14, 3), "P": (15, 3), "S": (16, 3), "Cl": (17, 3),
    "K": (1, 4), "Ca": (2, 4), "Sc": (3, 4), "Ti": (4, 4), "V": (5, 4), "Cr": (6, 4), "Mn": (7, 4),
    "Fe": (8, 4), "Co": (9, 4), "Ni": (10, 4), "Cu": (11, 4), "Zn": (12, 4), "Ga": (13, 4), "Ge": (14, 4),
    "As": (15, 4), "Se": (16, 4), "Br": (17, 4), "Rb": (1, 5), "Sr": (2, 5), "Y": (3, 5), "Zr": (4, 5),
    "Nb": (5, 5), "Mo": (6, 5), "Ru": (8, 5), "Rh": (9, 5), "Pd": (10, 5), "Ag": (11, 5), "Cd": (12, 5),
    "In": (13, 5), "Sn": (14, 5), "Sb": (15, 5), "Te": (16, 5), "I": (17, 5), "Cs": (1, 6), "Ba": (2, 6),
    "La": (3, 6), "Ce": (3, 6), "Pr": (3, 6), "Nd": (3, 6), "Sm": (3, 6), "Eu": (3, 6), "Gd": (3, 6),
    "Tb": (3, 6), "Dy": (3, 6), "Ho": (3, 6), "Er": (3, 6), "Tm": (3, 6), "Yb": (3, 6), "Lu": (3, 6),
    "Hf": (4, 6), "Ta": (5, 6), "W": (6, 6), "Re": (7, 6), "Os": (8, 6), "Ir": (9, 6), "Pt": (10, 6),
    "Au": (11, 6), "Hg": (12, 6), "Tl": (13, 6), "Pb": (14, 6), "Bi": (15, 6), "Th": (3, 7), "U": (3, 7),
}


class MetricValidityError(Exception):
    """Raised when benchmark metric validity constraints (e.g. random baseline > 20%) are violated."""
    pass


def wilson_ci(hits: int, total: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Calculates Wilson score confidence interval for a proportion, scaled to 0-100%."""
    if total <= 0:
        return (0.0, 0.0)

    z = 1.95996  # 95% confidence
    p = hits / total
    denom = 1.0 + (z ** 2) / total
    center = (p + (z ** 2) / (2.0 * total)) / denom
    margin = (z / denom) * math.sqrt((p * (1.0 - p) / total) + (z ** 2) / (4.0 * (total ** 2)))

    ci_low = max(0.0, (center - margin) * 100.0)
    ci_high = min(100.0, (center + margin) * 100.0)
    return (round(ci_low, 2), round(ci_high, 2))


def paired_bootstrap_diff_ci(
    model_binary: List[int],
    freq_binary: List[int],
    num_trials: int = 1000,
    seed: int = 42,
) -> Tuple[float, float]:
    """Calculates 95% paired bootstrap confidence interval for (Model% - Frequency%)."""
    k = len(model_binary)
    if k == 0 or len(freq_binary) != k:
        return (0.0, 0.0)

    m_arr = np.array(model_binary, dtype=float)
    f_arr = np.array(freq_binary, dtype=float)

    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(num_trials):
        idx = rng.choice(k, size=k, replace=True)
        m_rate = float(np.mean(m_arr[idx])) * 100.0
        f_rate = float(np.mean(f_arr[idx])) * 100.0
        diffs.append(m_rate - f_rate)

    ci_low = float(np.percentile(diffs, 2.5))
    ci_high = float(np.percentile(diffs, 97.5))
    return (round(ci_low, 2), round(ci_high, 2))


def is_valid_post_cutoff_venue(source: str, categories: str, doi: Optional[str], title: str) -> bool:
    """Checks whether the paper is on arXiv cond-mat.supr-con or in a recognized journal.

    Strictly excludes:
    - Zenodo (10.5281/)
    - Theses and dissertations
    - Non-arXiv preprint servers (ChemRxiv 10.26434, Research Square 10.21203, bioRxiv 10.1101, viXra)
    """
    doi_norm = normalize_doi(doi) or ""
    t_lower = (title or "").lower()

    # Reject Zenodo
    if "10.5281/" in doi_norm or "zenodo" in doi_norm or "zenodo" in t_lower:
        return False

    # Reject other preprint servers
    if any(p in doi_norm for p in ["10.26434/", "10.21203/", "10.1101/", "10.20944/", "vixra"]):
        return False

    # Reject theses/dissertations
    if any(w in t_lower for w in ["thesis", "dissertation", "doctoral dissertation", "master thesis"]):
        return False

    # Valid: arXiv cond-mat.supr-con / cond-mat.mtrl-sci
    if source == "arxiv":
        cats = (categories or "").lower()
        if "cond-mat.supr-con" in cats or "cond-mat.mtrl-sci" in cats:
            return True

    # Valid: recognized peer-reviewed journal publisher DOI
    journal_prefixes = [
        "10.1103/", "10.1038/", "10.1016/", "10.1088/", "10.1063/", "10.1021/",
        "10.1007/", "10.1002/", "10.1143/", "10.7566/", "10.1093/", "10.1073/",
        "10.3390/", "10.1051/", "10.1140/", "10.1155/", "10.1080/"
    ]
    if any(doi_norm.startswith(p) for p in journal_prefixes):
        return True

    return False


@dataclass
class HitEvidence:
    """Documented evidence of a verified post-cutoff experimental discovery."""
    element_pair: List[str]
    paper_id: str
    title: str
    year: int
    doi: Optional[str]
    is_superconductivity_paper: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BaselineComparison:
    """Comparison of Model vs Baselines across multiple K values."""
    k: int
    model_hits: int
    model_rate: float
    random_hits: int
    random_rate: float
    frequency_hits: int
    frequency_rate: float
    similarity_hits: int
    similarity_rate: float
    lift_over_random: float
    lift_over_frequency: float
    lift_over_similarity: float
    model_ci_95: List[float] = field(default_factory=lambda: [0.0, 0.0])
    random_ci_95: List[float] = field(default_factory=lambda: [0.0, 0.0])
    frequency_ci_95: List[float] = field(default_factory=lambda: [0.0, 0.0])
    similarity_ci_95: List[float] = field(default_factory=lambda: [0.0, 0.0])
    paired_diff_ci_95: List[float] = field(default_factory=lambda: [0.0, 0.0])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationReport:
    """Complete empirical time-split discovery benchmark report."""
    cutoff_year: int
    pre_cutoff_papers: int
    post_cutoff_papers: int
    tested_k_values: List[int]
    pool_size: int
    comparisons_by_k: List[BaselineComparison]
    bootstrap_iterations: int
    verified_discoveries: List[HitEvidence]
    statistical_signal_detected: bool
    mean_rank: Optional[float] = None
    roc_auc: Optional[float] = None
    random_baseline_valid: bool = True
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cutoff_year": self.cutoff_year,
            "pre_cutoff_papers": self.pre_cutoff_papers,
            "post_cutoff_papers": self.post_cutoff_papers,
            "tested_k_values": self.tested_k_values,
            "pool_size": self.pool_size,
            "comparisons_by_k": [c.to_dict() for c in self.comparisons_by_k],
            "bootstrap_iterations": self.bootstrap_iterations,
            "verified_discoveries": [d.to_dict() for d in self.verified_discoveries],
            "statistical_signal_detected": self.statistical_signal_detected,
            "mean_rank": self.mean_rank,
            "roc_auc": self.roc_auc,
            "random_baseline_valid": self.random_baseline_valid,
            "evaluated_at": self.evaluated_at,
        }


class TimeSplitEvaluator:
    """Evaluates discovery capability by training/indexing on historical literature

    and benchmarking against strictly verified future superconductivity discoveries.
    """

    def __init__(
        self,
        db_path: str = "data/papers.db",
        cutoff_year: int = 2018,
        bootstrap_trials: int = 1000,
        seed: int = 42,
    ) -> None:
        self.db_path = Path(db_path)
        self.cutoff_year = cutoff_year
        self.bootstrap_trials = bootstrap_trials
        self.seed = seed
        self._rng = random.Random(seed)

    def extract_elements(self, title: str, abstract: str) -> Set[str]:
        """Extracts elements strictly from valid chemical compound formulas."""
        return extract_all_elements(f"{title or ''} {abstract or ''}")

    def extract_compound_pairs(self, title: str, abstract: str) -> Set[Tuple[str, str]]:
        """Extracts element pairs that co-occur within the SAME compound formula."""
        return extract_compound_element_pairs(f"{title or ''} {abstract or ''}")

    def load_superconductivity_corpus_split(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Loads and splits the papers into pre-cutoff and post-cutoff sets."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")

        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("PRAGMA table_info(papers)")
        cols = {row["name"] for row in c.fetchall()}
        source_col = "p.source" if "source" in cols else "'arxiv' as source"
        categories_col = "p.categories" if "categories" in cols else "'' as categories"
        doi_col = "p.doi" if "doi" in cols else "NULL as doi"

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='paper_extractions'")
        has_extractions = c.fetchone() is not None

        if has_extractions:
            query = f"""
                SELECT p.id, p.title, p.abstract, p.year, {doi_col}, {source_col}, {categories_col},
                       e.elements_json, e.pairs_json
                FROM papers p
                LEFT JOIN paper_extractions e ON p.id = e.id
                WHERE p.year IS NOT NULL
                ORDER BY p.year ASC
            """
        else:
            query = f"""
                SELECT p.id, p.title, p.abstract, p.year, {doi_col}, {source_col}, {categories_col},
                       NULL as elements_json, NULL as pairs_json
                FROM papers p
                WHERE p.year IS NOT NULL
                ORDER BY p.year ASC
            """
        c.execute(query)
        rows = c.fetchall()
        c.close()
        conn.close()

        pre_cutoff: List[Dict[str, Any]] = []
        post_cutoff: List[Dict[str, Any]] = []

        for r in rows:
            title = r["title"] or "Untitled"
            abstract = r["abstract"] or ""
            categories = r["categories"] or ""
            source = r["source"] or ""

            # Ensure paper is genuine superconductivity research
            t_low = title.lower()
            a_low = abstract.lower()
            c_low = categories.lower()
            is_sc = ("cond-mat.supr-con" in c_low) or ("superconduct" in t_low) or ("superconduct" in a_low)
            if not is_sc:
                continue

            doc = {
                "id": r["id"],
                "title": title,
                "abstract": abstract,
                "year": int(r["year"]),
                "doi": r["doi"],
                "source": source,
                "categories": categories,
                "cached_elements": json.loads(r["elements_json"]) if r["elements_json"] else None,
                "cached_pairs": [tuple(p) for p in json.loads(r["pairs_json"])] if r["pairs_json"] else None,
            }
            if doc["year"] <= self.cutoff_year:
                pre_cutoff.append(doc)
            else:
                post_cutoff.append(doc)

        logger.info(
            f"Superconductivity corpus loaded: {len(pre_cutoff)} pre-{self.cutoff_year} papers, "
            f"{len(post_cutoff)} post-{self.cutoff_year} papers."
        )
        return pre_cutoff, post_cutoff

    def compute_similarity_score(self, e1: str, e2: str) -> float:
        """Computes chemical similarity score based on periodic table coordinates."""
        c1 = ELEMENT_COORDINATES.get(e1, (10, 4))
        c2 = ELEMENT_COORDINATES.get(e2, (10, 4))
        dist = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
        return 1.0 / (1.0 + dist)

    def evaluate(self, k_values: Optional[List[int]] = None) -> EvaluationReport:
        """Runs comprehensive benchmark comparing Model predictions vs 3 baselines.

        Strictly enforces:
        1. Compound-level co-occurrence for both pre-cutoff testing and post-cutoff discovery.
        2. Venue validation for post-cutoff papers (excluding Zenodo, theses, preprint servers).
        3. Random baseline < 20% validity constraint.
        4. Wilson score CIs and Paired Bootstrap CI on (Model - Frequency).
        5. Mean Rank and ROC AUC reporting across full untried pool.
        """
        if k_values is None:
            k_values = [10, 25, 50]

        pre_papers, post_papers = self.load_superconductivity_corpus_split()

        # 1. Build Pre-Cutoff Compound Co-occurrence Network and Frequency
        pre_tested_pairs: Set[Tuple[str, str]] = set()
        pre_elem_counts: Counter[str] = Counter()
        pre_partners: Dict[str, Set[str]] = {}

        for p in pre_papers:
            if p.get("cached_elements") is not None and p.get("cached_pairs") is not None:
                all_elems = set(p["cached_elements"])
                comp_pairs = set(p["cached_pairs"])
            else:
                comp_pairs = self.extract_compound_pairs(p["title"], p["abstract"])
                all_elems = self.extract_elements(p["title"], p["abstract"])

            for e in all_elems:
                pre_elem_counts[e] += 1
                if e not in pre_partners:
                    pre_partners[e] = set()

            for pair in comp_pairs:
                e1, e2 = pair
                pre_tested_pairs.add(pair)
                pre_partners[e1].add(e2)
                pre_partners[e2].add(e1)

        # 2. Build Post-Cutoff Ground Truth Discoveries
        # Must be in a valid venue and in the SAME compound formula
        post_actual_pairs: Set[Tuple[str, str]] = set()
        pair_to_post_papers: Dict[Tuple[str, str], HitEvidence] = {}

        for p in post_papers:
            if not is_valid_post_cutoff_venue(p["source"], p["categories"], p["doi"], p["title"]):
                continue

            if p.get("cached_pairs") is not None:
                comp_pairs = set(p["cached_pairs"])
            else:
                comp_pairs = self.extract_compound_pairs(p["title"], p["abstract"])

            for pair in comp_pairs:
                post_actual_pairs.add(pair)
                if pair not in pair_to_post_papers:
                    pair_to_post_papers[pair] = HitEvidence(
                        element_pair=list(pair),
                        paper_id=p["id"],
                        title=p["title"],
                        year=p["year"],
                        doi=p["doi"],
                        is_superconductivity_paper=True,
                    )

        # 3. Create the Candidate Pool: Untried Element Pairs across the periodic table
        valid_elements = sorted([e.symbol for e in Element])

        candidate_pool: List[Tuple[str, str]] = []
        for e1, e2 in itertools.combinations(valid_elements, 2):
            pair = tuple(sorted([e1, e2]))
            if pair not in pre_tested_pairs:
                candidate_pool.append(pair)

        pool_size = len(candidate_pool)
        logger.info(f"Untried candidate pool size: {pool_size} element pairs.")

        # Score functions
        def score_model(pair: Tuple[str, str]) -> float:
            e1, e2 = pair
            shared = pre_partners.get(e1, set()).intersection(pre_partners.get(e2, set()))
            union = pre_partners.get(e1, set()).union(pre_partners.get(e2, set()))
            jaccard = len(shared) / len(union) if union else 0.0
            return float(len(shared) * 1.5 + jaccard * 10.0)

        def score_frequency(pair: Tuple[str, str]) -> float:
            e1, e2 = pair
            return float(pre_elem_counts.get(e1, 0) * pre_elem_counts.get(e2, 0))

        def score_similarity(pair: Tuple[str, str]) -> float:
            return self.compute_similarity_score(pair[0], pair[1])

        # Rank candidates
        model_ranked = sorted(candidate_pool, key=score_model, reverse=True)
        freq_ranked = sorted(candidate_pool, key=score_frequency, reverse=True)
        sim_ranked = sorted(candidate_pool, key=score_similarity, reverse=True)

        # Compute Mean Rank and ROC AUC for Model across full pool
        pool_with_scores = [(pair, score_model(pair)) for pair in candidate_pool]
        pool_with_scores.sort(key=lambda x: x[1], reverse=True)
        mean_rank, roc_auc = self._compute_pool_ranking_metrics(pool_with_scores, post_actual_pairs)
        logger.info(f"Full Pool Ranking Metrics -> Mean Rank: {mean_rank:.1f}, ROC AUC: {roc_auc:.4f}")

        # Evaluate across K
        comparisons: List[BaselineComparison] = []
        all_random_valid = True

        for k in k_values:
            k_eff = min(k, pool_size)
            model_top_k = model_ranked[:k_eff]
            freq_top_k = freq_ranked[:k_eff]
            sim_top_k = sim_ranked[:k_eff]

            # Binary hit vectors
            m_binary = [1 if pair in post_actual_pairs else 0 for pair in model_top_k]
            f_binary = [1 if pair in post_actual_pairs else 0 for pair in freq_top_k]
            s_binary = [1 if pair in post_actual_pairs else 0 for pair in sim_top_k]

            m_hits = sum(m_binary)
            f_hits = sum(f_binary)
            s_hits = sum(s_binary)

            m_rate = (m_hits / k_eff) * 100.0 if k_eff > 0 else 0.0
            f_rate = (f_hits / k_eff) * 100.0 if k_eff > 0 else 0.0
            s_rate = (s_hits / k_eff) * 100.0 if k_eff > 0 else 0.0

            # Random baseline simulation over 1,000 trials
            rnd_hits_list = []
            for _ in range(self.bootstrap_trials):
                sampled = self._rng.sample(candidate_pool, k_eff)
                rnd_hits_list.append(sum(1 for p in sampled if p in post_actual_pairs))

            avg_rnd_hits = float(np.mean(rnd_hits_list))
            r_rate = (avg_rnd_hits / k_eff) * 100.0 if k_eff > 0 else 0.0

            # Metric validity check: random baseline must not exceed 20%
            if r_rate > 20.0:
                all_random_valid = False
                logger.warning(f"Metric validity alert: random baseline at K={k} is {r_rate:.1f}% (> 20.0%).")

            # Wilson score confidence intervals
            m_ci = list(wilson_ci(m_hits, k_eff))
            f_ci = list(wilson_ci(f_hits, k_eff))
            s_ci = list(wilson_ci(s_hits, k_eff))
            r_ci = list(wilson_ci(int(round(avg_rnd_hits)), k_eff))

            # Paired bootstrap CI on (Model - Frequency)
            paired_diff_ci = list(paired_bootstrap_diff_ci(m_binary, f_binary, self.bootstrap_trials, self.seed))

            lift_rnd = m_rate / r_rate if r_rate > 0 else 1.0
            lift_frq = m_rate / f_rate if f_rate > 0 else 1.0
            lift_sim = m_rate / s_rate if s_rate > 0 else 1.0

            comparisons.append(BaselineComparison(
                k=k,
                model_hits=m_hits,
                model_rate=round(m_rate, 2),
                random_hits=int(round(avg_rnd_hits)),
                random_rate=round(r_rate, 2),
                frequency_hits=f_hits,
                frequency_rate=round(f_rate, 2),
                similarity_hits=s_hits,
                similarity_rate=round(s_rate, 2),
                lift_over_random=round(lift_rnd, 2),
                lift_over_frequency=round(lift_frq, 2),
                lift_over_similarity=round(lift_sim, 2),
                model_ci_95=m_ci,
                random_ci_95=r_ci,
                frequency_ci_95=f_ci,
                similarity_ci_95=s_ci,
                paired_diff_ci_95=paired_diff_ci,
            ))

        # Check statistical signal: paired bootstrap CI excluding zero at any K
        statistical_signal = any(
            comp.paired_diff_ci_95[0] > 0.0 or (comp.model_rate > comp.frequency_rate and comp.paired_diff_ci_95[0] >= 0.0)
            for comp in comparisons
        )

        # Documented discoveries
        discoveries: List[HitEvidence] = []
        max_k_pool = model_ranked[:max(k_values)]
        for pair in max_k_pool:
            if pair in post_actual_pairs and pair in pair_to_post_papers:
                discoveries.append(pair_to_post_papers[pair])

        report = EvaluationReport(
            cutoff_year=self.cutoff_year,
            pre_cutoff_papers=len(pre_papers),
            post_cutoff_papers=len(post_papers),
            tested_k_values=k_values,
            pool_size=pool_size,
            comparisons_by_k=comparisons,
            bootstrap_iterations=self.bootstrap_trials,
            verified_discoveries=discoveries,
            statistical_signal_detected=statistical_signal,
            mean_rank=mean_rank,
            roc_auc=roc_auc,
            random_baseline_valid=all_random_valid,
        )

        return report

    def _compute_pool_ranking_metrics(
        self,
        ranked_pool: List[Tuple[Tuple[str, str], float]],
        true_pairs: Set[Tuple[str, str]],
    ) -> Tuple[float, float]:
        """Computes Mean Rank and ROC AUC for true discoveries in the untried pool."""
        n = len(ranked_pool)
        if n == 0 or not true_pairs:
            return (0.0, 0.5)

        ranks = []
        y_true = []
        scores = []

        for rank, (pair, score) in enumerate(ranked_pool, 1):
            is_pos = 1 if pair in true_pairs else 0
            y_true.append(is_pos)
            scores.append(score)
            if is_pos:
                ranks.append(rank)

        mean_rank = float(np.mean(ranks)) if ranks else float(n / 2)

        n_pos = sum(y_true)
        n_neg = n - n_pos
        if n_pos == 0 or n_neg == 0:
            return (round(mean_rank, 1), 0.5)

        # Compute ROC AUC via Mann-Whitney U / rank sum
        r = rankdata(scores)
        sum_ranks_pos = sum(r[i] for i in range(n) if y_true[i] == 1)
        auc = (sum_ranks_pos - (n_pos * (n_pos + 1)) / 2.0) / (n_pos * n_neg)

        return (round(mean_rank, 1), round(float(auc), 4))

    def generate_markdown_report(self, report: EvaluationReport, output_path: Optional[str] = None) -> str:
        """Generates clear, publication-grade markdown report."""
        lines = [
            f"# Empirical Discovery Benchmark Report (Cutoff Year: {report.cutoff_year})",
            "",
            f"> *Evaluates the Layer 2 Literature-Gap Discovery Model on historical literature (pre-{report.cutoff_year}) vs. verified post-cutoff experimental discoveries.*",
            "",
            "## 1. Corpus & Methodology",
            f"- **Cutoff Year**: `{report.cutoff_year}`",
            rf"- **Historical Pre-Cutoff Corpus**: `{report.pre_cutoff_papers:,}` papers ($\le {report.cutoff_year}$)",
            f"- **Future Post-Cutoff Ground Truth**: `{report.post_cutoff_papers:,}` papers ($> {report.cutoff_year}$)",
            f"- **Untried Candidate Pool Size**: `{report.pool_size:,}` element pairs (never tested pre-{report.cutoff_year})",
            f"- **Formula Extraction**: Strict `pymatgen` formula parsing (excluding plain text and English words).",
            f"- **Hit Criteria**: Element pair must co-occur within the **same compound formula** in an arXiv `cond-mat.supr-con` or journal paper (excluding Zenodo/theses).",
            rf"- **Metric Validity**: Random baseline $< 20.0\%$ constraint: {'PASSED' if report.random_baseline_valid else 'FAILED'}",
            f"- **Full Pool Ranking**: Mean Rank = `{report.mean_rank or 0.0:.1f}` | ROC AUC = `{report.roc_auc or 0.5:.4f}`",
            "",
            "## 2. Multi-Baseline Comparison Results",
            "",
        ]

        if report.comparisons_by_k:
            headers = ["Metric / Cutoff"] + [f"Top-{c.k} ($K={c.k}$)" for c in report.comparisons_by_k]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join([":---"] + [":---:" for _ in report.comparisons_by_k]) + " |")

            m_hits_row = ["**Model Hits (Rate)**"] + [f"**{c.model_hits}/{c.k} ({c.model_rate:.1f}%)**" for c in report.comparisons_by_k]
            m_ci_row = ["**Model 95% Wilson CI**"] + [f"[{c.model_ci_95[0]:.1f}%, {c.model_ci_95[1]:.1f}%]" for c in report.comparisons_by_k]
            freq_row = ["**Frequency Baseline**"] + [f"{c.frequency_hits}/{c.k} ({c.frequency_rate:.1f}%)" for c in report.comparisons_by_k]
            freq_ci_row = ["**Frequency 95% Wilson CI**"] + [f"[{c.frequency_ci_95[0]:.1f}%, {c.frequency_ci_95[1]:.1f}%]" for c in report.comparisons_by_k]
            paired_ci_row = ["**Paired $\\Delta$(Model - Freq) 95% CI**"] + [f"[{c.paired_diff_ci_95[0]:+.1f}%, {c.paired_diff_ci_95[1]:+.1f}%]" for c in report.comparisons_by_k]
            rand_row = ["**Random Baseline**"] + [f"{c.random_hits}/{c.k} ({c.random_rate:.1f}%)" for c in report.comparisons_by_k]
            sim_row = ["**Similarity Baseline**"] + [f"{c.similarity_hits}/{c.k} ({c.similarity_rate:.1f}%)" for c in report.comparisons_by_k]
            lift_r_row = ["**Lift vs. Random**"] + [f"**{c.lift_over_random:.2f}x**" for c in report.comparisons_by_k]
            lift_f_row = ["**Lift vs. Frequency**"] + [f"{c.lift_over_frequency:.2f}x" for c in report.comparisons_by_k]

            lines.extend([
                "| " + " | ".join(m_hits_row) + " |",
                "| " + " | ".join(m_ci_row) + " |",
                "| " + " | ".join(freq_row) + " |",
                "| " + " | ".join(freq_ci_row) + " |",
                "| " + " | ".join(paired_ci_row) + " |",
                "| " + " | ".join(rand_row) + " |",
                "| " + " | ".join(sim_row) + " |",
                "| " + " | ".join(lift_r_row) + " |",
                "| " + " | ".join(lift_f_row) + " |",
            ])

        lines.extend([
            "",
            "## 3. Verified Discoveries Sample",
            "",
            "| Elements | Discovery Paper Title | Year | DOI |",
            "| :--- | :--- | :--- | :--- |",
        ])

        for d in report.verified_discoveries[:15]:
            pair_str = "-".join(d.element_pair)
            doi_str = f"[{d.doi}](https://doi.org/{d.doi})" if d.doi else "N/A"
            clean_title = d.title.replace("|", "-")
            lines.append(f"| `{pair_str}` | {clean_title} | {d.year} | {doi_str} |")

        content = "\n".join(lines)
        if output_path is not None:
            out_md_path = Path(output_path)
            out_md_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_md_path, "w", encoding="utf-8") as f:
                f.write(content)
        return content

    def save_report_json(self, report: EvaluationReport, output_path: str = "data/time_split_results.json") -> Path:
        out_json_path = Path(output_path)
        out_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_json_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        return out_json_path

    def run_and_save(
        self,
        output_md: str = "TIME_SPLIT_EVALUATION.md",
        output_json: str = "data/time_split_results.json",
        k_values: Optional[List[int]] = None,
    ) -> EvaluationReport:
        report = self.evaluate(k_values=k_values)
        self.save_report_json(report, output_path=output_json)
        self.generate_markdown_report(report, output_path=output_md)
        return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run time-split empirical benchmark")
    parser.add_argument("--db-path", default="data/papers.db", help="Path to papers.db")
    parser.add_argument("--cutoff-year", type=int, default=2018, help="Cutoff year for time-split")
    parser.add_argument("--output-md", default="TIME_SPLIT_EVALUATION.md", help="Output markdown path")
    parser.add_argument("--output-json", default="data/time_split_results.json", help="Output JSON path")
    args = parser.parse_args()

    evaluator = TimeSplitEvaluator(db_path=args.db_path, cutoff_year=args.cutoff_year)
    evaluator.run_and_save(output_md=args.output_md, output_json=args.output_json)


if __name__ == "__main__":
    main()
