[![DOI](https://zenodo.org/badge/XXXX.svg)](https://doi.org/10.5281/zenodo.18936110)


# psma-dual-target-docking-md
Reproducible docking and molecular dynamics workflows for PSMA Glu–urea–Lys conjugates (JCIM 2026)


## Overview
This repository contains the docking setup, molecular dynamics (MD) parameter files, and analysis scripts used to evaluate whether incorporation of subcellular-targeting motifs (acridine orange and triphenylphosphonium) perturbs canonical PSMA recognition by Glu–urea–Lys–based conjugates.


## Repository Contents
- Prepared PSMA receptor structure (PDB ID: 5O5R)
- AutoDock Vina docking configuration files
- GROMACS 2024.4 MD parameter (`.mdp`) files for minimization, equilibration, and 400 ns production runs
- Python analysis scripts used to generate RMSD, RMSF, radius of gyration, protein–ligand contact, and minimum-distance analyses reported in the manuscript


## Computational Details

**Docking**
- AutoDock Vina 1.2.0  
- Grid centered on the PSMA active site (see docking configuration file)

**Molecular Dynamics**
- GROMACS 2024.4  
- AMBER99SB-ILDN force field  
- TIP3P water model  
- 0.15 M NaCl  
- Temperature: 310.15 K (V-rescale thermostat)  
- Pressure: 1 bar (Parrinello–Rahman barostat)  
- PME cutoff: 1.4 nm  
- Time step: 2 fs  
- 3 × 400 ns production runs per system  

**Analysis**
- Python 3.10  
- MDAnalysis  
- NumPy  
- Pandas



## Reproducibility
All simulations can be reproduced using the provided `.mdp` files and documented workflow.
Production MD trajectories are not included due to file size constraints but can be regenerated using the provided input parameters.



## License
MIT License
