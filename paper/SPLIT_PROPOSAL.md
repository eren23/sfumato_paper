# Split proposal: Paper A (substrate) + Paper B (aggregation)

Status: **proposal, not yet executed.** This document lays out
exactly what would go where if we split the current 41-page paper
into two papers. Decide here, then I tear up the LaTeX.

## Why split

The current paper has 10 contribution-list items. Reviewers will
read it as two coherent stories competing for the same abstract:

- **A "substrate"** story about why the hybrid AR/DDLM literature
  is contradictory: format brittleness + planner-content trust +
  diversity preservation, with a trainable fix on axis 1.
- **An "aggregation"** story about what `cmaj` is and isn't doing:
  consensus distillation as a design-sensitivity finding, the
  voting-rule gap, the verifier sweep, the K2 schedule toggle, the
  parallel mode-router/temporal-SC/RLHF/base-swap negatives, and
  the AR-baseline disclosure.

Both are real and self-supporting. Combining them dilutes the
substrate framing's claim-discipline (it has to defend the
aggregation contributions too) and dilutes the aggregation arc
(reviewers carry over their judgment of axis 2 into
\S{voting\_gap}). The reviewer feedback on the v1 draft converged
on: ship two papers.

## Per-section assignment

| Current file                           | Paper A | Paper B | Notes |
|----------------------------------------|:---:|:---:|---|
| `main.tex` abstract / intro / conclusion | rewrite (substrate) | rewrite (aggregation) | both new |
| `setup.tex`                            | trim | trim, refer to A | B's setup is shorter and references A |
| `axis1_brittleness.tex`                | ✓ | — | + new v1 catastrophe subsection |
| `axis2_planner_trust.tex`              | ✓ | — | reframed as phenomenon |
| `axis3_diversity.tex`                  | ✓ | — | |
| `consensus_distillation.tex`           | — | ✓ | Track 1 v3 cited as a "given" in B's setup |
| `self_consistency.tex`                 | — | ✓ | Qwen-SC rebuttal belongs to the aggregation arc |
| `voting_gap.tex`                       | — | ✓ | |
| `commit_lora_k2.tex`                   | — | ✓ | + cross-DLM-family scope subsection |
| `mode_router.tex`                      | — | ✓ | + parallel-negatives subsection |
| `discussion.tex`                       | substrate parts | aggregation parts | split per-subsection |
| `appendix/prereg_scorecard.tex`        | trim | trim | each appendix carries its predictions |
| `appendix/hyperparameters.tex`         | trim | trim | each carries its training config |
| `appendix/compute_spend.tex`           | A's phase 1 only | B's phases 2+3+4 | split table by phase |
| `appendix/spike_chain.tex`             | — | ✓ | spike chain is part of B |
| `appendix/open_exposures.tex`          | trim | trim | each lists relevant open exposures |

## Discussion split

The current `discussion.tex` has 6 subsections. Distribution:

