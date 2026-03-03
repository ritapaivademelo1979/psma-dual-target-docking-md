#!/usr/bin/env python3
from __future__ import annotations
import argparse
from dataclasses import dataclass
import numpy as np
import pandas as pd
import MDAnalysis as mda


def add_common_args(p: argparse.ArgumentParser) -> argparse.ArgumentParser:
    p.add_argument("--top", required=True, help="Topology file (e.g., .tpr, .pdb, .gro)")
    p.add_argument("--traj", required=True, help="Trajectory file (e.g., .xtc, .trr, .dcd)")
    p.add_argument("--stride", type=int, default=1, help="Frame stride (default: 1)")
    p.add_argument("--time-unit", choices=["ps", "ns"], default="ps", help="Time unit in output (default: ps)")
    return p


def time_value(ts, unit: str) -> float:
    """MDAnalysis gives ts.time typically in ps for GROMACS trajectories."""
    t_ps = float(ts.time)
    return t_ps if unit == "ps" else t_ps / 1000.0


def write_csv(df: pd.DataFrame, out: str) -> None:
    df.to_csv(out, index=False)
    print(f"Saved: {out}")


@dataclass
class Selections:
    protein: str = "protein"
    protein_backbone: str = "protein and backbone"
    ligand: str = "not protein and not resname SOL and not resname NA and not resname CL"
    # You can override ligand selection when you call scripts, e.g. "resname LIG"


def load_universe(top: str, traj: str) -> mda.Universe:
    return mda.Universe(top, traj)
