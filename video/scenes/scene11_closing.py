"""Scene 11 -- mid-arc transition out of the axes / distillation story.

Title, three short bullets recapping the axes + distillation findings,
and a one-line bridge into the aggregation arc that follows. No spend
footer here -- the cumulative tally lives in the unified close (scene 24).
All claims trace back to PAPER_DRAFT.md.
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


def _bullet_row(text: str, color: str) -> VGroup:
    dot = body_text("*", size=28, color=color, weight=BOLD)
    body = body_text(text, size=22, color=FG)
    return VGroup(dot, body).arrange(RIGHT, buff=0.30, aligned_edge=UP)


class ClosingScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Three axes characterized, two trainably fixed",
            size=30,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.6)

        # Three bullet rows, vertically arranged with comfortable spacing.
        bullet1 = _bullet_row(
            "Interface brittleness:  trainably fixable.",
            color=GOOD,
        )
        bullet2 = _bullet_row(
            "Planner-trust:  capacity-dependent in opposite directions.",
            color=ACCENT,
        )
        bullet3 = _bullet_row(
            "Consensus distillation:  design-sensitive, not architecture-limited.",
            color=GOOD,
        )

        bullets = VGroup(bullet1, bullet2, bullet3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45,
        )
        bullets.move_to(0 * RIGHT + DOWN * 0.1)

        # Bridge into the aggregation arc.
        bridge = body_text(
            "But cmaj itself leaves 8-12 pp on the table --"
            " what is going on with aggregation?",
            size=20,
            color=ACCENT,
            weight=BOLD,
        )
        bridge.to_edge(DOWN, buff=0.6)

        assert_no_overlap([title, bullet1, bullet2, bullet3, bridge])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.55)
        self.wait(0.2)
        self.play(FadeIn(bullet1, shift=UP * 0.1), run_time=0.55)
        self.wait(0.3)
        self.play(FadeIn(bullet2, shift=UP * 0.1), run_time=0.55)
        self.wait(0.3)
        self.play(FadeIn(bullet3, shift=UP * 0.1), run_time=0.55)
        self.wait(0.5)
        self.play(FadeIn(bridge, shift=UP * 0.1), run_time=0.55)
        self.wait(3.0)

        fade_out_all(self)
