"""Scene 14d — multi-round AR ↔ diff back-and-forth.

The user's original mental model of Sfumato: "AR started, DIF takes
on, generates some stuff, some tokens are found a nice candidate to
continue ar, in some tokens we continued ar at the same time, same
sentence, then again a diff maybe, then finalizing, going back and
forth like human beings."

Scene 14b showed ONE round (AR then diff). This scene shows the
MULTI-ROUND mechanism we actually tested in probe_interleaved.py's
`interleaved_8_4_x6` schedule: AR(8) → diff(4) repeated 6 times.

Each round:
  - AR-extend: cursor advances right, 8 new tokens appear left-to-right
  - diff-refine: last 4 tokens get re-masked (briefly highlighted),
    then resolved in non-sequential order
The line grows continuously; ~72 tokens by the end.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, FadeOut, Indicate, LEFT, RIGHT,
                   Scene, Transform, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _word(text: str, color, size: int = 14):
    return body_text(text, size=size, color=color, weight=BOLD)


class MultiRoundScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Multi-round AR ↔ diff", size=28, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("interleaved_8_4_x6:  AR(8) → diff(4) × 6 rounds, same line, growing",
                        size=14, color=MUTED).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.4)

        # Round counter at top-right
        round_lbl = body_text("round 0 / 6", size=14, color=ACCENT_2).to_edge(RIGHT, buff=0.8).shift(UP * 2.6)
        self.add(round_lbl)

        # Anchor: start of the row, well left of center
        row_y = 0.5
        row_origin_x = -6.0

        # Token sequence we'll build up. Six rounds of AR(8)+diff(4) = 72 tokens.
        # For visual flow we wrap onto two rows of ~36 tokens each.
        rounds = [
            # Each tuple: (ar_words, diff_words). diff_words is a 4-tuple that
            # replaces the LAST 4 AR words after the AR step.
            (["Janet", "has", "16", "ducks.", "She", "feeds", "them", "twice"],
             ["a", "day,", "every", "day."]),
            (["She", "sells", "the", "eggs", "for", "$2", "each", "at"],
             ["the", "local", "farmer's", "market."]),
            (["After", "feeding", "her", "ducks", "she", "has", "13", "eggs"],
             ["left", "for", "the", "market."]),
            # Three more rounds (rendered on second visual row)
            (["At", "$2", "each", "she", "makes", "13", "x", "$2"],
             ["=", "$26", "per", "day."]),
            (["Eating", "3", "for", "breakfast", "and", "baking", "4", "more"],
             ["leaves", "9", "to", "sell."]),
            (["9", "x", "$2", "=", "$18", "per", "day,", "or"],
             ["$126", "per", "week.", "Answer:"]),
        ]

        # We arrange the tokens in two visual rows of ~36 tokens (3 rounds each).
        all_word_mobs: list = []
        row_a_words: list = []
        row_b_words: list = []

        # Render rounds 1-3 on top row, rounds 4-6 on bottom row.
        row_a_y = 1.0
        row_b_y = -1.0
        x_step = 0.55  # horizontal spacing between words

        # Helper: place the next word at the next x position on a row
        def place_word(token_mob, row: str, idx: int):
            y = row_a_y if row == "A" else row_b_y
            x = row_origin_x + idx * x_step
            token_mob.move_to([x, y, 0])

        # We process rounds sequentially. For visual brevity each "AR token"
        # animates with a quick FadeIn(shift LEFT). Each diff round briefly
        # re-masks the last 4 tokens (transform to "___"), then resolves them
        # in a permuted order (FadeOut mask → FadeIn resolved word).
        diff_perm = [2, 0, 3, 1]  # order of resolution within each diff-4 block

        for r_idx, (ar_words, diff_words) in enumerate(rounds):
            row = "A" if r_idx < 3 else "B"
            row_list = row_a_words if row == "A" else row_b_words

            # Update round counter
            new_round_lbl = body_text(f"round {r_idx + 1} / 6", size=14,
                                      color=ACCENT_2).move_to(round_lbl.get_center())
            self.play(Transform(round_lbl, new_round_lbl), run_time=0.18)

            # --- AR step: append 8 words left-to-right
            ar_mobs = []
            for w in ar_words:
                mob = _word(w, ACCENT, size=12)
                place_word(mob, row, len(row_list))
                row_list.append(mob)
                self.play(FadeIn(mob, shift=LEFT * 0.05), run_time=0.04)
                ar_mobs.append(mob)
            # AR step done; brief settle
            self.wait(0.1)

            # --- Diff step: re-mask the last 4 AR words, then resolve them in
            # non-sequential order with the diff_words.
            mask_targets = ar_mobs[-4:]
            mask_positions = [m.get_center() for m in mask_targets]
            # Transform each into "____"
            mask_mobs = []
            for m in mask_targets:
                m_new = _word("___", DIFF, size=12).move_to(m.get_center())
                mask_mobs.append(m_new)
            self.play(*[Transform(m_old, m_new) for m_old, m_new in zip(mask_targets, mask_mobs)],
                      run_time=0.35)
            # Resolve in permuted order
            for slot in diff_perm:
                resolved = _word(diff_words[slot], DIFF, size=12).move_to(mask_positions[slot])
                self.play(Transform(mask_targets[slot], resolved), run_time=0.18)
                # Replace in row_list so future ops see the resolved value
                row_list[-4 + slot] = resolved
                self.play(Indicate(mask_targets[slot], color=WARN, scale_factor=1.2), run_time=0.18)

            # End of round
            self.wait(0.12)

        # Final settle: glow the whole sentence as "coherent paragraph"
        self.wait(0.5)
        # Sum-up caption
        cap1 = body_text("six rounds, 72 tokens, AR and diff alternating on one line",
                         size=13, color=ACCENT_2)
        cap2 = body_text("AR builds left-to-right.  Diff re-masks and resolves in parallel.",
                         size=13, color=ACCENT_2)
        cap = VGroup(cap1, cap2).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap), run_time=0.45)

        self.wait(5)
        fade_out_all(self, run_time=0.5)
