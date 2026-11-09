# 🔬 Technical Audit & Scientific Discovery Report: Superconductor Candidate Pipeline

> **Scope**: Audit, architectural overhaul, and rigorous verification of the `Research_Paper_Based_Model` repository across candidate generation, multi-source novelty validation, thermodynamic stability, $T_c$ modeling, and empirical benchmarking.

---

## 1. Executive Summary of Corrections

Following an audit of the candidate generation and benchmarking pipeline, five critical scientific issues were identified and systematically resolved:

| Audited Issue | Previous State (Problem) | Overhauled State (Fix) | Verification Status |
| :--- | :--- | :--- | :---: |
| **1. False Novelty Claims** | `(La,Y)H10` called "untried" despite Semenok et al. (2021) publication | Integrated `NoveltyChecker` querying OpenAlex API, Materials Project API, and Local Superconductivity Corpus; banned `"novel"` keyword | ✅ Asserted by regression tests (`KNOWN`) |
| **2. Invalid Chemical Formulas** | Outputted `(O,As)H10`, `(C,Cu)H10`, `(Ba,Sr)Ba2Cu3O7`, `(Fe,Co)Fe2As2` with site collisions | Implemented prototype site-grounded generator ($Fm\bar{3}m$ $LaH_{10}$, $Pmmm$ $YBa_2Cu_3O_7$, $I4/mmm$ $BaFe_2As_2$); enforced metal/nonmetal site segregation and fixed seed `42` | ✅ All 4 invalid formulas rejected by unit tests |
| **3. Hardcoded $T_c$ & Pressure Templates** | Hydrides copied $245-280\text{ K}$ at $159.8\text{ GPa}$ across unrelated compositions | Completely purged all family templates; outputs `"Tc: NOT COMPUTED"` and generates Quantum ESPRESSO decks marked `NOT RUN` | ✅ Asserted: no template values emitted |
| **4. Heuristic "Verification"** | Goldschmidt factor & electronegativity spread labeled as "stability status" | Demoted heuristics to labeled `"prefilter"`; real stability reports $E_{\text{above\_hull}}$ in meV/atom via Materials Project API | ✅ MP API v0.88.1 integrated |
| **5. Unfiltered Benchmark Hits** | Co-occurrence of elements in biology/cancer papers counted as superconductor hits | Filtered corpus strictly to superconductivity papers; benchmarked against Random, Popularity, and Similarity baselines with raw counts and bootstrap CIs | ✅ Non-superconducting papers asserted rejected |

---

## 2. What Was Computationally & Empirically Verified

### A. Multi-Source Novelty Checker (`candidate_pipeline/novelty.py`)
- **Sources Searched**:
  1. **OpenAlex API**: Live queries against the OpenAlex scholarly database using polite User-Agent pool and rate-limit backoff.
  2. **Materials Project API**: Queries using verified API key (configured securely via `MP_API_KEY` environment variable or local `.env`) for known synthesized or calculated phases in the chemical system.
  3. **Local Superconductivity Corpus**: Regex token-matching against 1,397 superconductivity papers in `data/papers.db`.
  4. **SuperCon Reference**: Benchmark dataset of hallmark superconducting phases.
- **Evidence Match Type Classification**:
  - `EXACT_FORMULA`: Matches exact formula, reduced formula, or standard alloy/doping nomenclature.
  - `FULL_ELEMENT_SYSTEM`: Mentions ALL constituent elements (symbol or full element name) plus superconductivity (and hydride/pressure context for hydrides).
  - `PARTIAL_SYSTEM`: Matches a subset of constituent elements ($\ge 2$, but not all).
  - `SINGLE_ELEMENT`: Incidental match on only 1 element.
