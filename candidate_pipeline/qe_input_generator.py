"""
Quantum ESPRESSO Electron-Phonon Input Deck Generator for Hydride Superconductors.
Generates standard DFT (PWscf), DFPT (PHonon), and EPW input decks for candidate hydrides.
All generated input decks are explicitly watermarked and marked as 'NOT RUN'.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional


def generate_qe_input_decks(
    formula: str,
    space_group: str,
    output_dir: Path,
    pressure_gpa: float = 150.0,
) -> Dict[str, Path]:
    """
    Generates standard Quantum ESPRESSO input decks for ab initio electron-phonon coupling
    and Eliashberg Tc calculation. Marks all decks explicitly as NOT RUN.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_name = formula.replace("(", "").replace(")", "").replace(".", "_")

    watermark = f"""! ==============================================================================
! STATUS: NOT RUN (DFT input generated for HPC execution)
! Candidate Material: {formula}
! Target Pressure: {pressure_gpa} GPa
! Prototype Space Group: {space_group}
! Code Suite: Quantum ESPRESSO v7.2+ (PWscf / PHonon / EPW)
! NOTE: Critical temperature (Tc) requires ab initio electron-phonon calculations
!       (Eliashberg function alpha2F) to be performed on high-performance compute clusters.
! ==============================================================================
"""

    # 1. SCF Input Deck (pw.in)
    pw_content = watermark + f"""
&CONTROL
  calculation = 'scf',
  restart_mode = 'from_scratch',
  prefix = '{clean_name}',
  outdir = './tmp/',
  pseudo_dir = './pseudo/',
  tstress = .true.,
  tprnfor = .true.,
/
&SYSTEM
  ibrav = 2,
  celldm(1) = 9.15,
  nat = 11,
  ntyp = 3,
  ecutwfc = 80.0,
  ecutrho = 800.0,
  occupations = 'smearing',
  smearing = 'mp',
  degauss = 0.02,
/
&ELECTRONS
  conv_thr = 1.0d-10,
  mixing_beta = 0.7,
/
ATOMIC_SPECIES
  La  138.905  La.pbe-spfn-kjpaw_psl.1.0.0.UPF
  Y    88.906  Y.pbe-spfn-kjpaw_psl.1.0.0.UPF
  H     1.008  H.pbe-kjpaw_psl.1.0.0.UPF
K_POINTS automatic
  16 16 16 0 0 0
"""

    # 2. Phonon Input Deck (ph.in)
    ph_content = watermark + f"""
Phonon dispersion and electron-phonon coupling grid for {clean_name}
&INPUTPH
  prefix = '{clean_name}',
  outdir = './tmp/',
  fildyn = '{clean_name}.dyn',
  ldisp = .true.,
  nq1 = 4, nq2 = 4, nq3 = 4,
  tr2_ph = 1.0d-14,
  electron_phonon = 'interpolated',
  el_ph_sigma = 0.02,
  el_ph_nsigma = 10,
/
"""

    # 3. EPW Input Deck (epw.in)
    epw_content = watermark + f"""
&INPUTEPW
  prefix = '{clean_name}',
  outdir = './tmp/',
  dvscf_dir = './save/',
  elph = .true.,
  ep_coupling = .true.,
  epb = .true.,
  epwwrite = .true.,
  epwread = .false.,
  wannierize = .true.,
  num_iter = 500,
  dis_win_max = 25.0,
  dis_froz_max = 12.0,
  wdata(1) = 'bands_plot = true',
  nk1 = 8, nk2 = 8, nk3 = 8,
  nq1 = 4, nq2 = 4, nq3 = 4,
  nkf1 = 24, nkf2 = 24, nkf3 = 24,
  nqf1 = 12, nqf2 = 12, nqf3 = 12,
  fildvscf = '{clean_name}.dvscf',
/
"""

    pw_path = output_dir / f"{clean_name}_pw.in"
    ph_path = output_dir / f"{clean_name}_ph.in"
    epw_path = output_dir / f"{clean_name}_epw.in"

    pw_path.write_text(pw_content, encoding="utf-8")
    ph_path.write_text(ph_content, encoding="utf-8")
    epw_path.write_text(epw_content, encoding="utf-8")

    return {
        "pw_in": pw_path,
        "ph_in": ph_path,
        "epw_in": epw_path,
    }
