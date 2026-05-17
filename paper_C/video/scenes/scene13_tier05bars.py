"""Scene 13 — Tier 0.5 results: loop-rate deltas across modes."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _bar(val, color, w=1.1, max_h=2.5):
    h = max(0.05, (val / 100.0) * max_h)
    rect = Rectangle(width=w, height=h, color=color, stroke_width=1.5,
                     fill_opacity=0.7).set_fill(color, opacity=0.7)
    pct = body_text(f"{val} %", size=12, color=color, weight=BOLD).next_to(rect, UP, buff=0.05)
    return VGroup(rect, pct)


class Tier05BarsScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Loop-rate per mode  (F9 N=50, first 10 sampled)", size=26, color=ACCENT).to_edge(UP, buff=0.4)

        modes = [
            ("ar_only", 100, 0, 0),
            ("ms_96_32", 100, 70, 10),
            ("ms_64_32", 100, 65, 20),
            ("paired_64_64", 100, 80, 40),
        ]

        groups = []
        for i, (mode, g, t0, t05) in enumerate(modes):
            bg = _bar(g, WARN)
            bt0 = _bar(t0, MUTED)
            bt05 = _bar(t05, GOOD)
            grp = VGroup(bg, bt0, bt05).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
            mlbl = body_text(mode, size=13, color=MUTED).next_to(grp, DOWN, buff=0.5)
            groups.append(VGroup(grp, mlbl))

        all_grp = VGroup(*groups).arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to(0 * RIGHT + DOWN * 0.3)

        # Legend
        legend = VGroup(
            VGroup(Rectangle(width=0.4, height=0.25, color=WARN, fill_opacity=0.7).set_fill(WARN, opacity=0.7),
                   body_text("greedy", size=14, color=WARN)).arrange(RIGHT, buff=0.15),
            VGroup(Rectangle(width=0.4, height=0.25, color=MUTED, fill_opacity=0.7).set_fill(MUTED, opacity=0.7),
                   body_text("Tier 0", size=14, color=MUTED)).arrange(RIGHT, buff=0.15),
            VGroup(Rectangle(width=0.4, height=0.25, color=GOOD, fill_opacity=0.7).set_fill(GOOD, opacity=0.7),
                   body_text("Tier 0.5 + count rep_pen", size=14, color=GOOD)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.8).next_to(title, DOWN, buff=0.3)

        foot = body_text("−40 to −60 pp loop-rate from a single sampler patch.",
                         size=20, color=GOOD, weight=BOLD).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(title), FadeIn(legend), run_time=0.5)
        self.play(FadeIn(all_grp), run_time=1.0)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(25)
        fade_out_all(self, run_time=0.5)
