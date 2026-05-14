"""Figure — data-efficiency crossover for composite vs ar_only AR-NLL.

Headline result of paper_C: composite wins at 500 problems (-0.40 NLL,
5.7sigma), ties at 1000 problems, loses by +0.13 at 2000, +0.26 at 4000,
+0.22 at 7500.

After E3c (the 800/1200/1500 refinement) lands, we extend with three new
data points and re-fit the curve.

Sources:
  - 500 / 2000 / 4000 / 1000 / 7500 → existing T0_PROBES_FINAL.md
  - 800 / 1200 / 1500 → e5/results/e3c_d3_crossover/summary.json (TODO)

Outputs:
  paper_C/figures/fig_data_curve.{png,pdf}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUT_DIR = HERE
E5_RESULTS = Path("/Users/eren/Documents/ai/sfumato/e5/results")


# Canonical Phase-D anchors (from T0_PROBES_FINAL.md). Values are mean AR-NLL.
ANCHORS = [
    # (size, composite_mean, ar_mean, n_seeds)
    (500, 4.49, 4.89, 3),
    (1000, 3.31, 3.32, 3),
    (2000, 3.02, 2.89, 3),
    (4000, 2.98, 2.71, 3),
    (7500, 2.80, 2.57, 8),
]


def load_e3c():
    """Return list of (size, composite_mean, ar_mean, n) from E3c if available."""
    p = E5_RESULTS / "e3c_d3_crossover" / "summary.json"
    if not p.exists():
        return []
    d = json.loads(p.read_text())
    by_size = {}
    for r in d:
        by_size.setdefault((r["size"], r["variant"]), []).append(r["avg_nll"])
    sizes = sorted({s for (s, _) in by_size})
    rows = []
    for size in sizes:
        comp = by_size.get((size, "composite"), [])
        ar = by_size.get((size, "ar_only"), [])
        if comp and ar:
            rows.append((size, sum(comp) / len(comp), sum(ar) / len(ar), len(comp)))
    return rows


def draw():
    fig, ax = plt.subplots(figsize=(7.5, 4.8))

    # Combine anchors + E3c
    rows = sorted(ANCHORS + load_e3c(), key=lambda r: r[0])
    xs = [r[0] for r in rows]
    deltas = [r[1] - r[2] for r in rows]
    comp = [r[1] for r in rows]
    ar = [r[2] for r in rows]

    # Composite vs AR curves (top)
    ax.plot(xs, comp, marker="o", color="#1d4ed8", linewidth=2.0, label="composite")
    ax.plot(xs, ar, marker="s", color="#9ca3af", linewidth=2.0, label="ar_only")

    # Crossover line at delta=0
    ax.axhline(0, color="#374151", linewidth=0.6, linestyle=":", alpha=0.0)

    ax.set_xscale("log")
    ax.set_xticks([500, 1000, 2000, 4000, 7500])
    ax.set_xticklabels(["500", "1k", "2k", "4k", "7.5k"])
    ax.set_xlabel("training data (GSM8K problems, log scale)")
    ax.set_ylabel("AR-axis NLL on held-out chunk (lower = better)")
    ax.set_title("Composite vs AR-only: data-efficiency curve at 200M, 3k steps")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", frameon=False)

    # Delta annotations
    for x, c, a in zip(xs, comp, ar):
        d = c - a
        ymid = (c + a) / 2
        sign = "+" if d > 0 else ""
        col = "#b45309" if d > 0 else "#065f46"
        ax.annotate(f"$\\Delta = {sign}{d:.2f}$",
                    xy=(x, ymid), xytext=(0, 0), textcoords="offset points",
                    fontsize=8.5, color=col, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor="none", alpha=0.85))

    # Annotate the crossover
    ax.annotate("crossover\n(~1k problems)", xy=(1000, 3.31), xytext=(1500, 4.2),
                fontsize=9, color="#1d4ed8",
                arrowprops=dict(arrowstyle="->", color="#1d4ed8", lw=0.8))

    fig.tight_layout()
    out_png = OUT_DIR / "fig_data_curve.png"
    out_pdf = OUT_DIR / "fig_data_curve.pdf"
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    print(f"wrote {out_png}")
    print(f"wrote {out_pdf}")
    print(f"included E3c data: {bool(load_e3c())}")


if __name__ == "__main__":
    draw()
