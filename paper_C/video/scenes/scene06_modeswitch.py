"""Scene 6 — mode-switching inference lift (E3a)."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _bar(label, val, color, w=1.4, h_unit=0.7):
    h = max(0.15, val * h_unit)
    r = Rectangle(width=w, height=h, color=color, stroke_width=2,
                  fill_opacity=0.6).set_fill(color, opacity=0.6)
    lbl = body_text(label, size=14, color=color, weight=BOLD).next_to(r, DOWN, buff=0.1)
    top = body_text(f"{val:.1f}%", size=14, color=FG).next_to(r, UP, buff=0.05)
    return VGroup(r, lbl, top)


class ModeSwitchScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Mode-switching at inference (E3a, n=5)", size=30, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("GSM8K-dev N=50, 200M-3k composite vs same-recipe ar_only", size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        # 4 modes × 2 variants
        modes = [
            ("ar_only", 2.8, 2.0),
            ("ms_96_32", 2.8, 1.6),
            ("ms_64_32", 4.0, 1.6),
            ("paired_64_64", 2.4, 1.6),
        ]
        groups = []
        x_anchor = LEFT * 5
        for i, (mode, c, a) in enumerate(modes):
            bc = _bar("composite", c, ACCENT)
            ba = _bar("ar_only", a, WARN)
            grp = VGroup(bc, ba).arrange(RIGHT, buff=0.25)
            grp.move_to(x_anchor + RIGHT * (i * 2.7) + DOWN * 0.6)
            mlbl = body_text(mode, size=14, color=MUTED).next_to(grp, DOWN, buff=0.7)
            groups.append(VGroup(grp, mlbl))

        all_grp = VGroup(*groups).move_to(0 * RIGHT + DOWN * 0.4)

        foot = body_text("Best lift: ms_64_32  composite 4.0 ± 0.6 %   vs   ar_only 1.6 ± 0.4 %",
                         size=18, color=GOOD, weight=BOLD).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(all_grp), run_time=1.0)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(25)
        fade_out_all(self, run_time=0.5)
