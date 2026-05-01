"""Scene 8 -- Track 2 consensus distillation timeline.

Three stages on a horizontal timeline. c2c (commit-to-c2 accuracy) values
from PAPER_DRAFT.md Section 6.1-6.2:

  v1 (1/3 modules matched, 4.2M params, last-block + answer-span)  c2c = 70.5%
  v2 (3/3 modules matched, 14M params,  last-block + answer-span)  c2c = 70.5%
  v3 (3/3 modules matched, 14M params,  n_blocks=3 + full-response) c2c = 79.0%

The annotation: 79% is within sampling error (+/- 5pp at N=200 binomial CI)
of the 80% pre-registered target.
"""
from __future__ import annotations

from manim import (
    Arrow,
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


def _stage_card(
    label: str,
    value: str,
    detail: str,
    color: str,
    w: float = 3.6,
    h: float = 2.0,
) -> VGroup:
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.18,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.14,
        stroke_width=2.4,
    )
    name = body_text(label, size=18, color=color, weight=BOLD)
    val = body_text(value, size=30, color=color, weight=BOLD)
    det = body_text(detail, size=15, color=MUTED)
    inner = VGroup(name, val, det).arrange(DOWN, buff=0.12)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class ConsensusDistillScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Track 2: distilling cmaj consensus into a single forward pass",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "the 6pp cmaj-vs-C2 gap, closed by design iteration",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Three stage cards arranged left to right.
        gap_x = 4.85
        v1_card = _stage_card(
            "v1  broken modules",
            "70.5%",
            "1/3 FFN matched (4.2M params)\nlast-block + answer-span",
            color=WARN,
        )
        v1_card.move_to(LEFT * gap_x + DOWN * 0.4)

        v2_card = _stage_card(
            "v2  fixed modules",
            "70.5%",
            "3/3 FFN matched (14M params)\nlast-block + answer-span",
            color=WARN,
        )
        v2_card.move_to(0 * RIGHT + DOWN * 0.4)

        v3_card = _stage_card(
            "v3  redesigned",
            "79.0%",
            "n_blocks = 3, full-response loss\n(same 14M params)",
            color=GOOD,
        )
        v3_card.move_to(RIGHT * gap_x + DOWN * 0.4)

        # Connecting arrows.
        arrow_12 = Arrow(
            v1_card[0].get_right(),
            v2_card[0].get_left(),
            buff=0.12,
            color=MUTED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow_23 = Arrow(
            v2_card[0].get_right(),
            v3_card[0].get_left(),
            buff=0.12,
            color=GOOD,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )

        # Delta labels above arrows.
        delta_12 = body_text("+0.0pp", size=18, color=WARN, weight=BOLD)
        delta_12.next_to(arrow_12, UP, buff=0.08)

        delta_23 = body_text("+8.5pp", size=20, color=GOOD, weight=BOLD)
        delta_23.next_to(arrow_23, UP, buff=0.08)

        # Pre-registered target line annotation
        target_box = RoundedRectangle(
            width=10.0,
            height=0.6,
            corner_radius=0.12,
            stroke_color=GOOD,
            fill_color=GOOD,
            fill_opacity=0.10,
            stroke_width=1.5,
        )
        target_box.to_edge(DOWN, buff=0.55)
        target_text = body_text(
            "79.0% is within sampling error (+/- 5pp, N=200) of the 80% pre-registered target.",
            size=18,
            color=GOOD,
            weight=BOLD,
        )
        target_text.move_to(target_box.get_center())

        assert_no_overlap(
            [
                title, sub,
                v1_card, v2_card, v3_card,
                delta_12, delta_23,
                target_box,
            ]
        )

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)

        self.play(FadeIn(v1_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(arrow_12), FadeIn(delta_12), run_time=0.4)
        self.play(FadeIn(v2_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.4)
        # Pause to let the "identical c2c despite 3.25x capacity" land.
        same_note = body_text(
            "identical c2c despite 3.25x capacity",
            size=16,
            color=WARN,
        )
        same_note.next_to(v2_card, DOWN, buff=0.30)
        assert_no_overlap(
            [title, sub, v1_card, v2_card, v3_card, delta_12, delta_23, same_note]
        )
        self.play(FadeIn(same_note, shift=UP * 0.1), run_time=0.5)
        self.wait(1.4)
        self.play(FadeIn(arrow_23), FadeIn(delta_23), run_time=0.4)
        self.play(FadeIn(v3_card, shift=UP * 0.15), run_time=0.6)
        self.wait(0.5)

        # Now the target annotation.
        self.play(FadeIn(target_box), FadeIn(target_text), run_time=0.6)
        self.wait(3.0)

        fade_out_all(self)
