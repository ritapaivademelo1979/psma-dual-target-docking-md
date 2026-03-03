# Quantum Mechanical Parameterization and Charge Derivation

This document describes the quantum mechanical (QM) workflow used to derive partial atomic charges for PSMA conjugates containing indium.

All QM calculations were performed using ORCA 6.0.1.

---

## 1. Ligand Preparation

The ligand structure was obtained from the docking pose.

- Indium was temporarily removed to allow initial GAFF2 atom typing.
- Hydrogens were added at pH 7.0 using Open Babel.
- Geometry was visually inspected and corrected when necessary.

Command used for hydrogen addition:

obabel -i pdb ligand_without_In.pdb -o pdb -O ligand_fixed.pdb -h --pH 7.0

---

## 2. Initial GAFF2 Atom Typing

The ligand was converted to GAFF2 atom types using Antechamber.

Dummy zero charges were initially assigned to enable atom typing.

antechamber -i ligand_fixed.pdb -fi pdb -o ligand_gaff2.mol2 -fo mol2 -at gaff2 -c rc -cf charges.dummy -pf y

The resulting MOL2 file contained GAFF2 atom types.

---

## 3. Inclusion of Indium

The indium atom was reintroduced into the MOL2 structure using coordinates from the docking pose.

- Atom types were manually verified.
- DOTA nitrogen atoms were assigned appropriate coordination types.
- Aromatic carbons were adjusted to type "ca".
- Bond orders were corrected where necessary.

The final structure including indium was saved as:

ligand_metal.mol2

---

## 4. Quantum Mechanical Calculations

Single-point QM calculations were performed to derive electrostatic charges.

Method:
- Functional: PBE0
- Basis set: def2-TZVP
- RIJCOSX approximation
- D3BJ dispersion correction
- TightSCF convergence
- UKS formalism (open-shell)

CHELPG charges were computed.

Example ORCA input:

! PBE0 def2-TZVP SP RIJCOSX D3BJ AutoAux TightSCF UKS
! CHELPG
%pal nprocs 16 end
%maxcore 5000
* xyz -3 2
(coordinates)
*

Total charge and multiplicity were defined according to the formal oxidation state of the system.

---

## 5. Charge Transfer to MOL2 File

CHELPG atomic charges were extracted from the ORCA output and inserted into the GAFF2 MOL2 file.

The final parameterized ligand file:

ligand_charged.mol2

This file was subsequently used for topology generation and molecular dynamics simulations.

---

End of QM parameterization protocol.
