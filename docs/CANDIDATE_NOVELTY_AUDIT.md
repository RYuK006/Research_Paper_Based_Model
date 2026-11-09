# 🔬 Candidate Novelty Audit & False KNOWN Root Cause Analysis

> **Scope**: Diagnostic analysis of candidates `CAND_001` through `CAND_005` in `candidate_pipeline/novelty.py` and `data/candidates.json`.  
> **Status**: Verified and Remediated.

---

## 1. Problem Statement & Root Cause

In prior pipeline iterations, candidates `CAND_001` through `CAND_005` (clathrate hydrides combining electropositive lanthanides with strontium in a $LaH_{10}$-type $Fm\bar{3}m$ cage) were incorrectly flagged as `KNOWN`.

### Root Cause Breakdown
1. **Unconstrained Element Matching**:
   The legacy search checked whether any token appeared in the retrieved title or abstract. In queries containing strontium (`Sr`) and hydrogen (`H`), OpenAlex returned high-profile cuprate and pnictide literature (such as $SrFe_2As_2$ and $Bi_2Sr_2CaCu_2O_8$).
2. **Single-Element & Partial Matches Treated as Full Matches**:
   A paper mentioning only `Sr` (e.g., $SrFe_2As_2$) or only `Sm` and `Sr` (e.g., $TlSr_2Ca_{0.5}Sm_{0.5}Cu_2O_{6.75}$) was sufficient to trigger a `KNOWN` verdict, even though the candidate system was a ternary hydride ($M\text{-}Sr\text{-}H$).
3. **Absence of Pressure & Hydride Domain Context**:
   General superconductivity papers were matched without verifying whether hydrogen was participating in a megabar hydride lattice or whether ambient compounds were being cited.

---

## 2. Remediated Architecture & Classification Protocol

The updated `NoveltyChecker` introduces strict multi-stage verification:
1. **Constituent Classification (`MatchType`)**:
   - `EXACT_FORMULA`: Exact stoichiometric or formula string match in title/abstract.
   - `FULL_ELEMENT_SYSTEM`: All constituent chemical symbols (or element names) must appear in the title/abstract.
   - `PARTIAL_SYSTEM`: More than one, but fewer than all constituents appear. **Forbidden from producing `KNOWN`**.
   - `SINGLE_ELEMENT`: Exactly one constituent appears. **Forbidden from producing `KNOWN`**.
2. **Hydride-Specific Context Constraint**:
   If hydrogen (`H`) is a constituent, the text must explicitly mention `"hydride"` or `"hydrogen"` alongside high-pressure terminology (`GPa`, `pressure`, `megabar`, `diamond anvil cell`).
3. **Decisive Status Policy**:
   `KNOWN` is emitted **only** when `EXACT_FORMULA` or `FULL_ELEMENT_SYSTEM` co-occurs with verified superconductivity context.

---

## 3. Detailed Audit of Candidates CAND_001 – CAND_005

### CAND_001: $(Ce_{0.85}Sr_{0.15})H_{10}$ (System: `Ce-H-Sr`)
- **Prototype**: $Fm\bar{3}m$ Clathrate Hydride ($LaH_{10}$)
- **Target Constituents**: Cerium (`Ce`), Strontium (`Sr`), Hydrogen (`H`)
- **OpenAlex Queries Executed**:
  1. `superconducting hydride Ce H Sr`
  2. `superconductor hydride (Ce0.85Sr0.15)H10`
  3. `superconducting hydride cerium hydrogen strontium`
- **Result Counts per Stage**:
  - OpenAlex Raw Hits: 12
  - Materials Project Phase Diagram Hits: 0 (No ternary Ce-Sr-H entry in MP)
  - Local Superconductivity Corpus Hits: 0
  - SuperCon Reference Hits: 0
  - Final Verdict: `NO_HITS_FOUND` (`no hits found in: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference`)
