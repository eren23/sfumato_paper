"""Re-export theme helpers from the shared visual_reps repo.

We extend sys.path so scenes can `from utils.theme_shim import ...` without
copy-pasting the helpers.  Scenes copied verbatim from visual_reps that still
say `from common.theme import ...` will also resolve via the path injection.
"""
from __future__ import annotations

import os
import sys

_VISUAL_REPS = os.path.expanduser(
    os.environ.get(
        "VISUAL_REPS_PATH",
        "/Users/eren/Documents/ai/visual_reps",
    )
)
if _VISUAL_REPS not in sys.path:
    sys.path.insert(0, _VISUAL_REPS)

# Re-export the helpers we need.
from common.theme import (  # noqa: E402
    ACCENT,
    ACCENT_2,
    ALIGN,
    BG,
    DETAIL,
    DIFF,
    ENCODER,
    FG,
    FONT,
    GOOD,
    MUTED,
    WARN,
    arrow_between,
    body_text,
    fade_out_all,
    patch_grid,
    pill,
    title_text,
)
from common.math_helpers import (  # noqa: E402
    comparison_table,
    complexity_bar,
)

__all__ = [
    "ACCENT",
    "ACCENT_2",
    "ALIGN",
    "BG",
    "DETAIL",
    "DIFF",
    "ENCODER",
    "FG",
    "FONT",
    "GOOD",
    "MUTED",
    "WARN",
    "arrow_between",
    "body_text",
    "comparison_table",
    "complexity_bar",
    "fade_out_all",
    "patch_grid",
    "pill",
    "title_text",
]
