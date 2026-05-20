"""Scene 14d — multi-round AR ↔ diff back-and-forth.

REDESIGN v3: simplified visualization that avoids Transform-induced
width collisions. Each row shows 8 tokens total = 4 AR (left) + 4 DIFF
(right). The two phases per round are now spatial-side rather than
time-overlap-then-replace, so wider diff tokens can never collide with
narrower AR tokens.

Original mechanism (in code) is still: AR generates a chunk, diff
re-fills last K tokens in parallel. Visualisation conveys this with
arrows or implicit ordering of fade-ins.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, LEFT, RIGHT, RoundedRectangle, Scene,
                   UP, VGroup, Line)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN,
                              body_text, fade_out_all, title_text)


def _word(text: str, color, size: int = 13):
    return body_text(text, size=size, color=color, weight=BOLD)


class MultiRoundScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Multi-round AR ↔ diff", size=26, color=ACCENT).to_edge(UP, buff=0.30)
        sub = body_text("each row = 1 round.  left half = AR(4 tokens), right half = diff(4 tokens)",
                        size=12, color=MUTED).next_to(title, DOWN, buff=0.10)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.4)

        # Story rounds. Each round has 4 AR words + 4 diff words.
        rounds = [
            (["Janet", "has", "16", "ducks."], ["a", "day,", "every", "day."]),
            (["She", "sells", "the", "eggs"], ["the", "local", "market.", "Yes."]),
            (["After", "feeding", "she", "has"], ["13", "left", "this", "week."]),
            (["At", "$2", "each", "she"], ["earns", "$26", "per", "day."]),
            (["Eating", "3", "for", "breakfast"], ["leaves", "9", "to", "sell."]),
            (["9", "x", "$2", "="], ["$18", "per", "day,", "good."]),
        ]

        row_ys = [1.85, 1.20, 0.55, -0.10, -0.75, -1.40]

        # Animate each row sequentially
        for r_idx, (ar_words, diff_words) in enumerate(rounds):
            row_y = row_ys[r_idx]

            # Round label on the far left
            lbl = body_text(f"r{r_idx + 1}", size=12, color=MUTED).move_to([-6.5, row_y, 0])
            self.play(FadeIn(lbl), run_time=0.10)

            # Build the AR group (left) and DIFF group (right) with arrange
            ar_group = VGroup(*[_word(w, ACCENT) for w in ar_words]).arrange(
                RIGHT, buff=0.18)
            ar_group.move_to([-3.0, row_y, 0])

            diff_group = VGroup(*[_word(w, DIFF) for w in diff_words]).arrange(
                RIGHT, buff=0.18)
            diff_group.move_to([2.3, row_y, 0])

            # Small "→" between the two halves
            arrow = body_text("→", size=14, color=MUTED).move_to([-0.2, row_y, 0])

            # Animate AR tokens appearing left-to-right
            for tok in ar_group:
                self.play(FadeIn(tok, shift=LEFT * 0.05), run_time=0.05)

            # Brief arrow + diff tokens in parallel
            self.play(FadeIn(arrow), run_time=0.10)
            self.play(*[FadeIn(d, shift=DOWN * 0.08) for d in diff_group], run_time=0.32)
            self.wait(0.12)

        # Caption: explain mechanism
        cap1 = body_text("AR builds left-to-right (cursor) ·  Diff fills next 4 in parallel (one forward)",
                        size=12, color=ACCENT_2)
        cap2 = body_text("6 rounds × 8 tokens = 48-token paragraph, alternating modes the whole way",
                        size=11, color=MUTED)
        cap = VGroup(cap1, cap2).arrange(DOWN, buff=0.10).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(cap), run_time=0.4)

        self.wait(5)
        fade_out_all(self, run_time=0.5)