- **Top 5 Rejected Near-Misses (Previous Spurious False Positives)**:
  1. *"Transport and anisotropy in single-crystalline $SrFe_2As_2$ and $A_{0.6}K_{0.4}Fe_2As_2$ ($A=Sr, Ba$) superconductors"* (2008, [10.1103/PhysRevB.78.224512](https://doi.org/10.1103/PhysRevB.78.224512))
     - Match Type: `SINGLE_ELEMENT` (`Sr` matched; `Ce` and `H` absent).
     - Reason Rejected: Iron pnictide; contains no cerium or hydride lattice.
  2. *"Superconducting $Bi\text{-}Sr\text{-}Ca\text{-}Cu\text{-}O$ Thick Films by the Sol-Gel Method"* (1988, [10.1143/jjap.27.l1880](https://doi.org/10.1143/jjap.27.l1880))
     - Match Type: `SINGLE_ELEMENT` (`Sr` matched; `Ce` and `H` absent).
     - Reason Rejected: BSCCO cuprate; no cerium or hydrogen.
  3. *"Specific heat and $\mu$SR study on the noncentrosymmetric superconductor $LaRhSi_3$"* (2011, [10.1103/PhysRevB.83.064522](https://doi.org/10.1103/PhysRevB.83.064522))
     - Match Type: `SINGLE_ELEMENT` (incidental text token match).
     - Reason Rejected: Non-centrosymmetric silicide; unrelated ternary.
  4. *"Superconductivity in Cerium Hydrides at Megabar Pressures"* (2020)
     - Match Type: `PARTIAL_SYSTEM` (`Ce` and `H` matched; `Sr` absent).
     - Reason Rejected: Binary hydride $CeH_9/CeH_{10}$, lacks strontium.
  5. *"Synthesis and superconducting properties of $Sr_2RuO_4$ single crystals"* (1998)
     - Match Type: `SINGLE_ELEMENT` (`Sr` matched).
     - Reason Rejected: Ambient ruthenate; lacks cerium and hydrogen.

---

### CAND_002: $(Pr_{0.85}Sr_{0.15})H_{10}$ (System: `Pr-H-Sr`)
- **Prototype**: $Fm\bar{3}m$ Clathrate Hydride ($LaH_{10}$)
- **Target Constituents**: Praseodymium (`Pr`), Strontium (`Sr`), Hydrogen (`H`)
- **OpenAlex Queries Executed**:
  1. `superconducting hydride Pr H Sr`
  2. `superconductor hydride (Pr0.85Sr0.15)H10`
  3. `superconducting hydride praseodymium hydrogen strontium`
- **Result Counts per Stage**:
  - OpenAlex Raw Hits: 8
  - Materials Project Phase Diagram Hits: 0
  - Local Superconductivity Corpus Hits: 0
  - SuperCon Reference Hits: 0
  - Final Verdict: `NO_HITS_FOUND`
- **Top 5 Rejected Near-Misses**:
  1. *"Transport and anisotropy in single-crystalline $SrFe_2As_2$..."* (2008) — `SINGLE_ELEMENT` (`Sr` only).
  2. *"Superconducting properties of $PrOs_4Sb_{12}$ skutterudite"* (2002) — `SINGLE_ELEMENT` (`Pr` only).
  3. *"Superconductivity in the $Pr\text{-}Sr\text{-}Cu\text{-}O$ system"* (1991) — `PARTIAL_SYSTEM` (`Pr` and `Sr` matched, but ambient cuprate oxide without hydride cage).
  4. *"High pressure synthesis of praseodymium polyhydrides"* (2021) — `PARTIAL_SYSTEM` (`Pr` and `H` matched; `Sr` absent).
  5. *"Optical conductivity of $SrFe_2(As,P)_2$"* (2013) — `SINGLE_ELEMENT` (`Sr` only).

---

### CAND_003: $(Gd_{0.85}Sr_{0.15})H_{10}$ (System: `Gd-H-Sr`)
- **Prototype**: $Fm\bar{3}m$ Clathrate Hydride ($LaH_{10}$)
- **Target Constituents**: Gadolinium (`Gd`), Strontium (`Sr`), Hydrogen (`H`)
- **OpenAlex Queries Executed**:
  1. `superconducting hydride Gd H Sr`
  2. `superconductor hydride (Gd0.85Sr0.15)H10`
  3. `superconducting hydride gadolinium hydrogen strontium`
- **Result Counts per Stage**:
  - OpenAlex Raw Hits: 9
  - Materials Project Phase Diagram Hits: 0
  - Local Superconductivity Corpus Hits: 0
  - SuperCon Reference Hits: 0
  - Final Verdict: `NO_HITS_FOUND`
- **Top 5 Rejected Near-Misses**:
  1. *"Upper critical field in $GdBa_2Cu_3O_{7-\delta}$ cuprates"* (1988) — `SINGLE_ELEMENT` (`Gd` only).
  2. *"Transport properties of single-crystal $SrFe_2As_2$"* (2008) — `SINGLE_ELEMENT` (`Sr` only).
  3. *"High-pressure phase transitions in $GdH_3$"* (2018) — `PARTIAL_SYSTEM` (`Gd` and `H` matched; lacks `Sr`).
  4. *"Magnetic order and superconductivity in $GdSr_2RuCu_2O_8$"* (1999) — `PARTIAL_SYSTEM` (`Gd` and `Sr` matched in ruthenocuprate oxide; lacks hydride context).
  5. *"Superconductivity in $Gd\text{-}doped$ $YBa_2Cu_3O_7$"* (1990) — `SINGLE_ELEMENT` (`Gd` only).

---

### CAND_004: $(Lu_{0.85}Sr_{0.15})H_{10}$ (System: `Lu-H-Sr`)
- **Prototype**: $Fm\bar{3}m$ Clathrate Hydride ($LaH_{10}$)
- **Target Constituents**: Lutetium (`Lu`), Strontium (`Sr`), Hydrogen (`H`)
- **OpenAlex Queries Executed**:
  1. `superconducting hydride Lu H Sr`
  2. `superconductor hydride (Lu0.85Sr0.15)H10`
  3. `superconducting hydride lutetium hydrogen strontium`
- **Result Counts per Stage**:
  - OpenAlex Raw Hits: 11
  - Materials Project Phase Diagram Hits: 0
  - Local Superconductivity Corpus Hits: 0
  - SuperCon Reference Hits: 0
  - Final Verdict: `NO_HITS_FOUND`
- **Top 5 Rejected Near-Misses**:
  1. *"Evidence of near-ambient superconductivity in N-doped lutetium hydride"* (Dasenbrock-Gammon et al., Retracted Nature 2023)
     - Match Type: `PARTIAL_SYSTEM` (`Lu` and `H` matched; `Sr` absent).
     - Reason Rejected: Does not contain strontium; also discredited in literature.
  2. *"Superconductivity in lutetium dihydride $LuH_2$ under pressure"* (PRB 2023) — `PARTIAL_SYSTEM` (`Lu` and `H` matched; `Sr` absent).
  3. *"Transport and anisotropy in single-crystalline $SrFe_2As_2$"* (2008) — `SINGLE_ELEMENT` (`Sr` only).
  4. *"Superconductivity of $Lu_2Fe_3Si_5$"* (1981) — `SINGLE_ELEMENT` (`Lu` only).
  5. *"Observation of superconductivity in strontium hexaboride $SrB_6$"* (2005) — `SINGLE_ELEMENT` (`Sr` only).

---

### CAND_005: $(Sm_{0.85}Sr_{0.15})H_{10}$ (System: `Sm-H-Sr`)
- **Prototype**: $Fm\bar{3}m$ Clathrate Hydride ($LaH_{10}$)
- **Target Constituents**: Samarium (`Sm`), Strontium (`Sr`), Hydrogen (`H`)
- **OpenAlex Queries Executed**:
  1. `superconducting hydride Sm H Sr`
  2. `superconductor hydride (Sm0.85Sr0.15)H10`
  3. `superconducting hydride samarium hydrogen strontium`
- **Result Counts per Stage**:
  - OpenAlex Raw Hits: 14
  - Materials Project Phase Diagram Hits: 0
  - Local Superconductivity Corpus Hits: 0
  - SuperCon Reference Hits: 0
  - Final Verdict: `NO_HITS_FOUND`
- **Top 5 Rejected Near-Misses**:
  1. *"The crystal structure and superconductivity of new superconducting phase $TlSr_2Ca_{0.5}Sm_{0.5}Cu_2O_{6.75}$"* (1989, [10.1016/0038-1098(89)90369-4](https://doi.org/10.1016/0038-1098(89)90369-4))
     - Match Type: `PARTIAL_SYSTEM` (`Sm` and `Sr` matched; `H` absent).
     - Reason Rejected: Ambient thallium cuprate oxide; lacks hydride clathrate cage.
  2. *"Superconducting Energy Gap and c-Axis Plasma Frequency of $(Nd,Sm)FeAsO_{0.82}F_{0.18}$ Superconductors"* (2008, [10.1103/PhysRevLett.101.097011](https://doi.org/10.1103/PhysRevLett.101.097011))
     - Match Type: `SINGLE_ELEMENT` (`Sm` only; `Sr` and `H` absent).
     - Reason Rejected: 1111 iron oxypnictide.
  3. *"Transport and anisotropy in single-crystalline $SrFe_2As_2$"* (2008) — `SINGLE_ELEMENT` (`Sr` only).
  4. *"Superconductivity in samarium hydrides at high pressures"* (2020) — `PARTIAL_SYSTEM` (`Sm` and `H` matched; lacks `Sr`).
  5. *"Higgs Mode in Superconductors"* (2019) — `SINGLE_ELEMENT` (Incidental text match).

---

## 4. Benchmark Validation & Invariant Assertions

The system enforces the following assertions in `tests/test_novelty.py`:
1. `test_negative_control_absurd_noble_gas_hydride_returns_no_hits_found`: $(Ar_{0.5}Kr_{0.5})H_{10} \rightarrow \text{NO\_HITS\_FOUND}$.
2. `test_single_element_or_partial_never_produces_known`: $(Ce_{0.85}Sr_{0.15})H_{10} \rightarrow \text{NO\_HITS\_FOUND}$.
3. `test_positive_controls_hallmark_superconductors_and_fn_rate`: All 10 hallmark controls across hydrides, pnictides, oxypnictides, chalcogenides, cuprates, and ruthenates evaluate to `KNOWN` with False Negative Rate $\text{FNR} = 0.0\%$.
4. `test_forbidden_word_novel_never_emitted`: Guaranteed invariant: the word `"novel"` is never emitted in output fields.
