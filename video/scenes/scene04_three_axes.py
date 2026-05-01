"""Scene 4 -- the three orthogonal failure axes the paper decomposes the
hybrid AR/DDLM failure surface into.

No numbers; just the decomposition. Three pill-style cards with one-line
descriptions arranged horizontally with non-overlapping bbox.
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


def _axis_card(
    index: str,
    headline: str,
    subline: str,
    color: str,
    width: float = 4.0,
    height: float = 2.0,
) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.20,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.12,
        stroke_width=2.4,
    )
    idx = body_text(index, size=18, color=color, weight=BOLD)
    head = body_text(headline, size=20, color=FG, weight=BOLD)
    sub = body_text(subline, size=16, color=MUTED)

    inner = VGroup(idx, head, sub).arrange(DOWN, buff=0.18)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class ThreeAxesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Three Orthogonal Failure Axes",
            size=34,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.5)

        sub = body_text(
            "hybrid AR/DDLM reasoning fails along independent dimensions",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Three cards positioned LEFT / CENTER / RIGHT, no overlap.
        card_w, card_h = 3.9, 2.2
        gap = 4.25
        left_card = _axis_card(
            "Axis 1",
            "Interface-format\nbrittleness",
            "fixable",
            color=ACCENT,
            width=card_w,
            height=card_h,
        )
        left_card.move_to(LEFT * gap)

        center_card = _axis_card(
            "Axis 2",
            "Planner-content\ntrust",
            "characterized",
            color=WARN,
            width=card_w,
            height=card_h,
        )
        center_card.move_to(0 * RIGHT)

        right_card = _axis_card(
            "Axis 3",
            "Sampling-diversity\npreservation",
            "expanded",
            color=GOOD,
            width=card_w,
            height=card_h,
        )
        right_card.move_to(RIGHT * gap)

        # Defensive non-overlap check.
        assert_no_overlap([title, sub, left_card, center_card, right_card])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(left_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(center_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(right_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.6)

        # Footer: the paper's promise.
        footer = body_text(
            "Two of the three are trainably fixable.",
            size=22,
            color=ACCENT_2,
            weight=BOLD,
        )
        footer.to_edge(DOWN, buff=0.6)

        # Re-check including the footer.
        assert_no_overlap([title, sub, left_card, center_card, right_card, footer])

        self.play(FadeIn(footer, shift=UP * 0.15), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
