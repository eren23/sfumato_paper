"""Scene 22 -- three more parallel sub-problems, same pathology.

Three side-by-side cards probing further parallel sub-problems of
test-time aggregation in diffusion LMs. Each lands as an honest
negative or within-CI signal, with the same diagnosis as the
verifier sweep (scenes 13-15) and the per-problem mode router
(scene 19):

  (a) Temporal-SC voting:    -4 pp  (GSM8K dev_200 N=100)
      schedule-weighted vote regressed under strict pattern matching.
      Diagnostic: answer span lands at sub-block 3/4 in 94% of branches.

  (b) Schedule-RLHF mini:    -1 problem (MATH-500 N=20, within CI)
      50-step GRPO, no KL anchor. Plumbing PASS, no signal.

  (c) Base-model swap:       -2 pp  (MATH-500 N=50, LLaDA-1.5)
      Adapter compat OK; capability transfer failed.

Headline: "the same pathology recurs across every aggregation
sub-problem we have probed."
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
    MUTED,
    WARN,
    body_text,
    fade_out_all,
    title_text,
)
from utils.layout import assert_no_overlap


def _finding_card(headline, comparison_lines, color, w=4.05, h=3.6):
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.18,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.10,
        stroke_width=2.2,
    )
    head = body_text(headline, size=18, color=color, weight=BOLD)
    body_lines = VGroup(
        *[body_text(line, size=15, color=FG) for line in comparison_lines]
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    inner = VGroup(head, body_lines).arrange(DOWN, buff=0.30)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class Phase4NegativesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Same pathology, three more sub-problems",
            size=26,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        sub = body_text(
            "temporal-SC voting, schedule-RLHF on commit-LoRA, base-model swap"
            " --- each lands negative or within CI",
            size=16,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.16)

        c1 = _finding_card(
            "Temporal-SC voting",
            [
                "schedule-weighted vote",
                "GSM8K dev_200 N=100",
                "cmajc-vote: 0.82",
                "Temporal-SC:  0.78",
                "  -4 pp under strict match",
                "answer span at block 3/4",
            ],
            color=WARN,
        )
        c2 = _finding_card(
            "Schedule-RLHF mini",
            [
                "50-step GRPO, no KL anchor",
                "MATH-500 N=20 paired",
                "trained:   0.350",
                "baseline:  0.400",
                "  -1 problem (within CI)",
                "plumbing PASS",
            ],
            color=WARN,
        )
        c3 = _finding_card(
            "Base-model swap",
            [
                "frozen v3 LoRAs",
                "MATH-500 N=50 cmajc-k3",
                "LLaDA-1.5:    0.56",
                "LLaDA-8B ref: 0.58",
                "  -2 pp",
                "capability transfer failed",
            ],
            color=WARN,
        )

        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.40)
        cards.move_to(0 * RIGHT + DOWN * 0.1)

        callout = body_text(
            "Same path forward as scenes 13 + 19: bigger encoders,"
            " process-reward signals, more data."
            "\nTest-time aggregation is not a single-classifier problem"
            " at the data scale we can afford.",
            size=17,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.4)

        assert_no_overlap([title, sub, c1, c2, c3, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.55)
        self.wait(0.35)
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.55)
        self.wait(0.35)
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.55)
        self.wait(0.6)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)

        fade_out_all(self)
