"""Scene 14b — watching composite generate text in place.

Version 2 of the generation visualisation. Earlier draft used abstract
token pill-boxes. User wanted it to look more like text actually forming
in place, the way you'd watch a model stream.

We render a single continuous line that grows word by word. Colour
codes mark the phase each word came from:
  MUTED   — prompt
  ACCENT  — AR-extended words (appear left-to-right, one at a time)
  DIM     — mask placeholders ("____") for the diff region
  DIFF    — diff-filled words (replace placeholders in non-sequential
            order, briefly flashing as they 'lock in')
  GOOD    — final line glows after all positions are filled
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, FadeOut, Indicate, LEFT, RIGHT, Scene, Transform, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _word(text: str, color, size: int = 18):
    return body_text(text, size=size, color=color, weight=BOLD)


class GenerationScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("How composite generates text", size=28, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("paired_64_64 mode on a GSM8K-dev prompt", size=14, color=MUTED).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.4)

        # The text we'll build up, split into two visual lines so it fits.
        prompt_line  = ["Question:", "Janet", "has", "16", "ducks", "that", "lay", "eggs.", "Answer:"]
        ar_line      = ["She", "feeds", "her", "ducks", "twice", "a", "day."]
        diff_targets = ["So", "she", "gets", "32", "eggs", "every", "day", "total."]
        # Order in which diff positions resolve — NOT left-to-right; shows that
        # the diff head fills in parallel, picking high-confidence first.
        unmask_order = [3, 5, 0, 4, 2, 6, 1, 7]

        # ----- Phase 0: prompt appears -----
        prompt_words = VGroup(*[_word(w, MUTED) for w in prompt_line]).arrange(RIGHT, buff=0.22)
        prompt_words.move_to([0, 1.6, 0])
        phase_lbl_p = body_text("prompt", size=14, color=MUTED, weight=BOLD).next_to(prompt_words, LEFT, buff=0.5)
        self.play(FadeIn(prompt_words), FadeIn(phase_lbl_p), run_time=0.6)
        self.wait(0.3)

        # ----- Phase 1: AR fill, one word at a time -----
        phase_lbl_a = body_text("AR fill", size=14, color=ACCENT, weight=BOLD).move_to([phase_lbl_p.get_x(), 0.7, 0])
        ar_words = VGroup(*[_word(w, ACCENT) for w in ar_line]).arrange(RIGHT, buff=0.22)
        ar_words.move_to([0, 0.7, 0])
        # animate: each word appears in turn, with a brief cursor effect
        cursor = body_text("|", size=20, color=ACCENT, weight=BOLD)
        self.play(FadeIn(phase_lbl_a), run_time=0.3)
        for i, w in enumerate(ar_words):
            # place cursor to the right of the most-recent word (or at row start
            # if this is the first word)
            anchor = ar_words[i - 1] if i > 0 else ar_words[0]
            if i == 0:
                cursor.next_to(ar_words, LEFT, buff=0.0)
            else:
                cursor.next_to(anchor, RIGHT, buff=0.08)
            self.add(cursor)
            self.play(FadeIn(w, shift=LEFT * 0.1), run_time=0.22)
            cursor.next_to(w, RIGHT, buff=0.08)
        self.remove(cursor)
        self.wait(0.3)

        # ----- Phase 2: mask placeholders appear after the AR row -----
        phase_lbl_m = body_text("mask", size=14, color=DIFF, weight=BOLD).move_to([phase_lbl_p.get_x(), -0.2, 0])
        mask_words = VGroup(*[_word("____", DIFF, size=18) for _ in diff_targets]).arrange(RIGHT, buff=0.22)
        mask_words.move_to([0, -0.2, 0])
        self.play(FadeIn(phase_lbl_m), run_time=0.3)
        self.play(FadeIn(mask_words, shift=UP * 0.1), run_time=0.6)
        self.wait(0.3)

        # ----- Phase 3: diff fill IN PLACE on the same mask row -----
        # No separate "diff fill" row. The mask label is replaced by the
        # diff-fill label at the same y position, so the eye sees ONE row
        # that goes from mask placeholders to resolved words.
        phase_lbl_d = body_text("diff fill", size=14, color=DIFF, weight=BOLD).move_to(phase_lbl_m.get_center())
        self.play(Transform(phase_lbl_m, phase_lbl_d), run_time=0.3)

        # Resolve positions in unmask_order, two at a time
        batch_size = 2
        for batch_start in range(0, len(unmask_order), batch_size):
            batch = unmask_order[batch_start : batch_start + batch_size]
            in_place_anims = []
            for pos in batch:
                new_word = _word(diff_targets[pos], DIFF, size=18).move_to(mask_words[pos].get_center())
                in_place_anims.append(Transform(mask_words[pos], new_word))
            self.play(*in_place_anims, run_time=0.45)
            self.play(*[Indicate(mask_words[pos], color=WARN, scale_factor=1.15)
                        for pos in batch], run_time=0.3)

        self.wait(0.3)

        # ----- Phase 4: full coherent line glows -----
        # Combine all the rows into the final flowing sentence at the bottom.
        full_text = body_text(
            "Question: Janet has 16 ducks that lay eggs. Answer:  She feeds her ducks twice a day. So she gets 32 eggs every day total.",
            size=14, color=GOOD,
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(full_text), run_time=0.6)
        self.play(Indicate(full_text, color=GOOD, scale_factor=1.04), run_time=0.5)

        caption = body_text(
            "AR builds the sketch left-to-right.  Diff infills in parallel, high-confidence first.  Shared backbone.",
            size=13, color=ACCENT_2,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption), run_time=0.4)

        self.wait(7)
        fade_out_all(self, run_time=0.5)
