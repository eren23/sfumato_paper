"""Scene 13 -- 17 peer-class verifiers all LOSS, frontier judge wins.

Vertical leaderboard. WIN-MINOR row at top (Claude Sonnet 4.5 + CoT, +6.16
pp), 11 representative LOSS rows below spanning 0.5B--72B encoders, embedding
models, math-tuned chat, process-MLP, symbolic.  Numbers from voting_gap.tex
Table 2 (top of leaderboard).

Headline: "every peer-class architecture loses; only the frontier judge wins."
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    LEFT,
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


# (label, delta_pp_str, color, decision)
ROWS = [
    ("Claude Sonnet 4.5 + CoT",        "+6.16", GOOD,  "WIN-MINOR"),
    ("Claude Sonnet 4.5 (YES/NO)",     "+3.79", MUTED, "inconclusive"),
    ("DeepSeek-R1-Distill-Qwen-32B",   "-3.00", WARN,  "LOSS"),
    ("Qwen2.5-32B-Instruct (4-bit)",   "-3.50", WARN,  "LOSS"),
    ("Qwen2.5-7B-Instruct + MLP",      "-4.00", WARN,  "LOSS"),
    ("Process-MLP (rich substrate)",   "-4.00", WARN,  "LOSS"),
    ("Qwen3-8B chat + MLP",            "-5.50", WARN,  "LOSS"),
    ("Qwen2.5-Math-7B + MLP",          "-6.50", WARN,  "LOSS"),
    ("Qwen3-Embedding-8B + MLP",       "-8.00", WARN,  "LOSS"),
    ("Qwen2.5-0.5B + MLP",             "-8.50", WARN,  "LOSS"),
    ("Symbolic arithmetic",            "-8.98", WARN,  "LOSS"),
    ("TF-IDF + LR",                    "-14.0", WARN,  "LOSS"),
]


def _row(label, delta, color, decision, w=10.4, h=0.42):
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.10,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.10,
        stroke_width=1.4,
    )
    name = body_text(label, size=15, color=FG)
    val = body_text(delta, size=15, color=color, weight=BOLD)
    dec = body_text(decision, size=14, color=color)
    name.move_to(box.get_left() + RIGHT * 2.6)
    val.move_to(box.get_center() + RIGHT * 1.6)
    dec.move_to(box.get_right() + LEFT * 1.0)
    return VGroup(box, name, val, dec)


class VerifierFailScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "17 peer-class verifiers tested. All lose to majority vote.",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.35)

        sub = body_text(
            "Delta_pp vs cmaj baseline; only Claude Sonnet 4.5 + CoT closes the gap",
            size=15,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.15)

        rows = [_row(*r) for r in ROWS]
        stack = VGroup(*rows).arrange(DOWN, buff=0.10)
        stack.next_to(sub, DOWN, buff=0.30)

        callout = body_text(
            "Math-tuning HURTS. Embedding-specific worst. Doubling substrate worse.",
            size=17,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)

        assert_no_overlap([title, sub, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)

        # Reveal WIN-MINOR row first, then cascade the LOSSes.
        self.play(FadeIn(rows[0], shift=UP * 0.1), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(rows[1], shift=UP * 0.05), run_time=0.3)
        self.wait(0.2)
        for r in rows[2:]:
            self.play(FadeIn(r, shift=UP * 0.04), run_time=0.18)
        self.wait(0.6)

        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
