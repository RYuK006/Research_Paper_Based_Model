# 🧪 Candidate Superconductor Materials Catalog

> *Generated from Layer 2 literature gap discovery, grounded in crystallographic prototypes, validated via OpenAlex/Materials Project novelty checks, and evaluated for thermodynamic convex hull stability.*

---

## 📋 Executive Summary Table

| ID | Formula | Prototype | Novelty Status | Thermodynamic Stability ($E_{\text{above\_hull}}$) | $T_c$ Status | Synthesis Recipe |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CAND_001** | `(Ce0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **KNOWN** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_002** | `(Pr0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **KNOWN** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_003** | `(Gd0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **KNOWN** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_004** | `(Lu0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **KNOWN** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_005** | `(Sm0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **KNOWN** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |

---

## 🔬 Detailed Candidate Evaluations

### Candidate CAND_001: `(Ce0.85Sr0.15)H10`
- **Structural Prototype**: **LaH10** in Space Group **Fm-3m (#225)** (Cubic)
- **Discovery Origin**: Untried element pair Ce-Sr mapped to clathrate hydride cage (Discovery Score: 55.0)
- **Constituent Elements**: Ce, H, Sr

#### 1. Novelty Assessment (Multi-Source Check)
- **Status**: `KNOWN`
- **Summary**: KNOWN: Established superconductor in literature (e.g., 'Superconducting Bi-Sr-Ca-Cu-O Thick Films by the Sol-Gel Method', 1988)
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**:
  - [OpenAlex API] *"Superconducting Bi-Sr-Ca-Cu-O Thick Films by the Sol-Gel Method"* (1988) -> `https://doi.org/10.1143/jjap.27.l1880`
  - [OpenAlex API] *"Transport and anisotropy in single-crystalline SrFe2As2 and A0.6K0.4Fe2As2 ( A=Sr , Ba) superconductors"* (2008) -> `https://doi.org/10.1103/physrevb.78.224512`
  - [OpenAlex API] *"Specific heat and μ SR study on the noncentrosymmetric superconductor LaRhSi 3"* (2011) -> `https://doi.org/10.1103/physrevb.83.064522`

#### 2. Thermodynamic & Physical Stability
- **Convex Hull Status**: **NOT COMPUTED (No ambient MP phase diagram entry for chemsys; requires high-pressure DFT relaxation)**
- **Energy Above Hull ($E_{\text{above\_hull}}$)**: **NOT COMPUTED**
- **Calculation Method**: Materials Project Phase Diagram (chemsys query) (Reference: `MP API v0.88.1`)
- **Prefilter Sanity Check**: `PASS` (Electronegativity Spread: 1.25, Tolerance: None)

#### 3. Critical Temperature ($T_c$) & Pressure Status
- **Critical Temperature ($T_c$)**: `Tc: NOT COMPUTED (Template values purged; requires ab initio electron-phonon calculation or calibrated model)`
- **Pressure**: `Pressure: NOT COMPUTED (Requires ab initio H(P) enthalpy calculation vs decomposition products)`
- **Quantum ESPRESSO Input Decks**: `Generated (Marked NOT RUN)`
  - SCF Deck: `data\dft_inputs\Ce0_85Sr0_15H10_pw.in`
  - Phonon Deck: `data\dft_inputs\Ce0_85Sr0_15H10_ph.in`
  - EPW Deck: `data\dft_inputs\Ce0_85Sr0_15H10_epw.in`

#### 4. Experimental Synthesis Protocol (Unvalidated Template)
> [!WARNING]
> **UNVALIDATED HEURISTIC TEMPLATE**: This protocol is an uncalibrated heuristic template derived from structural archetypes. It has NOT been experimentally validated in a wet lab and must be verified before execution.

- **Target Method**: Laser-heated diamond anvil cell (LH-DAC)
- **Starting Precursors**:
  - High-purity (Ce, Sr) metal foil or powder (purity $\ge 99.99\%$), stoichiometrically weighed.
  - Ammonia borane (NH3BH3) or pure molecular H2 gas loading as clean hydrogen donor.
  - Rhenium or tungsten gasket pre-indented to 25-35 $\mu$m thickness with 100 $\mu$m sample chamber.
- **Diagnostic Characterization Plan**:
  - In-situ Synchrotron Powder X-ray Diffraction ($\lambda=0.434$ Å) to confirm Fm-3m (#225) clathrate lattice formation.
  - Four-probe electrical resistance using sputtered Pt/Ti microelectrodes deposited on diamond culet.
  - Measure resistance transition: verify zero-resistance state and critical transition down to 2 K.
  - Magnetic susceptibility / AC susceptibility to confirm Meissner diamagnetic shielding.

---

### Candidate CAND_002: `(Pr0.85Sr0.15)H10`
- **Structural Prototype**: **LaH10** in Space Group **Fm-3m (#225)** (Cubic)
- **Discovery Origin**: Untried element pair Pr-Sr mapped to clathrate hydride cage (Discovery Score: 49.0)
- **Constituent Elements**: H, Pr, Sr

#### 1. Novelty Assessment (Multi-Source Check)
- **Status**: `KNOWN`
- **Summary**: KNOWN: Established superconductor in literature (e.g., 'Antiferroquadrupolar Ordering in a Pr-Based Superconductor PrIr2Zn20', 2011)
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**:
  - [OpenAlex API] *"Antiferroquadrupolar Ordering in a Pr-Based Superconductor PrIr2Zn20"* (2011) -> `https://doi.org/10.1103/physrevlett.106.177001`
  - [OpenAlex API] *"Linear-in-temperature resistivity for optimally superconducting (Nd,Sr)NiO2"* (2023) -> `https://doi.org/10.1038/s41586-023-06129-x`
  - [OpenAlex API] *"Transport and anisotropy in single-crystalline SrFe2As2 and A0.6K0.4Fe2As2 ( A=Sr , Ba) superconductors"* (2008) -> `https://doi.org/10.1103/physrevb.78.224512`

#### 2. Thermodynamic & Physical Stability
- **Convex Hull Status**: **NOT COMPUTED (No ambient MP phase diagram entry for chemsys; requires high-pressure DFT relaxation)**
- **Energy Above Hull ($E_{\text{above\_hull}}$)**: **NOT COMPUTED**
- **Calculation Method**: Materials Project Phase Diagram (chemsys query) (Reference: `MP API v0.88.1`)
- **Prefilter Sanity Check**: `PASS` (Electronegativity Spread: 1.25, Tolerance: None)

#### 3. Critical Temperature ($T_c$) & Pressure Status
- **Critical Temperature ($T_c$)**: `Tc: NOT COMPUTED (Template values purged; requires ab initio electron-phonon calculation or calibrated model)`
- **Pressure**: `Pressure: NOT COMPUTED (Requires ab initio H(P) enthalpy calculation vs decomposition products)`
- **Quantum ESPRESSO Input Decks**: `Generated (Marked NOT RUN)`
  - SCF Deck: `data\dft_inputs\Pr0_85Sr0_15H10_pw.in`
  - Phonon Deck: `data\dft_inputs\Pr0_85Sr0_15H10_ph.in`
  - EPW Deck: `data\dft_inputs\Pr0_85Sr0_15H10_epw.in`

#### 4. Experimental Synthesis Protocol (Unvalidated Template)
> [!WARNING]
> **UNVALIDATED HEURISTIC TEMPLATE**: This protocol is an uncalibrated heuristic template derived from structural archetypes. It has NOT been experimentally validated in a wet lab and must be verified before execution.

- **Target Method**: Laser-heated diamond anvil cell (LH-DAC)
- **Starting Precursors**:
  - High-purity (Pr, Sr) metal foil or powder (purity $\ge 99.99\%$), stoichiometrically weighed.
  - Ammonia borane (NH3BH3) or pure molecular H2 gas loading as clean hydrogen donor.
  - Rhenium or tungsten gasket pre-indented to 25-35 $\mu$m thickness with 100 $\mu$m sample chamber.
- **Diagnostic Characterization Plan**:
  - In-situ Synchrotron Powder X-ray Diffraction ($\lambda=0.434$ Å) to confirm Fm-3m (#225) clathrate lattice formation.
  - Four-probe electrical resistance using sputtered Pt/Ti microelectrodes deposited on diamond culet.
  - Measure resistance transition: verify zero-resistance state and critical transition down to 2 K.
  - Magnetic susceptibility / AC susceptibility to confirm Meissner diamagnetic shielding.

---

### Candidate CAND_003: `(Gd0.85Sr0.15)H10`
- **Structural Prototype**: **LaH10** in Space Group **Fm-3m (#225)** (Cubic)
- **Discovery Origin**: Untried element pair Gd-Sr mapped to clathrate hydride cage (Discovery Score: 43.0)
- **Constituent Elements**: Gd, H, Sr

#### 1. Novelty Assessment (Multi-Source Check)
- **Status**: `KNOWN`
- **Summary**: KNOWN: Established superconductor in literature (e.g., 'Antiferromagnetic ordering of Ru and Gd in superconducting RuSr2GdCu2O8', 2000)
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**:
  - [OpenAlex API] *"Antiferromagnetic ordering of Ru and Gd in superconducting RuSr2GdCu2O8"* (2000) -> `https://doi.org/10.1103/physrevb.61.r14964`
  - [OpenAlex API] *"Investigation of some physical properties of Gd added Bi-2223 superconductors"* (2010) -> `https://doi.org/10.1016/j.jallcom.2010.08.105`
  - [OpenAlex API] *"The Effect of Gd Concentration on the Physical and Magnetic Properties of Bi1.7Pb0.3-xGdxSr2Ca3Cu4O12+y Superconductors"* (2005) -> `https://doi.org/10.1007/s10909-005-6015-4`

#### 2. Thermodynamic & Physical Stability
- **Convex Hull Status**: **NOT COMPUTED (No ambient MP phase diagram entry for chemsys; requires high-pressure DFT relaxation)**
- **Energy Above Hull ($E_{\text{above\_hull}}$)**: **NOT COMPUTED**
- **Calculation Method**: Materials Project Phase Diagram (chemsys query) (Reference: `MP API v0.88.1`)
- **Prefilter Sanity Check**: `PASS` (Electronegativity Spread: 1.25, Tolerance: None)

#### 3. Critical Temperature ($T_c$) & Pressure Status
- **Critical Temperature ($T_c$)**: `Tc: NOT COMPUTED (Template values purged; requires ab initio electron-phonon calculation or calibrated model)`
- **Pressure**: `Pressure: NOT COMPUTED (Requires ab initio H(P) enthalpy calculation vs decomposition products)`
- **Quantum ESPRESSO Input Decks**: `Generated (Marked NOT RUN)`
  - SCF Deck: `data\dft_inputs\Gd0_85Sr0_15H10_pw.in`
  - Phonon Deck: `data\dft_inputs\Gd0_85Sr0_15H10_ph.in`
  - EPW Deck: `data\dft_inputs\Gd0_85Sr0_15H10_epw.in`

#### 4. Experimental Synthesis Protocol (Unvalidated Template)
> [!WARNING]
> **UNVALIDATED HEURISTIC TEMPLATE**: This protocol is an uncalibrated heuristic template derived from structural archetypes. It has NOT been experimentally validated in a wet lab and must be verified before execution.

- **Target Method**: Laser-heated diamond anvil cell (LH-DAC)
- **Starting Precursors**:
  - High-purity (Gd, Sr) metal foil or powder (purity $\ge 99.99\%$), stoichiometrically weighed.
  - Ammonia borane (NH3BH3) or pure molecular H2 gas loading as clean hydrogen donor.
  - Rhenium or tungsten gasket pre-indented to 25-35 $\mu$m thickness with 100 $\mu$m sample chamber.
- **Diagnostic Characterization Plan**:
  - In-situ Synchrotron Powder X-ray Diffraction ($\lambda=0.434$ Å) to confirm Fm-3m (#225) clathrate lattice formation.
  - Four-probe electrical resistance using sputtered Pt/Ti microelectrodes deposited on diamond culet.
  - Measure resistance transition: verify zero-resistance state and critical transition down to 2 K.
  - Magnetic susceptibility / AC susceptibility to confirm Meissner diamagnetic shielding.

---

### Candidate CAND_004: `(Lu0.85Sr0.15)H10`
- **Structural Prototype**: **LaH10** in Space Group **Fm-3m (#225)** (Cubic)
- **Discovery Origin**: Untried element pair Lu-Sr mapped to clathrate hydride cage (Discovery Score: 42.0)
- **Constituent Elements**: H, Lu, Sr

#### 1. Novelty Assessment (Multi-Source Check)
- **Status**: `KNOWN`
- **Summary**: KNOWN: Established superconductor in literature (e.g., 'Transport and anisotropy in single-crystalline SrFe2As2 and A0.6K0.4Fe2As2 ( A=Sr , Ba) superconductors', 2008)
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**:
  - [OpenAlex API] *"Transport and anisotropy in single-crystalline SrFe2As2 and A0.6K0.4Fe2As2 ( A=Sr , Ba) superconductors"* (2008) -> `https://doi.org/10.1103/physrevb.78.224512`
  - [OpenAlex API] *"Superconducting properties and μ SR study of the noncentrosymmetric superconductor Nb 0.5 Os 0.5"* (2017) -> `https://doi.org/10.1088/1361-648x/aaa376`
  - [OpenAlex API] *"Striped superconductors: how spin, charge and superconducting orders intertwine in the cuprates"* (2009) -> `https://doi.org/10.1088/1367-2630/11/11/115004`

#### 2. Thermodynamic & Physical Stability
- **Convex Hull Status**: **NOT COMPUTED (No ambient MP phase diagram entry for chemsys; requires high-pressure DFT relaxation)**
- **Energy Above Hull ($E_{\text{above\_hull}}$)**: **NOT COMPUTED**
- **Calculation Method**: Materials Project Phase Diagram (chemsys query) (Reference: `MP API v0.88.1`)
- **Prefilter Sanity Check**: `PASS` (Electronegativity Spread: 1.25, Tolerance: None)

#### 3. Critical Temperature ($T_c$) & Pressure Status
- **Critical Temperature ($T_c$)**: `Tc: NOT COMPUTED (Template values purged; requires ab initio electron-phonon calculation or calibrated model)`
- **Pressure**: `Pressure: NOT COMPUTED (Requires ab initio H(P) enthalpy calculation vs decomposition products)`
- **Quantum ESPRESSO Input Decks**: `Generated (Marked NOT RUN)`
  - SCF Deck: `data\dft_inputs\Lu0_85Sr0_15H10_pw.in`
  - Phonon Deck: `data\dft_inputs\Lu0_85Sr0_15H10_ph.in`
  - EPW Deck: `data\dft_inputs\Lu0_85Sr0_15H10_epw.in`

#### 4. Experimental Synthesis Protocol (Unvalidated Template)
> [!WARNING]
> **UNVALIDATED HEURISTIC TEMPLATE**: This protocol is an uncalibrated heuristic template derived from structural archetypes. It has NOT been experimentally validated in a wet lab and must be verified before execution.

- **Target Method**: Laser-heated diamond anvil cell (LH-DAC)
- **Starting Precursors**:
  - High-purity (Lu, Sr) metal foil or powder (purity $\ge 99.99\%$), stoichiometrically weighed.
  - Ammonia borane (NH3BH3) or pure molecular H2 gas loading as clean hydrogen donor.
  - Rhenium or tungsten gasket pre-indented to 25-35 $\mu$m thickness with 100 $\mu$m sample chamber.
- **Diagnostic Characterization Plan**:
  - In-situ Synchrotron Powder X-ray Diffraction ($\lambda=0.434$ Å) to confirm Fm-3m (#225) clathrate lattice formation.
  - Four-probe electrical resistance using sputtered Pt/Ti microelectrodes deposited on diamond culet.
  - Measure resistance transition: verify zero-resistance state and critical transition down to 2 K.
  - Magnetic susceptibility / AC susceptibility to confirm Meissner diamagnetic shielding.

---

### Candidate CAND_005: `(Sm0.85Sr0.15)H10`
- **Structural Prototype**: **LaH10** in Space Group **Fm-3m (#225)** (Cubic)
- **Discovery Origin**: Untried element pair Sm-Sr mapped to clathrate hydride cage (Discovery Score: 40.0)
- **Constituent Elements**: H, Sm, Sr

#### 1. Novelty Assessment (Multi-Source Check)
- **Status**: `KNOWN`
- **Summary**: KNOWN: Established superconductor in literature (e.g., 'Transport and anisotropy in single-crystalline SrFe2As2 and A0.6K0.4Fe2As2 ( A=Sr , Ba) superconductors', 2008)
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**:
  - [OpenAlex API] *"Transport and anisotropy in single-crystalline SrFe2As2 and A0.6K0.4Fe2As2 ( A=Sr , Ba) superconductors"* (2008) -> `https://doi.org/10.1103/physrevb.78.224512`
  - [OpenAlex API] *"Higgs Mode in Superconductors"* (2019) -> `https://doi.org/10.1146/annurev-conmatphys-031119-050813`
  - [OpenAlex API] *"The crystal structure and superconductivity of new superconducting phase TlSr2Ca0.5Sm0.5Cu2O6.75"* (1989) -> `https://doi.org/10.1016/0038-1098(89)90369-4`

#### 2. Thermodynamic & Physical Stability
- **Convex Hull Status**: **NOT COMPUTED (No ambient MP phase diagram entry for chemsys; requires high-pressure DFT relaxation)**
- **Energy Above Hull ($E_{\text{above\_hull}}$)**: **NOT COMPUTED**
- **Calculation Method**: Materials Project Phase Diagram (chemsys query) (Reference: `MP API v0.88.1`)
- **Prefilter Sanity Check**: `PASS` (Electronegativity Spread: 1.25, Tolerance: None)

#### 3. Critical Temperature ($T_c$) & Pressure Status
- **Critical Temperature ($T_c$)**: `Tc: NOT COMPUTED (Template values purged; requires ab initio electron-phonon calculation or calibrated model)`
- **Pressure**: `Pressure: NOT COMPUTED (Requires ab initio H(P) enthalpy calculation vs decomposition products)`
- **Quantum ESPRESSO Input Decks**: `Generated (Marked NOT RUN)`
  - SCF Deck: `data\dft_inputs\Sm0_85Sr0_15H10_pw.in`
  - Phonon Deck: `data\dft_inputs\Sm0_85Sr0_15H10_ph.in`
  - EPW Deck: `data\dft_inputs\Sm0_85Sr0_15H10_epw.in`

#### 4. Experimental Synthesis Protocol (Unvalidated Template)
> [!WARNING]
> **UNVALIDATED HEURISTIC TEMPLATE**: This protocol is an uncalibrated heuristic template derived from structural archetypes. It has NOT been experimentally validated in a wet lab and must be verified before execution.

- **Target Method**: Laser-heated diamond anvil cell (LH-DAC)
- **Starting Precursors**:
  - High-purity (Sm, Sr) metal foil or powder (purity $\ge 99.99\%$), stoichiometrically weighed.
  - Ammonia borane (NH3BH3) or pure molecular H2 gas loading as clean hydrogen donor.
  - Rhenium or tungsten gasket pre-indented to 25-35 $\mu$m thickness with 100 $\mu$m sample chamber.
- **Diagnostic Characterization Plan**:
  - In-situ Synchrotron Powder X-ray Diffraction ($\lambda=0.434$ Å) to confirm Fm-3m (#225) clathrate lattice formation.
  - Four-probe electrical resistance using sputtered Pt/Ti microelectrodes deposited on diamond culet.
  - Measure resistance transition: verify zero-resistance state and critical transition down to 2 K.
  - Magnetic susceptibility / AC susceptibility to confirm Meissner diamagnetic shielding.

---
