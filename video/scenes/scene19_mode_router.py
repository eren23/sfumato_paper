"""Scene 19 -- D1 mode router honest negative.

Three bars on a 20-problem x 12-condition substrate (LOOCV):

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
    ("best fixed",   "always-c2empty",        "75%",  75.0, DIFF),
    ("D1 bandit",    "logistic + LOOCV",      "65%",  65.0, WARN),
    ("oracle",       "any-condition correct", "85%",  85.0, GOOD),
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


class ModeRouterScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Per-problem mode router -- honest negative",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "20 problems x 12 conditions; LR over question features (length, numeric tokens, TF-IDF), LOOCV",
            size=15,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        chart_left, chart_right = -5.0, 5.0
        floor_y = -1.7
        unit = 0.06

        def y_for(acc):
            return floor_y + acc * unit

        usable_left, usable_right = chart_left + 0.5, chart_right - 0.5
        n = len(ROWS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 1.55

        bar_groups = []
        labels = []
        for i, (label, sub_lbl, val_str, val, color) in enumerate(ROWS):
            x_pos = usable_left + slot_w * (i + 0.5)
            top_y = y_for(val)
            h_abs = top_y - floor_y
            bar = _bar(h_abs, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (floor_y + h_abs / 2))

            val_lbl = body_text(val_str, size=24, color=color, weight=BOLD)
            val_lbl.next_to(bar, UP, buff=0.12)

            cond = body_text(label, size=18, color=FG, weight=BOLD)
            cond.move_to(RIGHT * x_pos + UP * (floor_y - 0.42))

            tag = body_text(sub_lbl, size=12, color=MUTED)
            tag.move_to(RIGHT * x_pos + UP * (floor_y - 0.78))

            bar_groups.append(VGroup(bar, val_lbl))
            labels.extend([cond, tag])

        delta_label = body_text(
            "delta = -10 pp vs best fixed   ->   pre-reg LOSS",
            size=20,
            color=WARN,
            weight=BOLD,
        )
        delta_label.move_to(LEFT * 0.0 + UP * 2.0)

        callout = body_text(
            "Same pathology as the verifier sweep: small N + large action space\n"
            "+ surface text features cannot recover the oracle ceiling.",
            size=18,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.45)

        assert_no_overlap([title, sub, delta_label, callout] + labels)

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(*[FadeIn(l) for l in labels], run_time=0.4)
        for g in bar_groups:
            self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), run_time=0.55)
            self.wait(0.2)
        self.play(FadeIn(delta_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.55)
        self.wait(3.5)

        fade_out_all(self)
