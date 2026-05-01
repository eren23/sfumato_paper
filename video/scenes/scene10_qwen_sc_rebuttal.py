"""Scene 10 -- Reviewer-resilience: ruling out generic self-consistency.

Two side-by-side boxes. Numbers from PAPER_DRAFT.md Section 7:
  Qwen-SC b=5 t=0.7   on GSM8K-test N=200:  40.5%
  LLaDA cmaj b=5 t=0.7 on GSM8K-test N=200: 79.0-82.5%
38-42pp gap. Generic self-consistency does NOT explain LLaDA's diffusion
cmaj advantage.
"""
from __future__ import annotations

from manim import (
    Arrow,
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


def _result_card(
    label: str,
    value_str: str,
    detail: str,
    color: str,
    w: float = 4.6,
    h: float = 2.6,
) -> VGroup:
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
    det = body_text(detail, size=16, color=MUTED)
    inner = VGroup(name, val, det).arrange(DOWN, buff=0.18)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class QwenSCRebuttalScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Generic self-consistency does not explain the diffusion advantage",
            size=23,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "GSM8K-test, N=200, b=5, t=0.7",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Two cards.
        gap_x = 3.4
        ar_card = _result_card(
            "Qwen-AR self-consistency",
            "40.5%",
            "Qwen-2.5-0.5B-Instruct\nb=5, t=0.7",
            color=WARN,
        )
        ar_card.move_to(LEFT * gap_x + DOWN * 0.2)

        diff_card = _result_card(
            "LLaDA cmaj",
            "79.0 - 82.5%",
            "LLaDA-8B-Instruct\nb=5, t=0.7",
            color=GOOD,
        )
        diff_card.move_to(RIGHT * gap_x + DOWN * 0.2)

        # Gap arrow + label between them.
        gap_label = body_text(
            "38 - 42 pp gap",
            size=22,
            color=ACCENT,
            weight=BOLD,
        )
        gap_label.move_to(0 * RIGHT + UP * 1.2)

        # Bottom callout.
        callout = body_text(
            "Whatever LLaDA's branching is doing, it depends on the diffusion sampler.",
            size=18,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.55)

        assert_no_overlap([title, sub, ar_card, diff_card, gap_label, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(ar_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(diff_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(gap_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
