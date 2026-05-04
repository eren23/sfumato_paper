"""Scene 17 -- Phase-2 epilogue closing.

Three short bullets summarizing the voting-rule-gap section, plus a compute
footer reflecting the new total ($13 across both phases).

Tagline: "problem comprehension, not arithmetic."
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    LEFT,
    RIGHT,
    Scene,
    UP,
    VGroup,
)

from utils.theme_shim import (
    ACCENT,
    BG,
    FG,
    GOOD,
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)
from utils.layout import assert_no_overlap


def _bullet_row(text, color):
    dot = body_text("*", size=28, color=color, weight=BOLD)
    body = body_text(text, size=20, color=FG)
    return VGroup(dot, body).arrange(RIGHT, buff=0.30, aligned_edge=UP)


class Phase2ClosingScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Phase 2  --  the voting-rule gap is structural",
            size=30,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.6)

        bullet1 = _bullet_row(
            "Oracle ceiling beats cmaj by 8-12 pp across 4 configs and 3 seeds.",
            color=WARN,
        )
        bullet2 = _bullet_row(
            "17 peer-class verifiers all LOSS; encoder scaling monotone but insufficient.",
            color=WARN,
        )
        bullet3 = _bullet_row(
            "Frontier judge + CoT closes 86% of the gap (79.1 -> 85.3 vs oracle 86.3).",
            color=GOOD,
        )

        bullets = VGroup(bullet1, bullet2, bullet3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45,
        )
        bullets.move_to(0 * RIGHT + DOWN * 0.0)

        tagline = body_text(
            "Failure mode: problem comprehension, not arithmetic.",
            size=22,
            color=ACCENT,
            weight=BOLD,
        )
        tagline.next_to(bullets, DOWN, buff=0.6)

        footer = body_text(
            "Total compute across both phases: ~$13.\n"
            "Adapters, datasets, traces, and judge driver public.",
            size=16,
            color=MUTED,
        )
        footer.to_edge(DOWN, buff=0.45)

        assert_no_overlap([title, bullet1, bullet2, bullet3, tagline, footer])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.55)
        self.wait(0.2)
        self.play(FadeIn(bullet1, shift=UP * 0.1), run_time=0.55)
        self.wait(0.3)
        self.play(FadeIn(bullet2, shift=UP * 0.1), run_time=0.55)
        self.wait(0.3)
        self.play(FadeIn(bullet3, shift=UP * 0.1), run_time=0.55)
        self.wait(0.5)
        self.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.55)
        self.wait(0.5)
        self.play(FadeIn(footer, shift=UP * 0.1), run_time=0.5)
        self.wait(4.5)

        fade_out_all(self)
