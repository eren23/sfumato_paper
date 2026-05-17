"""Scene 9 — why NLL hid the loop collapse."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _panel(title_str, body_lines, color, w=5.6, h=3.6):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2,
                           color=color, stroke_width=2, fill_opacity=0.08)
    t = body_text(title_str, size=20, color=color, weight=BOLD)
    body = VGroup(*[body_text(line, size=15, color=FG) for line in body_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    inner = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(box.get_center())
    return VGroup(box, inner)


class NLLHidScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Why NLL hid this", size=32, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("teacher-forced vs free-run decoding measure different things",
                        size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        left = _panel(
            "Teacher-forced (NLL)",
            ["each next-token is conditioned",
             "on the GOLD next-token",
             "(not the model's prediction)",
             "→ loops literally cannot form",
             "→ NLL = 3.96 looks fine"],
            ACCENT,
        ).move_to(LEFT * 3.5 + DOWN * 0.4)

        right = _panel(
            "Free-run (sampling)",
            ["each next-token is conditioned",
             "on the model's OWN prediction",
             "→ greedy + undertrained →",
             "  self-conditioning collapse",
             "→ samples loop"],
            WARN,
        ).move_to(RIGHT * 3.5 + DOWN * 0.4)

        foot = body_text("The gap between these two can be infinite.",
                         size=22, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left), run_time=0.6)
        self.play(FadeIn(right), run_time=0.6)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(20)
        fade_out_all(self, run_time=0.5)
