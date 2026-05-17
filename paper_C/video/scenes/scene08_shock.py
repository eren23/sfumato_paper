"""Scene 8 — the F9 sample-quality shock."""
from __future__ import annotations

from manim import (Text, BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, MUTED, WARN, body_text, fade_out_all, title_text)


class ShockScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("F9 final sample (greedy decode)", size=30, color=WARN).to_edge(UP, buff=0.4)
        sub = body_text("305M composite, 3B FineWeb tokens, GSM8K-dev Q0 — paired_64_64 mode",
                        size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        sample = Text(
            ('"She makes a lot of money by selling her eggs.\n'
             'She makes a lot of money by selling her eggs.\n'
             'She makes a lot of money by selling her eggs.\n'
             'She makes a lot of money by selling her eggs.\n'
             '...  x 17 ..."'),
            font="Courier", font_size=20, color=FG,
        ).move_to(0 * RIGHT + UP * 0.3)

        metrics = VGroup(
            body_text("val_ar_nll = 3.96      ✓  looks healthy", size=20, color=ACCENT, weight=BOLD),
            body_text("GSM8K-dev free-run accuracy:   0 / 50", size=22, color=WARN, weight=BOLD),
            body_text("Loop rate across all modes:    ~100 %", size=22, color=WARN, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.7).set_x(0)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(sample), run_time=0.7)
        self.wait(0.5)
        for m in metrics:
            self.play(FadeIn(m, shift=UP * 0.1), run_time=0.4)
            self.wait(0.3)
        self.wait(28)
        fade_out_all(self, run_time=0.5)
