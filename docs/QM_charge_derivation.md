# Quantum Mechanical Charge Derivation Protocol

This document describes the complete workflow used to derive partial atomic charges for indium-containing DOTA-based PSMA conjugates. The procedure combines GAFF2 atom typing with hybrid density functional theory (DFT) calculations and CHELPG electrostatic charge fitting to ensure compatibility with AMBER-family force fields used in subsequent molecular dynamics simulations.

---

## 1. Ligand Preparation

The starting ligand structure was extracted from the docking pose. To enable initial GAFF2 atom typing, the indium atom was temporarily removed from the ligand structure.

All hydrogen atoms were added at physiological pH using Open Babel:

obabel -i pdb ligand_without_In.pdb -o pdb -O ligand_fixed.pdb -h --pH 7.0

The protonation state and orientation of hydrogens, particularly within the DOTA macrocycle, were visually inspected and corrected when necessary prior to further processing.

---

## 2. GAFF2 Atom Typing

GAFF2 atom types were assigned using Antechamber (AmberTools).

Dummy zero charges were first generated to allow atom typing:

yes 0.0 | head -n N > charges.dummy

where N corresponds to the total number of ligand atoms (excluding indium).

Atom typing was then performed:

antechamber -i ligand_fixed.pdb -fi pdb -o ligand_gaff2.mol2 -fo mol2 -at gaff2 -c rc -cf charges.dummy -pf y

This procedure generates a MOL2 file containing GAFF2 atom types for the organic ligand framework.

---

## 3. Reinsertion of Indium

The indium atom was manually reintroduced into the GAFF2-typed MOL2 file using coordinates from the docking pose.

During this step:

- DOTA nitrogen atoms were assigned appropriate coordination atom types
- Aromatic carbons were assigned type `ca`
- Aromatic bonds were defined as `ar`
- Atom types and bonding patterns were manually verified for consistency

The resulting structure was saved as:

ligand_metal.mol2

---

## 4. Preparation of Geometry for QM Calculations

Atomic coordinates were extracted from the MOL2 file to generate the QM input geometry:

grep -A N "@<TRIPOS>ATOM" ligand_metal.mol2 | \
awk 'NR>1 {gsub(/[0-9]/,"",$2); printf("%-2s %10s %10s %10s\n",$2,$3,$4,$5)}' > geometry.inp

---

## 5. Quantum Mechanical Calculations

Single-point DFT calculations were performed using ORCA to derive electrostatic charges.

Computational details:

- Functional: PBE0
- Basis set: def2-TZVP
- RIJCOSX approximation
- D3BJ dispersion correction
- TightSCF convergence criteria
- CHELPG charge fitting
- Unrestricted Kohn–Sham (UKS) formalism when required

Example ORCA input:

! PBE0 def2-TZVP SP RIJCOSX D3BJ AutoAux TightSCF UKS
! CHELPG
%pal nprocs 16 end
%maxcore 5000
* xyz Q M
(coordinates)
*

Total charge (Q) and multiplicity (M) were defined according to the formal oxidation state and electronic configuration of the indium complex.

Successful completion of the calculation was confirmed by the presence of:

****ORCA TERMINATED NORMALLY****

in the output file.

---

## 6. Transfer of CHELPG Charges to MOL2 File

CHELPG atomic charges extracted from the ORCA output were transferred into the GAFF2-typed MOL2 file using:

awk 'NR==FNR { charges[NR]=$1; next }
     /^@<TRIPOS>ATOM/ { in_atoms=1; print; next }
     /^@<TRIPOS>/ && in_atoms { in_atoms=0; print; next }
     in_atoms {
       printf "%7d %-8s %10.4f %10.4f %10.4f %-6s %3d %-8s %10.6f\n", \
              $1, $2, $3, $4, $5, $6, $7, $8, charges[++i]
       next
     }
     { print }
' charges.txt ligand_metal.mol2 > ligand_charged.mol2

---

## 7. Final Output

The final parameterized ligand file:

ligand_charged.mol2

contains GAFF2 atom types and CHELPG-derived partial charges and was used for topology generation and subsequent molecular dynamics simulations.

---

End of protocol.
