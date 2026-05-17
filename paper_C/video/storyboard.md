# Sfumato Paper C — Video Storyboard

Silent companion video, ~8–9 minutes, 1080p60. Sixteen scenes in one
through-line that mirrors the paper plus the Phase H+ sample-quality
investigation appendix.

Reuses the Manim infrastructure from `../../video/` (theme_shim,
layout helpers). New scenes live under `scenes/`. Render via the
same `render_story.sh` pattern.

## What this video covers

- **What composite training is**: a single transformer backbone with
  two output heads (AR LM + diffusion mask-fill), trained jointly
  with an α-schedule that mixes both losses.
- **What we found at toy scale (60M–760M, GSM8K-train + FineWeb-Edu)**:
  a *symmetric* trade-off — composite gives up ~0.2 NLL on the AR
  axis vs a same-budget pure-AR baseline, and gains ~0.5–0.7 NLL on
  the diffusion axis vs a same-budget pure-diff baseline. The trade
  *reverses* in the low-data regime: at 500 GSM8K-train problems
  composite *also* wins the AR axis.
- **What the experiments locked**: a clean cross-over in the
  data-efficiency curve (E3c, 800–1500 problems), and a
  compute-matched control (E3b) where pure-diff trained for 2× the
  composite's diff-training compute *still* loses.
- **The Phase H+ saga (the new content)**: F9 (305M composite, 3B
  FineWeb tokens) finished with a healthy NLL but every free-run
  sample was a sentence-level token loop. Three independent root
  causes; two layers of decoder fixes; the "honest 0%" outcome on
  GSM8K-dev free-run; the F10 retrain that's in flight as we
  publish.
- **What this is *not*** : a deployment-ready model. The toy scale
  + the absence of Q/A training in F9 mean GSM8K accuracy is
  noise-floor regardless of decoder. The point is the *trade-off
  characterisation* and the *diff-head loop fix* (count-based
  repetition penalty on parallel mask-fill), both of which are
  novel contributions that survive at any scale.

## Claim discipline

- **The headline is the trade-off, the secondary finding is the
  sample-quality investigation.** Every scene must trace back to
  one or the other.
- **NLL is the metric, not GSM8K accuracy.** GSM8K accuracy at this
  scale is too noisy to support claims. The data-curve, the
  compute-matched control, and the diff-head loop fix all live in
  NLL space.
- **The diff-head fix matters beyond this paper.** Standard
  set-based repetition_penalty fails on parallel mask-fill decoders
  because a single forward pass fills N positions from the *same*
  logits — penalising "seen-once" doesn't bite. The count-based
  variant (`logit / rep_pen^count`) is a one-line patch that
  generalises to any diffusion / mask-fill LM (BD3-LMs, DiffuLLaMA,
  LLaDA, etc.).
- **F10 is in flight, not in the paper.** Mention it as the natural
  Tier-3 follow-up but do not let it gate the trade-off claims.

## Scene-by-scene

Total target: 8m30s. Times include the standard 0.5s fade-out from
the previous scene.

### Scene 0 — Title + headline (0:00 – 0:25, 25s)
Title card: *"Composite AR + Discrete-Diffusion Training at Toy
Scale: a Trade-off Characterisation with a Data-Efficiency
Crossover."* Subtitle: *"Plus: how we kept a 305M composite from
generating 'eggs eggs eggs eggs' on its first 3B-token training run."*
Author / date / venue placeholder.

### Scene 1 — What composite training is (0:25 – 0:55, 30s)
Two-pane diagram: left, a transformer backbone with **two output
heads** (AR / mask-fill). Right, the joint loss
`L = α · L_AR + (1 − α) · L_diff` with α-schedule descending from
1.0 to 0.5 over training. Caption: *"One backbone, two losses,
one model that can extend autoregressively or in-fill diffusively."*

### Scene 2 — The toy-scale setup (0:55 – 1:20, 25s)
Bullet card with the experimental envelope:
- 60M / 120M / 200M / 250M / 300M / 500M / 760M params
- GSM8K-train (4 M tokens) + FineWeb-Edu sample-10BT
- 3k-step recipe (~$0.10 per cell on A40)
- Baselines: AR-only same arch, diff-only same arch, B3 paired
  (two specialised half-size models, same total params)

