# Empirical Discovery Benchmark Report (Cutoff Year: 2020)

> *Evaluates the Layer 2 Literature-Gap Discovery Model on historical literature (pre-2020) vs. verified post-cutoff experimental discoveries.*

> [!WARNING]
> **TEMPORAL VOLUME IMBALANCE ALERT**: Post-cutoff publication rate (`1722.8` papers/yr) exceeds pre-cutoff publication rate (`258.7` papers/yr) by **`6.66x`** (> 2.0x threshold). Disproportionately accelerated post-cutoff literature volume expands confirmation opportunities.

## 1. Corpus & Methodology
- **Cutoff Year**: `2020`
- **Historical Pre-Cutoff Corpus**: `11,641` papers ($\le 2020$)
- **Future Post-Cutoff Ground Truth**: `10,337` papers ($> 2020$)
- **Publication Rates**: Pre = `258.7` papers/yr | Post = `1722.8` papers/yr (Ratio = `6.66x`)
- **Untried Candidate Pool Size**: `5,495` element pairs (never tested pre-2020)
- **Formula Extraction**: Strict `pymatgen` formula parsing (excluding plain text and English words).
- **Hit Criteria**: Element pair must co-occur within the **same compound formula** in an arXiv `cond-mat.supr-con` or journal paper (excluding Zenodo/theses).
- **Metric Validity**: Random baseline $< 20.0\%$ constraint: PASSED

## 2. Full-Pool Ranking & Discrimination Metrics

| Baseline Method | Full-Pool ROC AUC | Full-Pool Mean Rank | Paired $\Delta$AUC vs Frequency (95% CI) |
| :--- | :---: | :---: | :---: |
| **Model (Layer 2 Graph)** | **`0.9181`** | **`631.0`** | **`[+0.0028, +0.0163]`** |
| **Frequency Baseline** | `0.9086` | `679.2` | *Reference Baseline* |
| **Chemical Similarity** | `0.3834` | `3338.4` | N/A |
| **Uniform Random** | `0.5000` | `2748.0` | N/A |

## 3. Multi-Baseline Comparison Results (Top-K Discovery)

| Metric / Cutoff | Top-10 ($K=10$) | Top-25 ($K=25$) | Top-50 ($K=50$) |
| :--- | :---: | :---: | :---: |
| **Model Hits (Rate)** | **6/10 (60.0%)** | **14/25 (56.0%)** | **29/50 (58.0%)** |
| **Model 95% Wilson CI** | [31.3%, 83.2%] | [37.1%, 73.3%] | [44.2%, 70.6%] |
| **Frequency Baseline** | 3/10 (30.0%) | 11/25 (44.0%) | 23/50 (46.0%) |
| **Frequency 95% Wilson CI** | [10.8%, 60.3%] | [26.7%, 62.9%] | [33.0%, 59.6%] |
| **Paired $\Delta$(Model - Freq) 95% CI** | [-20.0%, +80.0%] | [-20.0%, +44.0%] | [-8.0%, +34.0%] |
| **Random Baseline** | 1/10 (7.6%) | 2/25 (7.8%) | 4/50 (7.9%) |
| **Similarity Baseline** | 0/10 (0.0%) | 1/25 (4.0%) | 1/50 (2.0%) |
| **Lift vs. Random** | **7.85x** | **7.16x** | **7.33x** |
| **Lift vs. Frequency** | 2.00x | 1.27x | 1.26x |

## 4. Verified Discoveries Sample

| Elements | Discovery Paper Title | Year | DOI |
| :--- | :--- | :--- | :--- |
| `As-S` | Magnetic texture modulated superconductivity in superconductor/ferromagnet shells of semiconductor nanowires | 2026 | N/A |
| `B-Se` | AI-accelerated metallized $σ$-bonding screening for superconductor discovery | 2026 | N/A |
| `B-Te` | Complex Magnetic Ordering in Candidate Topological Superconductors | 2025 | N/A |
| `In-Sr` | Pressure-induced Superconductivity in Zintl Topological Insulator SrIn2As2 | 2023 | [10.1103/physrevb.108.224510](https://doi.org/10.1103/physrevb.108.224510) |
| `Se-Si` | Field-Tunable Anisotropic Fulde-Ferrell Phase in NbSe$_2$/CrSiTe$_3$ Heterostructures | 2025 | N/A |
| `Ca-N` | Machine-learning Guided Search for Phonon-mediated Superconductivity in Boron and Carbon Compounds | 2024 | [10.1038/s41524-026-01962-w](https://doi.org/10.1038/s41524-026-01962-w) |
| `Nb-P` | Unveiling Intrinsic Triplet Superconductivity in Noncentrosymmetric NbRe through Inverse Spin-Valve Effects | 2025 | N/A |
| `La-Te` | Pressure-induced superconductivity in charge-density-wave compound LaTe2-xSbx (x=0 and 0.4) | 2022 | N/A |
| `Al-K` | Patterning of superconducting two-dimensional electron gases based on AlO$_x$/KTaO$_3$(111) interfaces | 2022 | N/A |
| `P-Y` | Universal logic circuit for gate-controlled superconductor-based switches operating at liquid-helium temperatures | 2026 | N/A |
| `Al-F` | Preparation and evaluation of alexandrite, forsterite, and topaz substrates for the epitaxial growth of rutile oxides | 2026 | [10.1063/5.0312234](https://doi.org/10.1063/5.0312234) |
| `As-Mg` | Decoding 122-Type Iron-Based Superconductors: A Comprehensive Simulation of Phase Diagrams and Transition Temperatures | 2023 | N/A |
| `B-Ge` | Tuning superconductivity in nanosecond laser annealed boron doped $Si_{1-x}Ge_{x}$ epilayers | 2024 | N/A |
| `K-La` | Superconductivity in epitaxially grown LaVO3/KTaO3(111) heterostructures | 2022 | [10.1088/1674-1056/acac1b](https://doi.org/10.1088/1674-1056/acac1b) |
| `Al-Ca` | Phase diagram and superconductivity of Calcium Alanates under pressure | 2023 | [10.1088/1361-648x/acea4c](https://doi.org/10.1088/1361-648x/acea4c) |