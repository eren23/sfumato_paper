"""Scene 14 -- three robust negative findings from the verifier sweep.

Three side-by-side cards:
  (a) math-tuning HURTS as a verifier
      Qwen2.5-Math-7B  -6.5 pp   vs Qwen2.5-7B chat -4.0 pp
  (b) embedding-specific models lose worst
      Qwen3-Embedding-8B -8.0 pp vs Qwen3-8B chat   -5.5 pp
  (c) doubling substrate makes it worse
      process-MLP N=200 -5.5 pp -> N=500 -6.16 pp;  symbolic -8.98 pp

Headline: "three publishable negatives, each one paragraph."
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


def _finding_card(headline, comparison_lines, color, w=4.05, h=3.6):
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.18,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.10,
        stroke_width=2.2,
    )
    head = body_text(headline, size=18, color=color, weight=BOLD)
    body_lines = VGroup(
        *[body_text(line, size=15, color=FG) for line in comparison_lines]
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    inner = VGroup(head, body_lines).arrange(DOWN, buff=0.30)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class ThreeNegativesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Three findings survive across the leaderboard",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "encoder-side patterns, robust under matched architecture",
            size=16,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        c1 = _finding_card(
            "Math-tuning HURTS",
            [
                "Qwen2.5-Math-7B:",
                "  -6.5 pp",
                "Qwen2.5-7B chat:",
                "  -4.0 pp",
                "math vocab >> math correctness",
            ],
            color=WARN,
        )
        c2 = _finding_card(
            "Embedding-specific worst",
            [
                "Qwen3-Embedding-8B:",
                "  -8.0 pp",
                "Qwen3-8B chat:",
                "  -5.5 pp",
                "cosine compresses similarity",
            ],
            color=WARN,
        )
        c3 = _finding_card(
            "Substrate doubling hurts",
            [
                "process-MLP N=200:",
                "  -5.5 pp",
                "process-MLP N=500:",
                "  -6.16 pp",
                "overfit to substrate noise",
            ],
            color=WARN,
        )

        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.40)
        cards.move_to(0 * RIGHT + DOWN * 0.1)

        callout = body_text(
            "Bottleneck is the supervised-classification objective, not feature quality.",
            size=18,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)

        assert_no_overlap([title, sub, c1, c2, c3, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.55)
        self.wait(0.35)
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.55)
        self.wait(0.35)
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.55)
        self.wait(0.6)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
