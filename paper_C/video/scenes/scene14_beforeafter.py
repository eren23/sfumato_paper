"""Scene 14 — before/after sample text on the same F9 prompt."""
from __future__ import annotations

from manim import (Text, BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _sample_panel(label, text, color, w=6.3, h=4.5):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2,
                           color=color, stroke_width=2, fill_opacity=0.08)
    head = body_text(label, size=18, color=color, weight=BOLD)
    body = Text(text, font="Courier", font_size=12, color=FG)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(box.get_center())
    return VGroup(box, inner)


class BeforeAfterScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Same prompt, same ckpt, decoder only", size=28, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("F9, GSM8K-dev Q0 (Janet's ducks),  paired_64_64 mode", size=14, color=MUTED).next_to(title, DOWN, buff=0.15)

        before = _sample_panel(
            "greedy (Tier 0):",
            ('"A duck\'s bill is 1,000 pounds.\n'
             ' eggs eggs eggs eggs eggs eggs\n'
             ' eggs eggs eggs eggs eggs eggs\n'
             ' eggs eggs eggs eggs eggs eggs\n'
             ' eggs eggs eggs eggs eggs eggs\n'
             ' eggs eggs eggs eggs eggs eggs\n'
             ' eggs eggs eggs eggs..."'),
            WARN,
        ).move_to(LEFT * 3.6 + DOWN * 0.3)

        after = _sample_panel(
            "Tier 0.5 + count rep_pen:",
            ('"Given that she needs to feed a\n'
             ' large number of chickens she\n'
             ' will need to know how to\n'
             ' produce eggs. If she doesn\'t\n'
             ' have access to food, she will\n'
             ' be unable to eat the eggs.\n'
             ' Egg-laying is an excellent way\n'
             ' to raise chickens. There are\n'
             ' many ways to raise an egg..."'),
            GOOD,
        ).move_to(RIGHT * 3.6 + DOWN * 0.3)

        foot = body_text("No retrain. No new data. One sampler patch.",
                         size=22, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(before), run_time=0.7)
        self.wait(0.3)
        self.play(FadeIn(after), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.5)
        self.wait(30)
        fade_out_all(self, run_time=0.5)
