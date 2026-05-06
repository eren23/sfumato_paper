"""Scene 21 -- final closing after the K2, mode-router, and AR-baseline scenes.

Three short bullets summarising the post-Phase-2 additions, plus an
updated compute footer (~$17 across all phases).

Tagline: "discrete schedule toggle wins, supervised classification loses,
AR alone wins on this bench."
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


class Phase3ClosingScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Wrapping up  --  schedule toggles win, classifiers lose, AR wins on this bench",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.6)

        bullet1 = _bullet_row(
            "K2 sweep: commit-LoRA peaks at k=3; sub-block-1 boundary load-bearing (+1.7, -3.2 pp).",
            color=GOOD,
        )
        bullet2 = _bullet_row(
            "D1 mode router LOSS at -10 pp; same pathology as the verifier sweep.",
            color=WARN,
        )
        bullet3 = _bullet_row(
            "Plain Qwen-2.5-7B AR alone beats hybrid cmajc (~86.5 vs 82.5) at fewer active params.",
            color=WARN,
        )

        bullets = VGroup(bullet1, bullet2, bullet3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45,
        )
        bullets.move_to(0 * RIGHT + DOWN * 0.0)

        tagline = body_text(
            "Substrate findings hold; head-to-head AR claim does not.",
            size=22,
            color=ACCENT,
            weight=BOLD,
        )
        tagline.next_to(bullets, DOWN, buff=0.6)

        footer = body_text(
            "Total compute across all phases: ~$17.\n"
            "K2 figure, D1 spike, S0-S4 spike chain, showcase web app -- all public.",
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