- **§Reconciling the Conflicting Reports** → A (it's about the three-axis frame)
- **§One-Sentence Diagnosis: Problem Comprehension, Not Arithmetic** → B (it's about the cmaj failure mode)
- **§Parallel Negatives Across Aggregation Sub-Problems** → B
- **§Honest Peer Baseline: Plain AR at Matched Scale** → B (about what cmajc is/isn't doing vs AR; A points to it as forward-looking)
- **§Implication: Distillation of Inference-Time Mechanisms** → B (it's about Track 2)
- **§Future Work** → split: cross-task and content-trust adapter to A, verifier paths and diversity-mechanism test to B
- **§Limitations** → split per scope: A's limitations are about axes 1/2/3 + capacity rungs; B's are about voting gap + N=200 single-seed on aggregation experiments

## Sample new abstracts

### Paper A — "Three Axes of Hybrid AR/Diffusion Reasoning Failure on GSM8K"

> The empirical record on hybrid pipelines that pair an
> autoregressive (AR) language model with a discrete-diffusion
> language model (DDLM) for chain-of-thought reasoning is
> contradictory: papers find that AR planning helps, that it
> hurts, that DDLM sampling diversity is preserved, that it
> collapses. We argue these conflicts collapse once the failure
> surface is decomposed. On GSM8K with LLaDA-8B-Instruct and
> Qwen-{0.5B,1.5B} planners we identify three substrate-level
> failure axes that can be measured independently:
> (i) **interface-format brittleness** — wrapping a question in
> any plan-shaped scaffold, even a content-free one, costs 8 pp
> versus no prefix, and an r=8 prefix-robust LoRA closes the
> static-prefix gap to within 1 pp at v3 capacity, with a
> measurable single-shot-vs-branch-vote capacity tradeoff;
> (ii) **planner-content trust as a phenomenon** — at v2 capacity
> a 1.5B planner helps and a 0.5B planner hurts; at v3 capacity
> the directions invert; we have two capacity rungs and call this
> a phenomenon, not yet a fully-resolved axis;
> (iii) **sampling-diversity preservation** — format-augmented
> LoRA training *expands* the variety of stochastic branches
> rather than collapsing it (5/5-branch agreement
> 51.5% → 47.5%), inverting the canonical
> diffusion-fine-tuning prediction. We also document a
> publishable masked-diffusion SFT pitfall: an early v1 recipe
> with too-wide mask-sampling support produced a
> bigram-repetition mode collapse that regressed C2 by 14.5 pp,
> fixable with four hyperparameter changes from a single design
> lesson. All adapters and datasets are public; total spend is
> approximately $4 on a single RTX 4090, batched into one GPU-day.
> A companion paper [B] uses the v3 prefix-robust LoRA as a fixed
> substrate and characterizes what cmaj majority-vote
> aggregation does and does not do on top of it.

### Paper B — "Test-Time Aggregation in Diffusion-LM Reasoning: Mechanism, Voting Gap, and Parallel Negatives"

> Majority-vote consensus over stochastic diffusion branches
> ("cmaj") is the strongest single mechanism we have for
> small-DDLM math reasoning: on GSM8K with LLaDA-8B-Instruct it
> reaches 79–82% on N=200, +6 pp over single-shot. This paper
> asks what cmaj is and isn't doing on top of a fixed
> prefix-robust substrate (the v3 LoRA from Paper A). Four
> findings: (i) **consensus distillation is design-sensitive,
> not architecture-limited** — distilling cmaj into a
> single forward pass via a late-block answer-span commit
> adapter plateaus at c2c = 70.5% across two iterations and a
> 3.25× capacity bump (a clean negative whose surface reading is
> "the adapter cannot do this"), but a multi-block, full-response
> variant recovers c2c = 79.0%, within sampling error of an 80%
> pre-registered target; disentangling ablations attribute +4 pp
> to block coverage and +2 pp to full-response training, with
> full-response training *alone* worth 0.0 pp — two design errors
> mask each other. (ii) **The cmaj voting-rule gap is structural
> and the failure mode is problem comprehension, not arithmetic.**
> The oracle ceiling exceeds majority-vote accuracy by 8–12 pp
> across four LoRA configurations and three seeds; 17 peer-class
> verifier architectures (text-bag, 0.5B–72B chat-LMs, embedding
> and reward models, process-feature MLPs, step-PRMs, symbolic
> arithmetic) all under-perform majority vote, while a frontier
> judge with chain-of-thought (Claude Sonnet 4.5) closes 86% of
> the gap; hand-inspection of cmaj-failed/oracle-recoverable
> problems shows wrong branches contain locally correct
> arithmetic applied to incorrect problem setups, predicting the
> entire verifier leaderboard from a single diagnosis.
> (iii) **Commit-LoRA is a discrete inference-time schedule
> toggle on block-structured mask diffusion.** A K2 sub-block
> ablation produces an inverted-U around the v3 default
> (k=3 peak, k=0 adapter-off −1.7 pp, k=4 always-on −3.2 pp),
> and a Phase-1 substrate audit of DiffuLLaMA confirms the
> toggle's identity does not carry to flat-schedule samplers.
> (iv) **Parallel aggregation negatives reinforce a unified
> diagnosis.** An offline-replay per-problem mode router, a
> schedule-conditional temporal-SC voting variant, KL-anchored
> schedule-RLHF on commit-LoRA, and a LLaDA-1.5 base swap all
> land as honest negatives or within-CI signals; all share the
> same small-N + large-action + surface-feature pathology.
> A parameter-matched plain Qwen-2.5-7B AR baseline reaches
> ∼86.5% on this benchmark, beating the hybrid cmajc at fewer
> active parameters; we surface this as disclosure rather than
> as a target. Total compute on top of Paper A's substrate is
> approximately $17, on a single RTX 4090.

## What changes for the video

The companion video (`/video/`) covers the full arc and stays as
one piece — both papers reference it as supplementary. We update
the storyboard to label scenes 1–11 as "Paper A material" and
scenes 12–24 as "Paper B material" without further restructuring.
Each paper's main.tex links to the same final_story_1080p60.mp4.

## What changes for the repo

```
sfumato_paper/
├── paper_A/                ← current /paper/, trimmed (substrate)
│   ├── main.tex
│   ├── sections/
│   │   ├── introduction.tex
│   │   ├── setup.tex
│   │   ├── axis1_brittleness.tex
│   │   ├── axis2_planner_trust.tex
│   │   ├── axis3_diversity.tex
│   │   ├── discussion.tex (substrate-only)
│   │   └── conclusion.tex
│   ├── appendix/
│   │   ├── prereg_scorecard.tex (Paper A predictions only)
│   │   ├── hyperparameters.tex  (Track 1 v2/v3 only)
│   │   ├── compute_spend.tex    (Phase 1 only, ~$4)
│   │   └── open_exposures.tex
│   ├── figures/
│   │   ├── fig1_prefix_hierarchy.pdf
│   │   ├── fig2_branch_agreement.pdf
│   │   └── (axes-only figures)
│   ├── references.bib
│   └── Makefile
├── paper_B/                ← new (aggregation)
│   ├── main.tex
│   ├── sections/
│   │   ├── introduction.tex
│   │   ├── setup.tex            (brief; refers to A)
│   │   ├── consensus_distillation.tex
│   │   ├── self_consistency.tex
│   │   ├── voting_gap.tex
│   │   ├── commit_lora_k2.tex
│   │   ├── mode_router.tex      (with parallel-negatives subsec)
│   │   ├── ar_baseline.tex      (extracted from current discussion §11.3)
│   │   ├── discussion.tex       (aggregation-only)
│   │   └── conclusion.tex
│   ├── appendix/
│   │   ├── prereg_scorecard.tex (Paper B predictions only)
│   │   ├── hyperparameters.tex  (Track 2, K2 sweep, mode router)
│   │   ├── compute_spend.tex    (Phases 2+3+4, ~$17)
│   │   ├── spike_chain.tex
│   │   └── open_exposures.tex
│   ├── figures/
│   │   ├── fig3_c2c_design_iteration.pdf
│   │   ├── fig4_b1_vs_b5_collapse.pdf
│   │   ├── fig_commit_lora_k2_sweep.pdf
│   │   └── (aggregation figures)
│   ├── references.bib            (shared ↔ paper_A; symlink or copy)
│   └── Makefile
├── docs/
│   ├── paper_A.pdf
│   └── paper_B.pdf
└── video/                  ← unchanged; both papers reference it
```

References handled by either symlinking `references.bib` between
the two paper directories (cleanest) or duplicating it (simpler).

## Length estimate

- **Paper A**: ~12–14 pages body + ~5 pages appendix → 17–19 pages
- **Paper B**: ~16–18 pages body + ~7 pages appendix → 23–25 pages

Down from the current 41 pages combined. Each fits comfortably
into a workshop or short-track main-conference slot.

## Open decisions for you

1. **Approve the split?** If yes, I execute the directory
   restructure + abstract/intro rewrites + appendix splits +
   verify both build, in roughly 60–90 minutes of editing.
2. **Submit-order question:** does Paper B *cite* Paper A as
   prior work (preferred — gives A air time first), or do they go
   together as "companion papers" (works for arXiv but is awkward
   for venue submissions)? My read is the former: Paper A is the
   citation A&B both rest on.
3. **Title for Paper B?** Two candidates:
   - "Test-Time Aggregation in Diffusion-LM Reasoning: Mechanism, Voting Gap, and Parallel Negatives"
   - "What Majority Vote Does and Doesn't Do in Diffusion-LM Reasoning"
   The second is punchier; the first is more search-friendly.
4. **Track 1 v3 in Paper B's setup**: re-derive briefly or cite
   Paper A as a ref-only? The latter is cleaner if you can rely
   on Paper A being on arXiv first; the former is safer if Paper
   B might be reviewed in isolation.

## What I will NOT do without sign-off

- Restructure the directory or rename files
- Rewrite `main.tex` for either paper
- Move sections between directories

The current /paper/ remains a single combined paper with the
framing-pass improvements applied (substrate framing in §1, axis 2
softened to phenomenon, v1 catastrophe in body, problem-
comprehension topic sentence in discussion). That stands as a
fallback if you want to ship one paper instead of two.
