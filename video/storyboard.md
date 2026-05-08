# Sfumato Paper 1 — Video Storyboard

Silent companion video, ~10–11 minutes, 1080p60. Twenty-three scenes
in one through-line that mirrors the paper:

- **Setup (1–3):** cognitive metaphor, four pipelines, the C3 < C2
  puzzle that sets up the rest.
- **Three axes + Track 2 (4–10):** brittleness, planner-trust,
  diversity, consensus distillation, design-iteration ablation, the
  branch-aggregation absorption (b=1 vs b=5), and the Qwen-SC
  rebuttal.
- **Mid-arc transition (11):** axes story closes; bridge into
  "but cmaj itself leaves 8–12 pp on the table."
- **Aggregation arc (12–16, 18, 19, 22, 23):** the voting-rule gap
  evidence and mechanism, the K2 schedule-toggle mechanistic positive,
  and five parallel sub-problems of test-time aggregation that all
  fall to the same pathology (verifier sweep, mode router,
  temporal-SC, schedule-RLHF, base-model swap).
- **Disclosure (20):** plain Qwen-2.5-7B AR baseline beats the hybrid
  at fewer active params on this benchmark — surfaced as honest
  disclosure, not a target.
- **Unified close (24):** three-axis recap, parallel-pathology
  recap, K2-as-block-structured-property scoping, $20.5 spend tally.

## Claim discipline

- **The paper's headline is a decomposition, not a single fix.**
  Hybrid AR/DDLM reasoning fails along *at least three orthogonal
  axes*: interface-format brittleness, planner-content trust, and
  sampling-diversity preservation. Every scene must trace back to one
  (or more) of these axes, to the Track 2 consensus-distillation
  finding, to the aggregation parallel-pathology arc, or to the K2
  scope claim.
- **Two trainable fixes, not three.** Track 1 (prefix-robust LoRA)
  addresses axis 1; Track 2 (commit-LoRA) addresses the cmaj-vs-c2c
  gap. Axis 2 is *characterized*, not fixed; axis 3 is *expanded*,
  not preserved.
- **The aggregation arc is one diagnosis, five instances.** The
  verifier sweep (scenes 13–16), the per-problem mode router
  (scene 19), schedule-conditional temporal-SC voting, KL-anchored
  schedule-RLHF on commit-LoRA, and the LLaDA-1.5 base swap (all in
  scenes 22–23) are five projections of the same underlying claim:
  at this data scale, supervised classification or single-toggle
  retraining over surface features cannot close the cmaj→oracle gap.
  The video makes the parallel structure visible by phrasing each
  scene's title and tagline against the same template.
- **The K2 result is mechanistic, scoped, not headline.** Scene 18
  reports the inverted-U around the v3 default; scene 24 surfaces
  the cross-family scope claim from the DiffuLLaMA substrate audit.
  We do not generalize K2 to flat-schedule samplers.
- **Track 2 v3 = 79.0% is "within sampling error" of the 80% pre-reg
  target**, *not* a clean hit. Phrase it that way.
- **Direction A is within CI on both pilots.** Mini-pilot is paired
  −1 / N=20; mid-pilot is paired +1 / N=50. We do NOT claim a WIN.
  The signal is the directional reversal once the KL anchor is wired.
- **The Qwen-SC rebuttal is a defensive scene.** It rules out generic
  self-consistency as an explanation for the diffusion cmaj advantage;
  it doesn't claim a new positive result.
- **The AR-baseline scene is disclosure, not a target.** The
  substrate-level findings are about the AR/DDLM stack, not about
  beating peer-class AR.
- **Numbers are load-bearing.** Every number that appears must trace
  back to the LaTeX paper or the source-repo
  `phase2/PAPER_DRAFT.md` / spike RESULT.md files. No invented numbers.
- **Total compute is $20.5 across four phases.** Only scene 24 carries
  the cumulative tally — earlier scenes do not show partial running
  spend (which goes stale).
- **No narration audio.** All claims live in on-screen text.

## Per-scene one-liners

