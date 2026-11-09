# 🧪 Candidate Superconductor Materials Catalog

> *Generated from Layer 2 literature gap discovery, grounded in crystallographic prototypes, validated via OpenAlex/Materials Project novelty checks, and evaluated for thermodynamic convex hull stability.*

---

## 📋 Executive Summary Table

| ID | Formula | Prototype | Novelty Status | Thermodynamic Stability ($E_{\text{above\_hull}}$) | $T_c$ Status | Synthesis Recipe |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CAND_001** | `(Ce0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **NO_HITS_FOUND** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_002** | `(Pr0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **NO_HITS_FOUND** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_003** | `(Gd0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **NO_HITS_FOUND** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_004** | `(Lu0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **NO_HITS_FOUND** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |
| **CAND_005** | `(Sm0.85Sr0.15)H10` | LaH10 (Fm-3m (#225)) | **NO_HITS_FOUND** | NOT COMPUTED (No ambient MP phase diagram ent... | `NOT COMPUTED` | *Unvalidated Template* |

---

## 🔬 Detailed Candidate Evaluations

### Candidate CAND_001: `(Ce0.85Sr0.15)H10`
- **Structural Prototype**: **LaH10** in Space Group **Fm-3m (#225)** (Cubic)
- **Discovery Origin**: Untried element pair Ce-Sr mapped to clathrate hydride cage (Discovery Score: 55.0)
- **Constituent Elements**: Ce, H, Sr

#### 1. Novelty Assessment (Multi-Source Check)
- **Status**: `NO_HITS_FOUND`
- **Summary**: no hits found in: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**: None (Zero matching records found)

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
- **Status**: `NO_HITS_FOUND`
- **Summary**: no hits found in: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**: None (Zero matching records found)

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
- **Status**: `NO_HITS_FOUND`
- **Summary**: no hits found in: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**: None (Zero matching records found)

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
- **Status**: `NO_HITS_FOUND`
- **Summary**: no hits found in: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**: None (Zero matching records found)

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
- **Status**: `NO_HITS_FOUND`
- **Summary**: no hits found in: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Sources Searched**: OpenAlex API, Materials Project, Local Superconductivity Corpus, SuperCon Reference
- **Traceable Evidence**: None (Zero matching records found)

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
