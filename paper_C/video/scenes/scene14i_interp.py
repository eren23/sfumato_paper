"""Scene 14i — Phase P interpretability headline.

Three panels in a row:
  Left   layer-by-layer AR-vs-diff residual cosine (drops 0.99 → 0.54)
  Center cross-head SAE feature overlap (mean cosine 0.169, modes specialise)
  Right  per-prompt top-8 feature index overlap (0 across all 12 prompts)

Bottom synthesis: "modes use DISJOINT internal features — mechanistic
support for the trade-off framing."
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, Rectangle, RoundedRectangle, Scene,
                   RIGHT, UP, VGroup, Line)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN,
                              body_text, fade_out_all, title_text)


def _panel_box(w, h, color):
    return RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                            stroke_width=2, fill_opacity=0.06)


class InterpScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Interpretability — AR and diff use disjoint features",
                           size=24, color=ACCENT).to_edge(UP, buff=0.30)
        sub = body_text("Phase P: TopK SAEs (k=64, 16384 features) on F10 backbone + per-head",
                        size=12, color=MUTED).next_to(title, DOWN, buff=0.10)

        # ---- LEFT PANEL: layer-by-layer cosine curve ----
        left_box = _panel_box(4.6, 4.2, ACCENT).move_to(LEFT * 4.7 + DOWN * 0.3)
        left_head = body_text("P.0 — residual divergence by layer",
                              size=13, color=ACCENT, weight=BOLD)
        left_head.next_to(left_box.get_top(), DOWN, buff=0.12)

        cos_per_layer = [0.987, 0.978, 0.957, 0.939, 0.929, 0.904, 0.879,
                         0.823, 0.762, 0.700, 0.650, 0.607, 0.570, 0.527,
                         0.506, 0.522, 0.519, 0.535, 0.539, 0.543]
        ox = left_box.get_center()[0] - 1.7
        oy = left_box.get_center()[1] - 1.3
        x_axis = Line([ox, oy, 0], [ox + 3.4, oy, 0], stroke_width=2, color=FG)
        y_axis = Line([ox, oy, 0], [ox, oy + 2.3, 0], stroke_width=2, color=FG)
        def pt(layer, cos):
            x = ox + (layer / 19) * 3.4
            y = oy + cos * 2.3
            return [x, y, 0]
        from manim import Polygon
        pts = [pt(i, c) for i, c in enumerate(cos_per_layer)]
        curve = Polygon(*pts, stroke_width=3, color=GOOD, fill_opacity=0)
        l_label_top = body_text("cos = 0.99", size=10, color=GOOD).move_to(pt(0, 0.987)).shift(UP*0.18 + RIGHT*0.6)
        l_label_bot = body_text("cos = 0.54", size=10, color=WARN, weight=BOLD).move_to(pt(19, 0.543)).shift(DOWN*0.18 + LEFT*0.4)
        x_lbl = body_text("layer 0 → 19", size=10, color=MUTED).next_to(x_axis, DOWN, buff=0.10)
        y_lbl = body_text("cos(AR, diff)", size=10, color=MUTED)
        y_lbl.rotate(3.14159 / 2).next_to(y_axis, LEFT, buff=0.12)
        left_inner = VGroup(x_axis, y_axis, curve, l_label_top, l_label_bot, x_lbl, y_lbl)
        left_foot = body_text("attention-mask cascades", size=12, color=ACCENT, weight=BOLD)
        left_foot.next_to(left_box.get_bottom(), UP, buff=0.18)
        left_group = VGroup(left_box, left_head, left_inner, left_foot)

        # ---- CENTER PANEL: SAE cosine number ----
        ctr_box = _panel_box(4.6, 4.2, DIFF).move_to(0 * RIGHT + DOWN * 0.3)
        ctr_head = body_text("P.2 — SAE feature cosine",
                             size=13, color=DIFF, weight=BOLD)
        ctr_head.next_to(ctr_box.get_top(), DOWN, buff=0.12)

        cosine_big = title_text("0.169", size=44, color=DIFF, weight=BOLD)
        cosine_big.move_to(ctr_box.get_center() + UP * 0.35)
        cosine_sub = body_text("mean best-cosine across 16384 features",
                               size=11, color=FG)
        cosine_sub.move_to(ctr_box.get_center() + DOWN * 0.10)

        # 3 rows of small percentages
        rows = VGroup(
            body_text("only 1.84% with sibling ≥ 0.5", size=11, color=MUTED),
            body_text("only 0.42% with sibling ≥ 0.7", size=11, color=MUTED),
            body_text("only 0.01% with sibling ≥ 0.9", size=11, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.move_to(ctr_box.get_center() + DOWN * 0.85)

        ctr_foot = body_text("modes SPECIALISE",
                             size=14, color=DIFF, weight=BOLD)
        ctr_foot.next_to(ctr_box.get_bottom(), UP, buff=0.18)
        ctr_group = VGroup(ctr_box, ctr_head, cosine_big, cosine_sub, rows, ctr_foot)

        # ---- RIGHT PANEL: per-prompt zero overlap ----
        right_box = _panel_box(4.6, 4.2, GOOD).move_to(RIGHT * 4.7 + DOWN * 0.3)
        right_head = body_text("P.3 — per-prompt confirmation",
                               size=13, color=GOOD, weight=BOLD)
        right_head.next_to(right_box.get_top(), DOWN, buff=0.12)

        big_zero = title_text("0", size=64, color=GOOD, weight=BOLD)
        big_zero.move_to(right_box.get_center() + UP * 0.40)
        zero_sub = body_text("top-8 feature index overlap",
                             size=11, color=FG)
        zero_sub.move_to(right_box.get_center() + DOWN * 0.10)
        zero_sub2 = body_text("across all 12 test prompts",
                              size=11, color=FG)
        zero_sub2.move_to(right_box.get_center() + DOWN * 0.32)

        prompt_classes = VGroup(
            body_text("4 GSM8K math problems", size=10, color=MUTED),
            body_text("4 FineWeb prose snippets", size=10, color=MUTED),
            body_text("4 explicit math-mode prompts", size=10, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        prompt_classes.move_to(right_box.get_center() + DOWN * 1.05)

        right_foot = body_text("same prompt, different features",
                               size=13, color=GOOD, weight=BOLD)
        right_foot.next_to(right_box.get_bottom(), UP, buff=0.18)
        right_group = VGroup(right_box, right_head, big_zero, zero_sub,
                             zero_sub2, prompt_classes, right_foot)

        # ---- Bottom synthesis ----
        synthesis = body_text(
            "Three independent measurements support 'modes use disjoint internal features'",
            size=14, color=ACCENT_2, weight=BOLD,
        ).to_edge(DOWN, buff=0.40)
        synth_sub = body_text(
            "Mechanistic support for paper's trade-off claim. ~$3 of compute, no retraining.",
            size=12, color=MUTED,
        ).next_to(synthesis, DOWN, buff=0.10)

        # ---- Animation ----
        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_group), run_time=0.7)
        self.play(FadeIn(ctr_group), run_time=0.7)
        self.play(FadeIn(right_group), run_time=0.7)
        self.play(FadeIn(synthesis), FadeIn(synth_sub), run_time=0.5)

        self.wait(10)
        fade_out_all(self, run_time=0.5)
