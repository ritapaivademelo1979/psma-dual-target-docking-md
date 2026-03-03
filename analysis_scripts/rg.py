#!/usr/bin/env python3
from __future__ import annotations
import argparse
import pandas as pd
import MDAnalysis as mda

from common import add_common_args, time_value, write_csv, load_universe


def main():
    p = argparse.ArgumentParser(description="Compute radius of gyration for protein and ligand vs time.")
    add_common_args(p)
    p.add_argument("--prot-sel", default="protein", help="Protein selection (default: protein).")
    p.add_argument("--lig-sel", default="resname LIG", help="Ligand selection (default: resname LIG).")
    p.add_argument("--out", default="rg.csv", help="Output CSV.")
    args = p.parse_args()

    u = load_universe(args.top, args.traj)
    prot = u.select_atoms(args.prot_sel)
    lig = u.select_atoms(args.lig_sel)
    if prot.n_atoms == 0:
        raise ValueError("Protein selection returned 0 atoms.")
    if lig.n_atoms == 0:
        raise ValueError("Ligand selection returned 0 atoms.")

    rows = []
    for ts in u.trajectory[::args.stride]:
        t = time_value(ts, args.time_unit)
        rows.append(
            {
                f"time_{args.time_unit}": t,
                "protein_rg_nm": prot.radius_of_gyration(),
                "ligand_rg_nm": lig.radius_of_gyration(),
            }
        )

    df = pd.DataFrame(rows)
    write_csv(df, args.out)


if __name__ == "__main__":
    main()
