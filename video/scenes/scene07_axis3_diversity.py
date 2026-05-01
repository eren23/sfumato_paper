"""Scene 7 -- Axis 3: format-augmented training EXPANDS sampling diversity.

Branch-agreement-rate histogram (5 bins) for {base on test, Track-1 v2 +
commit v2}. Numbers from PAPER_DRAFT.md Section 5 (lines 105-111).

  bin            | base   | v2+commit
  5/5 same       | 51.5%  | 47.5%
  4/5 unique     |  6.0%  |  8.5%
  3/5 unique     | 11.5%  | 18.0%
  2/5 unique     | 27.5%  | 19.5%
  5/5 unique     |  3.5%  |  6.5%
  mean unique    | 1.825  | 2.07
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


BINS = ["5/5 same", "4/5 unique", "3/5 unique", "2/5 unique", "5/5 unique"]
BASE = [0.515, 0.060, 0.115, 0.275, 0.035]
V2C = [0.475, 0.085, 0.180, 0.195, 0.065]


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


class Axis3DiversityScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Axis 3: format-augmented training EXPANDS diversity",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "branch-agreement distribution, b=5 t=0.7, GSM8K-test N=200",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Chart frame.
        chart_left, chart_right = -5.4, 5.4
        chart_bottom, chart_top = -2.2, 1.4
        plot_h = chart_top - chart_bottom

        x_axis = Line(
            LEFT * 5.4 + DOWN * 2.2,
            RIGHT * 5.4 + DOWN * 2.2,
            color=MUTED,
            stroke_width=2,
        )
        y_axis = Line(
            LEFT * 5.4 + DOWN * 2.2,
            LEFT * 5.4 + UP * 1.4,
            color=MUTED,
            stroke_width=2,
        )

        # Y ticks at 0/15/30/45/60% (max ~52%, so 60% ceiling)
        y_max = 0.60
        y_tick_lines = []
        y_tick_labels = []
        for t in (0.0, 0.15, 0.30, 0.45, 0.60):
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
        n = len(BINS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 0.42

        base_bars = []
        v2c_bars = []
        x_labels = []
        for i, (bin_label, base_p, v2c_p) in enumerate(zip(BINS, BASE, V2C)):
            x_center = usable_left + slot_w * (i + 0.5)
            x_b = x_center - bar_w * 0.65
            x_v = x_center + bar_w * 0.65

            h_b = (base_p / y_max) * plot_h
            base_bar = _bar(h_b, MUTED, width=bar_w, fill_opacity=0.40)
            base_bar.move_to(RIGHT * x_b + UP * (chart_bottom + h_b / 2))
            base_val = body_text(
                f"{int(round(base_p*1000))/10:g}", size=14, color=MUTED
            )
            base_val.next_to(base_bar, UP, buff=0.06)

            h_v = (v2c_p / y_max) * plot_h
            v2c_bar = _bar(h_v, GOOD, width=bar_w, fill_opacity=0.55)
            v2c_bar.move_to(RIGHT * x_v + UP * (chart_bottom + h_v / 2))
            v2c_val = body_text(
                f"{int(round(v2c_p*1000))/10:g}", size=14, color=GOOD, weight=BOLD
            )
            v2c_val.next_to(v2c_bar, UP, buff=0.06)

            cond_lbl = body_text(bin_label, size=16, color=MUTED)
            cond_lbl.move_to(RIGHT * x_center + UP * (chart_bottom - 0.32))

            base_bars.append(VGroup(base_bar, base_val))
            v2c_bars.append(VGroup(v2c_bar, v2c_val))
            x_labels.append(cond_lbl)

        # Legend
        leg_base_swatch = RoundedRectangle(
            width=0.32, height=0.20, corner_radius=0.04,
            stroke_color=MUTED, fill_color=MUTED, fill_opacity=0.40, stroke_width=2,
        )
        leg_base_text = body_text("base", size=16, color=MUTED)
        leg_base = VGroup(leg_base_swatch, leg_base_text).arrange(RIGHT, buff=0.15)
        leg_base.move_to(RIGHT * 2.4 + UP * 1.05)

        leg_v_swatch = RoundedRectangle(
            width=0.32, height=0.20, corner_radius=0.04,
            stroke_color=GOOD, fill_color=GOOD, fill_opacity=0.55, stroke_width=2,
        )
        leg_v_text = body_text("Track-1 v2 + commit v2", size=16, color=GOOD)
        leg_v = VGroup(leg_v_swatch, leg_v_text).arrange(RIGHT, buff=0.15)
        leg_v.next_to(leg_base, RIGHT, buff=0.6)

        # Bottom callout
        callout = body_text(
            "Mean unique answers / problem:  1.825  ->  2.07   (+13%)",
            size=20,
            color=GOOD,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.45)

        assert_no_overlap(
            [title, sub, leg_base, leg_v, callout] + x_labels + y_tick_labels
        )

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(x_axis), FadeIn(y_axis),
            *[FadeIn(t) for t in y_tick_lines],
            *[FadeIn(l) for l in y_tick_labels],
            *[FadeIn(l) for l in x_labels],
            FadeIn(leg_base), FadeIn(leg_v),
            run_time=0.5,
        )
        for b in base_bars:
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), run_time=0.30)
        for v in v2c_bars:
            self.play(GrowFromEdge(v[0], DOWN), FadeIn(v[1]), run_time=0.35)

        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.6)
        self.wait(3.0)

        fade_out_all(self)
