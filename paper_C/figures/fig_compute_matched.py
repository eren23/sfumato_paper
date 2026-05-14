"""Figure — compute-matched diffusion-axis win (D2 multi-scale).

Composite (3k steps) vs pure-diffusion (6k steps, i.e. 2x training compute)
on the diffusion task. The compute-matched control rules out the
"more gradient signal" explanation for any composite win.

Anchors (from T0_PROBES_FINAL.md and existing probe1 results):
  scale  composite-3k  pure-diff-3k  pure-diff-6k (compute-matched)
  60M    5.74          6.19          ? (E3b)
  120M   5.68          6.10          ? (E3b)
  200M   5.42          6.13          6.11
  300M   5.35          6.08          ? (E3b)

After E3b lands, we fill in the 60M/120M/300M pure-diff-6k cells.

Outputs:
  paper_C/figures/fig_compute_matched.{png,pdf}
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


# Anchors from T0_PROBES_FINAL.md. None = not yet measured.
ANCHORS_COMPOSITE_3K = {"60M": 5.74, "120M": 5.68, "200M": 5.42, "300M": 5.35}
ANCHORS_PUREDIFF_3K  = {"60M": 6.19, "120M": 6.10, "200M": 6.13, "300M": 6.08}
ANCHORS_PUREDIFF_6K  = {"60M": None, "120M": None, "200M": 6.11, "300M": None}


def load_e3b():
    """Return dict {scale: mean_nll} for pure-diff-6k from E3b summary."""
    p = E5_RESULTS / "e3b_multiscale_d2" / "summary.json"
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    by_scale = {}
    for r in d:
        by_scale.setdefault(r["scale"], []).append(r["avg_nll"])
    return {s: sum(v) / len(v) for s, v in by_scale.items()}


def draw():
    fig, ax = plt.subplots(figsize=(8.0, 5.0))

    # Merge anchors with E3b
    e3b = load_e3b()
    pd6 = {**ANCHORS_PUREDIFF_6K, **{k: v for k, v in e3b.items() if k in ANCHORS_COMPOSITE_3K}}

    scales = ["60M", "120M", "200M", "300M"]
    x = np.arange(len(scales))
    w = 0.27

    comp = [ANCHORS_COMPOSITE_3K[s] for s in scales]
    pd3 = [ANCHORS_PUREDIFF_3K[s] for s in scales]
    pd6_vals = [pd6.get(s) for s in scales]

    ax.bar(x - w, comp, w, color="#1d4ed8", label="composite (3k steps)")
    ax.bar(x,     pd3, w, color="#9ca3af", label="pure-diff (3k steps)")
    # pure-diff 6k as the compute-matched control — only plot where data exists
    pd6_x = [xi + w for xi, v in zip(x, pd6_vals) if v is not None]
    pd6_y = [v for v in pd6_vals if v is not None]
    ax.bar(pd6_x, pd6_y, w, color="#b45309", label="pure-diff (6k, compute-matched)")

    # Cells with no data yet — draw a hatched placeholder
    for xi, v in zip(x, pd6_vals):
        if v is None:
            ax.bar(xi + w, 6.0, w, color="white", edgecolor="#b45309",
                   linestyle="--", linewidth=1.0, hatch="//", alpha=0.4)
            ax.text(xi + w, 6.05, "TBD", ha="center", fontsize=7, color="#b45309")

    ax.set_xticks(x)
    ax.set_xticklabels(scales)
    ax.set_xlabel("model scale")
    ax.set_ylabel("diffusion-axis NLL (lower = better)")
    ax.set_title("Compute-matched diffusion-axis: composite-3k vs pure-diff-6k")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(5.0, 6.7)

    # Annotate composite advantage at each scale where we have 6k data
    for xi, c, p in zip(x, comp, pd6_vals):
        if p is not None:
            d = c - p
            ax.annotate(f"$\\Delta = {d:+.2f}$", xy=(xi - w/2, c - 0.15),
                        ha="center", fontsize=8.5, color="#1d4ed8")

    fig.tight_layout()
    out_png = OUT_DIR / "fig_compute_matched.png"
    out_pdf = OUT_DIR / "fig_compute_matched.pdf"
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    print(f"wrote {out_png}")
    print(f"wrote {out_pdf}")
    print(f"E3b cells present: {sorted(e3b.keys())}")


if __name__ == "__main__":
    draw()
