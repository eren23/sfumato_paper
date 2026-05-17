"""Scene 4 — data-efficiency crossover (E3c).

Fix: move crossover label off the curve so it does not overlap data
points; place the 'composite wins' / 'ar_only wins' annotations in
quadrants that are visibly empty.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Axes, Dot, Scene, UP, VGroup, Line)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


class CrossoverScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Data-efficiency crossover (E3c)", size=30, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("Δ_NLL = composite − ar_only,  200M, 3k steps,  varying GSM8K-train size",
                        size=14, color=MUTED).next_to(title, DOWN, buff=0.15)

        axes = Axes(
            x_range=[0, 8000, 1000], y_range=[-0.5, 0.4, 0.1],
            x_length=9, y_length=4,
            tips=False,
            axis_config={"color": FG, "stroke_width": 1.5},
        ).move_to(0 * RIGHT + DOWN * 0.4)
        x_lbl = body_text("GSM8K-train problems", size=14, color=MUTED).next_to(axes, DOWN, buff=0.3)
        y_lbl = body_text("Δ NLL", size=14, color=MUTED).next_to(axes, LEFT, buff=0.25).rotate(1.5708)

        data = [(500, -0.40), (800, -0.165), (1000, -0.01), (1200, 0.052),
                (1500, 0.180), (2000, 0.13), (4000, 0.26), (7500, 0.22)]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=ACCENT, radius=0.08) for x, y in data])
        lines = VGroup(*[
            Line(axes.c2p(data[i][0], data[i][1]), axes.c2p(data[i + 1][0], data[i + 1][1]),
                 color=ACCENT, stroke_width=2)
            for i in range(len(data) - 1)
        ])
        zero_line = Line(axes.c2p(0, 0), axes.c2p(8000, 0), color=MUTED, stroke_width=1.2)

        # Crossover marker: keep the dot at (1000, 0); push the label HIGH-LEFT
        # so it does not collide with the descending curve below or the points
        # to the right of it.
        cross_dot = Dot(axes.c2p(1000, 0), color=GOOD, radius=0.12)
        cross_lbl = body_text("crossover  ~ 1k problems", size=14, color=GOOD, weight=BOLD)
        cross_lbl.move_to(axes.c2p(2400, 0.32))

        # Annotations: composite-wins in the deep-negative region (bottom-left),
        # ar_only-wins in the positive plateau (top-right), both pushed clear
        # of the data points.
        below_lbl = body_text("composite wins", size=12, color=GOOD).move_to(axes.c2p(600, -0.46))
        above_lbl = body_text("ar_only wins", size=12, color=WARN).move_to(axes.c2p(6500, 0.36))

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(axes), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(zero_line), run_time=0.6)
        self.play(FadeIn(dots), FadeIn(lines), run_time=0.7)
        self.play(FadeIn(below_lbl), FadeIn(above_lbl), run_time=0.4)
        self.play(FadeIn(cross_dot), FadeIn(cross_lbl), run_time=0.5)
        self.wait(28)
        fade_out_all(self, run_time=0.5)