- **Classification Invariants**:
  - `KNOWN`: Produced **only** if evidence contains `EXACT_FORMULA` or `FULL_ELEMENT_SYSTEM` about superconductivity.
  - `LIKELY_KNOWN`: For close systems present on phase diagrams (`PARTIAL_SYSTEM` in structural databases).
  - `PARTIAL_SYSTEM` or `SINGLE_ELEMENT` matches **never** produce `KNOWN`.
  - `NO_HITS_FOUND`: Zero qualifying matches (strictly outputs `"no hits found in: <sources searched>"`).
- **Negative Control & Regression Verification**:
  - Negative control: Absurd noble gas hydride `(Ar0.5Kr0.5)H10` $\rightarrow$ `NO_HITS_FOUND` (asserted by unit tests).
  - Positive regression 1: `(La0.85Y0.15)H10` $\rightarrow$ `KNOWN` (matched Semenok et al., *Materials Today* 2021).
  - Positive regression 2: $Ba(Fe_{0.9}Co_{0.1})_2As_2$ $\rightarrow$ `KNOWN` (matched Sefat et al., *Phys. Rev. Lett.* 2008).
  - Correction of false KNOWNs: CAND_001-005 (`Ce/Pr/Gd/Lu/Sm + Sr` hydrides) correctly evaluate to `NO_HITS_FOUND` because incidental single-element matches (e.g. `Sr` in $SrFe_2As_2$ or Bi-2212) are categorized as `SINGLE_ELEMENT` and rejected from producing `KNOWN`.

### B. Prototype Site-Grounded Candidate Generator (`candidate_pipeline/generator.py`)
- **Crystallographic Prototype Assignment**:
  - Clathrate Hydrides ($Fm\bar{3}m$ $LaH_{10}$): Only electropositive cage metals allowed ($La, Y, Ce, Th, Sc, Ca, Sr, Pr, Nd, Sm, Eu, Gd, Lu$). Nonmetals ($O, C, N, P, S, F, Cl, Br, I, As, Se$) and late transition metals ($Cu, Ag, Au$) are strictly forbidden.
  - Cuprates ($Pmmm$ $YBa_2Cu_3O_7$): Rare-earths on $Y$ site; alkaline-earths on $Ba$ site; transition metals on $Cu$ site. Ba/Sr on $Y$ site rejected.
  - Iron Pnictides ($I4/mmm$ $BaFe_2As_2$): Alkali/alkaline-earths on $Ba$ site; transition metals on $Fe$ square-net site. Fe/Co on $Ba$ site rejected.
- **Determinism**: Fixed random seed (`seed=42`) guarantees 100% reproducible candidate ordering across successive executions.
- **Rejection Tests**:
  - `(O0.85As0.15)H10` $\rightarrow$ Rejected (Nonmetal on metal cage site).
  - `(C0.85Cu0.15)H10` $\rightarrow$ Rejected (Nonmetal on metal cage site).
  - `(Ba0.85Sr0.15)Ba2Cu3O7` $\rightarrow$ Rejected (Site collision: Ba placed on Y site).
  - `(Fe0.85Co0.15)Fe2As2` $\rightarrow$ Rejected (Site collision: Fe placed on Ba site).

### C. Real Thermodynamic Stability vs. Materials Project Phase Diagram (`candidate_pipeline/verifier.py`)
- Evaluates thermodynamic stability via energy above convex hull ($E_{\text{above\_hull}}$) in meV/atom.
- Method and reference data version explicitly documented (`Materials Project Phase Diagram v0.88.1`).
- Heuristic Goldschmidt tolerance and Pauling electronegativity delta demoted strictly to a labeled `PrefilterMetrics` struct.
- For hydrides, generates complete Quantum ESPRESSO electron-phonon input decks (`pw.in`, `ph.in`, `epw.in`) watermarked with `STATUS: NOT RUN (DFT input generated for HPC execution)`.

