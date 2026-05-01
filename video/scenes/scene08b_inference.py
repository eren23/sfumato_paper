"""Scene 8b -- Inside one inference: 4 sub-blocks of 32 tokens unmask in
order, with the v3 commit-LoRA firing on sub-blocks 2-4.

This is the concrete "what does a forward pass look like" picture. We use
GSM8K problem 0 (Janet's ducks, gold = 18) and a real cmaj branch trace to
ground the visuals. The mechanism shown:

  prompt -> 4 sub-blocks of 32 masked tokens -> denoise k=64 steps -> answer

For the c2c-v3 setup (paper headline), commit-LoRA is enabled while the
sampler denoises sub-blocks 2 through 4 of 4. The first sub-block is base
LLaDA only.

Numbers from RESULTS_TRACK2.md and PAPER_DRAFT.md:
  base LLaDA:      c2  = 74%
  c2c v1/v2:       70.5% (commit fires only on last sub-block: too late)
  c2c v3:          79.0% (commit fires on sub-blocks 2-4 of 4)
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    RIGHT,
    RoundedRectangle,
    Scene,
    Square,
    Transform,
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


# Paraphrased branch_0 of GSM8K-0 cmaj output (real, from
# e4/results/raw_cmaj_k64_seed0_b5.jsonl). Trimmed for legibility.
PROMPT_TEXT = (
    "Janet's ducks lay 16 eggs per day. She eats 3 for\n"
    "breakfast, bakes muffins with 4. She sells the rest\n"
    "at the farmers' market for $2 each. How much does\n"
    "she make every day?"
)
GOLD = "18"

# Decoded snippets at each sub-block boundary (truncated to fit).
SUB_BLOCK_SNIPPETS = [
    # k <= 16: sub-block 1 mostly unmasked
    "1. Janet has 16 eggs per day.",
    # k <= 32: sub-block 2 unmasked  (commit-v3 starts firing here)
    "2. She eats 3 for breakfast: 16 - 3 = 13.",
    # k <= 48: sub-block 3 unmasked  (commit fires)
    "3. She bakes 4 for muffins: 13 - 4 = 9.",
    # k <= 64: sub-block 4 unmasked, answer pinned  (commit fires)
    "4. 9 eggs * $2 / egg = $18.   Answer: 18.",
]


class InferenceScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Inside one inference (c2c-v3): 4 sub-blocks x 32 tokens",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.4)

        sub = body_text(
            "GSM8K problem 0 (Janet's ducks). Gold answer: 18.   k = 64 denoising steps total.",
            size=15,
            color=MUTED,
        )
        sub.next_to(title, DOWN, buff=0.18)

        # Prompt panel (top-left, rectangular box with text)
        prompt_box = RoundedRectangle(
            width=6.0, height=1.6,
            corner_radius=0.10,
            stroke_color=MUTED,
            fill_color=MUTED,
            fill_opacity=0.05,
            stroke_width=1.5,
        )
        prompt_box.move_to(LEFT * 3.4 + UP * 1.4)
        prompt_label = body_text("PROMPT", size=14, color=MUTED, weight=BOLD)
        prompt_label.next_to(prompt_box, UP, buff=0.05).align_to(prompt_box, LEFT)
        prompt_text = body_text(PROMPT_TEXT, size=12, color=FG)
        prompt_text.move_to(prompt_box.get_center())

        # 4 sub-blocks (right side, each = a row of 32 token cells).
        TOKEN_W = 0.13
        TOKEN_H = 0.20
        TOKENS_PER_BLOCK = 32
        block_y = [0.9, 0.45, 0.0, -0.45]  # 4 rows from top to bottom

        sub_blocks = []           # list of VGroup of 32 squares
        sub_block_labels = []
        commit_badges = []        # which sub-blocks have commit fire
        block_anchor_x = 1.5      # left edge of each row
        for i, y in enumerate(block_y):
            row = VGroup()
            for j in range(TOKENS_PER_BLOCK):
                cell = Square(
                    side_length=TOKEN_H,
                    stroke_color=MUTED,
                    stroke_width=0.8,
                    fill_color=MUTED,
                    fill_opacity=0.20,
                )
                cell.move_to(
                    RIGHT * (block_anchor_x + j * TOKEN_W) + UP * y
                )
                row.add(cell)
            sub_blocks.append(row)

            block_idx_label = body_text(
                f"sub-block {i+1}", size=12, color=MUTED,
            )
            block_idx_label.move_to(
                RIGHT * (block_anchor_x - 0.85) + UP * y
            )
            sub_block_labels.append(block_idx_label)

            # Commit badge for sub-blocks 2-4 (i.e. i in {1,2,3}) under v3.
            if i >= 1:
                badge = body_text(
                    "commit-v3", size=11, color=ACCENT_2, weight=BOLD,
                )
                badge.move_to(
                    RIGHT * (block_anchor_x + TOKENS_PER_BLOCK * TOKEN_W + 0.55)
                    + UP * y
                )
                commit_badges.append(badge)
            else:
                commit_badges.append(None)

        # Decoded text strip beneath the sub-blocks.
        decoded_box = RoundedRectangle(
            width=10.0, height=1.05,
            corner_radius=0.10,
            stroke_color=DIFF,
            fill_color=DIFF,
            fill_opacity=0.06,
            stroke_width=1.5,
        )
        decoded_box.move_to(DOWN * 1.7)
        decoded_label = body_text("DECODED SO FAR", size=12, color=MUTED, weight=BOLD)
        decoded_label.next_to(decoded_box, UP, buff=0.05).align_to(decoded_box, LEFT)
        decoded_text = body_text("(all tokens still masked)", size=14, color=MUTED)
        decoded_text.move_to(decoded_box.get_center())

        # Step counter (top-right of chart)
        step_counter = body_text("k = 0 / 64", size=14, color=ACCENT_2, weight=BOLD)
        step_counter.move_to(RIGHT * 5.5 + UP * 1.4)

        # Animate intro.
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.45)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.play(
            FadeIn(prompt_box), FadeIn(prompt_label), FadeIn(prompt_text),
            run_time=0.5,
        )
        self.play(
            *[FadeIn(b) for b in sub_blocks],
            *[FadeIn(l) for l in sub_block_labels],
            FadeIn(decoded_box), FadeIn(decoded_label), FadeIn(decoded_text),
            FadeIn(step_counter),
            run_time=0.55,
        )
        self.wait(0.4)

        # Progressive denoising: per sub-block, transition all 32 cells from
        # masked (muted) to unmasked (diffusion blue), update step counter and
        # decoded text, attach commit badge for blocks 2-4.
        for i, row in enumerate(sub_blocks):
            new_step = (i + 1) * 16
            new_counter = body_text(
                f"k = {new_step} / 64", size=14, color=ACCENT_2, weight=BOLD,
            )
            new_counter.move_to(step_counter.get_center())

            # Cell color transitions.
            cell_anims = []
            for cell in row:
                target = cell.copy()
                target.set_fill(DIFF, opacity=0.55)
                target.set_stroke(DIFF, width=1.0)
                cell_anims.append(Transform(cell, target))

            # Decoded text update.
            new_decoded = body_text(
                SUB_BLOCK_SNIPPETS[i], size=14, color=FG,
            )
            new_decoded.move_to(decoded_box.get_center())

            anims = cell_anims + [
                Transform(step_counter, new_counter),
                Transform(decoded_text, new_decoded),
            ]
            if commit_badges[i] is not None:
                anims.append(FadeIn(commit_badges[i]))

            self.play(*anims, run_time=0.85)
            self.wait(0.35)

        # Final answer callout.
        answer_callout = body_text(
            "answer: 18  --  matches gold.",
            size=22,
            color=GOOD,
            weight=BOLD,
        )
        answer_callout.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(answer_callout, shift=UP * 0.1), run_time=0.5)
        self.wait(0.6)

        # Close-out: c2c v3 vs v2 reminder.
        gloss = body_text(
            "v2 commit fired only on sub-block 4 -- answer was already pinned by sub-blocks 1-3.\n"
            "v3 commit fires on sub-blocks 2-4 -- the trajectory itself is malleable.",
            size=14,
            color=MUTED,
        )
        gloss.next_to(answer_callout, UP, buff=0.20)
        self.play(FadeIn(gloss, shift=UP * 0.1), run_time=0.6)
        self.wait(2.5)

        fade_out_all(self)
