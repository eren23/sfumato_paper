"""Scene 10 — three independent root causes."""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _cause(idx, name, detail, color, w=3.9, h=3.2):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.2, color=color,
                           stroke_width=2, fill_opacity=0.1)
    head = body_text(f"#{idx}", size=18, color=color, weight=BOLD)
    nm = body_text(name, size=18, color=color, weight=BOLD)
    body = VGroup(*[body_text(line, size=13, color=FG) for line in detail]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    inner = VGroup(head, nm, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(box.get_center())
    return VGroup(box, inner)


class CausesScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG
        title = title_text("Three independent root causes", size=32, color=ACCENT).to_edge(UP, buff=0.4)
        sub = body_text("from three parallel Explore-agent investigations",
                        size=16, color=MUTED).next_to(title, DOWN, buff=0.15)

        c1 = _cause(1, "decoder unwired",
                    ["gen_ar() had anti-rep flags",
                     "but all 4 probe5 call sites",
                     "passed defaults (= greedy).",
                     "train.py had its own inline",
                     "torch.argmax, didn't use",
                     "gen_ar() at all."],
                    ACCENT).move_to(LEFT * 4.5 + DOWN * 0.4)
        c2 = _cause(2, "format OOD",
                    ["F9 trained on raw",
                     "FineWeb-Edu only.",
                     "0 examples of",
                     '"Question:...Answer:"',
                     "structure.",
                     "eval prompt is OOD."],
                    DIFF).move_to(0 * RIGHT + DOWN * 0.4)
        c3 = _cause(3, "Chinchilla 49 %",
                    ["305M × 20 tok/p = 6.1B",
                     "F9 saw  3B (~49 %).",
                     "Holtzman 2020 / Li 2023:",
                     "undertrained models",
                     "loop harder via self-",
                     "conditioning collapse."],
                    WARN).move_to(RIGHT * 4.5 + DOWN * 0.4)

        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)
        self.play(FadeIn(c1), run_time=0.6)
        self.play(FadeIn(c2), run_time=0.6)
        self.play(FadeIn(c3), run_time=0.6)
        self.wait(30)
        fade_out_all(self, run_time=0.5)