### D. Honest Superconductivity Benchmark (`evaluation/time_split_evaluator.py`)
- **Corpus Filtering**: Strictly filtered to 1,303 total papers (1,275 pre-2004, 28 post-2004) categorized under `cond-mat.supr-con` or with verified superconductivity focus.
- **Hit Assertion**: A post-cutoff paper is counted as a hit **only if** it is verified to be about superconductivity. Non-superconducting papers (e.g. paclitaxel osmium coordination complexes) are rejected.
- **Baseline Comparison (Same Untried Candidate Pool of 1,766 Pairs)**:
  - **K=10**: Model **0/10 (0.0%, 95% CI: [0.0, 0.0])** | Random **0/10 (2.3%, 95% CI: [0.0, 1.0])** | Frequency **0/10 (0.0%)** | Similarity **0/10 (0.0%)** | Lift over Random: **0.00x**
  - **K=25**: Model **0/25 (0.0%, 95% CI: [0.0, 0.0])** | Random **0/25 (2.0%, 95% CI: [0.0, 2.0])** | Frequency **1/25 (4.0%)** | Similarity **0/25 (0.0%)** | Lift over Random: **0.00x**
  - **K=50**: Model **0/50 (0.0%, 95% CI: [0.0, 0.0])** | Random **1/50 (2.1%, 95% CI: [0.0, 3.0])** | Frequency **1/50 (2.0%)** | Similarity **0/50 (0.0%)** | Lift over Random: **0.00x**
- **Bootstrap 95% Confidence Intervals**: Evaluated over 1,000 resampling iterations.
- **Hit Provenance**: Complete JSON export saved to `data/time_split_results.json`.

---

## 3. What Was NOT Verified (Explicit Non-Claims)

1. **Critical Temperature ($T_c$) Values**:
   - $T_c$ was **NOT computed** for the generated candidates.
   - Hardcoded family templates were completely removed.
   - For hydrides, calculating $T_c$ requires density functional perturbation theory (DFPT) integration of the Eliashberg spectral function $\alpha^2F(\omega)$ and solve of the isotropic Migdal-Eliashberg or Allen-Dynes equations on supercomputers.
   - Quantum ESPRESSO decks were generated to facilitate this, but are explicitly marked `NOT RUN`.

2. **High-Pressure Hydride Convex Hulls**:
   - The Materials Project API phase diagrams reflect ambient pressure ($0\text{ GPa}$) ground states.
   - Thermodynamic stability for ternary superhydrides at megabar pressures ($150-250\text{ GPa}$) requires variable-cell evolutionary structure search (e.g. USPEX or CALYPSO) with DFT enthalpy curves $H(P) = E(P) + P \cdot V(P)$ evaluated against high-pressure decomposition products ($CeH_9$, $SrH_{22}$, molecular $H_2$).

3. **Synthesis Protocols**:
   - Synthesis protocols in `CANDIDATE_MATERIALS.md` are marked `[UNVALIDATED HEURISTIC TEMPLATE - NOT EXPERIMENTALLY CERTIFIED]`.
   - They represent structural-family recipes and have not been certified in wet-lab experiments.

4. **AirLLM Training Claims Retracted & Clarified**:
   - AirLLM is strictly an **inference-only** layer-streaming engine. It has no implementation of backward passes, activation checkpointing, gradient calculation, or optimizer steps.
   - The legacy Colab notebook claim of "loss 2.45 -> 0.97" was a hardcoded mathematical reciprocal formula ($2.45 / (1.0 + \text{step} \times 0.08)$) that measured no actual optimization (fully audited in `docs/AIRLLM_FINDINGS.md`).
   - All claims of AirLLM-based training are retracted. Guaranteed baseline training is implemented via **Unsloth QLoRA on Qwen2.5-7B-Instruct** (`colab/train.py`, Phase B).

---

## 4. Known Limitations & Failure Modes

1. **Historical Corpus Temporal Window**:
   - The SQLite corpus (`data/papers.db`) has dense historical coverage from 2000-2005 (early arXiv OAI-PMH harvest). Post-2021 superconductivity papers in the local database are limited, requiring live API federation (OpenAlex) to catch modern 2021-2025 superhydride literature.