### Scene 3 — The symmetric trade-off, F3 vs E3b (1:20 – 2:00, 40s)
Twin bar charts side-by-side:
- Left (F3): pure-AR-6k beats composite-3k on AR axis by **−0.70 NLL**
  at 200M (compute-matched).
- Right (E3b): composite-3k beats pure-diff-6k on diff axis by
  **−0.69 NLL** at 200M, growing to **−0.74** at 300M.
Caption: *"Compute can buy back the AR tax. Compute cannot buy back
the diff advantage. The trade is structural."*

### Scene 4 — The data-efficiency crossover, E3c (2:00 – 2:35, 35s)
Line plot of Δ_NLL (composite − ar_only) vs data size, 500 → 7500
GSM8K-train problems. Zero crossing localised in 800–1200p band.
Caption: *"Below ~1k problems, composite wins both axes. Above,
composite pays a small but consistent AR tax. The data-regime
matters."*

### Scene 5 — Honest negatives (2:35 – 3:05, 30s)
Two small tables: OOD (WikiText / OpenWebText, composite +0.05 to
+0.20 NLL worse) and ECE (composite slightly worse calibration at 4
of 5 scales). Caption: *"Composite does not transfer to OOD prose.
Calibration is not improved. We report these alongside the wins."*

### Scene 6 — Mode-switching inference, E3a (3:05 – 3:35, 30s)
Bar chart of GSM8K-dev N=50 accuracy across ar_only / mode_switch /
paired for composite vs ar_only ckpts at 200M-3k, n=5 seeds.
Composite mode_switch_64_32 = 4.0 ± 0.6 % vs pure-AR same mode
1.6 ± 0.4 %. Caption: *"A workshop-grade lift; not the headline."*

### Scene 7 — Scale-up to F-series (3:35 – 4:00, 25s)
Quick montage: F4 (500M), F7 (760M misadvertised as 1B), F8/F8b
(8M param-golf), F9 (305M FineWeb hero). Highlight F9's stats:
"305M, 3B FineWeb-Edu tokens, 33.8 h on A40, val_ar_nll = 3.96."

### Scene 8 — The shock (4:00 – 4:35, 35s)
Show a real F9 sample with greedy decoding. Verbatim:
> "She makes a lot of money by selling her eggs. She makes a lot
> of money by selling her eggs. She makes a lot of money by selling
> her eggs. ... × 17"
Caption: *"NLL = 3.96 looks healthy. But every free-run sample at
every probe5 mode is a degenerate loop. Free-run accuracy on
GSM8K-dev: 0 / 50."*

### Scene 9 — Why NLL hid this (4:35 – 5:00, 25s)
Diagram contrasting **teacher-forced decoding** (each next-token
conditioned on the gold token — loops cannot form because every
token is the gold answer) vs **free-run decoding** (each next-token
conditioned on the model's own previous prediction — loops
compound). Caption: *"NLL measures the first. Samples measure the
second. The gap can be infinite."*

### Scene 10 — Three independent root causes (5:00 – 5:35, 35s)
Three pill cards horizontal:
1. **Decoder unwired** — `gen_ar()` already had temp/top_p/rep_pen
   flags but all four probe5 call sites passed defaults (greedy).
   `train.py` had its own inline argmax, didn't use `gen_ar()` at all.
2. **Format OOD** — F9 trained on raw FineWeb-Edu only. The
   `"Question: ...\\nAnswer:"` eval prompt was never seen.
3. **Chinchilla 49 %** — 305M × 20 tok/param = 6.1 B; F9 saw 3 B.
   Holtzman 2020 + Li 2023: undertrained models loop harder.

### Scene 11 — Tier 0 fix: wire the AR-side anti-rep (5:35 – 6:00, 25s)
Code-diff card showing the one-line change at each call site (pass
`temperature=0.8 top_p=0.9 repetition_penalty=1.15
no_repeat_ngram_size=3`). Then a small table:
| Mode | greedy | Tier 0 |
| `ar_only` | 100 % loop | **0 % loop** |
| others | 60–90 % loop | 60–90 % loop |
Caption: *"AR mode rescued. Mode-switch and paired modes still loop
because they fill masks via raw argmax on the diff head."*

