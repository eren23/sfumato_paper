"""Scene 5 — honest negatives (OOD + ECE)."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, BG, FG, MUTED, WARN, body_text, fade_out_all, title_text)


def _kv(k, v, color=FG):
    return VGroup(body_text(k, size=18, color=color), body_text(v, size=18, color=color)).arrange(RIGHT, buff=0.8)


class NegativesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Honest negatives", size=32, color=WARN).to_edge(UP, buff=0.4)
        sub = body_text("we report these alongside the wins", size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        # Left card: OOD
        ood_title = body_text("OOD perplexity", size=22, color=FG, weight=BOLD).move_to(LEFT * 3.5 + UP * 1.5)
        ood_rows = VGroup(
            body_text("WikiText, 300M:  composite +0.18 NLL", size=18, color=WARN),
            body_text("OpenWebText, 300M:  composite +0.20", size=18, color=WARN),
            body_text("Monotonic with scale.", size=16, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ood_title, DOWN, buff=0.4)

        # Right card: ECE
        ece_title = body_text("Calibration (ECE)", size=22, color=FG, weight=BOLD).move_to(RIGHT * 3.5 + UP * 1.5)
        ece_rows = VGroup(
            body_text("composite ECE worse at 4/5 scales", size=18, color=WARN),
            body_text("top-1 acc lower at every scale", size=18, color=WARN),
            body_text("not 'better calibrated', just less confident.", size=16, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ece_title, DOWN, buff=0.4)

        ood_grp = VGroup(ood_title, ood_rows)
        ece_grp = VGroup(ece_title, ece_rows)

        foot = body_text("Composite does not transfer to OOD prose. Calibration is not improved.",
                         size=20, color=WARN, weight=BOLD).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(ood_grp), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(ece_grp), run_time=0.6)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(25)
        fade_out_all(self, run_time=0.5)
