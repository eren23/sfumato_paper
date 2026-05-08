"""Scene 23 -- Direction A: mini-pilot LOSS to mid-pilot GAIN, the directional reversal.

Two-row paired-table comparison of the Phase-4 Direction A spike before
and after wiring the KL anchor:

  Mini-pilot (commit fbc67b1):
    50-step GRPO, no KL anchor
    MATH-500 N=20 paired
    trained 0.350  vs  baseline 0.400  ->  -1 problem (within CI)

  Mid-pilot (commit 996f3a1):
    200-step GRPO + Schulman-k3 KL anchor (beta = 0.05)
    MATH-500 N=50 paired
    trained 0.560  vs  baseline 0.540  ->  +1 problem (within CI)
    49/50 predictions bit-identical; the one flip is wrong -> correct.

Both signals are inside binomial CI +/- 14 pp at N=50; the meaningful
evidence is the directional reversal, which says schedule-conditional
adapter retraining is at minimum non-destructive when KL-anchored.
A locked PRE_REG full pilot (3100 steps over 1550 prompts) is the
gating experiment.

Headline: "directional reversal is the signal, not the magnitude."
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
    FG,
    GOOD,
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)
from utils.layout import assert_no_overlap


def _pilot_card(headline, lines, color, w=5.6, h=3.6):
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.18,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.10,
        stroke_width=2.2,
    )
    head = body_text(headline, size=20, color=color, weight=BOLD)
    body_lines = VGroup(
        *[body_text(line, size=15, color=FG) for line in lines]
    ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    inner = VGroup(head, body_lines).arrange(DOWN, buff=0.28)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class DirectionAReversalScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Direction A: mini-pilot -> mid-pilot, the directional reversal",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "schedule-RLHF on commit-LoRA; both signals within CI on MATH-500",
            size=16,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        mini = _pilot_card(
            "Mini-pilot (fbc67b1)",
            [
                "50-step GRPO, no KL anchor",
                "MATH-500 N=20 paired",
                "trained:    0.350",
                "baseline:   0.400",
                "delta:    -1 problem  (within CI)",
                "plumbing PASS, no signal",
            ],
            color=WARN,
        )
        mid = _pilot_card(
            "Mid-pilot (996f3a1)",
            [
                "200-step GRPO + KL anchor (beta=0.05)",
                "MATH-500 N=50 paired",
                "trained:    0.560",
                "baseline:   0.540",
                "delta:    +1 problem  (within CI)",
                "49/50 identical; flip is wrong -> correct",
            ],
            color=GOOD,
        )

        cards = VGroup(mini, mid).arrange(RIGHT, buff=0.40)
        cards.move_to(0 * RIGHT + DOWN * 0.05)

        callout = body_text(
            "Reversal is the signal, not the magnitude:"
            " KL-anchored schedule-RLHF is at minimum non-destructive."
            "\nLocked PRE_REG full pilot (3100 steps) is the gating experiment.",
            size=17,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)

        assert_no_overlap([title, sub, mini, mid, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(mini, shift=UP * 0.15), run_time=0.55)
        self.wait(0.5)
        self.play(FadeIn(mid, shift=UP * 0.15), run_time=0.55)
        self.wait(0.6)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.55)
        self.wait(3.5)

        fade_out_all(self)
