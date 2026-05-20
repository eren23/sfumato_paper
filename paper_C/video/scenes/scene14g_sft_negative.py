"""Scene 14g — SFT Phase L: format learned, math not.

Honest-negative scene. Shows that SFT'ing F10 on GSM8K-train Q/A pairs
(7473 examples × 2 epochs) cuts training loss 2.84 → 1.0 but does NOT
lift GSM8K-dev accuracy beyond the F10 base ~4% floor.

Three panels:
  Left   Loss curve (qualitative): 2.84 → 1.0 in 7k steps
  Center Sample: format learned, math wrong
  Right  Final acc table: SFT 0-6%, within F10 noise
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RoundedRectangle, Scene, RIGHT,
                   UP, VGroup, Line, Polygon, Rectangle)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED,
                              WARN, body_text, fade_out_all, title_text)


def _panel_box(w, h, color):
    return RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                            stroke_width=2, fill_opacity=0.06)


class SFTNegativeScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Phase L  —  SFT on GSM8K-train: format learned, math not",
                           size=24, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("F10 + 7473 Q/A pairs × 2 epochs, BS=8, LR=3e-5, 7.8 min on A100",
                        size=13, color=MUTED).next_to(title, DOWN, buff=0.12)

        # ---- LEFT PANEL: loss curve sketch ----
        left_box = _panel_box(4.2, 4.6, DIFF).move_to(LEFT * 4.6 + DOWN * 0.2)
        left_head = body_text("Training loss curve", size=14, color=DIFF, weight=BOLD)
        left_head.next_to(left_box.get_top(), DOWN, buff=0.18)

        # Sketch: axes + decreasing curve from (0, 2.84) to (1, 1.0)
        axis_origin = left_box.get_center() + DOWN * 0.5 + LEFT * 1.3
        x_axis = Line(axis_origin, axis_origin + RIGHT * 2.6, stroke_width=2, color=FG)
        y_axis = Line(axis_origin, axis_origin + UP * 2.2, stroke_width=2, color=FG)

        # Curve: 5-point polyline 2.84 → 1.78 → 1.27 → 1.05 → 0.95 → ~1.0
        def pt(x_frac, loss):
            # loss 0 to 3 → y 0 to 2.2; x_frac 0 to 1 → x 0 to 2.6
            x = axis_origin[0] + x_frac * 2.6
            y = axis_origin[1] + (loss / 3.0) * 2.2
            return [x, y, 0]

        curve_pts = [pt(0, 2.84), pt(0.10, 1.78), pt(0.20, 1.27),
                     pt(0.40, 1.05), pt(0.60, 0.95), pt(1.0, 1.00)]
        curve = Polygon(*curve_pts, *reversed(curve_pts[1:]),
                        stroke_width=3, color=GOOD, fill_opacity=0)
        # Endpoint labels
        start_lbl = body_text("2.84", size=12, color=WARN, weight=BOLD)
        start_lbl.move_to(pt(0, 2.84)).shift(UP * 0.15 + LEFT * 0.15)
        end_lbl = body_text("≈1.0", size=12, color=GOOD, weight=BOLD)
        end_lbl.move_to(pt(1.0, 1.0)).shift(UP * 0.15 + RIGHT * 0.20)
        x_lbl = body_text("step (0 → 7472)", size=10, color=MUTED)
        x_lbl.next_to(x_axis, DOWN, buff=0.20)
        y_lbl = body_text("CE loss on answer tokens", size=10, color=MUTED)
        y_lbl.rotate(3.14159 / 2).next_to(y_axis, LEFT, buff=0.15)

        left_inner = VGroup(x_axis, y_axis, curve, start_lbl, end_lbl, x_lbl, y_lbl)
        left_foot = body_text("loss converges fine", size=13, color=GOOD, weight=BOLD)
        left_foot.next_to(left_box.get_bottom(), UP, buff=0.20)
        left_group = VGroup(left_box, left_head, left_inner, left_foot)

        # ---- CENTER PANEL: sample text ----
        ctr_box = _panel_box(5.0, 4.6, ACCENT).move_to(0 * RIGHT + DOWN * 0.2)
        ctr_head = body_text("Sample output (greedy)", size=14, color=ACCENT, weight=BOLD)
        ctr_head.next_to(ctr_box.get_top(), DOWN, buff=0.18)

        q = body_text("Q: Janet's ducks lay 16 eggs/day...", size=11, color=MUTED)
        a_intro = body_text("F10+SFT predicts:", size=11, color=FG, weight=BOLD)
        a_l1 = body_text("\"Half of blue is 2/2=<<2/2=1>>1/2 inch", size=11, color=WARN)
        a_l2 = body_text(" of white. So it takes 1/2=<<1/2=1>>", size=11, color=WARN)
        a_l3 = body_text(" 1/2 inch of white. So it takes 1/2...\"", size=11, color=WARN)

        verdict_lbl = body_text("→ format ✓  math ✗  loops at step 3",
                                size=12, color=WARN, weight=BOLD)

        ctr_inner = VGroup(q, a_intro, a_l1, a_l2, a_l3, verdict_lbl).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18)
        ctr_inner.move_to(ctr_box.get_center() + DOWN * 0.05)

        ctr_foot = body_text("learned the SHAPE, not arithmetic", size=12, color=WARN, weight=BOLD)
        ctr_foot.next_to(ctr_box.get_bottom(), UP, buff=0.18)
        ctr_group = VGroup(ctr_box, ctr_head, ctr_inner, ctr_foot)

        # ---- RIGHT PANEL: acc table ----
        right_box = _panel_box(4.2, 4.6, WARN).move_to(RIGHT * 4.6 + DOWN * 0.2)
        right_head = body_text("GSM8K-dev acc (N=50)", size=14, color=WARN, weight=BOLD)
        right_head.next_to(right_box.get_top(), DOWN, buff=0.18)

        header = VGroup(
            body_text("Mode", size=12, color=FG, weight=BOLD),
            body_text("F10", size=12, color=FG, weight=BOLD),
            body_text("+SFT", size=12, color=FG, weight=BOLD),
        ).arrange(RIGHT, buff=0.55, aligned_edge=DOWN)

        def _row(name, v10, vsft):
            return VGroup(
                body_text(name, size=11, color=FG),
                body_text(f"{v10:.0f}%", size=11, color=MUTED),
                body_text(f"{vsft:.0f}%", size=11, color=WARN if vsft <= v10 else GOOD, weight=BOLD),
            ).arrange(RIGHT, buff=0.55, aligned_edge=DOWN)

        rows = VGroup(
            header,
            _row("ar_only (samp)", 4, 0),
            _row("ar_only (greedy)", 4, 2),
            _row("mode_switch_96_32", 4, 6),
            _row("mode_switch_64_32", 4, 4),
            _row("paired", 4, 0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rows.move_to(right_box.get_center() + DOWN * 0.05)

        right_foot = body_text("Δ ≈ 0pp  (within noise)", size=13, color=WARN, weight=BOLD)
        right_foot.next_to(right_box.get_bottom(), UP, buff=0.18)
        right_group = VGroup(right_box, right_head, rows, right_foot)

        # ---- Bottom synthesis ----
        synthesis = body_text(
            "honest negative: 305M too small for math reasoning; SFT format-only",
            size=14, color=ACCENT_2, weight=BOLD,
        ).to_edge(DOWN, buff=0.45)

        # ---- Animation ----
        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_group), run_time=0.7)
        self.play(FadeIn(ctr_group), run_time=0.7)
        self.play(FadeIn(right_group), run_time=0.7)
        self.play(FadeIn(synthesis), run_time=0.5)

        self.wait(12)
        fade_out_all(self, run_time=0.5)
