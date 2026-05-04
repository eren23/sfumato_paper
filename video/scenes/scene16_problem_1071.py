"""Scene 16 -- anatomy of a cmaj failure: GSM8K-test problem 1071.

Question text in a frame at top, five branch cards below showing setup +
arithmetic + answer, three vote-tally rows at the bottom (cmaj wrong, oracle
right, judge right). Same content as Figure 5 in voting_gap.tex.

Mechanism: arithmetic correct in all 5 branches, but 3 share the same
misread setup (charge $6 to all 41 attending guests rather than the 21
ADDITIONAL guests beyond the first 20 covered by the $125 base fee).

Headline: "the failure mode is problem comprehension, not arithmetic."
"""
from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    FadeIn,
    LEFT,
    RIGHT,
    RoundedRectangle,
    Scene,
    UP,
    VGroup,
)

from utils.theme_shim import (
    ACCENT,
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
from utils.layout import assert_no_overlap


# (label, setup_str, answer, color, correct?)
BRANCHES = [
    ("0", "charge $6 to all 41", "$371", WARN, False),
    ("1", "charge $6 to 21 extra", "$251", GOOD, True),
    ("2", "charge $6 to 21 extra", "$251", GOOD, True),
    ("3", "charge $6 to all 41", "$371", WARN, False),
    ("4", "charge $6 to all 41", "$371", WARN, False),
]


def _branch_card(label, setup_str, answer, color, w=2.30, h=1.55):
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.12,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.13,
        stroke_width=2,
    )
    head = body_text(f"branch {label}", size=14, color=color, weight=BOLD)
    setup = body_text(setup_str, size=13, color=FG)
    ans = body_text(answer, size=22, color=color, weight=BOLD)
    inner = VGroup(head, setup, ans).arrange(DOWN, buff=0.10)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


class Problem1071Scene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG

        title = title_text(
            "Anatomy of a cmaj failure  --  GSM8K-test problem 1071",
            size=24,
            color=ACCENT,
        )
        title.to_edge(UP, buff=0.30)

        q_text = (
            "Theater fee: $125 for a party of 20, plus $6 for each ADDITIONAL guest.\n"
            "Kayla invited 25 + 7 + 13 = 45.  4 cannot come.  How much?"
            "      [Gold: $251]"
        )
        q_box = RoundedRectangle(
            width=11.6,
            height=1.05,
            corner_radius=0.15,
            stroke_color=ACCENT,
            fill_color=ACCENT,
            fill_opacity=0.07,
            stroke_width=1.8,
        )
        q_label = body_text(q_text, size=15, color=FG)
        q_label.move_to(q_box.get_center())
        q_group = VGroup(q_box, q_label)
        q_group.next_to(title, DOWN, buff=0.20)

        # Five branch cards in a row.
        cards = [_branch_card(*b[:4]) for b in BRANCHES]
        row = VGroup(*cards).arrange(RIGHT, buff=0.18)
        row.next_to(q_group, DOWN, buff=0.30)

        # Three vote rows.
        def vote_row(label, val, color):
            box = RoundedRectangle(
                width=11.6,
                height=0.50,
                corner_radius=0.10,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.10,
                stroke_width=1.4,
            )
            name = body_text(label, size=15, color=FG)
            v = body_text(val, size=16, color=color, weight=BOLD)
            name.move_to(box.get_left() + RIGHT * 3.4)
            v.move_to(box.get_right() + LEFT * 1.4)
            return VGroup(box, name, v)

        v_cmaj = vote_row(
            "cmaj majority vote (3 / 5)", "$371   wrong", WARN
        )
        v_oracle = vote_row(
            "oracle ceiling (any branch correct?)", "$251   right", GOOD
        )
        v_judge = vote_row(
            "frontier judge + chain-of-thought", "$251   right", GOOD
        )
        votes = VGroup(v_cmaj, v_oracle, v_judge).arrange(DOWN, buff=0.10)
        votes.next_to(row, DOWN, buff=0.25)

        callout = body_text(
            "Failure mode: problem comprehension, not arithmetic.",
            size=20,
            color=ACCENT,
            weight=BOLD,
        )
        callout.to_edge(DOWN, buff=0.30)

        assert_no_overlap([title, q_group, row, votes, callout])

        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(q_group, shift=UP * 0.1), run_time=0.55)
        self.wait(0.4)
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.05), run_time=0.22)
        self.wait(0.5)
        self.play(FadeIn(v_cmaj, shift=UP * 0.05), run_time=0.45)
        self.wait(0.3)
        self.play(FadeIn(v_oracle, shift=UP * 0.05), run_time=0.45)
        self.wait(0.3)
        self.play(FadeIn(v_judge, shift=UP * 0.05), run_time=0.45)
        self.wait(0.5)
        self.play(FadeIn(callout, shift=UP * 0.1), run_time=0.55)
        self.wait(3.5)

        fade_out_all(self)
