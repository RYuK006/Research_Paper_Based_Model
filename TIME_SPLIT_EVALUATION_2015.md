# Empirical Discovery Benchmark Report (Cutoff Year: 2015)

> *Evaluates the Layer 2 Literature-Gap Discovery Model on historical literature (pre-2015) vs. verified post-cutoff experimental discoveries.*

## 1. Corpus & Methodology
- **Cutoff Year**: `2015`
- **Historical Pre-Cutoff Corpus**: `9,141` papers ($\le 2015$)
- **Future Post-Cutoff Ground Truth**: `12,837` papers ($> 2015$)
- **Untried Candidate Pool Size**: `5,724` element pairs (never tested pre-2015)
- **Formula Extraction**: Strict `pymatgen` formula parsing (excluding plain text and English words).
- **Hit Criteria**: Element pair must co-occur within the **same compound formula** in an arXiv `cond-mat.supr-con` or journal paper (excluding Zenodo/theses).
- **Metric Validity**: Random baseline $< 20.0\%$ constraint: PASSED
- **Full Pool Ranking**: Mean Rank = `772.7` | ROC AUC = `0.9106`

## 2. Multi-Baseline Comparison Results

| Metric / Cutoff | Top-10 ($K=10$) | Top-25 ($K=25$) | Top-50 ($K=50$) |
| :--- | :--- | :--- | :--- |
| **Model Hits (Rate)** | **9/10 (90.0%)** | **19/25 (76.0%)** | **37/50 (74.0%)** |
| **Model 95% Wilson CI** | [59.6%, 98.2%] | [56.6%, 88.5%] | [60.5%, 84.1%] |
| **Frequency Baseline** | 7/10 (70.0%) | 16/25 (64.0%) | 31/50 (62.0%) |
| **Frequency 95% CI** | [39.7%, 89.2%] | [44.5%, 79.8%] | [48.1%, 74.1%] |
| **Paired $\Delta$(Model - Freq) 95% CI** | [+0.0%, +50.0%] | [-8.0%, +36.0%] | [-6.0%, +32.0%] |
| **Random Baseline** | 1/10 (12.1%) | 3/25 (11.6%) | 6/50 (11.7%) |
| **Similarity Baseline** | 0/10 (0.0%) | 1/25 (4.0%) | 1/50 (2.0%) |
| **Lift vs. Random** | **7.46x** | **6.58x** | **6.34x** |
| **Lift vs. Frequency** | 1.29x | 1.19x | 1.19x |

## 3. Verified Discoveries Sample

| Elements | Discovery Paper Title | Year | DOI |
| :--- | :--- | :--- | :--- |
| `B-Co` | A Low Temperature Functioning CoFeB/MgO Based Perpendicular Magnetic Tunnel Junction for Cryogenic Nonvolatile Random Access Memory | 2019 | [10.1063/1.5129553](https://doi.org/10.1063/1.5129553) |
| `As-N` | A New ZrCuSiAs-Type Superconductor: ThFeAsN | 2016 | [10.1021/jacs.6b00236](https://doi.org/10.1021/jacs.6b00236) |
| `As-S` | Magnetic texture modulated superconductivity in superconductor/ferromagnet shells of semiconductor nanowires | 2026 | N/A |
| `Si-Sr` | Microscopic investigation of the weakly correlated noncentrosymmetric superconductor SrAuSi$_3$ | 2018 | [10.1103/physrevb.97.024501](https://doi.org/10.1103/physrevb.97.024501) |
| `As-C` | MiTMoJCo: Microscopic Tunneling Model for Josephson Contacts | 2018 | [10.1016/j.cpc.2019.107091](https://doi.org/10.1016/j.cpc.2019.107091) |
| `Co-S` | Temperature-induced band shift in ferromagnetic Weyl semimetal Co3Sn2S2 | 2019 | [10.1103/physrevlett.124.077403](https://doi.org/10.1103/physrevlett.124.077403) |
| `Cu-K` | Hybrid Crystals of Cuprates and Iron-Based Superconductors | 2016 | [10.1088/1674-1056/25/7/077402](https://doi.org/10.1088/1674-1056/25/7/077402) |
| `O-Pd` | Stabilizing the Tb-based 214 cuprate by partial Pd substitution | 2018 | [10.1557/jmr.2018.102](https://doi.org/10.1557/jmr.2018.102) |
| `P-Y` | Universal logic circuit for gate-controlled superconductor-based switches operating at liquid-helium temperatures | 2026 | N/A |
| `Ca-N` | Machine-learning Guided Search for Phonon-mediated Superconductivity in Boron and Carbon Compounds | 2024 | [10.1038/s41524-026-01962-w](https://doi.org/10.1038/s41524-026-01962-w) |
| `In-Sr` | Pressure-induced Superconductivity in Zintl Topological Insulator SrIn2As2 | 2023 | [10.1103/physrevb.108.224510](https://doi.org/10.1103/physrevb.108.224510) |
| `S-Si` | Room-temperature ferroelectricity in CuInP2S6 ultrathin flakes | 2016 | [10.1038/ncomms12357](https://doi.org/10.1038/ncomms12357) |
| `B-Se` | AI-accelerated metallized $σ$-bonding screening for superconductor discovery | 2026 | N/A |
| `Al-Ca` | Phase diagram and superconductivity of Calcium Alanates under pressure | 2023 | [10.1088/1361-648x/acea4c](https://doi.org/10.1088/1361-648x/acea4c) |
| `B-Ge` | Tuning superconductivity in nanosecond laser annealed boron doped $Si_{1-x}Ge_{x}$ epilayers | 2024 | N/A |