# Molecular Docking Protocol — AutoDock Vina

This document describes the complete workflow used to perform molecular docking of PSMA conjugates using AutoDock Vina.

Docking calculations were performed using AutoDock Vina 1.2.0.

---

## 1. Protein Preparation

The PSMA crystal structure (PDB ID: 5O5R) was imported into PyMOL for structural inspection. Discontinuities and missing residues were identified. Missing regions were modeled using ChimeraX:

Tools → Structure Editing → Model Loops

The loop model with the lowest Z-DOPE score was selected, and the repaired structure was saved in PDB format.

The protein was then prepared in AutoDock Tools (ADT):

- Water molecules were removed.
- Polar hydrogens were added.
- Kollman charges were assigned.
- AD4 atom types were defined.
- The macromolecule was selected under Grid → Macromolecule → Choose.

The prepared receptor was saved as:

receptor.pdbqt

---

## 2. Ligand Preparation

Ligand structures were generated using ChemDraw and exported in MOL2 format.

Hydrogen atoms were added and geometry optimization was performed in Avogadro:

- Build → Add Hydrogens
- Extensions → Optimize Geometry

Optimization was repeated until convergence. Bonding within the DOTA macrocycle was carefully verified to ensure chemical consistency.

The optimized ligand was imported into AutoDock Tools:

- Ligand → Input → Open
- Gasteiger charges were assigned automatically.
- The ligand was saved in PDBQT format as:

ligand.pdbqt

---

## 3. Grid Box Definition

The prepared receptor was loaded in AutoDock Tools. Active-site residues were identified and selected.

The grid box was defined using:

Grid → Grid Box

The center coordinates and box dimensions were adjusted to fully encompass all catalytic and binding-site residues of PSMA.

Grid parameters were recorded for configuration file generation.

---

## 4. Docking Configuration

A configuration file named config.txt was created containing:

receptor = receptor.pdbqt
ligand = ligand.pdbqt

center_x = X
center_y = Y
center_z = Z

size_x = A
size_y = B
size_z = C

exhaustiveness = 8
num_modes = 10
energy_range = 3

The grid center coordinates (X, Y, Z) and box dimensions (A, B, C) were replaced with the values defined during grid box setup.

---

## 5. Docking Execution

Docking was performed from the command line using:

vina --receptor receptor.pdbqt --ligand ligand.pdbqt --config config.txt --log docking.log --out output.pdbqt

The calculation was allowed to complete until 100% progress was reached.

---

## 6. Post-Docking Analysis

The docking output file (output.pdbqt) was analyzed in PyMOL.

The prepared receptor structure was loaded, followed by the docking output. Binding poses were inspected and evaluated based on:

- Predicted binding affinity
- Zn²⁺ coordination geometry
- Hydrogen bonding interactions
- Steric compatibility within the PSMA active site

The best-scoring and chemically consistent pose was selected for subsequent molecular dynamics simulations.

---

## Output Files

The docking procedure generated the following files:

- receptor.pdbqt
- ligand.pdbqt
- config.txt
- docking.log
- output.pdbqt

---

End of docking protocol.
