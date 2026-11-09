# Empirical Discovery Benchmark Report (Cutoff Year: 2012)

> *Evaluates the Layer 2 Literature-Gap Discovery Model on historical literature (pre-2012) vs. verified post-cutoff experimental discoveries.*

> [!WARNING]
> **TEMPORAL VOLUME IMBALANCE ALERT**: Post-cutoff publication rate (`1024.0` papers/yr) exceeds pre-cutoff publication rate (`206.5` papers/yr) by **`4.96x`** (> 2.0x threshold). Disproportionately accelerated post-cutoff literature volume expands confirmation opportunities.

## 1. Corpus & Methodology
- **Cutoff Year**: `2012`
- **Historical Pre-Cutoff Corpus**: `7,642` papers ($\le 2012$)
- **Future Post-Cutoff Ground Truth**: `14,336` papers ($> 2012$)
- **Publication Rates**: Pre = `206.5` papers/yr | Post = `1024.0` papers/yr (Ratio = `4.96x`)
- **Untried Candidate Pool Size**: `5,865` element pairs (never tested pre-2012)
- **Formula Extraction**: Strict `pymatgen` formula parsing (excluding plain text and English words).
- **Hit Criteria**: Element pair must co-occur within the **same compound formula** in an arXiv `cond-mat.supr-con` or journal paper (excluding Zenodo/theses).
- **Metric Validity**: Random baseline $< 20.0\%$ constraint: PASSED

## 2. Full-Pool Ranking & Discrimination Metrics

| Baseline Method | Full-Pool ROC AUC | Full-Pool Mean Rank | Paired $\Delta$AUC vs Frequency (95% CI) |
| :--- | :---: | :---: | :---: |
| **Model (Layer 2 Graph)** | **`0.8975`** | **`920.3`** | **`[-0.0153, -0.0012]`** |
| **Frequency Baseline** | `0.9056` | `879.1` | *Reference Baseline* |
| **Chemical Similarity** | `0.3755` | `3563.2` | N/A |
| **Uniform Random** | `0.5000` | `2933.0` | N/A |

## 3. Multi-Baseline Comparison Results (Top-K Discovery)

| Metric / Cutoff | Top-10 ($K=10$) | Top-25 ($K=25$) | Top-50 ($K=50$) |
| :--- | :---: | :---: | :---: |
| **Model Hits (Rate)** | **9/10 (90.0%)** | **22/25 (88.0%)** | **42/50 (84.0%)** |
| **Model 95% Wilson CI** | [59.6%, 98.2%] | [70.0%, 95.8%] | [71.5%, 91.7%] |
| **Frequency Baseline** | 10/10 (100.0%) | 19/25 (76.0%) | 36/50 (72.0%) |
| **Frequency 95% Wilson CI** | [72.2%, 100.0%] | [56.6%, 88.5%] | [58.3%, 82.5%] |
| **Paired $\Delta$(Model - Freq) 95% CI** | [-30.0%, +0.0%] | [-8.0%, +32.0%] | [-4.0%, +28.0%] |
| **Random Baseline** | 1/10 (13.6%) | 3/25 (13.6%) | 7/50 (13.7%) |
| **Similarity Baseline** | 0/10 (0.0%) | 1/25 (4.0%) | 1/50 (2.0%) |
| **Lift vs. Random** | **6.60x** | **6.47x** | **6.11x** |
| **Lift vs. Frequency** | 0.90x | 1.16x | 1.17x |

## 4. Verified Discoveries Sample

| Elements | Discovery Paper Title | Year | DOI |
| :--- | :--- | :--- | :--- |
| `B-Co` | A Low Temperature Functioning CoFeB/MgO Based Perpendicular Magnetic Tunnel Junction for Cryogenic Nonvolatile Random Access Memory | 2019 | [10.1063/1.5129553](https://doi.org/10.1063/1.5129553) |
| `Co-Ni` | Memory Effect and Triplet Pairing Generation in the Superconducting Exchange Biased Co/CoOx/Cu41Ni59/Nb/Cu41Ni59 Layered Heterostructure | 2013 | [10.1063/1.4818266](https://doi.org/10.1063/1.4818266) |
| `B-Ce` | Resonant spin excitations in unconventional heavy fermion superconductors and Kondo lattice compounds | 2014 | [10.1142/9789814704090_0002](https://doi.org/10.1142/9789814704090_0002) |
| `H-Sr` | Two-gap superconducting properties of alkaline-earth intercalated $A_{x}(NH_{3})Fe_{2}Se_{2}$ (A = Ba or Sr) | 2015 | [10.1088/0953-2048/29/3/035005](https://doi.org/10.1088/0953-2048/29/3/035005) |
| `As-N` | A New ZrCuSiAs-Type Superconductor: ThFeAsN | 2016 | [10.1021/jacs.6b00236](https://doi.org/10.1021/jacs.6b00236) |
| `As-C` | MiTMoJCo: Microscopic Tunneling Model for Josephson Contacts | 2018 | [10.1016/j.cpc.2019.107091](https://doi.org/10.1016/j.cpc.2019.107091) |
| `Ba-N` | Two-gap superconducting properties of alkaline-earth intercalated $A_{x}(NH_{3})Fe_{2}Se_{2}$ (A = Ba or Sr) | 2015 | [10.1088/0953-2048/29/3/035005](https://doi.org/10.1088/0953-2048/29/3/035005) |
| `Si-Sr` | Microscopic investigation of the weakly correlated noncentrosymmetric superconductor SrAuSi$_3$ | 2018 | [10.1103/physrevb.97.024501](https://doi.org/10.1103/physrevb.97.024501) |
| `P-Y` | Universal logic circuit for gate-controlled superconductor-based switches operating at liquid-helium temperatures | 2026 | N/A |
| `Ba-S` | Ab initio downfolding study of the iron-based ladder superconductor BaFe$_2$S$_3$ | 2015 | [10.1103/physrevb.92.054515](https://doi.org/10.1103/physrevb.92.054515) |
| `P-Si` | Unfolding the physics of URu2Si2 through Si -> P substitution | 2015 | [10.1038/ncomms10712](https://doi.org/10.1038/ncomms10712) |
| `Ca-N` | Machine-learning Guided Search for Phonon-mediated Superconductivity in Boron and Carbon Compounds | 2024 | [10.1038/s41524-026-01962-w](https://doi.org/10.1038/s41524-026-01962-w) |
| `N-Sr` | Two-gap superconducting properties of alkaline-earth intercalated $A_{x}(NH_{3})Fe_{2}Se_{2}$ (A = Ba or Sr) | 2015 | [10.1088/0953-2048/29/3/035005](https://doi.org/10.1088/0953-2048/29/3/035005) |
| `H-Pt` | On the high-pressure superconducting phase in platinum hydride | 2015 | N/A |
| `Ba-In` | The Josephson current in Fe-based superconducting junctions: theory and experiment | 2013 | [10.1103/physrevb.91.214501](https://doi.org/10.1103/physrevb.91.214501) |