### Scene 12 — Why set-based repetition_penalty fails on parallel mask-fill (6:00 – 6:30, 30s)
Animation: a single diff forward pass produces logits at *N* masked
positions. All N positions argmax to the same word. Set-based
rep_pen penalises *"seen-once"* — applies the same `÷ 1.15` to all
N positions, but doesn't grow with frequency. Inset formula:
`logit / rep_pen^count(token in context)`. Caption: *"Count-based
is the unlock: 30 'eggs' in context → `÷ 1.15^30 ≈ 66`."*

### Scene 13 — Tier 0.5 results: loop-rate deltas (6:30 – 7:00, 30s)
Bar chart of loop_rate per mode, three columns (greedy / Tier 0 /
Tier 0.5+count). Numbers:
| Mode | greedy | Tier 0 | Tier 0.5+count |
| ar_only | 100 % | 0 % | 0 % |
| mode_switch_96_32 | 100 % | 70 % | **10 %** |
| mode_switch_64_32 | 100 % | 65 % | **20 %** |
| paired_64_64 | 100 % | 80 % | **40 %** |
Caption: *"−40 to −60 pp across all diff-touching modes from a
single sampler patch."*

### Scene 14 — Before/after sample text (7:00 – 7:35, 35s)
Two side-by-side text cards, same prompt (Q0 paired_64_64 on F9):
- **Greedy / Tier 0**: *"A duck's bill is 1,000 pounds. eggs eggs
  eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs
  eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs eggs
  eggs eggs eggs"*
- **Tier 0.5+count**: *"Given that she needs to feed a large number
  of chickens she will need to know how to produce eggs. If she
  doesn't have access to food, she will be unable to eat the eggs.
  Egg-laying is an excellent way to raise chickens. There are many
  ways to raise an egg…"*
Caption: *"Same model, same prompt, same checkpoint. Just the
decoder changed."*

### Scene 15 — F10 in flight + close (7:35 – 8:30, 55s)
A modest closing scene. Two halves:
- **Left**: F10 is training right now. Same 305M arch, same 3B
  budget, but `load_mixed_tokens` swaps in 5 % formatted GSM8K Q/A.
  Hypothesis: free-run accuracy moves off the 0 % floor; the model
  finally learns "Answer:" structure.
- **Right**: What this paper *does* claim, in three lines.
  1. Composite training trades a small AR tax for a substantial
     diff-axis gain at toy scale, *symmetrically* and
     *compute-stably*.
  2. The trade reverses in the data-constrained regime; the
     crossover is at ~1 k problems.
  3. Parallel mask-fill decoders need count-based repetition
     penalty, not set-based. One-line patch, big lift.

Final card: paper + repo links, spend tally (~ \$30 GPU for the full
study), thanks.

## Tone

Calm, methodical, no exclamation marks. Match the "honest negatives"
register of paper-1 scenes 14–17. Verbatim sample text in monospace
with no enlargement or styling — the "before" is meant to look
banal so the "after" feels earned.

## Render notes

- Reuse `../../video/utils/theme_shim.py` for ACCENT / FG / BG.
- Match font (whichever paper-1 video used).
- 1080p60. Fade-out 0.5 s between scenes.
- Frame budget: ~8m30s @ 60 fps ≈ 30 600 frames.
- For the side-by-side sample-text scene, fix the text height so
  the "eggs eggs eggs..." block visually overflows; the coherent
  paragraph fits cleanly. Visual contrast carries the point.

## Open todos before record

1. Generate `figures/loop_rate_bar.pdf` for Scene 13 from
   `e5/results/f9_300m_coherent/probe5_*.json` via
   `e5/scripts/loop_rate.py`. Place under
   `paper_C/video/media/figures/`.
2. Pull a longer F9 sample for Scene 14 (currently truncates at 280
   chars; the impact is bigger at ~600 chars).
3. Write narrator-free captions; this is a silent companion video.
4. Once F10 lands, replace Scene 15-left with the actual F10
   GSM8K-dev free-run accuracy table.

## What this video does NOT cover

- The original Sfumato vision (paper A / paper B inference-bandage
  arc). That has its own video in `../../video/`.
- Implementation details of the Manim scenes — those live in the
  Python scene files alongside this storyboard.
- Anything that requires citation-by-citation comparison to BD3-LMs,
  Transfusion, DiffuLLaMA. Those belong in the paper, not the video.
