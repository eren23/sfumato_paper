"""Scene 12 — set-based vs count-based rep_pen on parallel mask-fill."""
from __future__ import annotations

from manim import (Text, BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


class CountRepScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Why set-based rep_pen fails on parallel mask-fill", size=28, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("a single diff forward pass fills N masked positions from the same logits",
                        size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        # Top panel: set-based
        set_title = body_text("set-based rep_pen (standard)", size=20, color=WARN, weight=BOLD).move_to(LEFT * 4 + UP * 1.6)
        set_formula = Text("logit['eggs'] /=  1.15    (once)", font="Courier", font_size=18, color=WARN).next_to(set_title, DOWN, buff=0.2)
        set_consequence = body_text(
            "→  every masked position still argmaxes to 'eggs'",
            size=15, color=MUTED).next_to(set_formula, DOWN, buff=0.2)
        set_grp = VGroup(set_title, set_formula, set_consequence).move_to(LEFT * 3.5 + UP * 1.2)

        # Bottom panel: count-based
        cnt_title = body_text("count-based rep_pen (our fix)", size=20, color=GOOD, weight=BOLD).move_to(RIGHT * 4 + UP * 1.6)
        cnt_formula = Text("logit[tok] /=  1.15 ** count(tok)", font="Courier", font_size=18, color=GOOD).next_to(cnt_title, DOWN, buff=0.2)
        cnt_example = body_text(
            "30 'eggs' in context  →  / 1.15³⁰  ≈  66",
            size=15, color=GOOD).next_to(cnt_formula, DOWN, buff=0.2)
        cnt_grp = VGroup(cnt_title, cnt_formula, cnt_example).move_to(RIGHT * 3.5 + UP * 1.2)

        # Bottom: visualization of N masked positions all wanting 'eggs'
        viz_lbl = body_text("16 masked positions, single forward pass:", size=14, color=MUTED).move_to(0 * RIGHT + DOWN * 0.5)
        boxes = VGroup()
        for i in range(16):
            box = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.05,
                                   color=DIFF, stroke_width=1.5, fill_opacity=0.3)
            inner = body_text("eggs", size=8, color=FG)
            inner.move_to(box.get_center())
            grp = VGroup(box, inner)
            boxes.add(grp)
        boxes.arrange(RIGHT, buff=0.12).move_to(0 * RIGHT + DOWN * 1.2)

        foot = body_text("One-line patch. Generalises to any mask-fill / diffusion LM.",
                         size=18, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(set_grp), run_time=0.6)
        self.play(FadeIn(cnt_grp), run_time=0.6)
        self.play(FadeIn(viz_lbl), FadeIn(boxes), run_time=0.6)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(25)
        fade_out_all(self, run_time=0.5)
