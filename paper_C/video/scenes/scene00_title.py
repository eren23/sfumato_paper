"""Scene 0 -- Paper-C title card.

Opens with the paper title, the trade-off tagline, the sample-quality
sub-tag, and the dataset / scale range.

Reuses theme_shim from ../../../video/utils/theme_shim.py. To make
that import work when running from paper_C/video/scenes/, the
render_story.sh wrapper (TO BE WRITTEN) needs to prepend
../../video/utils to PYTHONPATH OR we symlink it locally.
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    Scene,
    UP,
    VGroup,
)

# These imports will resolve once render_story.sh sets PYTHONPATH to
# include the paper-1 video utils. For local manim render testing,
# either:
#   PYTHONPATH=../../video manim -pql scene00_title.py
# or symlink utils:
#   ln -s ../../video/utils utils
from utils.theme_shim import (
    BG,
    FG,
    MUTED,
    ACCENT,
    body_text,
    fade_out_all,
    title_text,
)


class TitleScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Mode Specialisation in Composite",
            color=FG,
            weight=BOLD,
        ).scale(0.95).to_edge(UP, buff=1.0)

        title2 = title_text(
            "AR + Discrete-Diffusion LMs",
            color=FG,
            weight=BOLD,
        ).scale(0.95).next_to(title, DOWN, buff=0.2)

        tagline = body_text(
            "Two heads on one backbone learn near-disjoint feature bases.",
            color=ACCENT,
        ).scale(0.7).next_to(title2, DOWN, buff=0.8)

        sub = body_text(
            "A mechanistic account of the toy-scale trade-off",
            color=MUTED,
        ).scale(0.55).next_to(tagline, DOWN, buff=0.8)

        sub2 = body_text(
            "+ a per-token cross-mode inference recipe (Phase K).",
            color=MUTED,
        ).scale(0.55).next_to(sub, DOWN, buff=0.1)

        meta = body_text(
            "Sfumato Paper C  ·  Draft  ·  May 2026",
            color=MUTED,
        ).scale(0.45).to_edge(DOWN, buff=0.8)

        all_text = VGroup(title, title2, tagline, sub, sub2, meta)
        self.play(FadeIn(all_text), run_time=1.2)
        self.wait(7)
        fade_out_all(self, run_time=0.5)
