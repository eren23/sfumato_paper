"""Scene 14e — Phase K: per-token diff-draft + AR-refill mechanism.

Visualises the K.2 recipe in three phases on a single line:
  Phase 1: AR generates 8 prefix tokens (ACCENT, left-to-right cursor)
  Phase 2: Diff fills 8 more tokens (DIFF, all appear at once but with
           commit-time confidence varying per position; shown as a
           small numeric badge under each token)
  Phase 3: The 4 lowest-conf tokens get highlighted (WARN), then
           transform to AR-refilled tokens (GOOD), with the badges
           dropping away
Final: synthesis line showing the headline numbers.
"""
from __future__ import annotations

from manim import (BOLD, DOWN, FadeIn, FadeOut, Indicate, LEFT, RIGHT,
                   Scene, Transform, UP, VGroup)
from utils.theme_shim import (ACCENT, ACCENT_2, BG, DIFF, FG, GOOD, MUTED, WARN, body_text, fade_out_all, title_text)


def _word(text: str, color, size: int = 16):
    return body_text(text, size=size, color=color, weight=BOLD)


def _conf_badge(value: str, color):
    return body_text(value, size=10, color=color)


class PhaseKScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text("Phase K — diff drafts, AR refills the worst",
                           size=26, color=ACCENT).to_edge(UP, buff=0.35)
        sub = body_text("commit-time conf percentile rank → bottom 50% get AR-refilled",
                        size=13, color=MUTED).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title), FadeIn(sub), run_time=0.5)

        # --- Phase 1: AR prefix ---
        phase_lbl = body_text("1.  AR generates prefix", size=14, color=ACCENT, weight=BOLD)
        phase_lbl.move_to([-5.6, 1.6, 0])
        self.play(FadeIn(phase_lbl), run_time=0.3)

        ar_words = ["Janet", "has", "16", "ducks.", "She", "feeds", "them", "each"]
        ar_mobs = [_word(w, ACCENT) for w in ar_words]
        ar_row = VGroup(*ar_mobs).arrange(RIGHT, buff=0.25)
        ar_row.move_to([0, 1.6, 0])
        for m in ar_mobs:
            self.play(FadeIn(m, shift=LEFT * 0.05), run_time=0.1)
        self.wait(0.2)

        # --- Phase 2: Diff fills next 8, all at once, with conf badges ---
        phase2_lbl = body_text("2.  Diff fills 8 tokens in parallel  +  conf badges",
                                size=14, color=DIFF, weight=BOLD)
        phase2_lbl.move_to([-3.5, 0.4, 0])
        self.play(FadeIn(phase2_lbl), run_time=0.3)

        diff_words = ["morning", "with", "a", "scoop", "of", "feed", "she", "buys"]
        conf_vals = [0.02, 0.01, 0.03, 0.06, 0.04, 0.01, 0.05, 0.02]
        order = sorted(range(len(conf_vals)), key=lambda i: conf_vals[i])
        bottom_half = set(order[:4])

        diff_mobs = [_word(w, DIFF) for w in diff_words]
        diff_row = VGroup(*diff_mobs).arrange(RIGHT, buff=0.25)
        diff_row.next_to(ar_row, RIGHT, buff=0.30)
        self.play(*[FadeIn(m, shift=DOWN * 0.1) for m in diff_mobs], run_time=0.6)

        badge_mobs = []
        for i, m in enumerate(diff_mobs):
            c = conf_vals[i]
            color = WARN if i in bottom_half else GOOD
            badge = _conf_badge(f"{c:.2f}", color).next_to(m, DOWN, buff=0.10)
            badge_mobs.append(badge)
        self.play(*[FadeIn(b) for b in badge_mobs], run_time=0.4)
        self.wait(0.3)

        # --- Phase 3: Bottom-50% flagged, then AR-refilled ---
        phase3_lbl = body_text("3.  AR refills the 4 lowest-conf positions",
                                size=14, color=GOOD, weight=BOLD)
        phase3_lbl.move_to([-3.5, -1.0, 0])
        self.play(FadeIn(phase3_lbl), run_time=0.3)

        flash_anims = []
        for i in bottom_half:
            flash_anims.append(Indicate(diff_mobs[i], color=WARN, scale_factor=1.2))
        self.play(*flash_anims, run_time=0.5)

        refill_words = {
            order[0]: "twice",
            order[1]: "from",
            order[2]: "the",
            order[3]: "local",
        }
        refill_anims = []
        for i in bottom_half:
            new_mob = _word(refill_words.get(i, "[AR]"), GOOD).move_to(diff_mobs[i].get_center())
            refill_anims.append(Transform(diff_mobs[i], new_mob))
            refill_anims.append(FadeOut(badge_mobs[i]))
        self.play(*refill_anims, run_time=0.7)
        keep_badges = [b for i, b in enumerate(badge_mobs) if i not in bottom_half]
        self.play(*[FadeOut(b) for b in keep_badges], run_time=0.3)

        # --- Synthesis ---
        synthesis_lbl = body_text("on F10 (305M, N=200):",
                                  size=14, color=MUTED, weight=BOLD).move_to([0, -2.0, 0])
        result_a = body_text("pure AR (128 tok): NLL = 12.56,  wall = 6.4 s",
                             size=14, color=WARN).move_to([0, -2.4, 0])
        result_b = body_text("K.2 pct50 (128 tok): NLL = 11.98,  wall = 5.0 s",
                             size=14, color=GOOD, weight=BOLD).move_to([0, -2.8, 0])
        synthesis = VGroup(synthesis_lbl, result_a, result_b)
        self.play(FadeIn(synthesis), run_time=0.5)

        head = body_text("-0.58 NLL/token  +  1.3x faster.  Composite-specific recipe.",
                         size=16, color=ACCENT_2, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(head), run_time=0.5)

        self.wait(8)
        fade_out_all(self, run_time=0.5)