1. `scene01_metaphor` (~25s): cognitive metaphor — sketch, iterate
   a vague chunk, continue. Sets up why hybrid AR/DDLM is interesting.
2. `scene02_e4_pipelines` (~30s): C1/C2/C3/C4 pipelines side by side.
3. `scene03_e4_results` (~35s): the headline number spread (C1=34,
   C2=74, C3=64, C4=54, cmaj=79). Callout: "C3 < C2 by 10 pp — the AR
   plan damages LLaDA". This is the puzzle the rest of the video
   unpacks.
4. `scene04_three_axes` (~30s): three pills — interface-format
   brittleness, planner-content trust, sampling-diversity
   preservation. The decomposition.
5. `scene05_axis1_brittleness` (~50s): axis 1, two phases. Base
   prefix-damage hierarchy (C2=74, C2hint=68, C2empty=66, C3p
   Q-0.5B=64, C3p Q-1.5B=60). Then post-Track-1-v2 hierarchy flattens
   (C2=70.5, C2hint=73.5, C2empty=73, C3p Q-0.5B=60, C3p
   Q-1.5B=67). Spread 8 pp → 3 pp on static prefixes.
6. `scene06_axis2_planner_trust` (~35s): axis 2. v2 (4/7 modules) vs
   v3 (7/7 modules) on Q-0.5B and Q-1.5B. Inversion: v2 has Q-1.5B
   helping (60→67), v3 has Q-1.5B catastrophically regressing
   (60→54).
7. `scene07_axis3_diversity` (~40s): axis 3. Branch-agreement
   histogram, base vs v2+commit. 5/5-same drops 51.5 → 47.5; mean
   unique answers 1.825 → 2.07. Diversity expanded, accuracy held.
8. `scene08_consensus_distill` (~60s): Track 2 timeline. v1 broken
   modules, v2 fixed modules — both stuck at c2c=70.5%. v3
   (n_blocks=3 + full-response loss) → c2c=79.0%, within sampling
   error of 80% target.
9. `scene09_ablation` (~35s): disentangling ablation. v3 alone=73,
   ABL_A (n_blocks=3 + answer-span)=77 (+4), ABL_B (n_blocks=1 +
   full-response)=73 (+0), v3 full=79 (+6). Block coverage is the
   dominant lever.
10. `scene10_qwen_sc_rebuttal` (~25s): Qwen-SC b=5 = 40.5% vs LLaDA
    cmaj b=5 = 79–82%. 38–41 pp gap. Generic SC does not explain the
    diffusion advantage.
11. `scene11_closing` (~25s): mid-arc transition. Three-axis recap +
    Track 2 finding, then bridge: "But cmaj itself leaves 8–12 pp on
    the table — what is going on with aggregation?" No spend footer
    here — the cumulative tally lives in scene 24.
12. `scene12_voting_gap` (~30s): the aggregation-arc opener. cmaj
    79.5% vs oracle 88.0% on the v3 LoRA substrate. 8.5 pp gap.
    Headline: majority vote discards the right answer.
13. `scene13_verifier_fail` (~50s): vertical leaderboard of 12
    entries. Claude Sonnet 4.5 + CoT WIN-MINOR (+6.16 pp) at top; 11
    LOSS rows cascading below across 0.5B–72B chat-LMs, embedding
    models, math-tuned chat, process-MLP, symbolic. Headline: every
    peer-class architecture underperforms majority vote.
14. `scene14_three_negatives` (~35s): three side-by-side cards.
    Math-tuning HURTS (Math-7B −6.5 vs chat-7B −4.0). Embedding-
    specific worst (Embedding-8B −8.0 vs chat-8B −5.5). Substrate
    doubling worse (process-MLP N=200 −5.5 vs N=500 −6.16).
    Bottleneck is the supervised-classification objective.
15. `scene15_encoder_scaling` (~30s): three bars dropping from a
    "0 pp cmaj baseline" line. TF-IDF −14, Qwen-0.5B −8.5, Qwen-7B
    −4.0. Dashed extrapolation toward Qwen-32B+. ~5 pp gap-closure
    per ~10× encoder scale. Trend is the publishable observation,
    not the extrapolation.
