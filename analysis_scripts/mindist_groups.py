#!/usr/bin/env python3
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from MDAnalysis.lib.distances import distance_array
import MDAnalysis as mda

from common import add_common_args, time_value, write_csv, load_universe


DEFAULT_GROUPS = {
    "water_coordination": ["GLU370", "TYR498"],
    "structural_support": ["ASP325", "GLU503", "PRO334", "ASN465"],
    "s1_pocket": ["ARG409", "ARG480", "ARG482"],
    "s1_stabilization": ["GLU403", "ASP411", "SER400"],
    "s1prime_pocket": ["ARG156", "ASN203", "LYS643", "TYR644"],
}


def sel_for_resnames(resnames: list[str]) -> str:
    # MDAnalysis resname uses three-letter codes; ensure you use the same.
    # Example: "protein and (resname ARG and resid 156)" is more precise,
    # but here we follow resname-only for a group.
    # Best practice: use resid-based selections; see note below.
    parts = [f"resname {rn}" for rn in resnames]
    return "protein and (" + " or ".join(parts) + ")"


def main():
    p = argparse.ArgumentParser(description="Compute minimum ligand distance to PSMA residue groups vs time.")
    add_common_args(p)
    p.add_argument("--lig-sel", default="resname LIG and not name H*", help="Ligand heavy-atom selection.")
    p.add_argument("--use-resid-map", action="store_true",
                  help="Use explicit residue IDs for PSMA groups (recommended) instead of resname-only.")
    p.add_argument("--out", default="mindist_groups.csv", help="Output CSV.")
    args = p.parse_args()

    u = load_universe(args.top, args.traj)
    lig = u.select_atoms(args.lig_sel)
    if lig.n_atoms == 0:
        raise ValueError("Ligand selection empty. Check --lig-sel.")

    # Strongly recommended: use resid-based selections to avoid mixing multiple residues with same resname.
    # If you set --use-resid-map, we define explicit residues typical in PSMA numbering.
    if args.use_resid_map:
        groups = {
            "water_coordination": "protein and ((resid 370 and resname GLU) or (resid 498 and resname TYR))",
            "structural_support": "protein and ((resid 325 and resname ASP) or (resid 503 and resname GLU) or (resid 334 and resname PRO) or (resid 465 and resname ASN))",
            "s1_pocket": "protein and ((resid 409 and resname ARG) or (resid 480 and resname ARG) or (resid 482 and resname ARG))",
            "s1_stabilization": "protein and ((resid 403 and resname GLU) or (resid 411 and resname ASP) or (resid 400 and resname SER))",
            "s1prime_pocket": "protein and ((resid 156 and resname ARG) or (resid 203 and resname ASN) or (resid 643 and resname LYS) or (resid 644 and resname TYR))",
        }
    else:
        groups = {k: sel_for_resnames(v) for k, v in DEFAULT_GROUPS.items()}

    group_atoms = {}
    for name, sel in groups.items():
        ag = u.select_atoms(sel + " and not name H*")
        if ag.n_atoms == 0:
            raise ValueError(f"Group '{name}' selection returned 0 atoms: {sel}")
        group_atoms[name] = ag

    rows = []
    for ts in u.trajectory[::args.stride]:
        t = time_value(ts, args.time_unit)
        row = {f"time_{args.time_unit}": t}
        for gname, ag in group_atoms.items():
            d = distance_array(lig.positions, ag.positions)  # Angstrom
            row[f"mindist_{gname}_nm"] = float(d.min() / 10.0)
        rows.append(row)

    df = pd.DataFrame(rows)
    write_csv(df, args.out)
    print("Tip: Prefer --use-resid-map for PSMA to avoid ambiguity in residue selection.")


if __name__ == "__main__":
    main()
