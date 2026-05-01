"""Scene 1 -- Cognitive metaphor: AR sketch -> diffuse a vague chunk -> AR continue.

Verbatim port of visual_reps/concepts/sfumato_e4_iterative_thinking/scenes/scene01_metaphor.py
with imports rerouted through utils.theme_shim.
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    LEFT,
    ORIGIN,
    RIGHT,
    RoundedRectangle,
    Scene,
    Transform,
    UP,
    VGroup,
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
    pill,
    title_text,
)


def _token_box(label: str, color: str, width: float = 1.05, height: float = 0.55) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.18,
        stroke_width=2,
    )
    txt = body_text(label, size=18, color=color, weight=BOLD)
    txt.move_to(box.get_center())
    return VGroup(box, txt)


def _vague_box(width: float = 1.05, height: float = 0.55) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=DIFF,
        fill_color=DIFF,
        fill_opacity=0.10,
        stroke_width=2,
    )
    glyph = body_text("~~", size=22, color=DIFF, weight=BOLD)
    glyph.move_to(box.get_center())
    return VGroup(box, glyph)


class SfumatoMetaphorScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "How a thought actually forms",
            size=32,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.5)

        sub = body_text(
            "serial sketch  ->  iterate a vague chunk  ->  serial continue",
            size=22,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)

        # ---- Phase 1: AR sketch ------------------------------------------
        ar_label = body_text("AR (serial)", size=20, color=ACCENT_2, weight=BOLD)
        ar_label.move_to(UP * 1.6 + LEFT * 4.5)

        sketch = ["Carlos", "plants", "tree,"]
        ar_boxes = [_token_box(w, ACCENT_2, width=1.25) for w in sketch]
        ar_row = VGroup(*ar_boxes).arrange(RIGHT, buff=0.18)
        ar_row.move_to(UP * 0.4 + LEFT * 3.0)

        self.play(FadeIn(ar_label, shift=UP * 0.15), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.25) for b in ar_boxes],
                lag_ratio=0.4,
            ),
            run_time=1.8,
        )
        self.wait(0.3)

        # ---- Phase 2: Diffusion on a vague chunk -------------------------
        diff_label = body_text("Diffusion (iterate)", size=20, color=DIFF, weight=BOLD)
        diff_label.move_to(UP * 1.6)

        vague_boxes = [_vague_box(width=1.05) for _ in range(3)]
        vague_row = VGroup(*vague_boxes).arrange(RIGHT, buff=0.18)
        vague_row.next_to(ar_row, RIGHT, buff=0.25)

        self.play(FadeIn(diff_label, shift=UP * 0.15), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.15) for b in vague_boxes],
                lag_ratio=0.18,
            ),
            run_time=0.7,
        )

        self.wait(0.4)

        # Refinement steps: vague -> partial -> resolved
        partial_words = [["?", "?", "?"], ["years", "to", "?"], ["years", "to", "earn"]]
        for words in partial_words:
            new_boxes = []
            for box, w in zip(vague_boxes, words):
                color = DIFF if w == "?" else FG
                opacity = 0.10 if w == "?" else 0.30
                new_box = RoundedRectangle(
                    width=1.05,
                    height=0.55,
                    corner_radius=0.10,
                    stroke_color=color,
                    fill_color=color,
                    fill_opacity=opacity,
                    stroke_width=2,
                )
                new_box.move_to(box[0].get_center())
                new_txt = body_text(
                    "~~" if w == "?" else w,
                    size=18,
                    color=color,
                    weight=BOLD,
                )
                new_txt.move_to(new_box.get_center())
                new_boxes.append(VGroup(new_box, new_txt))
            self.play(
                *[Transform(old, new) for old, new in zip(vague_boxes, new_boxes)],
                run_time=0.8,
            )
            self.wait(0.25)

        self.wait(0.6)

        # ---- Phase 3: AR continue ----------------------------------------
        cont_label = body_text("AR (serial)", size=20, color=ACCENT_2, weight=BOLD)
        cont_label.move_to(UP * 1.6 + RIGHT * 4.5)

        cont = ["fruit:", "13", "yrs."]
        cont_boxes = [_token_box(w, ACCENT_2, width=1.05) for w in cont]
        cont_row = VGroup(*cont_boxes).arrange(RIGHT, buff=0.18)
        cont_row.next_to(vague_row, RIGHT, buff=0.25)

        self.play(FadeIn(cont_label, shift=UP * 0.15), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.25) for b in cont_boxes],
                lag_ratio=0.40,
            ),
            run_time=1.4,
        )
        self.wait(0.7)

        # Insight pill
        insight = body_text(
            "Cognition mixes serial autoregression with iterative refinement.",
            size=22,
            color=ACCENT,
            weight=BOLD,
        )
        insight.move_to(DOWN * 1.4)
        self.play(FadeIn(insight, shift=UP * 0.15), run_time=0.7)
        self.wait(3.0)

        fade_out_all(self)
