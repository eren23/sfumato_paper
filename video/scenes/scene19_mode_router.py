"""Scene 19 -- D1 mode router honest negative.

Three bars on a 20-problem x 12-condition substrate (LOOCV), drawn on
a truncated y-axis (acc 50-92) so labels do not collide with the
title and the delta callout has room above the bar tops:

  best fixed (c2empty / cmajc):     75%
  D1 LR-bandit (LOOCV):             65%   (-10 pp vs best fixed, LOSS)
  oracle (any-condition correct):   85%

Numbers from sections/mode_router.tex Table 1 and
phase2/spikes/D1-mode-router/RESULT.md.

Headline: "the offline-replay mode router loses -- same pathology as
the verifier sweep."
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    GrowFromEdge,
    LEFT,
    Line,
    RIGHT,
    RoundedRectangle,
    Scene,
    UP,
    VGroup,
)

from utils.theme_shim import (
    ACCENT,
    BG,
    DIFF,
    FG,
    GOOD,
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)
from utils.layout import assert_no_overlap


# (label, sub_label, value_str, value, color)
ROWS = [
    ("best fixed",   "always-c2empty",         "75%",  75.0, DIFF),
    ("D1 bandit",    "logistic + LOOCV",       "65%",  65.0, WARN),
    ("best-case",    "any-condition correct",  "85%",  85.0, GOOD),
]


# Truncated y-axis -- compresses 0-50 so the 65/75/85 spread is visible
ACC_FLOOR = 50.0
ACC_CEIL  = 92.0
BAR_FLOOR = -2.0
BAR_CEIL  =  1.05


def _bar(height_abs, color, width):
    return RoundedRectangle(
        width=width,
        height=max(0.05, height_abs),
        corner_radius=0.06,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.45,
        stroke_width=2,
    )


def _y_for(acc: float) -> float:
    return BAR_FLOOR + (acc - ACC_FLOOR) * (BAR_CEIL - BAR_FLOOR) / (ACC_CEIL - ACC_FLOOR)


class ModeRouterScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Same pathology, second sub-problem -- per-problem mode router",
            size=22,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "20 problems x 12 conditions; LR over question features"
            " (length, numeric tokens, TF-IDF), LOOCV",
            size=14,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        chart_left, chart_right = -5.0, 5.0
        usable_left, usable_right = chart_left + 0.5, chart_right - 0.5
        n = len(ROWS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 1.55

        # truncated-axis indicator on the left edge
        axis_line = Line(
            LEFT * 5.7 + UP * BAR_FLOOR,
            LEFT * 5.7 + UP * BAR_CEIL,
            color=MUTED,
            stroke_width=1.5,
        )
        axis_lo = body_text(f"{int(ACC_FLOOR)}%", size=12, color=MUTED)
        axis_lo.move_to(LEFT * 6.05 + UP * BAR_FLOOR)
        axis_hi = body_text(f"{int(ACC_CEIL)}%", size=12, color=MUTED)
        axis_hi.move_to(LEFT * 6.05 + UP * BAR_CEIL)
        break_lo = Line(
            LEFT * 5.85 + UP * (BAR_FLOOR - 0.18),
            LEFT * 5.55 + UP * (BAR_FLOOR - 0.08),
            color=MUTED,
            stroke_width=1.5,
        )
        break_hi = Line(
            LEFT * 5.85 + UP * (BAR_FLOOR - 0.10),
            LEFT * 5.55 + UP * (BAR_FLOOR + 0.00),
            color=MUTED,
            stroke_width=1.5,
        )

        bar_groups = []
        labels = []
        for i, (label, sub_lbl, val_str, val, color) in enumerate(ROWS):
            x_pos = usable_left + slot_w * (i + 0.5)
            top_y = _y_for(val)
            h_abs = top_y - BAR_FLOOR
            bar = _bar(h_abs, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (BAR_FLOOR + h_abs / 2))

            val_lbl = body_text(val_str, size=22, color=color, weight=BOLD)
            val_lbl.next_to(bar, UP, buff=0.10)

            cond = body_text(label, size=18, color=FG, weight=BOLD)
            cond.move_to(RIGHT * x_pos + UP * (BAR_FLOOR - 0.42))

            tag = body_text(sub_lbl, size=12, color=MUTED)
            tag.move_to(RIGHT * x_pos + UP * (BAR_FLOOR - 0.78))

            bar_groups.append(VGroup(bar, val_lbl))
            labels.extend([cond, tag])

        delta_label = body_text(
            "delta = -10 pp vs best fixed   ->   pre-reg LOSS",
            size=18,
            color=WARN,
            weight=BOLD,
        )
        delta_label.move_to(0 * RIGHT + UP * (BAR_CEIL + 0.65))

        callout = body_text(
            "Same pathology as the verifier sweep:"
            " small N + large action space\n"
            "+ surface text features cannot recover the best-case ceiling.",
            size=17,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.40)

        assert_no_overlap(
            [title, sub, delta_label, callout, axis_lo, axis_hi] + labels
        )

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(axis_line),
            FadeIn(axis_lo),
            FadeIn(axis_hi),
            FadeIn(break_lo),
            FadeIn(break_hi),
            *[FadeIn(l) for l in labels],
            run_time=0.4,
        )
        for g in bar_groups:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), run_time=0.55)
            self.wait(0.2)
        self.play(FadeIn(delta_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.55)
        self.wait(3.5)

        fade_out_all(self)
