"""Scene 24 -- unified close.

The single finale of the video. Four bullets recap the paper's
findings in the same order as the paper sections:

  (1) Three failure axes of hybrid AR/DDLM reasoning, two trainably
      fixed. (Track 1 + Track 2.)
  (2) Consensus distillation is design-sensitive, not architecture-
      limited. (Track 2 v3 c2c = 79% within CI of 80% target.)
  (3) Test-time aggregation of diffusion branches recurs as the same
      pathology across five parallel sub-problems we have probed.
  (4) Commit-LoRA is a discrete inference-time schedule toggle, defined
      on block-structured mask-diffusion samplers (LLaDA / BD3 /
      Planned Diffusion). Flat-schedule generalization is open.

Footer carries the cumulative compute tally:
  ~$3.50  Phase 1: three-axis decomposition + Track 2 distillation
  ~$9.50  Phase 2: voting-rule gap + verifier sweep
  ~$4.00  Phase 2/3: K2 sweep, mode router, S0-S4 spike chain
  ~$3.50  Phase 4: parallel aggregation negatives + cross-family audit
  ~$20.5  total

Tagline: "the substrate findings hold; the head-to-head AR claim does not."
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    LEFT,
    RIGHT,
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


def _bullet_row(text, color):
    dot = body_text("*", size=28, color=color, weight=BOLD)
    body = body_text(text, size=20, color=FG)
    return VGroup(dot, body).arrange(RIGHT, buff=0.30, aligned_edge=UP)


class Phase4ClosingScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Sfumato  --  three axes, two fixes, and the parallel pathology",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.45)

        bullet1 = _bullet_row(
            "Three failure axes characterized; brittleness and distillation trainably fixed.",
            color=GOOD,
        )
        bullet2 = _bullet_row(
            "Consensus distillation is design-sensitive, not architecture-limited.",
            color=GOOD,
        )
        bullet3 = _bullet_row(
            "Test-time aggregation: same pathology across five parallel sub-problems.",
            color=WARN,
        )
        bullet4 = _bullet_row(
            "Commit-LoRA: a discrete schedule toggle on block-structured mask diffusion.",
            color=ACCENT,
        )

        bullets = VGroup(bullet1, bullet2, bullet3, bullet4).arrange(
            DOWN, aligned_edge=LEFT, buff=0.32,
        )
        bullets.move_to(0 * RIGHT + DOWN * 0.05)

        tagline = body_text(
            "Substrate findings hold; the head-to-head AR claim does not.",
            size=21,
            color=ACCENT,
            weight=BOLD,
        )
        tagline.next_to(bullets, DOWN, buff=0.45)

        footer = body_text(
            "Total compute across four phases:  ~$20.5"
            "  ($3.50 + $9.50 + $4.00 + $3.50).\n"
            "All adapters, datasets, traces, and spike result files are public.",
            size=15,
            color=MUTED,
        )
        footer.to_edge(DOWN, buff=0.4)

        assert_no_overlap(
            [title, bullet1, bullet2, bullet3, bullet4, tagline, footer]
        )

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.55)
        self.wait(0.2)
        self.play(FadeIn(bullet1, shift=UP * 0.1), run_time=0.55)
        self.wait(0.25)
        self.play(FadeIn(bullet2, shift=UP * 0.1), run_time=0.55)
        self.wait(0.25)
        self.play(FadeIn(bullet3, shift=UP * 0.1), run_time=0.55)
        self.wait(0.25)
        self.play(FadeIn(bullet4, shift=UP * 0.1), run_time=0.55)
        self.wait(0.45)
        self.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.55)
        self.wait(0.45)
        self.play(FadeIn(footer, shift=UP * 0.1), run_time=0.5)
        self.wait(4.5)

        fade_out_all(self)
