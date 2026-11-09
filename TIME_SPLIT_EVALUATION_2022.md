# Empirical Discovery Benchmark Report (Cutoff Year: 2022)

> *Evaluates the Layer 2 Literature-Gap Discovery Model on historical literature (pre-2022) vs. verified post-cutoff experimental discoveries.*

> [!WARNING]
> **TEMPORAL VOLUME IMBALANCE ALERT**: Post-cutoff publication rate (`2110.0` papers/yr) exceeds pre-cutoff publication rate (`288.0` papers/yr) by **`7.33x`** (> 2.0x threshold). Disproportionately accelerated post-cutoff literature volume expands confirmation opportunities.

## 1. Corpus & Methodology
- **Cutoff Year**: `2022`
- **Historical Pre-Cutoff Corpus**: `13,538` papers ($\le 2022$)
- **Future Post-Cutoff Ground Truth**: `8,440` papers ($> 2022$)
- **Publication Rates**: Pre = `288.0` papers/yr | Post = `2110.0` papers/yr (Ratio = `7.33x`)
- **Untried Candidate Pool Size**: `5,347` element pairs (never tested pre-2022)
- **Formula Extraction**: Strict `pymatgen` formula parsing (excluding plain text and English words).
- **Hit Criteria**: Element pair must co-occur within the **same compound formula** in an arXiv `cond-mat.supr-con` or journal paper (excluding Zenodo/theses).
- **Metric Validity**: Random baseline $< 20.0\%$ constraint: PASSED

## 2. Full-Pool Ranking & Discrimination Metrics

| Baseline Method | Full-Pool ROC AUC | Full-Pool Mean Rank | Paired $\Delta$AUC vs Frequency (95% CI) |
| :--- | :---: | :---: | :---: |
| **Model (Layer 2 Graph)** | **`0.9329`** | **`482.3`** | **`[+0.0020, +0.0183]`** |
| **Frequency Baseline** | `0.9230` | `532.4` | *Reference Baseline* |
| **Chemical Similarity** | `0.3917` | `3222.3` | N/A |
| **Uniform Random** | `0.5000` | `2674.0` | N/A |

## 3. Multi-Baseline Comparison Results (Top-K Discovery)

| Metric / Cutoff | Top-10 ($K=10$) | Top-25 ($K=25$) | Top-50 ($K=50$) |
| :--- | :---: | :---: | :---: |
| **Model Hits (Rate)** | **5/10 (50.0%)** | **12/25 (48.0%)** | **25/50 (50.0%)** |
| **Model 95% Wilson CI** | [23.7%, 76.3%] | [30.0%, 66.5%] | [36.6%, 63.4%] |
| **Frequency Baseline** | 3/10 (30.0%) | 10/25 (40.0%) | 19/50 (38.0%) |
| **Frequency 95% Wilson CI** | [10.8%, 60.3%] | [23.4%, 59.3%] | [25.9%, 51.9%] |
| **Paired $\Delta$(Model - Freq) 95% CI** | [-10.0%, +60.0%] | [-20.0%, +36.0%] | [-10.0%, +34.0%] |
| **Random Baseline** | 1/10 (5.3%) | 1/25 (5.3%) | 3/50 (5.3%) |
| **Similarity Baseline** | 0/10 (0.0%) | 1/25 (4.0%) | 1/50 (2.0%) |
| **Lift vs. Random** | **9.42x** | **9.00x** | **9.34x** |
| **Lift vs. Frequency** | 1.67x | 1.20x | 1.32x |

## 4. Verified Discoveries Sample

| Elements | Discovery Paper Title | Year | DOI |
| :--- | :--- | :--- | :--- |
| `As-S` | Magnetic texture modulated superconductivity in superconductor/ferromagnet shells of semiconductor nanowires | 2026 | N/A |
| `B-Se` | AI-accelerated metallized $σ$-bonding screening for superconductor discovery | 2026 | N/A |
| `B-Te` | Complex Magnetic Ordering in Candidate Topological Superconductors | 2025 | N/A |
| `Se-Si` | Field-Tunable Anisotropic Fulde-Ferrell Phase in NbSe$_2$/CrSiTe$_3$ Heterostructures | 2025 | N/A |
| `In-Sr` | Pressure-induced Superconductivity in Zintl Topological Insulator SrIn2As2 | 2023 | [10.1103/physrevb.108.224510](https://doi.org/10.1103/physrevb.108.224510) |
| `Nb-P` | Unveiling Intrinsic Triplet Superconductivity in Noncentrosymmetric NbRe through Inverse Spin-Valve Effects | 2025 | N/A |
| `Ca-N` | Machine-learning Guided Search for Phonon-mediated Superconductivity in Boron and Carbon Compounds | 2024 | [10.1038/s41524-026-01962-w](https://doi.org/10.1038/s41524-026-01962-w) |
| `Ni-Ru` | Demonstration of 0-pi transition in Josephson junctions containing unbalanced synthetic antiferromagnets | 2024 | [10.1063/5.0215364](https://doi.org/10.1063/5.0215364) |
| `K-Nb` | Time-reversal symmetry-breaking phenomena in transport study of kagome superconductivity | 2024 | [10.7498/aps.73.20240917](https://doi.org/10.7498/aps.73.20240917) |
| `Al-F` | Preparation and evaluation of alexandrite, forsterite, and topaz substrates for the epitaxial growth of rutile oxides | 2026 | [10.1063/5.0312234](https://doi.org/10.1063/5.0312234) |
| `H-Rh` | First-Principles Study of High-Temperature Superconductivity in X2MH6 Compounds under 20 GPa | 2024 | N/A |
| `Sb-Y` | Metastability and high-Tc superconductivity in A15-type ternary hydride YSbH6 at moderate pressure | 2025 | N/A |
| `C-Te` | Complex Magnetic Ordering in Candidate Topological Superconductors | 2025 | N/A |
| `Al-Ca` | Phase diagram and superconductivity of Calcium Alanates under pressure | 2023 | [10.1088/1361-648x/acea4c](https://doi.org/10.1088/1361-648x/acea4c) |
| `Ir-Sb` | Ir-Sb Binary System: Unveiling Nodeless Unconventional Superconductivity Proximate to Honeycomb-Vacancy Ordering | 2024 | N/A |