"""Scene 5 -- Axis 1: interface-format brittleness is trainably fixable.

Two phases (with fade_out_all between):
  Phase A: base prefix-damage hierarchy on LLaDA. 5 bars.
  Phase B: same chart with Track-1 v2 LoRA bars next to each base bar; the
           spread on static prefixes (C2/C2hint/C2empty) collapses 8pp -> 3pp.

All numbers from PAPER_DRAFT.md Section 3.1 (base) and Section 3.2 (v2).
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
    ACCENT_2,
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


# Numbers from PAPER_DRAFT.md.
CONDS = ["C2", "C2hint", "C2empty", "C3p Q-0.5B", "C3p Q-1.5B"]
BASE = [0.74, 0.68, 0.66, 0.64, 0.60]
V2 = [0.705, 0.735, 0.730, 0.600, 0.670]


class Axis1BrittlenessScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        # ----- Phase A: base prefix-damage hierarchy ----------------------
        title_a = title_text(
            "Base prefix-damage: 8pp spread",
            size=30,
            color=WARN,
        )
        title_a.to_edge(UP, buff=0.5)

        sub_a = body_text(
            "LLaDA-8B-Instruct, GSM8K-test, N=200, k=64",
            size=18,
            color=MUTED,
        )
        sub_a.next_to(title_a, DOWN, buff=0.18)

        # Chart frame
        chart_left, chart_right = -5.0, 5.0
        chart_bottom, chart_top = -2.6, 1.4
        plot_h = chart_top - chart_bottom
        x_axis = Line(
            LEFT * 5.0 + DOWN * 2.6,
            RIGHT * 5.0 + DOWN * 2.6,
            color=MUTED,
            stroke_width=2,
        )
        y_axis = Line(
            LEFT * 5.0 + DOWN * 2.6,
            LEFT * 5.0 + UP * 1.4,
            color=MUTED,
            stroke_width=2,
        )

        # Y ticks
        y_tick_lines = []
        y_tick_labels = []
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            y_pos = chart_bottom + t * plot_h
            tl = Line(
                LEFT * 5.0 + UP * y_pos,
                RIGHT * 5.0 + UP * y_pos,
                color=MUTED,
                stroke_width=0.8,
            )
            tl.set_opacity(0.18)
            y_tick_lines.append(tl)
            lbl = body_text(f"{int(t*100)}%", size=16, color=MUTED)
            lbl.move_to(LEFT * 5.4 + UP * y_pos)
            y_tick_labels.append(lbl)

        # Layout 5 base bars across x in [chart_left+0.7, chart_right-0.5]
        usable_left, usable_right = chart_left + 0.8, chart_right - 0.5
        n = len(CONDS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 0.7

        base_bars = []
        x_labels = []
        for i, (cond, acc) in enumerate(zip(CONDS, BASE)):
            x_pos = usable_left + slot_w * (i + 0.5)
            h = acc * plot_h
            bar = _bar(h, WARN, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (chart_bottom + h / 2))
            val = body_text(f"{int(round(acc*100))}%", size=16, color=WARN, weight=BOLD)
            val.next_to(bar, UP, buff=0.08)
            cond_lbl = body_text(cond, size=16, color=MUTED)
            cond_lbl.next_to(bar, DOWN, buff=0.18).move_to(
                RIGHT * x_pos + UP * (chart_bottom - 0.32)
            )
            base_bars.append(VGroup(bar, val))
            x_labels.append(cond_lbl)

        # Pre-construction overlap check on titles + axes labels (bars
        # animate in via GrowFromEdge so we just check static text/labels).
        assert_no_overlap([title_a, sub_a] + x_labels + y_tick_labels)

        self.play(FadeIn(title_a, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub_a, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(x_axis), FadeIn(y_axis),
            *[FadeIn(t) for t in y_tick_lines],
            *[FadeIn(l) for l in y_tick_labels],
            *[FadeIn(l) for l in x_labels],
            run_time=0.5,
        )
        for g in base_bars:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), run_time=0.45)
            self.wait(0.18)

        # 8pp spread annotation across C2..C2empty
        spread = body_text(
            "spread: 74% - 66% = 8pp on static prefixes",
            size=20,
            color=WARN,
            weight=BOLD,
        )
        spread.to_edge(DOWN, buff=0.4)
        assert_no_overlap([title_a, sub_a, spread] + x_labels)
        self.play(FadeIn(spread, shift=UP * 0.1), run_time=0.5)
        self.wait(2.5)

        fade_out_all(self)

        # ----- Phase B: post-Track-1 v2 ----------------------------------
        title_b = title_text(
            "After Track-1 v2 LoRA: spread flattens to ~3pp on static prefixes",
            size=24,
            color=GOOD,
        )
        title_b.to_edge(UP, buff=0.5)

        sub_b = body_text(
            "r=8 prefix-robust LoRA, 4/7 modules, ~10M params",
            size=18,
            color=MUTED,
        )
        sub_b.next_to(title_b, DOWN, buff=0.18)

        # Re-create axes
        x_axis2 = Line(
            LEFT * 5.0 + DOWN * 2.6,
            RIGHT * 5.0 + DOWN * 2.6,
            color=MUTED,
            stroke_width=2,
        )
        y_axis2 = Line(
            LEFT * 5.0 + DOWN * 2.6,
            LEFT * 5.0 + UP * 1.4,
            color=MUTED,
            stroke_width=2,
        )
        y_tick_lines2 = []
        y_tick_labels2 = []
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            y_pos = chart_bottom + t * plot_h
            tl = Line(
                LEFT * 5.0 + UP * y_pos,
                RIGHT * 5.0 + UP * y_pos,
                color=MUTED,
                stroke_width=0.8,
            )
            tl.set_opacity(0.18)
            y_tick_lines2.append(tl)
            lbl = body_text(f"{int(t*100)}%", size=16, color=MUTED)
            lbl.move_to(LEFT * 5.4 + UP * y_pos)
            y_tick_labels2.append(lbl)

        # Two bars per condition: base (WARN, ghosted) + v2 (GOOD).
        bar_w2 = 0.32
        base_pairs = []
        v2_pairs = []
        x_labels2 = []
        for i, (cond, base_acc, v2_acc) in enumerate(zip(CONDS, BASE, V2)):
            x_center = usable_left + slot_w * (i + 0.5)
            x_base = x_center - bar_w2 * 0.65
            x_v2 = x_center + bar_w2 * 0.65

            h_b = base_acc * plot_h
            base_bar = _bar(h_b, WARN, width=bar_w2, fill_opacity=0.25)
            base_bar.move_to(RIGHT * x_base + UP * (chart_bottom + h_b / 2))

            h_v = v2_acc * plot_h
            v2_bar = _bar(h_v, GOOD, width=bar_w2, fill_opacity=0.55)
            v2_bar.move_to(RIGHT * x_v2 + UP * (chart_bottom + h_v / 2))

            v_label = body_text(
                f"{int(round(v2_acc*100))}",
                size=14,
                color=GOOD,
                weight=BOLD,
            )
            v_label.next_to(v2_bar, UP, buff=0.06)

            cond_lbl = body_text(cond, size=16, color=MUTED)
            cond_lbl.move_to(RIGHT * x_center + UP * (chart_bottom - 0.32))

            base_pairs.append(base_bar)
            v2_pairs.append(VGroup(v2_bar, v_label))
            x_labels2.append(cond_lbl)

        # Legend
        leg_base_swatch = RoundedRectangle(
            width=0.32, height=0.20, corner_radius=0.04,
            stroke_color=WARN, fill_color=WARN, fill_opacity=0.25, stroke_width=2,
        )
        leg_base_text = body_text("base", size=16, color=WARN)
        leg_base = VGroup(leg_base_swatch, leg_base_text).arrange(RIGHT, buff=0.15)
        leg_base.move_to(RIGHT * 2.3 + UP * 1.05)

        leg_v2_swatch = RoundedRectangle(
            width=0.32, height=0.20, corner_radius=0.04,
            stroke_color=GOOD, fill_color=GOOD, fill_opacity=0.55, stroke_width=2,
        )
        leg_v2_text = body_text("Track-1 v2", size=16, color=GOOD)
        leg_v2 = VGroup(leg_v2_swatch, leg_v2_text).arrange(RIGHT, buff=0.15)
        leg_v2.next_to(leg_base, RIGHT, buff=0.6)

        assert_no_overlap(
            [title_b, sub_b, leg_base, leg_v2] + x_labels2 + y_tick_labels2
        )

        self.play(FadeIn(title_b, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub_b, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(x_axis2), FadeIn(y_axis2),
            *[FadeIn(t) for t in y_tick_lines2],
            *[FadeIn(l) for l in y_tick_labels2],
            *[FadeIn(l) for l in x_labels2],
            FadeIn(leg_base), FadeIn(leg_v2),
            run_time=0.5,
        )

        # Animate base bars in (faded) first, then v2 over them.
        for b in base_pairs:
            self.play(GrowFromEdge(b, DOWN), run_time=0.25)
        for v in v2_pairs:
            self.play(GrowFromEdge(v[0], DOWN), FadeIn(v[1]), run_time=0.4)

        callout = body_text(
            "Static-prefix spread:  8pp -> 3pp.  Q-1.5B plan now helps.",
            size=20,
            color=GOOD,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)
        assert_no_overlap([title_b, sub_b, leg_base, leg_v2, callout] + x_labels2)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
