"""Scene 11 — Tier 0 fix: wire the AR-side anti-rep."""
from __future__ import annotations

from manim import (Text, BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


class Tier0Scene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Tier 0: wire the existing AR-side patches", size=30, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("one-line change at each call site, no retrain", size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        before = Text(
            'gen_ar(m, pr, max_new=128)',
            font="Courier", font_size=20, color=MUTED).move_to(LEFT * 4 + UP * 1.0)
        before_lbl = body_text("before — pure greedy:", size=14, color=MUTED).next_to(before, UP, buff=0.15)

        arrow = body_text("v", size=28, color=ACCENT).move_to(0 * RIGHT + UP * 0.5)

        after = Text(
            ('gen_ar(m, pr, max_new=128,\n'
             '       temperature=0.8,  top_p=0.9,\n'
             '       repetition_penalty=1.15,\n'
             '       no_repeat_ngram_size=3)'),
            font="Courier", font_size=18, color=GOOD).move_to(0 * RIGHT + DOWN * 0.5)
        after_lbl = body_text("after — sampled with anti-rep:", size=14, color=GOOD).next_to(after, UP, buff=0.15)

        # Results card
        result = VGroup(
            body_text("Loop-rate (greedy → Tier 0):",  size=16, color=FG, weight=BOLD),
            body_text("ar_only        100 %  →  0 %",  size=16, color=GOOD),
            body_text("mode_switch    100 %  →  60-70 %",  size=16, color=WARN),
            body_text("paired         100 %  →  80 %",  size=16, color=WARN),
            body_text("AR mode rescued; diff-touching modes still loop.", size=14, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.55).set_x(0)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(before_lbl), FadeIn(before), run_time=0.5)
        self.play(FadeIn(arrow), run_time=0.3)
        self.play(FadeIn(after_lbl), FadeIn(after), run_time=0.5)
        self.play(FadeIn(result), run_time=0.6)
        self.wait(20)
        fade_out_all(self, run_time=0.5)
