# Comprehensive Corpus Report: 10,000 Scientific Research Papers

> Automated synthesis and domain analysis of scientific literature harvested from **arXiv**, **OpenAlex**, and **Semantic Scholar** / Open Academic Graph.

## 1. Executive Summary

- **Total Papers Collected**: **10,000**
- **Target Milestone**: 10,000 papers
- **Database Index**: SQLite (`data/papers.db`) with full JSONL stream (`data/manifests/papers_manifest.jsonl`)
- **Target Google Drive Storage**: `https://drive.google.com/drive/folders/1kYS059jeKZsFENUvd7ClgeIBlwAJibdL`

### Source Distribution

| Data Source | Collected Count | Percentage | Focus Domains |
| :--- | :---: | :---: | :--- |
| **ARXIV** | 4,000 | 40.0% | Superconductivity (`cond-mat.supr-con`), Materials Science (`cond-mat.mtrl-sci`) |
| **OPENALEX** | 3,000 | 30.0% | Chemistry, Chemical Elements, Novel Compounds, Open-Access Works |
| **SEMANTICSCHOLAR** | 3,000 | 30.0% | Chemical Compounds, Materials Synthesis, Crossref Open Graph |
| **TOTAL** | **10,000** | **100.0%** | Comprehensive Physical Sciences Corpus |

---

## 2. Chemical Elements Frequency

Most prominently studied chemical elements identified in paper titles and abstracts across the corpus:

| Rank | Element | Frequency (Papers) | Percentage of Corpus |
| :---: | :--- | :---: | :---: |
| 1 | **Carbon** | 442 | 4.4% |
| 2 | **Oxygen** | 434 | 4.3% |
| 3 | **Lead** | 433 | 4.3% |
| 4 | **Hydrogen** | 328 | 3.3% |
| 5 | **Nitrogen** | 197 | 2.0% |
| 6 | **Iron** | 157 | 1.6% |
| 7 | **Sodium** | 155 | 1.6% |
| 8 | **Copper** | 126 | 1.3% |
| 9 | **Silicon** | 113 | 1.1% |
| 10 | **Lithium** | 105 | 1.1% |
| 11 | **Zinc** | 99 | 1.0% |
| 12 | **Sulfur** | 93 | 0.9% |
| 13 | **Calcium** | 84 | 0.8% |
| 14 | **Boron** | 71 | 0.7% |
| 15 | **Potassium** | 68 | 0.7% |
| 16 | **Gold** | 67 | 0.7% |
| 17 | **Nickel** | 65 | 0.7% |
| 18 | **Cobalt** | 64 | 0.6% |
| 19 | **Silver** | 60 | 0.6% |
| 20 | **Phosphorus** | 56 | 0.6% |

---

## 3. Compound & Materials Class Distribution

Distribution of papers across key material families, superconducting structures, and novel chemical compounds:

| Material / Compound Class | Paper Count | Proportion |
| :--- | :---: | :---: |
| Perovskites & Oxides | 491 | 4.9% |
| Cuprates / High-Tc Superconductors | 294 | 2.9% |
| Iron-based Pnictides & Chalcogenides | 137 | 1.4% |
| Intermetallics & Heavy Fermions | 121 | 1.2% |
| 2D Materials & Dichalcogenides | 112 | 1.1% |
| Superhydrides & High-Pressure Phases | 46 | 0.5% |
| Metal-Organic Frameworks (MOFs) | 43 | 0.4% |
| Topological & Quantum Materials | 4 | 0.0% |

---

## 4. Publication Timeline

Distribution of publications by year across the corpus:

| Year Span | Number of Papers | Proportion |
| :--- | :---: | :---: |
| Pre-2000 (Foundational) | 1,243 | 12.4% |
| 2000 - 2009 | 5,259 | 52.6% |
| 2010 - 2019 | 2,136 | 21.4% |
| 2020 - 2023 | 872 | 8.7% |
| 2024 - 2026 (Recent Frontiers) | 490 | 4.9% |

---

## 5. Top Highly-Cited Landmark Papers in Corpus

| Citations | Title | Source | Link / DOI |
| :---: | :--- | :---: | :--- |
| **316,200** | PROTEIN MEASUREMENT WITH THE FOLIN PHENOL REAGENT | OPENALEX | `10.1016/s0021-9258(19)52451-6` |
| **67,323** | Electric Field Effect in Atomically Thin Carbon Films | OPENALEX | `10.1126/science.1102896` |
| **50,672** | Densely Connected Convolutional Networks | OPENALEX | `10.1109/cvpr.2017.243` |
| **47,311** | Short-Term Effects of Nose-Only Cigarette Smoke Exposure on Glutathione Redox Homeostasis,... | OPENALEX | `10.1159/000350087` |
| **30,984** | Molecular dynamics with coupling to an external bath | OPENALEX | `10.1063/1.448118` |
| **30,666** | The M06 suite of density functionals for main group thermochemistry, thermochemical kineti... | OPENALEX | `10.1007/s00214-007-0310-x` |
| **29,256** | Methods for Dietary Fiber, Neutral Detergent Fiber, and Nonstarch Polysaccharides in Relat... | OPENALEX | `10.3168/jds.s0022-0302(91)78551-2` |
| **29,084** | The PRISMA Statement for Reporting Systematic Reviews and Meta-Analyses of Studies That Ev... | OPENALEX | `10.1371/journal.pmed.1000100` |
| **26,721** | Random sample consensus | OPENALEX | `10.1145/358669.358692` |
| **25,956** | The iron cage revisited institutional isomorphism and collective rationality in organizati... | OPENALEX | `10.1016/s0742-3322(00)17011-1` |
| **24,758** | Reporting physisorption data for gas/solid systems with special reference to the determina... | OPENALEX | `10.1351/pac198557040603` |
| **24,419** | Unpaired Image-to-Image Translation Using Cycle-Consistent Adversarial Networks | OPENALEX | `10.1109/iccv.2017.244` |
| **24,084** | Image-to-Image Translation with Conditional Adversarial Networks | OPENALEX | `10.1109/cvpr.2017.632` |
| **24,060** | Two new Later Stone Age sites from the Final Pleistocene in the Falémé Valley, eastern Sen... | OPENALEX | `10.3929/ethz-b-000667478` |
| **23,169** | MRBAYES: Bayesian inference of phylogenetic trees | OPENALEX | `10.1093/bioinformatics/17.8.754` |

---

## 6. Pipeline Artifacts & Local Manifests

- **SQLite Database**: `data/papers.db` (indexes, schema, full text and citation counts)
- **JSONL Stream Manifest**: `data/manifests/papers_manifest.jsonl`
- **Raw Payloads**: `data/papers/arxiv/`, `data/papers/openalex/`, `data/papers/semanticscholar/`
- **Google Drive Uploader**: `drive_sync/gdrive_uploader.py`
- **Target Google Drive**: `https://drive.google.com/drive/folders/1kYS059jeKZsFENUvd7ClgeIBlwAJibdL`

_Report generated autonomously by Antigravity Pipeline under author RYuK006._
