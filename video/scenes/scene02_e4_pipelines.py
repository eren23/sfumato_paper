"""Scene 2 -- Four E4 conditions C1..C4 as side-by-side pipelines.

Verbatim port of visual_reps/concepts/sfumato_e4_iterative_thinking/scenes/scene02_pipelines.py
with imports rerouted through utils.theme_shim.
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    LaggedStart,
    LEFT,
    ORIGIN,
    RIGHT,
    RoundedRectangle,
    Scene,
    UP,
    VGroup,
    Arrow,
)

from utils.theme_shim import (
    ACCENT,
    ACCENT_2,
    BG,
    DIFF,
    FG,
    MUTED,
    body_text,
    fade_out_all,
    title_text,
)


def _stage(label: str, color: str, width: float = 1.5, height: float = 0.55) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.20,
        stroke_width=2,
    )
    txt = body_text(label, size=15, color=color, weight=BOLD)
    txt.move_to(box.get_center())
    return VGroup(box, txt)


def _arrow(left, right, color: str = MUTED) -> Arrow:
    return Arrow(
        left.get_right(),
        right.get_left(),
        buff=0.05,
        color=color,
        stroke_width=2.2,
        max_tip_length_to_length_ratio=0.18,
    )


def _condition_row(
    code: str,
    desc: str,
    stages: list[tuple[str, str]],
    y: float,
) -> VGroup:
    code_label = body_text(code, size=22, color=FG, weight=BOLD)
    code_label.move_to(LEFT * 6.3 + UP * y)

    desc_label = body_text(desc, size=15, color=MUTED)
    desc_label.next_to(code_label, DOWN, buff=0.10).align_to(code_label, LEFT)

    boxes = [_stage(lab, col, width=1.6) for lab, col in stages]
    pipeline = VGroup()
    for i, b in enumerate(boxes):
        pipeline.add(b)
        if i < len(boxes) - 1:
            pass  # arrows added after layout
    row = VGroup(*boxes).arrange(RIGHT, buff=0.4)
    row.move_to(RIGHT * 1.2 + UP * y)

    arrows = []
    for a, b in zip(boxes, boxes[1:]):
        arrows.append(_arrow(a, b))

    return VGroup(code_label, desc_label, row, *arrows)


class SfumatoPipelinesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Four E4 conditions", size=32, color=ACCENT)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.45)

        sub = body_text(
            "varying how AR (Qwen-0.5B) and diffusion (LLaDA-8B) hand off",
            size=18,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.35)

        # ---- Build rows --------------------------------------------------
        c1 = _condition_row(
            "C1",
            "AR only -- Qwen left to right",
            [("Qwen AR", ACCENT_2), ("...", ACCENT_2), ("answer", ACCENT_2)],
            y=1.4,
        )
        c2 = _condition_row(
            "C2",
            "Diffusion only -- LLaDA mask + denoise",
            [("mask all", DIFF), ("LLaDA denoise", DIFF), ("answer", DIFF)],
            y=0.2,
        )
        c3 = _condition_row(
            "C3",
            "Plan -> denoise -> finalize  (text handoff)",
            [("Qwen plan", ACCENT_2), ("LLaDA denoise", DIFF), ("Qwen finalize", ACCENT_2)],
            y=-1.0,
        )
        c4 = _condition_row(
            "C4",
            "C3 + extra (extend, diffuse-again) round",
            [("Qwen plan", ACCENT_2), ("LLaDA", DIFF), ("Qwen extend", ACCENT_2), ("LLaDA again", DIFF)],
            y=-2.2,
        )

        for row in (c1, c2, c3, c4):
            self.play(FadeIn(row, shift=UP * 0.12), run_time=1.0)
            self.wait(0.65)

        self.wait(3.0)

        fade_out_all(self)
