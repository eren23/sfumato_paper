# Sfumato Paper 1 — Video Storyboard

Silent companion video, ~5-6 minutes, 1080p60. Eleven scenes split into a
short motivation (1-3) and the paper's three-axis decomposition + Track 2
design iteration (4-11).

## Claim discipline

- **The paper's headline is a decomposition, not a single fix.** Hybrid
  AR/DDLM reasoning fails along *at least three orthogonal axes*:
  interface-format brittleness, planner-content trust, and sampling-diversity
  preservation. Every scene must trace back to one (or more) of these axes
  or to the Track 2 consensus-distillation design-sensitivity finding.
- **Two trainable fixes, not three.** Track 1 (prefix-robust LoRA) addresses
  axis 1; Track 2 (commit-LoRA) addresses the cmaj-vs-c2c gap. Axis 2 is
  *characterized*, not fixed; axis 3 is *expanded*, not preserved.
- **Numbers are load-bearing.** Every number that appears must trace back to
  `sfumato/e2/PAPER_DRAFT.md`. No invented numbers.
- **Track 2 v3 = 79.0% is "within sampling error" of the 80% pre-reg
  target**, *not* a clean hit. Phrase it that way.
- **The Qwen-SC rebuttal is a defensive scene, not a centerpiece.** It rules
  out generic self-consistency as an explanation; it doesn't claim a new
  result.
- **No narration audio.** All claims live in on-screen text.

## Per-scene one-liners

1. `scene01_metaphor` (~25s): cognitive metaphor — sketch, iterate a vague
   chunk, continue. Sets up why hybrid AR/DDLM is interesting.
2. `scene02_e4_pipelines` (~30s): C1/C2/C3/C4 pipelines side by side.
3. `scene03_e4_results` (~35s): the headline number spread (C1=34, C2=74,
   C3=64, C4=54, cmaj=79). Callout: "C3 < C2 by 10pp — the AR plan damages
   LLaDA". This is the puzzle the rest of the video unpacks.
4. `scene04_three_axes` (~30s): three pills — interface-format brittleness,
   planner-content trust, sampling-diversity preservation. The decomposition.
5. `scene05_axis1_brittleness` (~50s): axis 1, two phases. Base prefix-damage
   hierarchy (C2=74, C2hint=68, C2empty=66, C3p Q-0.5B=64, C3p Q-1.5B=60).
   Then post-Track-1-v2 hierarchy flattens (C2=70.5, C2hint=73.5, C2empty=73,
   C3p Q-0.5B=60, C3p Q-1.5B=67). Spread 8pp -> 3pp on static prefixes.
6. `scene06_axis2_planner_trust` (~35s): axis 2. v2 (4/7 modules) vs v3 (7/7
   modules) on Q-0.5B and Q-1.5B. Inversion: v2 has Q-1.5B helping (60->67),
   v3 has Q-1.5B catastrophically regressing (60->54).
7. `scene07_axis3_diversity` (~40s): axis 3. Branch-agreement histogram, base
   vs v2+commit. 5/5-same drops 51.5 -> 47.5; mean unique answers 1.825 ->
   2.07. Diversity expanded, accuracy held.
8. `scene08_consensus_distill` (~60s): Track 2 timeline. v1 broken modules,
   v2 fixed modules — both stuck at c2c=70.5%. v3 (n_blocks=3 + full-response
   loss) -> c2c=79.0%, within sampling error of 80% target.
9. `scene09_ablation` (~35s): disentangling ablation. v3 alone=73, ABL_A
   (n_blocks=3 + answer-span)=77 (+4), ABL_B (n_blocks=1 + full-response)=73
   (+0), v3 full=79 (+6). Block coverage is the dominant lever.
10. `scene10_qwen_sc_rebuttal` (~25s): Qwen-SC b=5 = 40.5% vs LLaDA cmaj b=5
    = 79-82%. 38-41pp gap. Generic SC does not explain the diffusion advantage.
11. `scene11_closing` (~25s): three-axis recap, two-fix tagline, compute
    footer ($3.50 on 1xRTX-4090).

## Text non-overlap rules (hard constraint)

These rules apply to every scene:

1. Position every text mobject via `.move_to()` or `.next_to()` BEFORE
   `self.add()` / `self.play()`.
2. Max 1 title + 1 body block on screen at once. Multi-row content uses
   `comparison_table()` or a `VGroup.arrange(DOWN, buff=0.35)`.
3. Before adding a new text mobject, fade out the previous one.
   `fade_out_all(self)` between sub-sections.
4. After rendering, run `review_frames.sh <scene>` and visually scan for
   overlap.
5. No font smaller than size 16.
6. Use the `assert_no_overlap(mobjects)` helper from `utils/layout.py` once
   per scene (in practice, once per phase).
