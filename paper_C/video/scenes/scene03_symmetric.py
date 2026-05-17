"""Scene 3 — symmetric trade-off (F3 vs E3b)."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _bar(label, value, label_top, color, w=2.2, h_unit=2.0):
    h = h_unit * (value / 0.8)
    rect = Rectangle(width=w, height=h, color=color, stroke_width=2, fill_opacity=0.6).set_fill(color, opacity=0.6)
    lbl = body_text(label, size=18, color=color, weight=BOLD).next_to(rect, DOWN, buff=0.15)
    top = body_text(label_top, size=16, color=FG).next_to(rect, UP, buff=0.1)
    return VGroup(rect, lbl, top)


class SymmetricScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("The symmetric trade-off", size=32, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("compute-matched: F3 (AR axis)  vs  E3b (diff axis), 200M, 3k vs 6k steps",
                        size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        # Left chart: F3 AR axis
        left_title = body_text("AR axis (F3)", size=20, color=FG, weight=BOLD).move_to(LEFT * 4 + UP * 1.5)
        b_comp_ar = _bar("composite-3k", 2.80, "2.80", ACCENT).move_to(LEFT * 5 + DOWN * 0.5)
        b_ar_6k = _bar("ar_only-6k", 2.10, "2.10", GOOD).move_to(LEFT * 3 + DOWN * 0.5)
        ann_l = body_text("ar_only wins:  −0.70 NLL", size=16, color=GOOD, weight=BOLD).move_to(LEFT * 4 + DOWN * 2.6)

        # Right chart: E3b diff axis
        right_title = body_text("diff axis (E3b)", size=20, color=FG, weight=BOLD).move_to(RIGHT * 4 + UP * 1.5)
        b_comp_diff = _bar("composite-3k", 5.42, "5.42", ACCENT).scale(0.55).move_to(RIGHT * 3 + DOWN * 0.5)
        b_diff_6k = _bar("diff_only-6k", 6.11, "6.11", DIFF).scale(0.55).move_to(RIGHT * 5 + DOWN * 0.5)
        ann_r = body_text("composite wins:  −0.69 NLL", size=16, color=ACCENT, weight=BOLD).move_to(RIGHT * 4 + DOWN * 2.6)

        # Footer
        foot = body_text("Compute can buy back the AR tax. Compute cannot buy back the diff advantage.",
                         size=20, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_title), FadeIn(right_title), run_time=0.4)
        self.play(FadeIn(b_comp_ar), FadeIn(b_ar_6k), run_time=0.6)
        self.play(FadeIn(ann_l), run_time=0.4)
        self.wait(0.4)
        self.play(FadeIn(b_comp_diff), FadeIn(b_diff_6k), run_time=0.6)
        self.play(FadeIn(ann_r), run_time=0.4)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(34)
        fade_out_all(self, run_time=0.5)
