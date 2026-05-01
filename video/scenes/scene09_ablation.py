"""Scene 9 -- disentangling ablation: which design change carries the lift?

Bar chart with four bars, all built on the Track-1 v3 base, varying one of
{n_blocks, training-loss span}. Numbers from PAPER_DRAFT.md Section 6.3 table:

  v3 alone (no commit):                                73.0%
  ABL_A: n_blocks = 3, answer-span loss:               77.0%   (+4.0pp)
  ABL_B: n_blocks = 1, full-response loss:             73.0%   (+0.0pp)
  v3 full:  n_blocks = 3, full-response loss:          79.0%   (+6.0pp)

Headline: "Block coverage is the dominant lever."
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


CONDS = [
    ("v3 alone\nno commit", 0.73, "+0pp", MUTED),
    ("ABL_A\nn_blocks=3,\nanswer-span", 0.77, "+4pp", GOOD),
    ("ABL_B\nn_blocks=1,\nfull-response", 0.73, "+0pp", WARN),
    ("v3 full\nn_blocks=3,\nfull-response", 0.79, "+6pp", GOOD),
]


def _bar(height: float, color: str, width: float, fill_opacity: float = 0.45) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=max(0.05, height),
        corner_radius=0.06,
        stroke_color=color,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_width=2,
    )


class AblationScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Disentangling: which design change carries the lift?",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "all four conditions on Track-1 v3 base, varying one factor",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Chart layout (extra room at bottom for multi-line condition labels).
        chart_left, chart_right = -5.4, 5.4
        chart_bottom, chart_top = -1.6, 1.6
        plot_h = chart_top - chart_bottom

        x_axis = Line(
            LEFT * 5.4 + UP * chart_bottom,
            RIGHT * 5.4 + UP * chart_bottom,
            color=MUTED,
            stroke_width=2,
        )
        y_axis = Line(
            LEFT * 5.4 + UP * chart_bottom,
            LEFT * 5.4 + UP * chart_top,
            color=MUTED,
            stroke_width=2,
        )

        # Y-axis: from 0% to ~85% so the 79% bar leaves headroom.
        y_max = 0.85
        y_tick_lines = []
        y_tick_labels = []
        for t in (0.0, 0.20, 0.40, 0.60, 0.80):
            y_pos = chart_bottom + (t / y_max) * plot_h
            tl = Line(
                LEFT * 5.4 + UP * y_pos,
                RIGHT * 5.4 + UP * y_pos,
                color=MUTED,
                stroke_width=0.8,
            )
            tl.set_opacity(0.18)
            y_tick_lines.append(tl)
            lbl = body_text(f"{int(t*100)}%", size=16, color=MUTED)
            lbl.move_to(LEFT * 5.8 + UP * y_pos)
            y_tick_labels.append(lbl)

        usable_left, usable_right = chart_left + 0.7, chart_right - 0.4
        n = len(CONDS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 0.95

        bar_groups = []
        x_labels = []
        for i, (cond_label, acc, delta_str, color) in enumerate(CONDS):
            x_pos = usable_left + slot_w * (i + 0.5)
            h = (acc / y_max) * plot_h
            bar = _bar(h, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (chart_bottom + h / 2))

            val = body_text(
                f"{int(round(acc*100))}%", size=18, color=color, weight=BOLD
            )
            val.next_to(bar, UP, buff=0.10)

            delta = body_text(delta_str, size=16, color=color)
            delta.next_to(val, UP, buff=0.04)

            cond_lbl = body_text(cond_label, size=15, color=MUTED)
            cond_lbl.move_to(RIGHT * x_pos + UP * (chart_bottom - 0.55))

            bar_groups.append(VGroup(bar, val, delta))
            x_labels.append(cond_lbl)

        # Bottom callout.
        callout = body_text(
            "Block coverage is the dominant lever:  +4pp from where commit fires.",
            size=20,
            color=GOOD,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)

        assert_no_overlap(
            [title, sub, callout] + x_labels + y_tick_labels
        )

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(x_axis), FadeIn(y_axis),
            *[FadeIn(t) for t in y_tick_lines],
            *[FadeIn(l) for l in y_tick_labels],
            *[FadeIn(l) for l in x_labels],
            run_time=0.5,
        )
        for g in bar_groups:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), FadeIn(g[2]), run_time=0.55)
            self.wait(0.25)

        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
