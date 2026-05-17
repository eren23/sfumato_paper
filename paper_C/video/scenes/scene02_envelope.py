"""Scene 2 — the toy-scale envelope."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, BG, FG, MUTED, body_text, fade_out_all, title_text)


class EnvelopeScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("The toy-scale envelope", size=34, color=ACCENT).to_edge(UP, buff=0.5)
        sub = body_text("60M  →  760M params, 3k–183k steps", size=18, color=MUTED).next_to(title, DOWN, buff=0.18)

        bullets = VGroup(
            body_text("•  60M / 120M / 200M / 250M / 300M / 500M / 760M (composite, AR-only, diff-only)",
                      size=22, color=FG),
            body_text("•  GSM8K-train  (≈4M tokens)   +   FineWeb-Edu sample-10BT  (≈3–6B tokens)",
                      size=22, color=FG),
            body_text("•  3k-step recipe  ≈  $0.10 per cell on A40",
                      size=22, color=FG),
            body_text("•  Baselines: AR-only, diff-only, B3 paired (two specialised half-size models)",
                      size=22, color=FG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(sub, DOWN, buff=0.6)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        for b in bullets:
            self.play(FadeIn(b, shift=UP * 0.1), run_time=0.35)
            self.wait(0.2)
        self.wait(20)
        fade_out_all(self, run_time=0.5)
