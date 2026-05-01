"""Scene 6 -- Axis 2: planner-content trust is capacity-dependent in
opposite directions across planners.

Two-row layout. Each row has a Q-0.5B box and a Q-1.5B box; values come from
PAPER_DRAFT.md Section 3.3 (the v2/v3 capacity tradeoff). The "inversion"
is the visual point: at v2 the bigger planner helps; at v3 it
catastrophically regresses.

  v2 (4/7 modules): Q-0.5B = 60%, Q-1.5B = 67%   (Q-1.5B helps)
  v3 (7/7 modules): Q-0.5B = 65%, Q-1.5B = 54%   (Q-1.5B hurts -13pp)
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


def _value_box(label: str, value_str: str, color: str, w: float = 2.6, h: float = 1.2) -> VGroup:
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.16,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.16,
        stroke_width=2.2,
    )
    lbl = body_text(label, size=16, color=MUTED)
    val = body_text(value_str, size=28, color=color, weight=BOLD)
    inner = VGroup(lbl, val).arrange(DOWN, buff=0.10)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


def _row_label(text: str, color: str) -> VGroup:
    return body_text(text, size=20, color=color, weight=BOLD)


class Axis2PlannerTrustScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Axis 2: Planner-trust is capacity-dependent",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "C3p accuracy with Qwen-{0.5B, 1.5B} planner upstream of LLaDA  /  4 of 7 vs 7 of 7 LoRA target modules",
            size=15,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Row 1: v2 (4/7 modules)
        row1_y = 0.7
        row1_label = _row_label("v2  (4 / 7 modules)", ACCENT_2)
        row1_label.move_to(LEFT * 5.4 + UP * row1_y)

        v2_q05 = _value_box("Q-0.5B", "60%", color=WARN)
        v2_q05.move_to(LEFT * 1.5 + UP * row1_y)
        v2_q15 = _value_box("Q-1.5B", "67%", color=GOOD)
        v2_q15.move_to(RIGHT * 2.0 + UP * row1_y)

        # Row 2: v3 (7/7 modules)
        row2_y = -1.4
        row2_label = _row_label("v3  (7 / 7 modules)", ACCENT_2)
        row2_label.move_to(LEFT * 5.4 + UP * row2_y)

        v3_q05 = _value_box("Q-0.5B", "65%", color=GOOD)
        v3_q05.move_to(LEFT * 1.5 + UP * row2_y)
        v3_q15 = _value_box("Q-1.5B", "54%", color=WARN)
        v3_q15.move_to(RIGHT * 2.0 + UP * row2_y)

        # Inversion arrows + delta labels (positioned to the right)
        delta_v2 = body_text("+7pp", size=22, color=GOOD, weight=BOLD)
        delta_v2.move_to(RIGHT * 4.6 + UP * row1_y)

        delta_v3 = body_text("-11pp", size=22, color=WARN, weight=BOLD)
        delta_v3.move_to(RIGHT * 4.6 + UP * row2_y)

        # Bottom annotation
        callout = body_text(
            "Bigger planner HELPS at v2, then catastrophically REGRESSES at v3.",
            size=20,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.55)

        # Phase 1 layout check (everything visible by end of scene).
        assert_no_overlap(
            [
                title, sub,
                row1_label, v2_q05, v2_q15, delta_v2,
                row2_label, v3_q05, v3_q15, delta_v3,
                callout,
            ]
        )

        # Animate.
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)

        self.play(FadeIn(row1_label, shift=RIGHT * 0.1), run_time=0.4)
        self.play(FadeIn(v2_q05, shift=UP * 0.15), run_time=0.45)
        self.play(FadeIn(v2_q15, shift=UP * 0.15), run_time=0.45)
        self.play(FadeIn(delta_v2, shift=LEFT * 0.1), run_time=0.4)
        self.wait(0.6)

        self.play(FadeIn(row2_label, shift=RIGHT * 0.1), run_time=0.4)
        self.play(FadeIn(v3_q05, shift=UP * 0.15), run_time=0.45)
        self.play(FadeIn(v3_q15, shift=UP * 0.15), run_time=0.45)
        self.play(FadeIn(delta_v3, shift=LEFT * 0.1), run_time=0.4)
        self.wait(0.6)

        # Inversion arrow connecting Q-1.5B at v2 (green) to Q-1.5B at v3 (red)
        inv_arrow = Arrow(
            v2_q15[0].get_bottom() + DOWN * 0.05,
            v3_q15[0].get_top() + UP * 0.05,
            buff=0.08,
            color=WARN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.10,
        )
        self.play(FadeIn(inv_arrow), run_time=0.45)

        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
