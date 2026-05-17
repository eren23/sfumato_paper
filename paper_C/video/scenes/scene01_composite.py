"""Scene 1 — what composite training is."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, body_text, fade_out_all, title_text)


def _head(label: str, color):
    box = RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15,
                            color=color, stroke_width=2, fill_opacity=0.12)
    lbl = body_text(label, size=22, color=color, weight=BOLD)
    return VGroup(box, lbl)


class CompositeScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("What composite training is", size=34, color=ACCENT).to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)

        # Backbone block
        backbone = RoundedRectangle(width=5.0, height=1.6, corner_radius=0.2,
                                    color=FG, stroke_width=2, fill_opacity=0.06)
        bb_lbl = body_text("Shared transformer backbone", size=20, color=FG, weight=BOLD)
        bb = VGroup(backbone, bb_lbl).move_to(0 * RIGHT + 0.5 * UP)

        # Two heads beneath
        ar_head = _head("AR LM head", ACCENT).move_to(LEFT * 3 + DOWN * 1.5)
        diff_head = _head("Diffusion mask-fill head", DIFF).move_to(RIGHT * 3 + DOWN * 1.5)

        # Loss formula
        formula = body_text("L  =  α · L_AR  +  (1 − α) · L_diff", size=24, color=ACCENT_2, weight=BOLD)
        formula.next_to(diff_head, DOWN, buff=0.8).set_x(0)

        sched = body_text("α-schedule: 1.0 → 0.5 over training", size=18, color=MUTED)
        sched.next_to(formula, DOWN, buff=0.2)

        self.play(FadeIn(bb), run_time=0.6)
        self.play(FadeIn(ar_head), FadeIn(diff_head), run_time=0.6)
        self.play(FadeIn(formula), run_time=0.6)
        self.play(FadeIn(sched), run_time=0.4)
        self.wait(26)
        fade_out_all(self, run_time=0.5)
