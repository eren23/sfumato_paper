"""Scene 14c — Phase J measured composite advantages.

Three panels in one scene:
  Left   speedup bars (composite_ar_128 vs composite_diff_revise_128_16)
  Center FIM capability (AR full == AR no-suffix; structural limit)
  Right  revision NLL Δ (mode_switch_96_32 wins by 2.20 NLL in 64-96)

Slotted between scene14_beforeafter and scene15_close.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, Rectangle, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _bar(label_top, val, label_bot, color, w=0.9, h_scale=0.03):
    h = max(0.1, val * h_scale)
    rect = Rectangle(width=w, height=h, color=color, stroke_width=2,
                     fill_opacity=0.7).set_fill(color, opacity=0.7)
    top = body_text(label_top, size=14, color=color, weight=BOLD).next_to(rect, UP, buff=0.08)
    bot = body_text(label_bot, size=12, color=MUTED).next_to(rect, DOWN, buff=0.1)
    return VGroup(rect, top, bot)


def _panel_box(w, h, color):
    return RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                            stroke_width=2, fill_opacity=0.06)


class PhaseJScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Phase J — what composite delivers", size=30, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("three measured advantages on F10 final, no retraining",
                        size=14, color=MUTED).next_to(title, DOWN, buff=0.15)

        # ---- LEFT PANEL: speedup bars ----
        left_box = _panel_box(4.2, 4.4, ACCENT).move_to(LEFT * 4.5 + DOWN * 0.2)
        left_head = body_text("J.0 parallel decode", size=16, color=ACCENT, weight=BOLD)
        left_head.next_to(left_box.get_top(), DOWN, buff=0.2)

        b1 = _bar("20.1", 20.1, "AR-128\n(128 forwards)", WARN, w=0.9)
        b2 = _bar("109.5", 109.5, "diff-fill\n(16 forwards)", GOOD, w=0.9)
        bars = VGroup(b1, b2).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to(left_box.get_center() + DOWN * 0.2)

        left_foot = body_text("5.43× faster", size=20, color=GOOD, weight=BOLD)
        left_foot.next_to(left_box.get_bottom(), UP, buff=0.25)
        left_group = VGroup(left_box, left_head, bars, left_foot)

        # ---- CENTER PANEL: FIM capability ----
        ctr_box = _panel_box(4.2, 4.4, DIFF).move_to(0 * RIGHT + DOWN * 0.2)
        ctr_head = body_text("J.1 FIM capability", size=16, color=DIFF, weight=BOLD)
        ctr_head.next_to(ctr_box.get_top(), DOWN, buff=0.2)

        # Show two AR conditions producing identical NLL → proves causal-only
        ar_full_lbl = body_text("AR with full sequence:", size=12, color=FG)
        ar_full_val = body_text("NLL = 1.23 per token", size=12, color=WARN, weight=BOLD)
        ar_full_row = VGroup(ar_full_lbl, ar_full_val).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        ar_no_lbl = body_text("AR with prefix only:", size=12, color=FG)
        ar_no_val = body_text("NLL = 1.23 per token", size=12, color=WARN, weight=BOLD)
        ar_no_row = VGroup(ar_no_lbl, ar_no_val).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        identity = body_text("identical: AR ignores suffix", size=11, color=GOOD, weight=BOLD)

        diff_lbl = body_text("DIFF bidirectional:", size=12, color=DIFF)
        diff_val = body_text("can predict masked", size=12, color=DIFF, weight=BOLD)
        diff_val2 = body_text("middle from suffix", size=12, color=DIFF)
        diff_row = VGroup(diff_lbl, diff_val, diff_val2).arrange(DOWN, aligned_edge=LEFT, buff=0.04)

        ctr_inner = VGroup(ar_full_row, ar_no_row, identity, diff_row).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        ctr_inner.move_to(ctr_box.get_center() + DOWN * 0.1)

        ctr_foot = body_text("AR structurally can't", size=14, color=DIFF, weight=BOLD)
        ctr_foot.next_to(ctr_box.get_bottom(), UP, buff=0.25)
        ctr_group = VGroup(ctr_box, ctr_head, ctr_inner, ctr_foot)

        # ---- RIGHT PANEL: revision NLL ----
        right_box = _panel_box(4.2, 4.4, GOOD).move_to(RIGHT * 4.5 + DOWN * 0.2)
        right_head = body_text("J.2 revision NLL", size=16, color=GOOD, weight=BOLD)
        right_head.next_to(right_box.get_top(), DOWN, buff=0.2)

        # Three rows showing the NLL Δ
        row_a = VGroup(
            body_text("AR-128", size=12, color=WARN),
            body_text("NLL = 12.56", size=12, color=WARN, weight=BOLD),
        ).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        row_b = VGroup(
            body_text("mode-switch", size=12, color=GOOD),
            body_text("NLL = 11.82", size=12, color=GOOD, weight=BOLD),
        ).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        row_c = body_text("Δ = −0.74 NLL/token", size=14, color=GOOD, weight=BOLD)
        row_d = body_text("(−2.20 in revise band)", size=12, color=GOOD)
        right_inner = VGroup(row_a, row_b, row_c, row_d).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        right_inner.move_to(right_box.get_center() + DOWN * 0.1)

        right_foot = body_text("revision works", size=14, color=GOOD, weight=BOLD)
        right_foot.next_to(right_box.get_bottom(), UP, buff=0.25)
        right_group = VGroup(right_box, right_head, right_inner, right_foot)

        # ---- Bottom synthesis line ----
        synthesis = body_text(
            "5.43× speedup  ·  unique FIM capability  ·  −0.74 NLL revision  ·  no AR-axis tax",
            size=16, color=ACCENT_2, weight=BOLD,
        ).to_edge(DOWN, buff=0.45)

        # ---- Animation ----
        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_group), run_time=0.7)
        self.play(FadeIn(ctr_group), run_time=0.7)
        self.play(FadeIn(right_group), run_time=0.7)
        self.play(FadeIn(synthesis), run_time=0.5)

        self.wait(20)
        fade_out_all(self, run_time=0.5)
