#!/usr/bin/env python3
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from MDAnalysis.analysis import align, rms
import MDAnalysis as mda

from common import add_common_args, write_csv, load_universe


def main():
    p = argparse.ArgumentParser(description="Compute RMSF (protein per-residue and ligand per-atom).")
    add_common_args(p)
    p.add_argument("--fit-sel", default="protein and backbone", help="Fit selection (default: protein backbone).")
    p.add_argument("--prot-sel", default="protein and backbone", help="Protein selection for RMSF (default: backbone).")
    p.add_argument("--lig-sel", default="resname LIG", help="Ligand selection for RMSF (default: resname LIG).")
    p.add_argument("--out-protein", default="rmsf_protein.csv", help="Protein RMSF CSV (per residue).")
    p.add_argument("--out-ligand", default="rmsf_ligand.csv", help="Ligand RMSF CSV (per atom).")
    args = p.parse_args()

    u = load_universe(args.top, args.traj)

    # Align trajectory to first frame using fit selection
    align.AlignTraj(u, u, select=args.fit_sel, in_memory=True).run()

    # Protein RMSF (per residue): compute on CA for clarity (common in papers)
    prot = u.select_atoms(args.prot_sel)
    if prot.n_atoms == 0:
        raise ValueError("Protein selection returned 0 atoms.")

    # If selection is backbone, reduce to CA per residue
    ca = u.select_atoms("protein and name CA")
    if ca.n_atoms > 0:
        prot_for_rmsf = ca
        mode = "CA"
    else:
        prot_for_rmsf = prot
        mode = "selection"

    R = rms.RMSF(prot_for_rmsf).run()
    rmsf_A = R.results.rmsf  # Angstrom

    if mode == "CA":
        resid = prot_for_rmsf.resids
        resname = prot_for_rmsf.resnames
        dfp = pd.DataFrame(
            {"resid": resid, "resname": resname, "rmsf_nm": rmsf_A / 10.0}
        )
    else:
        dfp = pd.DataFrame({"atom_index": prot_for_rmsf.indices, "rmsf_nm": rmsf_A / 10.0})

    write_csv(dfp, args.out_protein)

    # Ligand RMSF (per atom)
    lig = u.select_atoms(args.lig_sel)
    if lig.n_atoms == 0:
        raise ValueError("Ligand selection returned 0 atoms. Adjust --lig-sel (e.g., 'resname LIG').")

    Rl = rms.RMSF(lig).run()
    dfL = pd.DataFrame(
        {"atom_index": lig.indices, "atom_name": lig.names, "rmsf_nm": Rl.results.rmsf / 10.0}
    )
    write_csv(dfL, args.out_ligand)


if __name__ == "__main__":
    main()
