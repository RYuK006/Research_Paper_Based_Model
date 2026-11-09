# Empirical Discovery Benchmark Report (Cutoff Year: 2018)

> *Evaluates the Layer 2 Literature-Gap Discovery Model on historical literature (pre-2018) vs. verified post-cutoff experimental discoveries.*

> [!WARNING]
> **TEMPORAL VOLUME IMBALANCE ALERT**: Post-cutoff publication rate (`1417.0` papers/yr) exceeds pre-cutoff publication rate (`247.5` papers/yr) by **`5.73x`** (> 2.0x threshold). Disproportionately accelerated post-cutoff literature volume expands confirmation opportunities.

## 1. Corpus & Methodology
- **Cutoff Year**: `2018`
- **Historical Pre-Cutoff Corpus**: `10,642` papers ($\le 2018$)
- **Future Post-Cutoff Ground Truth**: `11,336` papers ($> 2018$)
- **Publication Rates**: Pre = `247.5` papers/yr | Post = `1417.0` papers/yr (Ratio = `5.73x`)
- **Untried Candidate Pool Size**: `5,584` element pairs (never tested pre-2018)
- **Formula Extraction**: Strict `pymatgen` formula parsing (excluding plain text and English words).
- **Hit Criteria**: Element pair must co-occur within the **same compound formula** in an arXiv `cond-mat.supr-con` or journal paper (excluding Zenodo/theses).
- **Metric Validity**: Random baseline $< 20.0\%$ constraint: PASSED

## 2. Full-Pool Ranking & Discrimination Metrics

| Baseline Method | Full-Pool ROC AUC | Full-Pool Mean Rank | Paired $\Delta$AUC vs Frequency (95% CI) |
| :--- | :---: | :---: | :---: |
| **Model (Layer 2 Graph)** | **`0.9209`** | **`661.3`** | **`[+0.0064, +0.0184]`** |
| **Frequency Baseline** | `0.9086` | `724.0` | *Reference Baseline* |
| **Chemical Similarity** | `0.3791` | `3404.8` | N/A |
| **Uniform Random** | `0.5000` | `2792.5` | N/A |

## 3. Multi-Baseline Comparison Results (Top-K Discovery)

| Metric / Cutoff | Top-10 ($K=10$) | Top-25 ($K=25$) | Top-50 ($K=50$) |
| :--- | :---: | :---: | :---: |
| **Model Hits (Rate)** | **7/10 (70.0%)** | **18/25 (72.0%)** | **32/50 (64.0%)** |
| **Model 95% Wilson CI** | [39.7%, 89.2%] | [52.4%, 85.7%] | [50.1%, 75.9%] |
| **Frequency Baseline** | 4/10 (40.0%) | 13/25 (52.0%) | 27/50 (54.0%) |
| **Frequency 95% Wilson CI** | [16.8%, 68.7%] | [33.5%, 70.0%] | [40.4%, 67.0%] |
| **Paired $\Delta$(Model - Freq) 95% CI** | [+0.0%, +60.0%] | [+0.0%, +44.0%] | [-8.0%, +26.0%] |
| **Random Baseline** | 1/10 (9.0%) | 2/25 (9.3%) | 5/50 (9.6%) |
| **Similarity Baseline** | 0/10 (0.0%) | 1/25 (4.0%) | 1/50 (2.0%) |
| **Lift vs. Random** | **7.79x** | **7.70x** | **6.67x** |
| **Lift vs. Frequency** | 1.75x | 1.38x | 1.19x |

## 4. Verified Discoveries Sample

| Elements | Discovery Paper Title | Year | DOI |
| :--- | :--- | :--- | :--- |
| `As-S` | Magnetic texture modulated superconductivity in superconductor/ferromagnet shells of semiconductor nanowires | 2026 | N/A |
| `B-Co` | A Low Temperature Functioning CoFeB/MgO Based Perpendicular Magnetic Tunnel Junction for Cryogenic Nonvolatile Random Access Memory | 2019 | [10.1063/1.5129553](https://doi.org/10.1063/1.5129553) |
| `B-Se` | AI-accelerated metallized $σ$-bonding screening for superconductor discovery | 2026 | N/A |
| `Co-S` | Temperature-induced band shift in ferromagnetic Weyl semimetal Co3Sn2S2 | 2019 | [10.1103/physrevlett.124.077403](https://doi.org/10.1103/physrevlett.124.077403) |
| `P-Y` | Universal logic circuit for gate-controlled superconductor-based switches operating at liquid-helium temperatures | 2026 | N/A |
| `Ca-N` | Machine-learning Guided Search for Phonon-mediated Superconductivity in Boron and Carbon Compounds | 2024 | [10.1038/s41524-026-01962-w](https://doi.org/10.1038/s41524-026-01962-w) |
| `C-Nb` | Superconductivity and Fermi Surface Nesting in the Candidate Dirac Semimetal NbC | 2020 | [10.1103/physrevb.102.205117](https://doi.org/10.1103/physrevb.102.205117) |
| `In-Sr` | Pressure-induced Superconductivity in Zintl Topological Insulator SrIn2As2 | 2023 | [10.1103/physrevb.108.224510](https://doi.org/10.1103/physrevb.108.224510) |
| `F-Nb` | Monolayer NbF$_4$: a $4d^1$-analogue of cuprates | 2019 | N/A |
| `K-La` | Superconductivity in epitaxially grown LaVO3/KTaO3(111) heterostructures | 2022 | [10.1088/1674-1056/acac1b](https://doi.org/10.1088/1674-1056/acac1b) |
| `Al-Ca` | Phase diagram and superconductivity of Calcium Alanates under pressure | 2023 | [10.1088/1361-648x/acea4c](https://doi.org/10.1088/1361-648x/acea4c) |
| `B-Te` | Complex Magnetic Ordering in Candidate Topological Superconductors | 2025 | N/A |
| `Al-K` | Patterning of superconducting two-dimensional electron gases based on AlO$_x$/KTaO$_3$(111) interfaces | 2022 | N/A |
| `Ir-Ni` | Discovery of the Superconductivity in 3d Element Ni doped IrTe$_2$ | 2020 | N/A |
| `Al-F` | Preparation and evaluation of alexandrite, forsterite, and topaz substrates for the epitaxial growth of rutile oxides | 2026 | [10.1063/5.0312234](https://doi.org/10.1063/5.0312234) |