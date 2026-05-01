"""Scene 0 -- Paper title card.

Opens the video with the actual paper title, the three-axis tagline, the
two-fix promise, and the dataset/model names. Sets the viewer's expectation
before the cognitive metaphor starts in scene 1.
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
    ACCENT_2,
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


class IntroScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        # Paper title (matches main.tex line 37-38)
        title_top = title_text(
            "Three Orthogonal Failure Axes",
            size=42,
            color=ACCENT,
        )
        title_bot = title_text(
            "in Hybrid AR / Diffusion Reasoning",
            size=42,
            color=ACCENT,
        )
        subtitle = body_text(
            "with Trainable Fixes for Two of Them",
            size=26,
            color=ACCENT_2,
        )
        title_group = VGroup(title_top, title_bot, subtitle).arrange(
            DOWN, aligned_edge=LEFT, buff=0.20,
        )
        title_group.move_to(UP * 1.6)

        # Three-axis tagline.
        axis_pill1 = body_text("interface-format brittleness", size=18, color=DIFF)
        axis_pill2 = body_text("planner-content trust", size=18, color=ACCENT)
        axis_pill3 = body_text("sampling-diversity preservation", size=18, color=GOOD)
        sep1 = body_text("|", size=18, color=MUTED)
        sep2 = body_text("|", size=18, color=MUTED)
        axes_line = VGroup(axis_pill1, sep1, axis_pill2, sep2, axis_pill3).arrange(
            RIGHT, buff=0.30
        )
        axes_line.move_to(DOWN * 0.6)

        # Setup line: models + benchmark + total compute.
        setup_line = body_text(
            "LLaDA-8B-Instruct  +  Qwen2.5-{0.5B, 1.5B}-Instruct   on   GSM8K-test (N=200)",
            size=18,
            color=MUTED,
        )
        setup_line.move_to(DOWN * 1.6)

        compute_line = body_text(
            "Total compute: ~$3.50 on a single RTX-4090.   All adapters + datasets public on HF Hub.",
            size=16,
            color=MUTED,
        )
        compute_line.move_to(DOWN * 2.4)

        # Author + repo footer.
        footer = body_text(
            "github.com/eren23/sfumato_paper",
            size=14,
            color=ACCENT_2,
        )
        footer.to_edge(DOWN, buff=0.4)

        assert_no_overlap(
            [title_top, title_bot, subtitle,
             axes_line,
             setup_line, compute_line, footer]
        )

        self.play(FadeIn(title_top, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(title_bot, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(subtitle, shift=UP * 0.10), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(axes_line, shift=UP * 0.10), run_time=0.55)
        self.wait(0.3)
        self.play(FadeIn(setup_line), FadeIn(compute_line), run_time=0.55)
        self.wait(0.4)
        self.play(FadeIn(footer), run_time=0.4)
        self.wait(2.5)

        fade_out_all(self)
