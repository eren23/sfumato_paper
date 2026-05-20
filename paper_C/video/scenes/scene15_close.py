"""Scene 15 — what we delivered + close.

Replaces older "F10 in flight" framing now that F10 and F11 both shipped.
Left panel: the measured deliverables (post-F11 hardening).
Right panel: the claims that survived the pressure test.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, FG, GOOD, MUTED, body_text, fade_out_all, title_text)


def _panel(title_str, lines, color, w=6.4, h=5.0):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                           stroke_width=2, fill_opacity=0.08)
    head = body_text(title_str, size=20, color=color, weight=BOLD)
    body_items = [body_text(line, size=13, color=FG) for line in lines]
    body = VGroup(*body_items).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(box.get_center())
    return VGroup(box, inner)


class CloseScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Sfumato — what we delivered", size=28, color=ACCENT).to_edge(UP, buff=0.4)

        left = _panel(
            "trained + measured",
            ["F10: 305M composite, 3B mixed tokens",
             "F11: α=0.30 fine-tune (+30k steps)",
             "Phase J: 5.4× speed, FIM, revision",
             "Phase K: K.2 pct50 = 11.40 NLL",
             "    (−0.58 vs F10 base of 11.98)"],
            ACCENT,
        ).move_to(LEFT * 3.6 + DOWN * 0.2)

        right = _panel(
            "what we claim",
            ["1. small AR tax, big diff gain",
             "2. data-efficiency crossover ~1k",
             "3. per-token cross-mode routing",
             "    (diff drafts + AR refills the worst)",
             "4. α=0.30 sharpens the routing signal"],
            GOOD,
        ).move_to(RIGHT * 3.6 + DOWN * 0.2)

        foot = body_text("paper_C/main.pdf   ·   github.com/eren23/sfumato   ·   huggingface.co/eren23/sfumato-composite-ckpts",
                         size=12, color=MUTED).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(left), run_time=0.7)
        self.play(FadeIn(right), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.4)
        self.wait(25)
        fade_out_all(self, run_time=0.5)
