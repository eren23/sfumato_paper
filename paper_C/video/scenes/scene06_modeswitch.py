"""Scene 6 — mode-switching inference lift (E3a).

Fix: 4 modes laid out with enough spacing; per-mode bar pairs
bottom-aligned; labels under bars don't collide with neighbours.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, BG, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _bar(val, color, w=0.55, h_scale=0.6):
    h = max(0.1, val * h_scale)
    rect = Rectangle(width=w, height=h, color=color, stroke_width=1.5,
                     fill_opacity=0.7).set_fill(color, opacity=0.7)
    return rect


def _bar_pair(val_c, val_a):
    bc = _bar(val_c, ACCENT)
    ba = _bar(val_a, WARN)
    grp = VGroup(bc, ba).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    top_c = body_text(f"{val_c:.1f}%", size=11, color=ACCENT, weight=BOLD).next_to(bc, UP, buff=0.05)
    top_a = body_text(f"{val_a:.1f}%", size=11, color=WARN, weight=BOLD).next_to(ba, UP, buff=0.05)
    return VGroup(grp, top_c, top_a)


class ModeSwitchScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Mode-switching at inference (E3a, n=5)", size=28, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("GSM8K-dev N=50,  200M-3k composite vs same-recipe ar_only",
                        size=14, color=MUTED).next_to(title, DOWN, buff=0.12)

        # Legend
        legend = VGroup(
            VGroup(Rectangle(width=0.3, height=0.2, color=ACCENT, fill_opacity=0.7).set_fill(ACCENT, opacity=0.7),
                   body_text("composite", size=13, color=ACCENT)).arrange(RIGHT, buff=0.12),
            VGroup(Rectangle(width=0.3, height=0.2, color=WARN, fill_opacity=0.7).set_fill(WARN, opacity=0.7),
                   body_text("ar_only", size=13, color=WARN)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.6).next_to(sub, DOWN, buff=0.3)

        # 4 modes × 2 bars each
        modes = [
            ("ar_only",      2.8, 2.0),
            ("ms_96_32",     2.8, 1.6),
            ("ms_64_32",     4.0, 1.6),
            ("paired_64_64", 2.4, 1.6),
        ]
        cells = []
        for mode, c, a in modes:
            pair = _bar_pair(c, a)
            mlbl = body_text(mode, size=13, color=MUTED).next_to(pair, DOWN, buff=0.4)
            cells.append(VGroup(pair, mlbl))

        all_groups = VGroup(*cells).arrange(RIGHT, buff=1.1, aligned_edge=DOWN).move_to(0 * RIGHT + DOWN * 0.3)

        foot = body_text("Best lift:  ms_64_32  composite 4.0 ± 0.6 %   vs   ar_only 1.6 ± 0.4 %",
                         size=16, color=GOOD, weight=BOLD).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(legend), run_time=0.4)
        self.play(FadeIn(all_groups), run_time=0.9)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(24)
        fade_out_all(self, run_time=0.5)
