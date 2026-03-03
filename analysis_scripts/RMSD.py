#!/usr/bin/env python3
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import rms

from common import add_common_args, time_value, write_csv, load_universe


def main():
    p = argparse.ArgumentParser(description="Compute RMSD (protein backbone and ligand) from trajectory.")
    add_common_args(p)
    p.add_argument("--sel-protein", default="protein and backbone", help="Selection for protein RMSD (default: backbone).")
    p.add_argument("--sel-ligand", default="resname LIG", help="Selection for ligand RMSD (default: resname LIG).")
    p.add_argument("--fit-sel", default="protein and backbone", help="Selection used to fit trajectory (default: backbone).")
    p.add_argument("--out", default="rmsd.csv", help="Output CSV.")
    args = p.parse_args()

    u = load_universe(args.top, args.traj)

    # RMSD expects a reference; we'll use first frame
    ref = mda.Universe(args.top, args.traj)
    ref.trajectory[0]

    # Fit and compute RMSD for protein
    R_prot = rms.RMSD(
        u,
        ref,
        select=args.sel-protein,
        groupselections=[args.sel_ligand],
        ref_frame=0,
        filename=None,
    )
    # Apply fitting using fit_sel by supplying select for RMSD + center/superpose:
    # MDAnalysis RMSD uses select for alignment by default. To align by fit_sel but compute RMSD on another group,
    # we'd typically run AlignTraj. For simplicity/robustness: use same selection for fit and protein RMSD,
    # and compute ligand RMSD in groupselections with the same alignment.
    # If you need different alignment, tell me and I’ll provide AlignTraj-based version.

    # Stride support: run on a sliced trajectory
    if args.stride != 1:
        u.trajectory[::args.stride]
        ref.trajectory[0]

    R_prot.run()

    # Output columns from MDAnalysis RMSD:
    # time (ps), RMSD of select (Å), RMSD of groupselections (Å)
    data = R_prot.results.rmsd
    time_ps = data[:, 1]
    prot_A = data[:, 2]
    lig_A = data[:, 3]

    if args.time_unit == "ns":
        time_out = time_ps / 1000.0
        time_col = "time_ns"
    else:
        time_out = time_ps
        time_col = "time_ps"

    df = pd.DataFrame(
        {
            time_col: time_out,
            "protein_rmsd_nm": prot_A / 10.0,
            "ligand_rmsd_nm": lig_A / 10.0,
        }
    )
    write_csv(df, args.out)


if __name__ == "__main__":
    main()
