"""Scene 1 -- cognitive metaphor: AR sketch -> diffuse a vague chunk -> AR continue.

The example is a multi-digit multiplication a person actually does in their
head. The sketch lays down the operands serially, the middle is a vague
chunk that flickers through several candidate values before settling, and
the answer is read out serially.

The point of the iteration phase is to show that a thought really does
*pass through* alternatives -- not the polished CoT a model writes after
the fact.
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    LEFT,
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
    GOOD,
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)


# ---- low-level helpers ----------------------------------------------------

TOKEN_W = 1.20
TOKEN_H = 0.62


def _token_box(label: str, color: str, width: float = TOKEN_W,
               height: float = TOKEN_H, fill_opacity: float = 0.18,
               size: int = 20) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=color,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_width=2,
    )
    txt = body_text(label, size=size, color=color, weight=BOLD)
    txt.move_to(box.get_center())
    return VGroup(box, txt)


def _vague_box(width: float = TOKEN_W, height: float = TOKEN_H) -> VGroup:
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=DIFF,
        fill_color=DIFF,
        fill_opacity=0.10,
        stroke_width=2,
    )
    glyph = body_text("?", size=24, color=DIFF, weight=BOLD)
    glyph.move_to(box.get_center())
    return VGroup(box, glyph)


# ---- scene ----------------------------------------------------------------


class SfumatoMetaphorScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        # ---------- title ---------------------------------------------------
        title = title_text(
            "How a thought actually forms",
            size=32,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.5)

        sub = body_text(
            "serial sketch  ->  iterate a vague chunk  ->  serial continue",
            size=20,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.22)

        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.wait(0.2)

        # ---------- prompt strip --------------------------------------------
        prompt = body_text(
            "Q:  what is  17 x 13 ?",
            size=22,
            color=FG,
        )
        prompt.move_to(UP * 1.55)
        self.play(FadeIn(prompt, shift=UP * 0.1), run_time=0.45)
        self.wait(0.3)

        # ---------- phase rail (labels above each band) ---------------------
        ar1_label = body_text("AR (serial)",       size=16, color=ACCENT_2, weight=BOLD)
        diff_label = body_text("diffusion (iterate)", size=16, color=DIFF,     weight=BOLD)
        ar2_label = body_text("AR (serial)",       size=16, color=ACCENT_2, weight=BOLD)

        ar1_label.move_to(UP * 0.35 + LEFT * 4.5)
        diff_label.move_to(UP * 0.35)
        ar2_label.move_to(UP * 0.35 + RIGHT * 4.5)

        # ---------- phase 1: AR sketch (left) -------------------------------
        sketch_tokens = ["17", "x", "13", "="]
        ar1_boxes = [
            _token_box(w, ACCENT_2, width=0.72 if w == "x" else TOKEN_W)
            for w in sketch_tokens
        ]
        ar1_row = VGroup(*ar1_boxes).arrange(RIGHT, buff=0.16)
        ar1_row.move_to(DOWN * 0.55 + LEFT * 3.6)

        self.play(FadeIn(ar1_label, shift=UP * 0.1), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.25) for b in ar1_boxes],
                lag_ratio=0.4,
            ),
            run_time=1.2,
        )
        self.wait(0.3)

        # ---------- phase 2: diffusion middle (iterate over candidates) -----
        vague = _vague_box(width=1.45, height=TOKEN_H)
        vague.next_to(ar1_row, RIGHT, buff=0.25)

        self.play(FadeIn(diff_label, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(vague, shift=UP * 0.1), run_time=0.45)
        self.wait(0.3)

        # candidate values that an actual mental-arithmetic process passes
        # through before settling. final value (221) is correct.
        candidates = [
            ("210", WARN, 0.20),
            ("220", WARN, 0.30),
            ("221", GOOD, 0.40),
        ]
        for value, color, opacity in candidates:
            new_box = RoundedRectangle(
                width=1.45,
                height=TOKEN_H,
                corner_radius=0.10,
                stroke_color=color,
                fill_color=color,
                fill_opacity=opacity,
                stroke_width=2,
            )
            new_box.move_to(vague[0].get_center())
            new_txt = body_text(value, size=22, color=color, weight=BOLD)
            new_txt.move_to(new_box.get_center())
            new_group = VGroup(new_box, new_txt)
            self.play(Transform(vague, new_group), run_time=0.65)
            self.wait(0.4)

        # ---------- phase 3: AR continue (right) ----------------------------
        ar2_tokens = ["Answer:", "221"]
        ar2_boxes = [_token_box(w, ACCENT_2, width=1.45 if w == "Answer:" else TOKEN_W)
                     for w in ar2_tokens]
        ar2_row = VGroup(*ar2_boxes).arrange(RIGHT, buff=0.16)
        ar2_row.next_to(vague, RIGHT, buff=0.25)

        self.play(FadeIn(ar2_label, shift=UP * 0.1), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.25) for b in ar2_boxes],
                lag_ratio=0.40,
            ),
            run_time=0.9,
        )
        self.wait(0.7)

        # ---------- closing line --------------------------------------------
        insight = body_text(
            "Cognition mixes serial autoregression with iterative refinement.",
            size=21,
            color=ACCENT,
            weight=BOLD,
        )
        insight.move_to(DOWN * 2.2)

        sub_insight = body_text(
            "the polished CoT a model writes after the fact hides the iteration",
            size=15,
            color=MUTED,
        )
        sub_insight.next_to(insight, DOWN, buff=0.18)

        self.play(FadeIn(insight, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub_insight, shift=UP * 0.08), run_time=0.4)
        self.wait(3.0)

        fade_out_all(self)
