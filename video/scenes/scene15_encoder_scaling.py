"""Scene 15 -- encoder scaling is monotone but insufficient.

Three bars left-to-right showing Delta_pp vs cmaj at three encoder scales.
Numbers from voting_gap.tex Table 3 (5-fold CV by problem_id, N=1750):
  TF-IDF + LR (250K params):    -14.0 pp
  Qwen2.5-0.5B + MLP (500M):     -8.5 pp
  Qwen2.5-7B + MLP (7.6B):       -4.0 pp

Each ~10x scale-up narrows the gap by ~5 pp. Linear extrapolation suggests
Qwen-32B might cross the cmaj baseline; we label the trend, not the
extrapolation.

Headline: "encoder scaling narrows the gap monotonically, but does not
close it at our scale."
"""
from __future__ import annotations

from manim import (
    BOLD,
    DashedLine,
    DOWN,
    FadeIn,
    GrowFromEdge,
    LEFT,
    Line,
    RIGHT,
    RoundedRectangle,
    Scene,
    UP,
    VGroup,
)

from utils.theme_shim import (
    ACCENT,
    BG,
    DIFF,
    FG,
    GOOD,
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)
from utils.layout import assert_no_overlap


# (label, params_str, delta_pp_value, delta_pp_str, color)
ROWS = [
    ("TF-IDF + LR",        "~250K", -14.0, "-14.0 pp", WARN),
    ("Qwen2.5-0.5B + MLP", "500M",   -8.5, " -8.5 pp", DIFF),
    ("Qwen2.5-7B + MLP",   "7.6B",   -4.0, " -4.0 pp", GOOD),
]


def _bar(height_abs, color, width):
    return RoundedRectangle(
        width=width,
        height=max(0.05, height_abs),
        corner_radius=0.06,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.45,
        stroke_width=2,
    )


class EncoderScalingScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Encoder scaling narrows the gap monotonically",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "5-fold CV by problem_id on 1750 cmaj branches; chat-LM mean-pool + MLP head",
            size=16,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        # Bars hang downward from a zero line (Delta_pp is negative).
        chart_left, chart_right = -5.0, 5.0
        zero_y = 1.6   # the "0 pp" line sits high; bars drop below.
        unit = 0.12    # per pp of |delta|.
        plot_bottom = zero_y - 16 * unit

        zero_line = Line(
            LEFT * 5.4 + UP * zero_y,
            RIGHT * 5.4 + UP * zero_y,
            color=GOOD,
            stroke_width=2,
        )
        zero_lbl = body_text("0 pp (cmaj baseline)", size=14, color=GOOD)
        zero_lbl.next_to(zero_line.get_right(), UP, buff=0.05)

        usable_left, usable_right = chart_left + 0.6, chart_right - 0.6
        n = len(ROWS)
        slot_w = (usable_right - usable_left) / n
        bar_w = 1.2

        bar_groups = []
        labels = []
        for i, (label, params, delta_val, delta_str, color) in enumerate(ROWS):
            x_pos = usable_left + slot_w * (i + 0.5)
            h_abs = abs(delta_val) * unit
            bar = _bar(h_abs, color, width=bar_w)
            bar.move_to(RIGHT * x_pos + UP * (zero_y - h_abs / 2))

            val = body_text(delta_str, size=18, color=color, weight=BOLD)
            val.next_to(bar, DOWN, buff=0.12)

            cond_lbl = body_text(label, size=14, color=FG)
            cond_lbl.move_to(RIGHT * x_pos + UP * (plot_bottom - 0.45))
            params_lbl = body_text(params, size=13, color=MUTED)
            params_lbl.move_to(RIGHT * x_pos + UP * (plot_bottom - 0.78))

            bar_groups.append(VGroup(bar, val))
            labels.extend([cond_lbl, params_lbl])

        # Dashed extrapolation arrow gesturing toward the baseline.
        extrap = DashedLine(
            start=RIGHT * (usable_right - 0.4) + UP * (zero_y - abs(-4.0) * unit),
            end=RIGHT * (usable_right + 1.2) + UP * (zero_y - 0.05),
            color=MUTED,
            stroke_width=2,
            dash_length=0.18,
        )
        extrap_lbl = body_text(
            "?  32B+",
            size=14,
            color=MUTED,
        )
        extrap_lbl.next_to(extrap.get_end(), UP, buff=0.05)

        callout = body_text(
            "~5 pp gap closure per ~10x scale; the trend is the publishable observation.",
            size=18,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.45)

        assert_no_overlap([title, sub, zero_lbl, callout] + labels)

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(zero_line), FadeIn(zero_lbl),
                  *[FadeIn(l) for l in labels], run_time=0.5)
        for g in bar_groups:
            self.play(GrowFromEdge(g[0], UP), FadeIn(g[1]), run_time=0.55)
            self.wait(0.2)
        self.play(FadeIn(extrap), FadeIn(extrap_lbl), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
