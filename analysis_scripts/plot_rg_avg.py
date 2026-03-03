#!/usr/bin/env python3
from __future__ import annotations

import argparse
import numpy as np
import matplotlib.pyplot as plt

from common_xvg import align_replicas_by_time, time_to_ns, mean_std


def main():
    p = argparse.ArgumentParser(description="Plot mean ± std radius of gyration across replicas (.xvg).")
    p.add_argument("--xvg", nargs="+", required=True, help="Rg .xvg files (e.g., rg1.xvg rg2.xvg rg3.xvg)")
    p.add_argument("--time-unit", default="ps", choices=["ps", "ns"], help="Time unit in the XVG files.")
    p.add_argument("--out", default="rg_mean.png", help="Output figure filename.")
    p.add_argument("--csv", default="rg_mean.csv", help="Output CSV filename.")
    p.add_argument("--title", default="Radius of gyration", help="Plot title.")
    p.add_argument("--ylim", nargs=2, type=float, default=None, metavar=("YMIN", "YMAX"), help="Optional y-limits.")
    p.add_argument("--xlim", nargs=2, type=float, default=None, metavar=("XMIN", "XMAX"), help="Optional x-limits.")
    args = p.parse_args()

    aligned = align_replicas_by_time(args.xvg, time_col=0, y_col=1)
    t_ns = time_to_ns(aligned.t_common, args.time_unit)

    mean_y, std_y = mean_std(aligned.y_matrix, ddof=1)

    # global stats over all points & replicas
    all_vals = aligned.y_matrix.ravel()
    print(f"Global mean Rg = {np.mean(all_vals):.4f} nm; global std = {np.std(all_vals, ddof=1):.4f} nm")

    # save CSV
    np.savetxt(
        args.csv,
        np.column_stack([t_ns, mean_y, std_y]),
        delimiter=",",
        header="time_ns,mean_rg_nm,std_rg_nm",
        comments=""
    )

    # plot (no explicit colors)
    plt.figure(figsize=(8, 5))
    plt.plot(t_ns, mean_y, linewidth=1.0, label="Mean")
    plt.fill_between(t_ns, mean_y - std_y, mean_y + std_y, alpha=0.25, label="± SD")
    plt.xlabel("Time (ns)")
    plt.ylabel("Radius of gyration (nm)")
    plt.title(args.title)
    if args.ylim:
        plt.ylim(args.ylim)
    if args.xlim:
        plt.xlim(args.xlim)
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out, dpi=300)
    plt.close()
    print(f"Saved: {args.out} and {args.csv}")


if __name__ == "__main__":
    main()