16. `scene16_problem_1071` (~50s): GSM8K-test problem 1071 (the Kayla
    theater example). Question text in a frame, five branch cards
    showing setup + answer (3 wrong "$371", 2 right "$251"), three
    vote rows (cmaj 371 wrong, oracle 251 right, judge+CoT 251
    right). Mechanism payoff: failure mode is problem comprehension,
    not arithmetic.
18. `scene18_k2_sweep` (~30s): K2 mechanistic positive. Three bars
    (k=0 / k=3 / k=4) showing the inverted-U around the v3 default.
    Sub-block-1 boundary is load-bearing in both directions: off
    costs −1.7 pp, on costs another −3.2 pp.
19. `scene19_mode_router` (~35s): "Same pathology, second sub-problem
    — per-problem mode router". Best-fixed 75% / D1 LR-bandit 65% /
    oracle 85% on a 20-problem × 12-condition LOOCV substrate.
    Callout makes the rhyme with the verifier sweep explicit.
22. `scene22_phase4_negatives` (~35s): "Same pathology, three more
    sub-problems". Three side-by-side cards: temporal-SC voting
    (−4 pp), schedule-RLHF mini-pilot (−1 / N=20, within CI), base-
    model swap (LLaDA-1.5, −2 pp). Tagline points back to scenes
    13 + 19 for the path forward.
23. `scene23_direction_a_reversal` (~30s): paired-card comparison of
    the schedule-RLHF mini-pilot vs the mid-pilot once a KL anchor
    is wired. Both within CI; the directional reversal (−1 → +1) is
    the meaningful evidence. Locked PRE_REG full pilot is the gating
    experiment.
20. `scene20_ar_baseline` (~30s): two bars — hybrid cmajc-v3
    (~82.5%) vs plain Qwen-2.5-7B AR (~86.5%); subtitle calls out
    planner-invariance (82–83% across Qwen-0.5B → 7B planners). The
    monolithic AR wins this benchmark with fewer active parameters.
24. `scene24_phase4_closing` (~30s): unified close. Four bullets
    recap the paper (axes + fixes / distillation design-sensitivity
    / aggregation parallel pathology / K2 scope), tagline
    "substrate findings hold; the head-to-head AR claim does not.",
    full $20.5 four-phase spend tally in the footer.

## Phase-2 claim discipline (additional)

- **The frontier-judge result is on N=500, not N=200.** Numbers come
  from `phase2/PHASE2_FINAL_SUMMARY.md` and
  `phase2/spikes/strong-judge/`. The cmaj baseline shifts 79.0% (N=200)
  → 79.1% (N=500), within sampling noise.
- **17 verifier architectures lost** is the load-bearing count;
  scene 13's leaderboard shows 11 representative entries plus the top
  two (Claude+CoT WIN, Claude YES/NO inconclusive) and pointers to
  the rest via `phase2/RANKING.md` in the paper.
- **Encoder-scaling trend, not extrapolation.** Scene 15 shows the
  three measured points; the dashed line gestures toward 32B+ but
  is explicitly labelled "?" in the source. We do not claim the
  encoder family closes the gap.
- **Mechanism comes from hand inspection, not a learned probe.**
  Problem 1071 is one of 15 cmaj-failed/oracle-recoverable problems
  hand-inspected in `phase2/spikes/option3-process-reward/cmaj_failures_inspection.md`.

## Text non-overlap rules (hard constraint)

These rules apply to every scene:

1. Position every text mobject via `.move_to()` or `.next_to()`
   BEFORE `self.add()` / `self.play()`.
2. Max 1 title + 1 body block on screen at once. Multi-row content
   uses `comparison_table()` or a `VGroup.arrange(DOWN, buff=0.35)`.
3. Before adding a new text mobject, fade out the previous one.
   `fade_out_all(self)` between sub-sections.
4. After rendering, run `review_frames.sh <scene>` and visually scan
   for overlap.
5. No font smaller than size 16.
6. Use the `assert_no_overlap(mobjects)` helper from
   `utils/layout.py` once per scene (in practice, once per phase).
