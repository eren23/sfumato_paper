"""Scene 20 -- honest AR-baseline disclosure.

Head-to-head bars on GSM8K-test, with a truncated y-axis (acc 50-92)
so the +4.0 pp delta is visible without bars colliding with the title:
  hybrid sfumato cmajc-v3 (LLaDA-8B + Qwen 0.5-1.5B planner): 82.5%
  plain Qwen-2.5-7B AR alone:                                  ~86.5%

Plus a planner-invariance note: hybrid accuracy is approximately constant
(82-83%) across Qwen-0.5B through Qwen-7B planners. The diffusion
substrate, not the planner, is the bottleneck.

Source: discussion.tex sec:ar_baseline; phase2/PAPER_DRAFT.md negative
results section.

Headline: "honest disclosure -- a parameter-matched AR baseline beats
the hybrid on this benchmark; the substrate findings are about
the AR/DDLM stack, not about beating peer-class AR."
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
    ("hybrid cmajc-v3", "LLaDA-8B + Qwen 0.5-1.5B planner + LoRAs",       "82.5%", 82.5, DIFF),
    ("Qwen-2.5-7B AR",  "plain monolithic AR, no diffusion, no planner",   "86.5%", 86.5, GOOD),
]

# Truncated y-axis -- acc range mapped onto a fixed pixel band
# leaves headroom above the bars for value labels + delta arrow
# without colliding with the title/subtitle band.
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


class ARBaselineScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Peer baseline -- AR alone beats the hybrid at fewer active params",
            size=22,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "GSM8K-test, same eval. Hybrid is ~9B active at inference; AR is 7B.",
            size=15,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        chart_left, chart_right = -4.5, 4.5
        usable_left, usable_right = chart_left + 0.5, chart_right - 0.5
        n = len(ROWS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 2.0

        # truncated-axis indicator on the left edge
        axis_line = Line(
            LEFT * 5.4 + UP * BAR_FLOOR,
            LEFT * 5.4 + UP * BAR_CEIL,
            color=MUTED,
            stroke_width=1.5,
        )
        axis_lo = body_text(f"{int(ACC_FLOOR)}%", size=12, color=MUTED)
        axis_lo.move_to(LEFT * 5.7 + UP * BAR_FLOOR)
        axis_hi = body_text(f"{int(ACC_CEIL)}%", size=12, color=MUTED)
        axis_hi.move_to(LEFT * 5.7 + UP * BAR_CEIL)
        # "axis break" tick marks indicating the truncation
        break_lo = Line(
            LEFT * 5.55 + UP * (BAR_FLOOR - 0.18),
            LEFT * 5.25 + UP * (BAR_FLOOR - 0.08),
            color=MUTED,
            stroke_width=1.5,
        )
        break_hi = Line(
            LEFT * 5.55 + UP * (BAR_FLOOR - 0.10),
            LEFT * 5.25 + UP * (BAR_FLOOR + 0.00),
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

            val_lbl = body_text(val_str, size=26, color=color, weight=BOLD)
            val_lbl.next_to(bar, UP, buff=0.10)

            cond = body_text(label, size=20, color=FG, weight=BOLD)
            cond.move_to(RIGHT * x_pos + UP * (BAR_FLOOR - 0.42))

            tag = body_text(sub_lbl, size=12, color=MUTED)
            tag.move_to(RIGHT * x_pos + UP * (BAR_FLOOR - 0.78))

            bar_groups.append(VGroup(bar, val_lbl))
            labels.extend([cond, tag])

        # delta annotation sits between the two value labels, just above bars
        gap_label = body_text(
            "delta = +4.0 pp",
            size=18,
            color=WARN,
            weight=BOLD,
        )
        gap_label.move_to(0 * RIGHT + UP * (BAR_CEIL + 0.55))

        invariance_note = body_text(
            "Hybrid acc is ~planner-invariant"
            " (82-83% across Qwen 0.5B -> 7B planners, 14x range)"
            " -- the bottleneck is LLaDA-8B.",
            size=14,
            color=MUTED,
        )
        invariance_note.move_to(0 * RIGHT + UP * (BAR_FLOOR - 1.10))

        callout = body_text(
            "Honest disclosure: substrate findings hold;"
            " head-to-head accuracy claim does not.",
            size=17,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.30)

        assert_no_overlap(
            [title, sub, gap_label, invariance_note, callout, axis_lo, axis_hi]
            + labels
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
            self.wait(0.25)
        self.play(FadeIn(gap_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(invariance_note, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
