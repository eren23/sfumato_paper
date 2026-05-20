"""Scene 14f — F11 vs F10 head-to-head (α=0.30 fine-tune effect).

Shows the proper Phase K hardening: F11 (F10 + 30k steps with α=0.30
fixed) beats F10 by -0.58 NLL on K.2 pct50 AND +2pp on GSM8K-dev acc.

Three columns:
  Left   K.2 sweep bar chart: F10 vs F11 across pct10/25/50/75
  Right  probe5 acc table: F10 vs F11 (ar_only, mode_switch, paired)
  Bottom Headline: α-schedule effect is real
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, Rectangle, RoundedRectangle,
                   Scene, RIGHT, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED,
                              WARN, body_text, fade_out_all, title_text)


def _bar(val, color, w=0.45, h_scale=0.35):
    h = max(0.1, (val - 11.0) * h_scale * 4)  # zoom in on 11.0-12.5 band
    rect = Rectangle(width=w, height=h, color=color, stroke_width=2,
                     fill_opacity=0.75).set_fill(color, opacity=0.75)
    return rect


def _panel_box(w, h, color):
    return RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                            stroke_width=2, fill_opacity=0.06)


class F11Head2HeadScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("F11 vs F10  —  α=0.30 fine-tune effect",
                           size=28, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("305M composite, fine-tuned from F10 step 183k +30k steps with α fixed at 0.30",
                        size=13, color=MUTED).next_to(title, DOWN, buff=0.12)

        # ---- LEFT PANEL: K.2 NLL sweep bars ----
        left_box = _panel_box(6.0, 4.4, ACCENT).move_to(LEFT * 3.5 + DOWN * 0.2)
        left_head = body_text("K.2 routing NLL (lower = better)",
                              size=15, color=ACCENT, weight=BOLD)
        left_head.next_to(left_box.get_top(), DOWN, buff=0.15)

        # 4 paired bars: pct10, pct25, pct50, pct75
        pcts = ["pct10", "pct25", "pct50", "pct75"]
        f10_vals = [12.10, 12.19, 11.98, 12.37]
        f11_vals = [11.58, 11.48, 11.40, 11.72]

        bar_groups = []
        for i, (lbl, f10v, f11v) in enumerate(zip(pcts, f10_vals, f11_vals)):
            b_f10 = _bar(f10v, WARN)
            b_f11 = _bar(f11v, GOOD)
            pair = VGroup(b_f10, b_f11).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
            lbl_t = body_text(lbl, size=11, color=MUTED).next_to(pair, DOWN, buff=0.08)
            v10 = body_text(f"{f10v:.2f}", size=9, color=WARN).next_to(b_f10, UP, buff=0.05)
            v11 = body_text(f"{f11v:.2f}", size=9, color=GOOD).next_to(b_f11, UP, buff=0.05)
            group = VGroup(b_f10, b_f11, lbl_t, v10, v11)
            bar_groups.append(group)
        bars = VGroup(*bar_groups).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        bars.move_to(left_box.get_center() + DOWN * 0.15)

        # Mini-legend
        leg_f10 = VGroup(
            Rectangle(width=0.25, height=0.18, color=WARN, fill_opacity=0.75).set_fill(WARN, opacity=0.75),
            body_text("F10 final", size=11, color=WARN),
        ).arrange(RIGHT, buff=0.08)
        leg_f11 = VGroup(
            Rectangle(width=0.25, height=0.18, color=GOOD, fill_opacity=0.75).set_fill(GOOD, opacity=0.75),
            body_text("F11 (α=0.30)", size=11, color=GOOD, weight=BOLD),
        ).arrange(RIGHT, buff=0.08)
        legend = VGroup(leg_f10, leg_f11).arrange(RIGHT, buff=0.5)
        legend.next_to(left_box.get_bottom(), UP, buff=0.18)

        left_group = VGroup(left_box, left_head, bars, legend)

        # ---- RIGHT PANEL: probe5 acc table ----
        right_box = _panel_box(5.6, 4.4, DIFF).move_to(RIGHT * 3.7 + DOWN * 0.2)
        right_head = body_text("GSM8K-dev acc (N=50)", size=15, color=DIFF, weight=BOLD)
        right_head.next_to(right_box.get_top(), DOWN, buff=0.15)

        header_row = VGroup(
            body_text("Mode", size=13, color=FG, weight=BOLD),
            body_text("F10", size=13, color=WARN, weight=BOLD),
            body_text("F11", size=13, color=GOOD, weight=BOLD),
            body_text("Δ", size=13, color=ACCENT_2, weight=BOLD),
        ).arrange(RIGHT, buff=0.7, aligned_edge=DOWN)

        def _row(name, v10, v11):
            d = v11 - v10
            d_color = GOOD if d > 0 else (WARN if d < 0 else MUTED)
            sign = "+" if d > 0 else ""
            return VGroup(
                body_text(name, size=12, color=FG),
                body_text(f"{v10:.0f}%", size=12, color=WARN),
                body_text(f"{v11:.0f}%", size=12, color=GOOD, weight=BOLD),
                body_text(f"{sign}{d:.0f}pp", size=12, color=d_color, weight=BOLD),
            ).arrange(RIGHT, buff=0.6, aligned_edge=DOWN)

        r1 = _row("ar_only", 4, 6)
        r2 = _row("mode_switch_96_32", 6, 0)
        r3 = _row("mode_switch_64_32", 4, 2)
        r4 = _row("paired_64_64", 0, 4)
        rows = VGroup(header_row, r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        rows.move_to(right_box.get_center() + DOWN * 0.05)

        right_foot = body_text("ar_only: +2pp, mode noisy", size=13, color=DIFF, weight=BOLD)
        right_foot.next_to(right_box.get_bottom(), UP, buff=0.18)
        right_group = VGroup(right_box, right_head, rows, right_foot)

        # ---- Bottom synthesis ----
        synthesis = body_text(
            "α=0.30 fine-tune (30k steps) → −0.58 NLL/token on K.2  +  +2pp on AR-only",
            size=15, color=ACCENT_2, weight=BOLD,
        ).to_edge(DOWN, buff=0.40)
        synthesis_sub = body_text(
            "Control: F10@step35k K.2 pct50 = 11.84 → not undertrained-artifact, real α effect",
            size=12, color=MUTED,
        ).next_to(synthesis, DOWN, buff=0.10)

        # ---- Animation ----
        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_group), run_time=0.7)
        self.play(FadeIn(right_group), run_time=0.7)
        self.play(FadeIn(synthesis), FadeIn(synthesis_sub), run_time=0.5)

        self.wait(12)
        fade_out_all(self, run_time=0.5)
