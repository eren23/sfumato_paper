"""Layout assertions for the Sfumato paper video.

Defensive checks that fire at scene-construction time so a broken layout
cannot silently render with overlapping text mobjects.
"""
from __future__ import annotations

from typing import Iterable


def _bbox(mobject) -> tuple[float, float, float, float]:
    """Return (left, right, bottom, top) of a mobject in scene coordinates."""
    return (
        mobject.get_left()[0],
        mobject.get_right()[0],
        mobject.get_bottom()[1],
        mobject.get_top()[1],
    )


def _intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float], eps: float = 0.02) -> bool:
    al, ar, ab, at = a
    bl, br, bb, bt = b
    horiz = (al < br - eps) and (bl < ar - eps)
    vert = (ab < bt - eps) and (bb < at - eps)
    return horiz and vert


def _label(mobject) -> str:
    txt = getattr(mobject, "text", None) or getattr(mobject, "tex_string", None)
    if txt is not None:
        return f"{type(mobject).__name__}({txt[:40]!r})"
    return type(mobject).__name__


def assert_no_overlap(mobjects: Iterable, eps: float = 0.02) -> None:
    """Pairwise bbox-intersection check; raises AssertionError on collision."""
    items = [m for m in mobjects if m is not None]
    bboxes = [_bbox(m) for m in items]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if _intersects(bboxes[i], bboxes[j], eps=eps):
                raise AssertionError(
                    f"Layout overlap: {_label(items[i])} <-> {_label(items[j])} "
                    f"bboxes={bboxes[i]} {bboxes[j]}"
                )