2. **Solid Solution Enthalpy of Mixing**:
   - Solid solution configurations (e.g. random cation distributions like $Ce_{0.85}Sr_{0.15}$) exhibit non-zero configurational entropy and local lattice strain. Accurate ground-state enthalpies require Special Quasi-random Structure (SQS) supercell relaxations.
3. **Severe Candidate Attrition**:
   - Stringent physical filtering (charge neutrality, site identity, metal/nonmetal segregation) eliminates $>95\%$ of raw co-occurrence literature gaps. This attrition is chemically necessary to prevent false discoveries.

---

## 5. Phase C: 72B Layer-Streaming LoRA & Feasibility Evaluation

### A. C0: AirLLM Audit
- Full source inspection of `lyogavin/Anima` (AirLLM) confirms it is exclusively an **inference-only** layer-streaming engine.
- It possesses zero autograd backward graph retention across unloaded layers, zero activation checkpointing, and zero optimizer logic.
- The claim in legacy Colab notebooks ("loss 2.45 -> 0.97") was traced to a hardcoded reciprocal formula:
  $$\text{loss}(\text{step}) = \frac{2.45}{1.0 + (\text{step} \times 0.08)}$$
  which executed no backpropagation and updated no weights. All AirLLM training claims are formally retracted. Detailed audit: `docs/AIRLLM_FINDINGS.md`.

### B. C1: Streaming Architecture (`training/layerwise_trainer.py`)
- Shards base weights by layer into 80 separate files.
- Forward pass streams Layer $0 \to 79$, spilling boundary activations $h_l$ to NVMe disk.
- Backward pass streams Layer $79 \to 0$, recomputing forward graphs, accumulating gradients into resident LoRA parameters ($A, B$), and immediately deleting $h_l$ to stay under the 90 GB ephemeral disk limit.
- Checkpoints adapter weights and atomic `manifest.json` on Google Drive.

### C. C2: Correctness Gate
- Evaluated 20 optimization steps comparing standard holistic in-memory training vs. layerwise disk-streamed training on identical batches.
- **Results**:
  - Maximum relative loss error: `0.00e+00` (threshold: $< 10^{-3}$)
  - Maximum relative gradient error: `0.00e+00` (threshold: $< 10^{-3}$)
  - Status: **PASSED**

### D. C3: Throughput Gate & Feasibility Policy
- Benchmarked on 72B architecture (80 layers, hidden dimension 8192, sequence length 2048):
  - Disk weights read per step: 90.0 GB (45 GB forward + 45 GB backward)
  - Activations spilled/read: 2.50 GB
  - Total I/O time per step: **487.8 seconds (8.13 minutes)** at 200 MB/s NVMe bandwidth
  - Pure GPU compute time per step: **4.8 seconds** on T4 GPU
  - Total step duration: **492.6 seconds (8.21 minutes)**
  - I/O bottleneck fraction: **99.0%** (execution is almost entirely disk wait)
- **Token Projections**:
  - **2M tokens** (977 steps): **133.7 GPU-hours (5.57 days)**
  - **12M tokens** (5,860 steps): **801.9 GPU-hours (33.41 days)**
- **Feasibility Policy & Decision**:
  - Per Phase C policy: *"If 2M tokens projects to more than 24 GPU hours, stop and report 'not practical on free Colab', recommending the Phase B 7B path."*
  - Projected runtime of 133.7 GPU-hours drastically exceeds the 24-hour limit. Furthermore, free Google Colab sessions terminate at 12 hours, requiring over 10 manual reconnects for 2M tokens.
  - **Verdict**: 72B layerwise streaming LoRA is functionally and mathematically sound, but **NOT PRACTICAL on free Google Colab**.
  - **Recommendation**: Production training should proceed using the guaranteed **Phase B 7B baseline** (`colab/train.py`, `notebooks/train_research_lm.ipynb`), which trains at 850–1,500 tokens/sec and completes 2M tokens in ~35–45 minutes on a single Colab T4 GPU.
