"""Scene 18 -- commit-LoRA K2 schedule-toggle sweep.

Three bars showing the inverted-U around the v3 default. Numbers from
sections/commit_lora_k2.tex Table 1 (GSM8K-test N=200, b=5, t=0.7,
Track-1 v3 + commit-v3 substrate, COMMIT_N_BLOCKS sweep):

  k=0 (commit off, sanity floor):           80.5%   = -1.7 pp vs peak
  k=3 (sub-blocks 2-4, sfumato-v3 default): 82.2%   peak (sigma ~ 0.85 pp)
  k=4 (always on):                          79.0%   = -3.2 pp vs peak

Both off-peak deltas exceed 1 sigma. The sub-block-1 boundary is
load-bearing in both directions: turning it off costs 1.7 pp, turning
it on costs another 3.2 pp.

Headline: "the schedule toggle peaks at k=3, drops on either side."
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


# (k_label, sub_block_caption, accuracy_str, accuracy_value, delta_str, color)
ROWS = [
    ("k=0",  "commit off",            "80.5%", 80.5, "-1.7 pp", WARN),
    ("k=3",  "sub-blocks 2-4 (v3)",   "82.2%", 82.2, "peak",    GOOD),
    ("k=4",  "always on",             "79.0%", 79.0, "-3.2 pp", WARN),
]


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


class K2SweepScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Commit-LoRA timing -- the schedule toggle peaks at k=3",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "GSM8K-test N=200, b=5, t=0.7; Track-1-v3 + commit-v3; COMMIT_N_BLOCKS sweep",
            size=16,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        # Bars rise from a baseline; we plot accuracy points 76 .. 84 mapped
        # onto a fixed pixel band. Reference is the cmaj=79.5% no-commit line.
        chart_left, chart_right = -5.0, 5.0
        floor_y = -1.6   # the y-coordinate that maps to 76% accuracy
        unit = 0.34      # one accuracy point in scene units

        def y_for(acc):
            return floor_y + (acc - 76.0) * unit

        cmaj_y = y_for(79.5)
        baseline_line = Line(
            LEFT * 5.4 + UP * cmaj_y,
            RIGHT * 5.4 + UP * cmaj_y,
            color=DIFF,
            stroke_width=2,
        )
        baseline_lbl = body_text("cmaj baseline 79.5% (no commit-LoRA)", size=13, color=DIFF)
        baseline_lbl.next_to(baseline_line.get_right(), UP, buff=0.04)

        usable_left, usable_right = chart_left + 0.6, chart_right - 0.6
        n = len(ROWS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 1.45

        bar_groups = []
        labels = []
        for i, (k_lbl, sub_lbl, acc_str, acc_val, delta_str, color) in enumerate(ROWS):
            x_pos = usable_left + slot_w * (i + 0.5)
            top_y = y_for(acc_val)
            h_abs = top_y - floor_y
            bar = _bar(h_abs, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (floor_y + h_abs / 2))

            val = body_text(acc_str, size=20, color=color, weight=BOLD)
            val.next_to(bar, UP, buff=0.10)

            delta = body_text(delta_str, size=14, color=color)
            delta.next_to(val, UP, buff=0.05)

            k_label = body_text(k_lbl, size=18, color=FG, weight=BOLD)
            k_label.move_to(RIGHT * x_pos + UP * (floor_y - 0.40))
            cap = body_text(sub_lbl, size=12, color=MUTED)
            cap.move_to(RIGHT * x_pos + UP * (floor_y - 0.74))

            bar_groups.append(VGroup(bar, val, delta))
            labels.extend([k_label, cap])

        callout = body_text(
            "Sub-block-1 boundary is load-bearing in both directions:\n"
            "off costs -1.7 pp, on costs another -3.2 pp.",
            size=18,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.45)

        assert_no_overlap([title, sub, baseline_lbl, callout] + labels)

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(baseline_line), FadeIn(baseline_lbl),
                  *[FadeIn(l) for l in labels], run_time=0.5)
        for g in bar_groups:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), FadeIn(g[2]), run_time=0.55)
            self.wait(0.2)
        self.wait(0.4)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.55)
        self.wait(3.0)

        fade_out_all(self)
