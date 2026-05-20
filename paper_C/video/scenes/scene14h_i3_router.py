"""Scene 14h — I.3 learned router via REINFORCE on frozen F10.

Tiny router (500K params) learns to chunk-route between AR and diff
to minimize loop_rate + maximize task-correct reward. Backbone frozen.

Shows: loop_rate over training steps drops 0.69 → 0.00 (router learns
coherence). acc stays at 0% (routing alone doesn't lift task capability).

Two panels:
  Left   Curve: loop_rate descent over 100 steps
  Right  Schematic: composite + frozen heads + trainable router head
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, Line, Polygon, RoundedRectangle,
                   Scene, RIGHT, UP, VGroup, Rectangle, Arrow)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED,
                              WARN, body_text, fade_out_all, title_text)


def _panel_box(w, h, color):
    return RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                            stroke_width=2, fill_opacity=0.06)


class I3RouterScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("I.3  —  learned router via REINFORCE on frozen F10",
                           size=24, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("router: 500K params, 4 actions {ar_chunk, diff_short, diff_long, end}, backbone frozen",
                        size=13, color=MUTED).next_to(title, DOWN, buff=0.12)

        # ---- LEFT PANEL: loop_rate curve ----
        left_box = _panel_box(6.5, 4.6, GOOD).move_to(LEFT * 3.3 + DOWN * 0.2)
        left_head = body_text("loop_rate vs REINFORCE step",
                              size=14, color=GOOD, weight=BOLD)
        left_head.next_to(left_box.get_top(), DOWN, buff=0.18)

        # Axes
        axis_origin = left_box.get_center() + DOWN * 0.6 + LEFT * 2.4
        x_axis = Line(axis_origin, axis_origin + RIGHT * 4.6, stroke_width=2, color=FG)
        y_axis = Line(axis_origin, axis_origin + UP * 2.6, stroke_width=2, color=FG)

        # Curve: step 0..99, loop_rate 0.69 → 0.00 with some bumps
        def pt(step_frac, lr):
            # step 0..1 → x 0..4.6; lr 0..1 → y 0..2.6
            x = axis_origin[0] + step_frac * 4.6
            y = axis_origin[1] + lr * 2.6
            return [x, y, 0]

        # Approximate the observed curve from training log:
        # step 0=0.69, 10=0.12, 20=0.06, 30=0.06, 40=0.12, 50=0.00, 60=0.19,
        # 70=0.00, 80=0.00, 90=0.00, 99=0.00
        loops = [(0, .69), (.1, .12), (.2, .06), (.3, .06), (.4, .12),
                 (.5, .00), (.6, .19), (.7, .00), (.8, .00), (.9, .00), (1.0, .00)]
        curve_pts = [pt(s, lr) for s, lr in loops]
        # Build polyline as one strip then back so Polygon closes
        curve = Polygon(*curve_pts, stroke_width=3, color=GOOD, fill_opacity=0)

        # Annotations
        start_dot = Rectangle(width=0.12, height=0.12, color=WARN,
                              fill_opacity=1).move_to(curve_pts[0])
        start_lbl = body_text("0.69", size=12, color=WARN, weight=BOLD)
        start_lbl.next_to(start_dot, UP, buff=0.10)

        end_dot = Rectangle(width=0.12, height=0.12, color=GOOD,
                            fill_opacity=1).move_to(curve_pts[-1])
        end_lbl = body_text("0.00", size=12, color=GOOD, weight=BOLD)
        end_lbl.next_to(end_dot, UP, buff=0.10).shift(LEFT * 0.1)

        x_lbl = body_text("REINFORCE step (0 → 99)", size=10, color=MUTED)
        x_lbl.next_to(x_axis, DOWN, buff=0.20)
        y_lbl = body_text("loop_rate", size=10, color=MUTED)
        y_lbl.rotate(3.14159 / 2).next_to(y_axis, LEFT, buff=0.15)

        curve_grp = VGroup(x_axis, y_axis, curve, start_dot, start_lbl,
                           end_dot, end_lbl, x_lbl, y_lbl)
        left_foot = body_text("router learns coherence", size=14, color=GOOD, weight=BOLD)
        left_foot.next_to(left_box.get_bottom(), UP, buff=0.18)
        left_group = VGroup(left_box, left_head, curve_grp, left_foot)

        # ---- RIGHT PANEL: architecture schematic ----
        right_box = _panel_box(5.4, 4.6, DIFF).move_to(RIGHT * 4.0 + DOWN * 0.2)
        right_head = body_text("architecture", size=14, color=DIFF, weight=BOLD)
        right_head.next_to(right_box.get_top(), DOWN, buff=0.18)

        # Backbone block
        bb = Rectangle(width=2.6, height=0.8, color=MUTED, stroke_width=2,
                       fill_opacity=0.12).set_fill(MUTED, opacity=0.12)
        bb_lbl = body_text("F10 backbone (frozen)", size=12, color=MUTED, weight=BOLD)
        bb_lbl.move_to(bb.get_center())
        bb_grp = VGroup(bb, bb_lbl).move_to(right_box.get_center() + UP * 0.7)

        # Heads row
        head_ar = Rectangle(width=1.2, height=0.6, color=ACCENT, stroke_width=2,
                            fill_opacity=0.12).set_fill(ACCENT, opacity=0.12)
        head_ar_lbl = body_text("AR head\n(frozen)", size=10, color=ACCENT)
        head_ar_lbl.move_to(head_ar.get_center())
        head_ar_grp = VGroup(head_ar, head_ar_lbl)

        head_diff = Rectangle(width=1.2, height=0.6, color=DIFF, stroke_width=2,
                              fill_opacity=0.12).set_fill(DIFF, opacity=0.12)
        head_diff_lbl = body_text("Diff head\n(frozen)", size=10, color=DIFF)
        head_diff_lbl.move_to(head_diff.get_center())
        head_diff_grp = VGroup(head_diff, head_diff_lbl)

        router_h = Rectangle(width=1.2, height=0.6, color=GOOD, stroke_width=3,
                             fill_opacity=0.2).set_fill(GOOD, opacity=0.2)
        router_lbl = body_text("Router\n(TRAIN)", size=10, color=GOOD, weight=BOLD)
        router_lbl.move_to(router_h.get_center())
        router_grp = VGroup(router_h, router_lbl)

        heads_row = VGroup(head_ar_grp, head_diff_grp, router_grp).arrange(
            RIGHT, buff=0.25).move_to(right_box.get_center() + DOWN * 0.4)

        # Arrows from backbone to each head
        arrows = []
        for h_grp in (head_ar_grp, head_diff_grp, router_grp):
            arr = Arrow(bb.get_bottom(), h_grp[0].get_top(), buff=0.05,
                        stroke_width=2, color=MUTED, tip_length=0.15)
            arrows.append(arr)
        arrows_grp = VGroup(*arrows)

        # Bottom: action space
        actions_lbl = body_text("actions: ar_chunk · diff_short · diff_long · end",
                                size=10, color=GOOD)
        actions_lbl.next_to(right_box.get_bottom(), UP, buff=0.30)

        right_foot = body_text("0% acc lift  — routing ≠ capability",
                               size=12, color=WARN, weight=BOLD)
        right_foot.next_to(right_box.get_bottom(), UP, buff=0.10)

        right_group = VGroup(right_box, right_head, bb_grp, heads_row,
                             arrows_grp, actions_lbl, right_foot)

        # ---- Bottom synthesis ----
        synthesis = body_text(
            "router solves the loop problem  ·  not the math problem  (capability bounded by frozen backbone)",
            size=13, color=ACCENT_2, weight=BOLD,
        ).to_edge(DOWN, buff=0.40)

        # ---- Animation ----
        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(left_group), run_time=0.7)
        self.play(FadeIn(right_group), run_time=0.7)
        self.play(FadeIn(synthesis), run_time=0.5)

        self.wait(12)
        fade_out_all(self, run_time=0.5)
