"""Scene 12 -- the voting-rule gap.

Two cards side by side: cmaj majority-vote accuracy vs oracle ceiling, on
the v3-LoRA substrate. Numbers from voting_gap.tex Table 1
(GSM8K-test N=200, b=5, t=0.7, Track-1 v3 LoRA):

  cmaj a_b   = 79.5%   [73.3, 84.9]
  oracle     = 88.0%   [82.7, 92.2]
  gap        = 8.5 pp

Headline: "majority vote discards the right answer".
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
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


def _result_card(label, value_str, detail, color, w=4.8, h=2.6):
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.20,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.14,
        stroke_width=2.4,
    )
    name = body_text(label, size=20, color=color, weight=BOLD)
    val = body_text(value_str, size=42, color=color, weight=BOLD)
    det = body_text(detail, size=15, color=MUTED)
    inner = VGroup(name, val, det).arrange(DOWN, buff=0.18)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class VotingGapScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "But majority vote is not the ceiling",
            size=28,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "GSM8K-test, N=200, b=5, t=0.7, Track-1 v3 LoRA",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        gap_x = 3.4
        cmaj_card = _result_card(
            "cmaj majority vote",
            "79.5%",
            "[73.3, 84.9]\n5 branches, plurality",
            color=DIFF,
        )
        cmaj_card.move_to(LEFT * gap_x + DOWN * 0.2)

        oracle_card = _result_card(
            "oracle ceiling",
            "88.0%",
            "[82.7, 92.2]\nany branch correct?",
            color=GOOD,
        )
        oracle_card.move_to(RIGHT * gap_x + DOWN * 0.2)

        gap_label = body_text(
            "8.5 pp gap",
            size=24,
            color=ACCENT,
            weight=BOLD,
        )
        gap_label.move_to(0 * RIGHT + UP * 1.15)

        callout = body_text(
            "In the median problem the right answer IS in some branch.\n"
            "Majority vote throws it away.",
            size=19,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.5)

        assert_no_overlap([title, sub, cmaj_card, oracle_card, gap_label, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(cmaj_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.35)
        self.play(FadeIn(oracle_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.35)
        self.play(FadeIn(gap_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.55)
        self.wait(3.5)

        fade_out_all(self)
