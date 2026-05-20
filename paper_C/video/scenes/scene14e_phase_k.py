"""Scene 14e — Phase K: per-token diff-draft + AR-refill mechanism.

REDESIGN: clearer 3-row layout. Each phase gets its own VERTICAL position
so it is unambiguous which tokens are being replaced when. Slower.

  ROW 1 (y≈1.5): AR prefix (8 ACCENT tokens)
  ROW 2 (y≈0):   Diff fills 8 tokens (DIFF), with commit-time conf badges
                 BELOW each token
  ROW 3 (y≈-1.5): AR refills the 4 lowest-conf positions — those 4 turn
                 GOOD; the 4 winners stay DIFF; badges fade away

Bottom: F10 N=200 synthesis numbers.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, FadeOut, Indicate, LEFT, RIGHT,
                   Scene, Transform, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN,
                              body_text, fade_out_all, title_text)


def _word(text: str, color, size: int = 14):
    return body_text(text, size=size, color=color, weight=BOLD)


def _conf_badge(value: str, color):
    return body_text(value, size=10, color=color)


class PhaseKScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Phase K — diff drafts, AR refills the worst",
                           size=24, color=ACCENT).to_edge(UP, buff=0.30)
        sub = body_text("commit-time conf percentile rank → bottom 50% get AR-refilled",
                        size=12, color=MUTED).next_to(title, DOWN, buff=0.10)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.4)

        # ---- ROW 1: AR prefix ----
        row1_y = 1.6
        row1_lbl = body_text("1.  AR generates 8 prefix tokens",
                             size=13, color=ACCENT, weight=BOLD)
        row1_lbl.move_to([-4.8, row1_y + 0.6, 0])
        self.play(FadeIn(row1_lbl), run_time=0.4)

        ar_words = ["Janet", "has", "16", "ducks.", "She", "feeds", "them", "each"]
        ar_mobs = [_word(w, ACCENT) for w in ar_words]
        ar_row = VGroup(*ar_mobs).arrange(RIGHT, buff=0.22)
        ar_row.move_to([0.5, row1_y, 0])
        for m in ar_mobs:
            self.play(FadeIn(m, shift=LEFT * 0.05), run_time=0.08)
        self.wait(0.4)

        # ---- ROW 2: Diff fill + confidence badges ----
        row2_y = 0.0
        row2_lbl = body_text("2.  Diff fills 8 tokens in parallel (with commit-time conf)",
                             size=13, color=DIFF, weight=BOLD)
        row2_lbl.move_to([-4.0, row2_y + 0.6, 0])
        self.play(FadeIn(row2_lbl), run_time=0.4)

        diff_words = ["morning", "with", "a", "scoop", "of", "feed", "she", "buys"]
        conf_vals = [0.02, 0.01, 0.03, 0.06, 0.04, 0.01, 0.05, 0.02]
        order = sorted(range(len(conf_vals)), key=lambda i: conf_vals[i])
        bottom_half = set(order[:4])

        diff_mobs = [_word(w, DIFF) for w in diff_words]
        diff_row = VGroup(*diff_mobs).arrange(RIGHT, buff=0.22)
        diff_row.move_to([0.5, row2_y, 0])
        self.play(*[FadeIn(m, shift=DOWN * 0.1) for m in diff_mobs], run_time=0.6)

        badge_mobs = []
        for i, m in enumerate(diff_mobs):
            c = conf_vals[i]
            color = WARN if i in bottom_half else GOOD
            badge = _conf_badge(f"{c:.2f}", color).next_to(m, DOWN, buff=0.12)
            badge_mobs.append(badge)
        self.play(*[FadeIn(b) for b in badge_mobs], run_time=0.5)
        self.wait(0.6)

        # ---- ROW 3: Highlight bottom-50% + AR-refill ----
        row3_y = -1.6
        row3_lbl = body_text("3.  AR refills the 4 lowest-conf positions",
                             size=13, color=GOOD, weight=BOLD)
        row3_lbl.move_to([-4.4, row3_y + 0.6, 0])
        self.play(FadeIn(row3_lbl), run_time=0.4)

        # Build row3 = copies of diff_mobs, projected down to row3_y
        row3_mobs: list = []
        for i, m in enumerate(diff_mobs):
            # Decide if this position will be refilled or kept
            is_refilled = i in bottom_half
            color = GOOD if is_refilled else DIFF
            text = ({
                order[0]: "twice",
                order[1]: "from",
                order[2]: "the",
                order[3]: "local",
            }.get(i, diff_words[i]) if is_refilled else diff_words[i])
            m3 = _word(text, color).move_to([m.get_center()[0], row3_y, 0])
            row3_mobs.append(m3)

        # Animate: flash warns on bottom-half in row2, draw arrows down, fade in row3 tokens
        flash_anims = [Indicate(diff_mobs[i], color=WARN, scale_factor=1.2)
                       for i in bottom_half]
        self.play(*flash_anims, run_time=0.7)

        # Fade in row3 tokens (refilled in GOOD, kept in DIFF)
        self.play(*[FadeIn(m, shift=DOWN * 0.2) for m in row3_mobs], run_time=0.7)
        # Fade out conf badges to declutter
        self.play(*[FadeOut(b) for b in badge_mobs], run_time=0.4)

        # ---- Synthesis numbers at bottom ----
        synthesis_lbl = body_text("on F10 (305M, N=200):", size=13, color=MUTED, weight=BOLD)
        synthesis_lbl.move_to([0, -2.6, 0])
        result_a = body_text("pure AR (128 tok): NLL = 12.56",
                             size=13, color=WARN).move_to([0, -2.95, 0])
        result_b = body_text("K.2 pct50 (128 tok): NLL = 11.98",
                             size=13, color=GOOD, weight=BOLD).move_to([0, -3.25, 0])
        synthesis = VGroup(synthesis_lbl, result_a, result_b)
        self.play(FadeIn(synthesis), run_time=0.5)

        head = body_text("−0.58 NLL/token  ·  composite-specific recipe",
                         size=15, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.20)
        self.play(FadeIn(head), run_time=0.4)

        self.wait(8)
        fade_out_all(self, run_time=0.5)
