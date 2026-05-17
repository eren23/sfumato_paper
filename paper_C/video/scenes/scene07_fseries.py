"""Scene 7 — F-series scale-up + F9 hero stats."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, body_text, fade_out_all, title_text)


class FSeriesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("From toy to scale: F-series", size=32, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("the same recipe, six orders of magnitude in compute spend",
                        size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        runs = [
            ("F4", "500M",  "GSM8K", "$0.30"),
            ("F6", "B3 / 254M+254M", "GSM8K", "$0.30"),
            ("F7", "760M (mislabelled 1B)", "FineWeb 2B", "$8"),
            ("F8b/F8c", "8M param-golf", "FineWeb 200M", "$0.40"),
            ("F9", "305M hero", "FineWeb 3B", "$15"),
        ]
        rows = VGroup()
        for name, scale, data, cost in runs:
            r = VGroup(
                body_text(name, size=18, color=ACCENT_2, weight=BOLD).set_x(0),
                body_text(scale, size=18, color=FG),
                body_text(data, size=18, color=MUTED),
                body_text(cost, size=18, color=GOOD),
            ).arrange(RIGHT, buff=0.7)
            rows.add(r)
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(0 * RIGHT + UP * 0.0)

        hero_box = Rectangle(width=10, height=1.4, color=ACCENT, stroke_width=2,
                             fill_opacity=0.08).set_fill(ACCENT, opacity=0.08).to_edge(DOWN, buff=0.6)
        hero_lbl = body_text("F9: 305M composite,  3B FineWeb tokens,  33.8 h on A40,  val_ar_nll = 3.96",
                             size=20, color=ACCENT, weight=BOLD).move_to(hero_box)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(rows), run_time=0.9)
        self.play(FadeIn(hero_box), FadeIn(hero_lbl), run_time=0.6)
        self.wait(20)
        fade_out_all(self, run_time=0.5)
