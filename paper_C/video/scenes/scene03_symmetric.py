"""Scene 3 — symmetric trade-off (F3 vs E3b).

Fix: clean grouped bars per chart, consistent scale across charts via
absolute heights; no overlap between bars or with footer.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _bar(val, color, w=0.85, h_scale=0.55):
    h = max(0.2, val * h_scale)
    rect = Rectangle(width=w, height=h, color=color, stroke_width=2,
                     fill_opacity=0.7).set_fill(color, opacity=0.7)
    return rect


def _bar_group(label_top1, val1, color1, label1, label_top2, val2, color2, label2):
    """Two bars side-by-side bottom-aligned with shared baseline."""
    b1 = _bar(val1, color1)
    b2 = _bar(val2, color2)
    # Bottom-align them
    grp = VGroup(b1, b2).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
    top1 = body_text(label_top1, size=13, color=FG).next_to(b1, UP, buff=0.08)
    top2 = body_text(label_top2, size=13, color=FG).next_to(b2, UP, buff=0.08)
    lbl1 = body_text(label1, size=12, color=color1, weight=BOLD).next_to(b1, DOWN, buff=0.1)
    lbl2 = body_text(label2, size=12, color=color2, weight=BOLD).next_to(b2, DOWN, buff=0.1)
    return VGroup(grp, top1, top2, lbl1, lbl2)


class SymmetricScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("The symmetric trade-off", size=30, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("compute-matched: F3 (AR axis)  vs  E3b (diff axis), 200M params, 3k vs 6k steps",
                        size=14, color=MUTED).next_to(title, DOWN, buff=0.12)

        # Left chart — AR axis: composite-3k 2.80  vs  ar_only-6k 2.10
        left_title = body_text("AR axis (F3)", size=18, color=FG, weight=BOLD)
        left_bars = _bar_group(
            "2.80", 2.80, ACCENT, "composite-3k",
            "2.10", 2.10, GOOD,   "ar_only-6k",
        )
        left_ann = body_text("ar_only wins:  −0.70 NLL", size=14, color=GOOD, weight=BOLD)
        left_chart = VGroup(left_title, left_bars, left_ann).arrange(DOWN, buff=0.18)
        left_chart.move_to(LEFT * 3.6 + DOWN * 0.3)

        # Right chart — diff axis: composite-3k 5.42  vs  diff_only-6k 6.11
        right_title = body_text("diff axis (E3b)", size=18, color=FG, weight=BOLD)
        right_bars = _bar_group(
            "5.42", 5.42, ACCENT, "composite-3k",
            "6.11", 6.11, DIFF,   "diff_only-6k",
        )
        # diff bars are bigger numbers → bigger bars; scale them down for visual parity
        right_bars.scale(0.55)
        right_ann = body_text("composite wins:  −0.69 NLL", size=14, color=ACCENT, weight=BOLD)
        right_chart = VGroup(right_title, right_bars, right_ann).arrange(DOWN, buff=0.18)
        right_chart.move_to(RIGHT * 3.6 + DOWN * 0.3)

        foot = body_text("Compute can buy back the AR tax. Compute cannot buy back the diff advantage.",
                         size=16, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_chart), run_time=0.7)
        self.play(FadeIn(right_chart), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(32)
        fade_out_all(self, run_time=0.5)
