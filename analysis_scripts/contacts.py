#!/usr/bin/env python3
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from MDAnalysis.lib.distances import capped_distance
import MDAnalysis as mda

from common import add_common_args, time_value, write_csv, load_universe


def main():
    p = argparse.ArgumentParser(description="Compute protein–ligand heavy-atom contacts vs time.")
    add_common_args(p)
    p.add_argument("--prot-sel", default="protein and not name H*", help="Protein heavy atoms selection.")
    p.add_argument("--lig-sel", default="resname LIG and not name H*", help="Ligand heavy atoms selection.")
    p.add_argument("--cutoff", type=float, default=0.45, help="Contact cutoff in nm (default: 0.45 nm).")
    p.add_argument("--out", default="contacts.csv", help="Output CSV.")
    args = p.parse_args()

    u = load_universe(args.top, args.traj)
    prot = u.select_atoms(args.prot_sel)
    lig = u.select_atoms(args.lig_sel)
    if prot.n_atoms == 0 or lig.n_atoms == 0:
        raise ValueError("Empty selection. Check --prot-sel / --lig-sel.")

    cutoff_A = args.cutoff * 10.0  # MDAnalysis uses Angstrom distances

    rows = []
    for ts in u.trajectory[::args.stride]:
        t = time_value(ts, args.time_unit)
        pairs = capped_distance(prot.positions, lig.positions, max_cutoff=cutoff_A, return_distances=False)
        n_contacts = pairs.shape[0]
        rows.append({f"time_{args.time_unit}": t, "contacts": int(n_contacts)})

    df = pd.DataFrame(rows)
    write_csv(df, args.out)


if __name__ == "__main__":
    main()
