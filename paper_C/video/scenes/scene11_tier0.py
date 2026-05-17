"""Scene 11 — Tier 0 fix: wire the AR-side anti-rep.

Side-by-side before / after code panels.
"""
from __future__ import annotations

from manim import (Text, BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _code_panel(label, code, color, w=5.6, h=2.6):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2,
                           color=color, stroke_width=2, fill_opacity=0.08)
    head = body_text(label, size=16, color=color, weight=BOLD)
    code_t = Text(code, font="Courier", font_size=14, color=FG)
    inner = VGroup(head, code_t).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(box.get_center())
    return VGroup(box, inner)


class Tier0Scene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Tier 0: wire the existing AR-side patches", size=28, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("one-line change at each call site, no retrain", size=14, color=MUTED).next_to(title, DOWN, buff=0.15)

        before = _code_panel(
            "before — pure greedy:",
            "gen_ar(m, pr, max_new=128)",
            WARN,
        ).move_to(LEFT * 3.5 + UP * 0.4)

        after = _code_panel(
            "after — sampled with anti-rep:",
            ("gen_ar(m, pr, max_new=128,\n"
             "       temperature=0.8,\n"
             "       top_p=0.9,\n"
             "       repetition_penalty=1.15,\n"
             "       no_repeat_ngram_size=3)"),
            GOOD,
        ).move_to(RIGHT * 3.5 + UP * 0.4)

        # Results below the two panels
        res_title = body_text("Loop-rate (greedy → Tier 0):", size=16, color=FG, weight=BOLD)
        rows = VGroup(
            body_text("ar_only        100 %  →  0 %",      size=16, color=GOOD),
            body_text("mode_switch    100 %  →  60–70 %",  size=16, color=WARN),
            body_text("paired         100 %  →  80 %",     size=16, color=WARN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        result = VGroup(res_title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        result.move_to(0 * RIGHT + DOWN * 2.2)

        foot = body_text("AR mode rescued; diff-touching modes still loop on the diff side.",
                         size=14, color=MUTED).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(before), run_time=0.5)
        self.play(FadeIn(after), run_time=0.5)
        self.play(FadeIn(result), run_time=0.5)
        self.play(FadeIn(foot), run_time=0.4)
        self.wait(19)
        fade_out_all(self, run_time=0.5)
