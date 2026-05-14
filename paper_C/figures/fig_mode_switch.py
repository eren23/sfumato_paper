"""Figure — mode-switching inference lift at n=8.

Per-seed accuracy across 4 inference modes for composite vs ar_only at
200M-3k. After E3a lands we'll have n=8 seeds (70..74 fresh + 50/52/53
prior).

For now, plot what's in e5/results/e3a_probe5_n8/summary.json plus the
prior n=3 cells if we can backfill them.

Outputs:
  paper_C/figures/fig_mode_switch.{png,pdf}
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


# Prior Phase D anchors (from T0_PROBES_FINAL.md). Composite seeds 50/52/53.
PRIOR_COMPOSITE_64_32 = [0.0, 0.16, 0.12]    # 0/50, 8/50, 6/50  →  0%, 16%, 12%
PRIOR_ARONLY_64_32 = [0.04, 0.06, 0.0]       # 2%, 3%, 0% — approximations from the Phase-D summary
MODES = ["ar_only", "mode_switch_96_32", "mode_switch_64_32", "paired_64_64"]


def load_e3a():
    """Return list of per-seed rows with composite + ar_only accuracies per mode."""
    p = E5_RESULTS / "e3a_probe5_n8" / "summary.json"
    if not p.exists():
        return []
    return json.loads(p.read_text())


def draw():
    e3a = load_e3a()
    print(f"E3a seeds present: {len(e3a)}")

    # Per-mode aggregation across all seeds (E3a only for now; prior overnight
    # seeds 50/52/53 had different config, so we plot them as a separate group)
    comp_by_mode = {m: [] for m in MODES}
    ar_by_mode = {m: [] for m in MODES}
    for row in e3a:
        for m in MODES:
            if "composite" in row and m in row["composite"] and "accuracy" in row["composite"][m]:
                comp_by_mode[m].append(row["composite"][m]["accuracy"] * 100)
            if "ar_only" in row and m in row["ar_only"] and "accuracy" in row["ar_only"][m]:
                ar_by_mode[m].append(row["ar_only"][m]["accuracy"] * 100)

    fig, ax = plt.subplots(figsize=(8.5, 5.0))

    x = np.arange(len(MODES))
    w = 0.36

    comp_means = [np.mean(comp_by_mode[m]) if comp_by_mode[m] else 0.0 for m in MODES]
    ar_means   = [np.mean(ar_by_mode[m]) if ar_by_mode[m] else 0.0 for m in MODES]
    comp_sems  = [np.std(comp_by_mode[m]) / np.sqrt(len(comp_by_mode[m])) if comp_by_mode[m] else 0.0 for m in MODES]
    ar_sems    = [np.std(ar_by_mode[m]) / np.sqrt(len(ar_by_mode[m])) if ar_by_mode[m] else 0.0 for m in MODES]

    ax.bar(x - w/2, comp_means, w, yerr=comp_sems, color="#1d4ed8",
           label=f"composite (n={len(e3a)})", capsize=3)
    ax.bar(x + w/2, ar_means, w, yerr=ar_sems, color="#9ca3af",
           label=f"ar_only (n={len(e3a)})", capsize=3)

    # Annotate per-mode delta
    for xi, c, a in zip(x, comp_means, ar_means):
        d = c - a
        col = "#065f46" if d > 0 else "#b45309"
        sign = "+" if d > 0 else ""
        ax.annotate(f"{sign}{d:.1f}pp", xy=(xi, max(c, a) + 0.5),
                    ha="center", fontsize=8.5, color=col)

    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("_", " ").replace("mode switch", "ms") for m in MODES])
    ax.set_xlabel("inference mode")
    ax.set_ylabel("GSM8K-dev N=50 accuracy (%)")
    ax.set_title(f"Mode-switching inference lift at 200M-3k (E3a fresh seeds, n={len(e3a)})")
    ax.legend(loc="upper left", frameon=False)
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    out_png = OUT_DIR / "fig_mode_switch.png"
    out_pdf = OUT_DIR / "fig_mode_switch.pdf"
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    print(f"wrote {out_png}")
    print(f"wrote {out_pdf}")


if __name__ == "__main__":
    draw()
