"""Scene 14d — multi-round AR ↔ diff back-and-forth.

REDESIGN: 6 short rows (one per round) so tokens never run off-screen
and the AR-vs-diff colour split stays visually legible. Each row shows:
  [round k]  AR(8 tokens, ACCENT)  →  DIFF(4 tokens, DIFF)
Labels on the left make the rhythm explicit.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, FadeOut, Indicate, LEFT, RIGHT, Scene,
                   Transform, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN,
                              body_text, fade_out_all, title_text)


def _word(text: str, color, size: int = 11):
    return body_text(text, size=size, color=color, weight=BOLD)


class MultiRoundScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Multi-round AR ↔ diff", size=26, color=ACCENT).to_edge(UP, buff=0.30)
        sub = body_text("AR(8) → diff(4)  ×  6 rounds  (one row per round)",
                        size=13, color=MUTED).next_to(title, DOWN, buff=0.10)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.4)

        # The story rounds. Each round = 8 AR tokens + 4 diff-resolved tokens.
        # The diff_words REPLACE the last 4 AR tokens (which become "___" briefly).
        rounds = [
            (["Janet", "has", "16", "ducks.", "She", "feeds", "them", "twice"],
             ["a", "day,", "every", "day."]),
            (["She", "sells", "the", "eggs", "for", "$2", "each", "at"],
             ["the", "local", "farmer's", "market."]),
            (["After", "feeding", "her", "ducks", "she", "has", "13", "eggs"],
             ["left", "for", "the", "week."]),
            (["At", "$2", "each", "she", "earns", "13", "x", "$2"],
             ["=", "$26", "per", "day."]),
            (["Eating", "3", "for", "breakfast", "and", "baking", "4", "more"],
             ["leaves", "9", "to", "sell."]),
            (["9", "x", "$2", "=", "$18", "per", "day,", "or"],
             ["$126", "per", "week.", "Answer."]),
        ]

        # 6 rows stacked vertically. y from 2.0 down to -2.0 in steps of -0.65.
        row_ys = [1.85, 1.20, 0.55, -0.10, -0.75, -1.40]
        diff_perm = [2, 0, 3, 1]

        # Label all 6 rounds at the very left so the structure is obvious
        # even at a glance, then fill them progressively.
        all_round_labels = [
            body_text(f"r{r_idx + 1}", size=11, color=MUTED)
              .move_to([-6.5, row_ys[r_idx], 0])
            for r_idx in range(6)
        ]
        self.play(*[FadeIn(lbl) for lbl in all_round_labels], run_time=0.4)

        for r_idx, (ar_words, diff_words) in enumerate(rounds):
            row_y = row_ys[r_idx]
            # token row starts at x=-5.6 (just right of the round label)
            row_origin_x = -5.6
            word_buff = 0.10  # space between token bounding boxes
            row_right = row_origin_x

            ar_mobs = []

            def place(mob, x_right_now):
                w = mob.width
                mob.move_to([x_right_now + w / 2, row_y, 0])
                return x_right_now + w + word_buff

            # ---- AR step: append 8 tokens left-to-right
            for w in ar_words:
                m = _word(w, ACCENT)
                row_right = place(m, row_right)
                ar_mobs.append(m)
                self.play(FadeIn(m, shift=LEFT * 0.05), run_time=0.04)

            # ---- Diff step: re-mask the last 4 tokens, resolve in permuted order
            mask_targets = ar_mobs[-4:]
            mask_positions = [m.get_center() for m in mask_targets]
            mask_mobs = []
            for m in mask_targets:
                m_new = _word("___", DIFF).move_to(m.get_center())
                mask_mobs.append(m_new)
            self.play(*[Transform(m_old, m_new) for m_old, m_new in zip(mask_targets, mask_mobs)],
                      run_time=0.25)
            for slot in diff_perm:
                resolved = _word(diff_words[slot], DIFF).move_to(mask_positions[slot])
                self.play(Transform(mask_targets[slot], resolved), run_time=0.12)
                self.play(Indicate(mask_targets[slot], color=WARN, scale_factor=1.2), run_time=0.12)
            self.wait(0.18)

        # Sum-up caption at bottom
        cap1 = body_text("6 rounds = 72 tokens  ·  AR builds left-to-right  ·  Diff re-masks last 4 each round",
                        size=12, color=ACCENT_2)
        cap2 = body_text("the user's original mental model of Sfumato — running on F10 via probe_interleaved.py",
                        size=11, color=MUTED)
        cap = VGroup(cap1, cap2).arrange(DOWN, buff=0.10).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(cap), run_time=0.4)

        self.wait(5)
        fade_out_all(self, run_time=0.5)
