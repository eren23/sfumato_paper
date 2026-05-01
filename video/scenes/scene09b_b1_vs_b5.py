"""Scene 9b -- branch aggregation absorbs the v2->v3 structural correction at b=5.

Numbers from PAPER_DRAFT.md / consensus_distillation.tex:

  c2c   (b=1, single-pass):     v2 = 70.5%   v3 = 79.0%    Delta = +8.5 pp
  cmajc (b=5, branch-vote):     v2 = 82.0%   v3 = 82.5%    Delta = +0.5 pp

Headline: "Single-pass inference is where structural correction pays."

Both v2 and v3 commit-LoRAs are trained on the same dataset; v3 fixes
two design errors (commit fires on multi-blocks, full-response loss).
At b=1 the structural fix matters; at b=5 stochastic branch aggregation
already recovers the consensus quality the late-block-only v2 misses,
and v3's structural advantage has nowhere to go.
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


# (label, accuracy, delta-vs-pair, color, panel)
CONDS = [
    ("commit v2\n(b=1, c2c)", 0.705, "70.5%", WARN,  "left"),
    ("commit v3\n(b=1, c2c)", 0.790, "79.0%", GOOD,  "left"),
    ("commit v2\n(b=5, cmajc)", 0.820, "82.0%", WARN,  "right"),
    ("commit v3\n(b=5, cmajc)", 0.825, "82.5%", GOOD,  "right"),
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


class B1VsB5Scene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Branch aggregation absorbs the v2->v3 structural correction at b=5",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "+8.5pp gap at b=1 collapses to a CI-overlap tie at b=5",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

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

        y_max = 0.90
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
        bars_by_panel: dict[str, list] = {"left": [], "right": []}
        for i, (cond_label, acc, val_str, color, panel) in enumerate(CONDS):
            x_pos = usable_left + slot_w * (i + 0.5)
            h = (acc / y_max) * plot_h
            bar = _bar(h, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (chart_bottom + h / 2))

            val = body_text(val_str, size=18, color=color, weight=BOLD)
            val.next_to(bar, UP, buff=0.10)

            cond_lbl = body_text(cond_label, size=14, color=MUTED)
            cond_lbl.move_to(RIGHT * x_pos + UP * (chart_bottom - 0.55))

            bar_groups.append(VGroup(bar, val))
            x_labels.append(cond_lbl)
            bars_by_panel[panel].append((x_pos, acc))

        # Panel separator (faint vertical line between b=1 and b=5 groups).
        sep_x = usable_left + slot_w * 2
        sep = Line(
            RIGHT * sep_x + UP * chart_bottom,
            RIGHT * sep_x + UP * (chart_top + 0.1),
            color=MUTED,
            stroke_width=0.8,
        )
        sep.set_opacity(0.25)

        # Panel labels.
        b1_label = body_text(
            "b=1 (single pass)", size=16, color=MUTED, weight=BOLD,
        )
        b1_x = usable_left + slot_w * 1
        b1_label.move_to(RIGHT * b1_x + UP * (chart_top + 0.35))

        b5_label = body_text(
            "b=5 (branch vote)", size=16, color=MUTED, weight=BOLD,
        )
        b5_x = usable_left + slot_w * 3
        b5_label.move_to(RIGHT * b5_x + UP * (chart_top + 0.35))

        # Delta annotations between paired bars.
        # b=1 delta: +8.5pp.
        b1_x1, b1_acc1 = bars_by_panel["left"][0]
        b1_x2, b1_acc2 = bars_by_panel["left"][1]
        b1_delta_y = chart_bottom + ((b1_acc1 + b1_acc2) / 2 / y_max) * plot_h
        b1_delta = body_text("+8.5 pp", size=18, color=GOOD, weight=BOLD)
        b1_delta.move_to(RIGHT * ((b1_x1 + b1_x2) / 2) + UP * (b1_delta_y - 0.10))

        # b=5 delta: +0.5pp (within CI overlap).
        b5_x1, b5_acc1 = bars_by_panel["right"][0]
        b5_x2, b5_acc2 = bars_by_panel["right"][1]
        b5_delta_y = chart_bottom + ((b5_acc1 + b5_acc2) / 2 / y_max) * plot_h
        b5_delta = body_text("+0.5 pp", size=18, color=MUTED, weight=BOLD)
        b5_delta.move_to(RIGHT * ((b5_x1 + b5_x2) / 2) + UP * (b5_delta_y - 0.10))
        b5_note = body_text(
            "(within CI)", size=14, color=MUTED,
        )
        b5_note.next_to(b5_delta, DOWN, buff=0.05)

        callout = body_text(
            "Single-pass inference is where structural correction pays.",
            size=20,
            color=GOOD,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)

        assert_no_overlap(
            [title, sub, callout, b1_label, b5_label]
            + x_labels + y_tick_labels
        )

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(x_axis), FadeIn(y_axis), FadeIn(sep),
            FadeIn(b1_label), FadeIn(b5_label),
            *[FadeIn(t) for t in y_tick_lines],
            *[FadeIn(l) for l in y_tick_labels],
            *[FadeIn(l) for l in x_labels],
            run_time=0.5,
        )
        for g in bar_groups:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), run_time=0.5)
            self.wait(0.2)

        self.play(FadeIn(b1_delta), run_time=0.4)
        self.wait(0.4)
        self.play(FadeIn(b5_delta), FadeIn(b5_note), run_time=0.4)
        self.wait(0.5)

        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
