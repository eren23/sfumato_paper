"""Scene 3 -- GSM8K N=200 results: accuracy vs FLOPs (log).

Port of visual_reps/concepts/sfumato_e4_iterative_thinking/scenes/scene03_results.py
with three changes:
  1. Imports rerouted through utils.theme_shim.
  2. cmaj headline accuracy aligned to PAPER_DRAFT.md Section 6.5 (test cmaj=79%).
     The 80% number was the dev-set / pre-reg target; we use the test-set value
     here to set up the "c2c-vs-cmaj gap" later in the video.
  3. The closing callout switches from "inverse hybrid wins" to the puzzle
     this video unpacks: "C3 < C2 by 10pp -- the AR plan damages LLaDA".
"""
from __future__ import annotations

import math

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    GrowFromEdge,
    LaggedStart,
    LEFT,
    Line,
    ORIGIN,
    RIGHT,
    RoundedRectangle,
    Scene,
    UP,
    VGroup,
)

from utils.theme_shim import (
    ACCENT,
    ACCENT_2,
    ALIGN,
    BG,
    DETAIL,
    DIFF,
    FG,
    GOOD,
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)


def _bar(height: float, color: str, width: float = 0.95) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=max(0.05, height),
        corner_radius=0.06,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.45,
        stroke_width=2,
    )


class SfumatoResultsScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("GSM8K, N=200: accuracy vs compute", size=30, color=ACCENT)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.45)

        # Layout: chart area roughly LEFT 4..RIGHT 4, BOTTOM y=-2.6, TOP y=1.8
        x_left, x_right = -4.5, 4.5
        y_bottom, y_top = -2.6, 1.8
        plot_h = y_top - y_bottom

        # Axes
        x_axis = Line(LEFT * 4.5 + DOWN * 2.6, RIGHT * 4.5 + DOWN * 2.6, color=MUTED, stroke_width=2)
        y_axis = Line(LEFT * 4.5 + DOWN * 2.6, LEFT * 4.5 + UP * 1.8, color=MUTED, stroke_width=2)

        # Y gridlines + tick labels first so we can place the axis labels
        # past them without overlap.
        y_ticks = [0.0, 0.25, 0.5, 0.75, 1.0]
        y_tick_lines = []
        y_tick_labels = []
        for t in y_ticks:
            y_pos = y_bottom + t * plot_h
            tl = Line(
                LEFT * 4.5 + RIGHT * 0.0 + UP * y_pos,
                RIGHT * 4.5 + UP * y_pos,
                color=MUTED,
                stroke_width=0.8,
            )
            tl.set_opacity(0.18)
            y_tick_lines.append(tl)
            lbl = body_text(f"{int(t*100)}%", size=16, color=MUTED)
            lbl.move_to(LEFT * 4.85 + UP * y_pos)
            y_tick_labels.append(lbl)

        # Axis labels: y rotated and placed LEFT of the tick labels;
        # x placed BELOW where the tick labels will land (further down).
        y_label = body_text("accuracy", size=16, color=MUTED)
        y_label.rotate(90 * 3.14159265 / 180)
        y_label.move_to(LEFT * 5.55 + UP * (y_bottom + plot_h / 2))
        # x_label drops well below the tick label row (which lands ~0.3 units
        # below y_bottom). Hard-coded buffer chosen empirically from rendered
        # frames so "(log scale)" never collides with the "1e13" tick label.
        x_label = body_text("FLOPs / sample (log scale)", size=16, color=MUTED)
        x_label.move_to(DOWN * 3.55)

        self.play(FadeIn(x_axis), FadeIn(y_axis), FadeIn(x_label), FadeIn(y_label), run_time=0.4)

        self.play(
            *[FadeIn(t) for t in y_tick_lines],
            *[FadeIn(l) for l in y_tick_labels],
            run_time=0.35,
        )

        # FLOPs in log10 -- map [11.0 .. 15.0] to [x_left+0.6 .. x_right-0.4]
        log_lo, log_hi = 11.0, 15.0
        usable_left = x_left + 0.6
        usable_right = x_right - 0.4

        def x_for_log(lf: float) -> float:
            return usable_left + (lf - log_lo) / (log_hi - log_lo) * (usable_right - usable_left)

        # X axis ticks at 1e11, 1e12, 1e13, 1e14, 1e15
        x_tick_labels = []
        for exp in (11, 12, 13, 14, 15):
            x_pos = x_for_log(exp)
            tick = Line(
                RIGHT * 0 + UP * y_bottom,
                RIGHT * 0 + UP * (y_bottom - 0.10),
                color=MUTED,
                stroke_width=1.5,
            )
            tick.move_to(RIGHT * x_pos + UP * (y_bottom - 0.05))
            lbl = body_text(f"1e{exp}", size=16, color=MUTED)
            lbl.next_to(tick, DOWN, buff=0.05)
            x_tick_labels.append(VGroup(tick, lbl))
        self.play(*[FadeIn(t) for t in x_tick_labels], run_time=0.3)

        # Conditions: (label, accuracy, flops, color, family).
        # Numbers from PAPER_DRAFT.md Section 3.1 (base hierarchy) and 6.5
        # (test cmaj = 79%).
        data = [
            ("C1", 0.34, 2.81e11, ACCENT_2, "base"),
            ("C2", 0.74, 1.31e14, DIFF, "base"),
            ("C3", 0.64, 1.31e14, ACCENT, "base"),
            ("C4", 0.54, 2.63e14, WARN, "base"),
            ("cmaj b=5", 0.79, 6.57e14, DETAIL, "branch"),
        ]

        bars = []
        bar_groups = []
        bar_w = 0.55
        x_offsets = {
            "C2": -bar_w * 0.7,
            "C3": +bar_w * 0.7,
            "C4": -bar_w * 0.4,
            "cmaj b=5": +bar_w * 0.25,
        }

        for code, acc, flops, color, _family in data:
            lf = math.log10(flops)
            x_pos = x_for_log(lf) + x_offsets.get(code, 0.0)
            h = acc * plot_h
            bar = _bar(h, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (y_bottom + h / 2))
            label = body_text(code, size=16, color=color, weight=BOLD)
            label.next_to(bar, UP, buff=0.08)
            acc_label = body_text(f"{int(acc*100)}%", size=16, color=color)
            acc_label.next_to(label, UP, buff=0.04)
            bars.append(bar)
            bar_groups.append(VGroup(bar, label, acc_label))

        for g in bar_groups:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), FadeIn(g[2]), run_time=0.55)
            self.wait(0.3)

        # Closing callout: the puzzle the rest of the video unpacks.
        callout = body_text(
            "C3 < C2 by 10pp -- the AR plan damages LLaDA.",
            size=22,
            color=WARN,
            weight=BOLD,
        )
        callout.move_to(DOWN * 3.85)
        self.play(FadeIn(callout, shift=UP * 0.15), run_time=0.7)
        self.wait(3.0)

        fade_out_all(self)
