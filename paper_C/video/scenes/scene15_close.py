"""Scene 15 — F10 in flight + close.

Third try. Earlier versions had the bullet lines crashing into each
other inside the panels because the buff inside the VGroup body was
too tight for the chosen font's metrics. This version:
  - bumps inter-line buff to 0.45 (was 0.16)
  - widens panels (w=6.0, h=5.0) and uses font_size 14 for body
  - keeps lines short so wrapping never happens

The two-column layout is preserved.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, body_text, fade_out_all, title_text)


def _panel(title_str, lines, color, w=6.0, h=5.0):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                           stroke_width=2, fill_opacity=0.08)
    head = body_text(title_str, size=20, color=color, weight=BOLD)
    body_items = [body_text(line, size=14, color=FG) for line in lines]
    body = VGroup(*body_items).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(box.get_center())
    return VGroup(box, inner)


class CloseScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("F10 in flight  +  what we claim", size=28, color=ACCENT).to_edge(UP, buff=0.4)

        left = _panel(
            "F10 (in flight)",
            ["same arch: 305M composite",
             "same 3B token budget",
             "95 % FineWeb + 5 % Q/A",
             "hypothesis: GSM8K acc",
             "moves off the 0 % floor"],
            ACCENT,
        ).move_to(LEFT * 3.6 + DOWN * 0.2)

        right = _panel(
            "What we claim",
            ["1. small AR tax, big diff gain",
             "2. trade reverses below ~1k",
             "3. count-based rep_pen on",
             "    parallel mask-fill is the",
             "    one-line fix nobody had"],
            GOOD,
        ).move_to(RIGHT * 3.6 + DOWN * 0.2)

        foot = body_text("paper_C/main.pdf   ·   github.com/eren23/sfumato   ·   ~$30 GPU",
                         size=14, color=MUTED).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(left), run_time=0.7)
        self.play(FadeIn(right), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.4)
        self.wait(45)
        fade_out_all(self, run_time=0.5)
