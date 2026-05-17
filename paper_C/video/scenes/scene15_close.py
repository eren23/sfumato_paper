"""Scene 15 — F10 in flight + close."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, body_text, fade_out_all, title_text)


def _panel(title_str, lines, color, w=5.6, h=4.4):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                           stroke_width=2, fill_opacity=0.08)
    head = body_text(title_str, size=20, color=color, weight=BOLD)
    body = VGroup(*[body_text(line, size=15, color=FG) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(box.get_center())
    return VGroup(box, inner)


class CloseScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("F10 in flight  +  what we claim", size=30, color=ACCENT).to_edge(UP, buff=0.4)

        left = _panel(
            "F10 (in flight)",
            ["same arch as F9: 305M composite",
             "same 3B token budget",
             "but: load_mixed_tokens",
             "= 95 % FineWeb-Edu + 5 %",
             "formatted GSM8K Q/A",
             "",
             "hypothesis: accuracy moves",
             "off the 0 % free-run floor;",
             "model finally learns the",
             "\"Answer:\" structure."],
            ACCENT,
        ).move_to(LEFT * 3.5 + DOWN * 0.4)

        right = _panel(
            "What we claim",
            ["1. Composite trades small AR",
             "   tax for substantial diff",
             "   gain, symmetric and",
             "   compute-stable.",
             "2. The trade reverses in the",
             "   data-constrained regime;",
             "   crossover at ~1k problems.",
             "3. Parallel mask-fill decoders",
             "   need count-based rep_pen,",
             "   not set-based. One-line",
             "   patch, big lift."],
            GOOD,
        ).move_to(RIGHT * 3.5 + DOWN * 0.4)

        foot = body_text("paper:  /paper_C/main.pdf      ·      repo:  github.com/eren23/sfumato      ·      spend: ~$30 GPU",
                         size=15, color=MUTED).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(left), run_time=0.7)
        self.play(FadeIn(right), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(45)
        fade_out_all(self, run_time=0.5)
