"""Robust chemical formula parser and element extractor for superconductivity literature.

Enforces strict physical constraints:
1. Extracts elements ONLY from formula-like tokens (e.g. LaNiGa2, YScH8, (Dy1-xErx)Rh3.8Ru0.2B4).
2. Uses pymatgen.core.Composition and Element for validation and normalization.
3. Never matches element symbols that are ordinary words or units (In, As, Be, At, I, K, Pm, Ne in 'Ne FIB').
4. Treats Tc as technetium strictly inside inorganic formulas; never as critical temperature (Tc, T_c, Tc = 39 K).
5. Strictly excludes elements with Z > 94 (transuranic elements beyond Pu).
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from pymatgen.core import Composition, Element

logger = logging.getLogger(__name__)

# Common English words and units that collide with periodic table symbols
STOPWORD_ELEMENTS: Set[str] = {
    "In", "As", "Be", "At", "I", "K", "He", "No", "Am", "Pm", "Ne", "Is",
    "It", "To", "Or", "If", "By", "On", "An", "So", "At", "Us", "Me", "We",
    "Do", "Up", "Go", "My", "La", "Ac"
}

# Standalone acronyms and instrument names common in materials science
COMMON_ACRONYMS: Set[str] = {
    "FIB", "XRD", "BCS", "DFT", "NMR", "TEM", "SEM", "STM", "AFM", "EDS",
    "EDX", "XPS", "SQUID", "PPMS", "MPMS", "ARPES", "DOS", "MIT", "SOC", "QCP",
    "CDW", "SDW", "AFM", "FM", "PM", "HF", "LF", "RF", "DC", "AC", "RMS", "CW",
    "FWHM", "STEM", "EELS", "UPS", "XANES", "EXAFS", "PES", "LEED", "RHEED",
    "SRF", "TDGL", "GL", "MBE", "PLD", "CVD", "MOCVD", "ALD", "RIXS", "XAS",
    "INS", "TAS", "TOF", "VNA", "MW", "LDOS", "TI", "WSM", "DSM", "TMD",
    "2DEG", "2DHG", "SC", "HTS", "YBCO", "BSCCO", "NCCO", "BKBO", "B-T", "H-T",
    "USA", "THE", "AND", "FOR", "NOT", "ALL", "NEW", "ONE", "TWO", "CAN",
    "MAY", "HAD", "HAS", "WAS", "SEE", "FIG", "REF", "SEC", "MIN", "MAX"
}

# Elements with atomic number Z > 94 to exclude
EXCLUDED_Z_ELEMENTS: Set[str] = {e.symbol for e in Element if e.Z > 94}


def sanitize_text_for_formulas(text: str) -> str:
    """Preprocess text to normalize math notation and mask non-chemical symbols."""
    if not text:
        return ""

    # Remove LaTeX subscript/superscript markup: $La_{0.85}Y_{0.15}H_{10}$ -> La0.85Y0.15H10
    cleaned = re.sub(r"[\$\{\}]", "", text)
    cleaned = re.sub(r"\\(?:text|mathrm|mathbf)\{([^}]+)\}", r"\1", cleaned)
    cleaned = re.sub(r"\\(?:delta|Delta|alpha|beta|gamma|chi)", "d", cleaned)
    cleaned = re.sub(r"[_^]", "", cleaned)

    # Mask critical temperature notation Tc / T_c so 'Tc' is not parsed as Technetium
    cleaned = re.sub(
        r"\bT[cC]\b(?:\s*[:=~≈\<\>±]\s*|\s+(?:of|was|is|reached|reaches|up|around|above|below|near|values?|ranging|\()\s*|\s*\d+\.?\d*\s*K\b)",
        " crit_temp ",
        cleaned,
    )
    cleaned = re.sub(r"\bT[cC]\s*[\-\–]\s*values?", " crit_temp ", cleaned)
    cleaned = re.sub(r"\b[Tt]ransition\s+temperature\s+T[cC]\b", " crit_temp ", cleaned)
    cleaned = re.sub(r"\bsuperconducting\s+T[cC]\b", " crit_temp ", cleaned)

    # Mask instrumentation units and phrases like 'Ne FIB'
    cleaned = re.sub(r"\bNe\s+FIB\b", " ion_beam ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bK\s*[\-\–]?\s*band\b", " frequency_band ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bK\s*[\-\–]?\s*edge\b", " absorption_edge ", cleaned, flags=re.IGNORECASE)

    # Mask standalone temperature units like 'at 10 K', '4.2 K'
    cleaned = re.sub(r"(?<=\d)\s*K\b", " kelvin ", cleaned)

    return cleaned


def normalize_formula_for_pymatgen(raw_token: str) -> str:
    """Converts algebraic/doped formula notations into stoichiometric formulas parseable by pymatgen.

    Correctly identifies element boundaries (including 2-letter symbols like Dy, Er, Ca, Fe)
    so stoichiometric variables x, y, z are not confused with Dysprosium or other elements.
    """
    tok = raw_token.strip(".,;:?!'\"~")

    # 1. Handle (1-x) or (2-x) expressions
    tok = re.sub(r"1\s*[\-\–]\s*[xyz]", "0.5", tok)
    tok = re.sub(r"2\s*[\-\–]\s*[xyz]", "1.5", tok)

    # 2. Remove +x, -d, -delta notation
    tok = re.sub(r"[\+\-]\s*(?:[0-9\.]*[xyzd\delta]?|[xyzd\delta])(?![a-zA-Z])", "", tok)

    # 3. Tokenize by element symbols, safely replacing trailing variables x, y, z with numeric proxy
    res: List[str] = []
    i = 0
    n = len(tok)
    while i < n:
        if tok[i].isupper():
            sym = tok[i]
            if i + 1 < n and tok[i + 1].islower():
                two_letter = tok[i:i + 2]
                try:
                    Element(two_letter)
                    sym = two_letter
                    i += 1
                except (ValueError, KeyError):
                    pass
            res.append(sym)
            i += 1
            # Check if immediately followed by an algebraic variable x, y, z
            if i < n and tok[i] in "xyz" and (i + 1 == n or not tok[i + 1].islower()):
                res.append("0.5")
                i += 1
            # Or if immediately followed by a comma or slash in solid solution shorthand e.g. (Ca,Sr)
            elif i < n and tok[i] in ",/":
                res.append("0.5")
                i += 1
        elif tok[i] in ",/":
            i += 1
        else:
            res.append(tok[i])
            i += 1

    return "".join(res)


def extract_compounds_and_elements(text: str) -> List[Dict[str, Any]]:
    """Extracts genuine chemical compounds and their constituent elements from text.

    Returns:
        List of dicts: [{'formula': str, 'elements': Set[str]}]
    """
    if not text:
        return []

    cleaned = sanitize_text_for_formulas(text)
    compounds: List[Dict[str, Any]] = []
    seen_formulas: Set[str] = set()

    token_pattern = re.compile(r"[A-Za-z0-9\(\)\[\]\.\,\-\+\_\/]{2,}")

    for match in token_pattern.finditer(cleaned):
        raw_tok = match.group(0).strip(".,;:?!'\"")
        if not raw_tok or len(raw_tok) < 2:
            continue

        # Skip all-lowercase tokens
        if raw_tok.islower():
            continue

        # English words or word stems have 3 or more consecutive lowercase letters (e.g. "Radio", "Frequency")
        if re.search(r"[a-z]{3,}", raw_tok):
            continue

        stripped_tok = raw_tok.strip("()[]{}")

        # Skip common uppercase acronyms without digits
        if stripped_tok.isupper() and not any(c.isdigit() for c in stripped_tok):
            if stripped_tok in COMMON_ACRONYMS or raw_tok in COMMON_ACRONYMS:
                continue
            if len(stripped_tok) <= 3 and stripped_tok in STOPWORD_ELEMENTS:
                continue

        # Skip single English words colliding with element symbols
        if raw_tok in STOPWORD_ELEMENTS or stripped_tok in STOPWORD_ELEMENTS:
            continue

        # Reject tokens containing masked non-chemical placeholders
        if any(w in raw_tok.lower() for w in ["crit_temp", "ion_beam", "kelvin", "frequency_band"]):
            continue

        # Scan for periodic table elements
        element_candidates = re.findall(r"([A-Z][a-z]?)", raw_tok)
        valid_symbols: List[str] = []
        for s in element_candidates:
            try:
                el = Element(s)
                if el.Z <= 94:
                    valid_symbols.append(s)
            except (ValueError, KeyError):
                pass

        if not valid_symbols:
            continue

        has_digits = any(c.isdigit() for c in raw_tok)

        # Rule: A single element symbol without numbers is an English word/element mention, NOT a compound formula
        unique_symbols = set(valid_symbols)
        if len(unique_symbols) == 1 and not has_digits:
            continue

        # Rule: Technetium (Tc) is only valid if part of a multi-element formula
        if "Tc" in unique_symbols and raw_tok in {"Tc", "TC", "T_c", "tc"}:
            continue

        # Parse formula with pymatgen Composition
        norm_formula = normalize_formula_for_pymatgen(raw_tok)
        parsed_elements: Set[str] = set()

        try:
            comp = Composition(norm_formula)
            # If pymatgen created any DummySpecies (e.g. R, X, radical/ligand placeholders), reject token
            if any(not isinstance(el, Element) for el in comp.elements):
                continue
            for el in comp.elements:
                if el.Z <= 94:
                    parsed_elements.add(str(el))
        except Exception:
            # Strictly require pymatgen validation. If pymatgen fails to parse, reject token.
            pass

        if parsed_elements and raw_tok not in seen_formulas:
            seen_formulas.add(raw_tok)
            compounds.append({
                "formula": raw_tok,
                "elements": parsed_elements,
            })

    return compounds


def extract_all_elements(text: str) -> Set[str]:
    """Returns the set of all chemical elements extracted from valid compounds in text."""
    compounds = extract_compounds_and_elements(text)
    all_elems: Set[str] = set()
    for c in compounds:
        all_elems.update(c["elements"])
    return all_elems


def extract_compound_element_pairs(text: str) -> Set[Tuple[str, str]]:
    """Returns all unique element pairs (E1, E2) that co-occur within the SAME compound formula.

    Pairs are returned as sorted tuples: (min(E1, E2), max(E1, E2)).
    """
    compounds = extract_compounds_and_elements(text)
    pairs: Set[Tuple[str, str]] = set()

    for c in compounds:
        elems = sorted(list(c["elements"]))
        n = len(elems)
        for i in range(n):
            for j in range(i + 1, n):
                pairs.add((elems[i], elems[j]))

    return pairs
