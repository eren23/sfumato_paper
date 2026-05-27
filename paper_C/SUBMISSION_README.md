# Paper C — TMLR submission package

**Title:** Mode Specialisation in Composite AR + Discrete-Diffusion
Language Models: a Mechanistic Account of the Toy-Scale Trade-off
and a Cross-Mode Inference Recipe

**Author:** Eren Akbulut

**Length:** 31 pages (well within TMLR's no-page-limit policy)

**Compiled:** 2026-05-27 — `main.pdf` (457 KB) ✓

---

## What's in the package

```
paper_C/
├── main.tex                  # entry; \input's all sections
├── main.pdf                  # COMPILED — submit this
├── references.bib            # bibliography
├── Makefile                  # `make` reproduces main.pdf
├── README.md                 # paper-level notes
├── TMLR_READINESS.md         # the readiness checklist (already passing)
├── appendix_provenance.md
├── sections/                 # 13 section files \input'd by main.tex
│   ├── introduction.tex
│   ├── method.tex
│   ├── results_curve.tex          # data-efficiency crossover
│   ├── results_compute_control.tex # compute-matched diff win
│   ├── results_modeswitch.tex
│   ├── results_negatives.tex      # honest negatives ledger
│   ├── sample_quality.tex
│   ├── interleaved_routing.tex    # Phase I scope-negative
│   ├── diff_draft_refill.tex      # Phase K — UPDATED with K.2.4 N_outer sweep
│   ├── interpretability.tex       # Phase P — UPDATED with P.2b by-depth
│   ├── discussion.tex
│   ├── related.tex
│   └── limitations.tex
├── tables/   # auxiliary tables
└── figures/  # paper figures
```

## What's new in this revision (since the v1 readiness lock)

1. **Title pivot** to "Mode Specialisation..." — leads with the
   mechanistic finding (P.2 / P.2b) that organises the rest of the
   paper.
2. **Abstract**: new "Mechanistic headline" paragraph before training
   axes; recasts the AR/diff trade-offs as consequences of disjoint
   sparse circuits.
3. **Section 10 (interp) §P.2b — Specialisation by depth.** Replaces
   the ln_f-only P.2 claim with full 10-layer symmetric coverage:
   mean cosine in [0.157, 0.162] across blocks 6–15, with ln_f at
   0.169 actually being slightly *less* specialised than internal
   blocks. Stronger claim: backbone-wide property, not a
   `head_diff_proj` artefact.
4. **Section 9 (Phase K) §K.2.4 — Iteration sweep.** Adds
   $N_\text{outer} \in \{1, 2, 3\}$ table at matched $N=100$:
   NLL saturates after two outer iterations, loop rate keeps
   improving (drops to 6% at $N_\text{outer}=3$/pct25). Sweet-spot
   pct shifts left as $N_\text{outer}$ grows — distributing refill
   across more rounds beats concentrating it.
5. **WikiText substrate transfer** (already in v1 §K.2.3) confirmed
   with new $N_\text{outer}=2$ data — pct50 sweet spot replicates on
   non-math prose.

All other sections unchanged from the readiness-locked draft.

---

## TMLR submission — step-by-step (manual, ~10 min)

TMLR submits via OpenReview, which requires your account/credentials
and a few manual choices. The agent can't click submit for you. Here
is exactly what to do:

### 1. Create the OpenReview submission

- Go to <https://openreview.net/group?id=TMLR>
- Click **"TMLR Submission"** (top of page; opens a submission form)
- Required fields:
  - **Title:** "Mode Specialisation in Composite AR + Discrete-Diffusion Language Models: a Mechanistic Account of the Toy-Scale Trade-off and a Cross-Mode Inference Recipe"
  - **Authors:** Eren Akbulut (eren23 on OpenReview)
  - **Abstract:** paste the abstract from main.tex (lines 41-95 of `paper_C/main.tex` after the `\begin{abstract}` block — TMLR wants plain text; strip LaTeX)
  - **PDF upload:** `paper_C/main.pdf`
  - **Code/data:** point to `https://github.com/eren23/sfumato` (HEAD `df40506` or later) and `https://huggingface.co/eren23/sfumato-composite-ckpts` (artefacts)
  - **Keywords:** discrete diffusion, autoregressive, language model, mechanistic interpretability, sparse autoencoder, mode specialisation, inference recipe
  - **Subject area:** check "deep learning" / "interpretability" boxes
  - **Reviewer suggestions:** leave blank (TMLR AC assigns)
- Click **Submit** → you'll get a confirmation email with the
  paper ID.

### 2. Optional pre-submit polish (skip if you want to ship today)

- The agent did NOT regenerate the figures/ since no new figures
  were added. Existing figures from the v1 lock are still current.
- The agent did NOT update `TMLR_READINESS.md` to reflect the v2
  changes; you may want to add a one-line note that P.2b and K.2.4
  were added post-readiness-lock. Not blocking.
- `tables/` and `figures/` directories contain the v1 artefacts.

### 3. After submission

- TMLR turn-around is typically 4–6 weeks to first decision.
- Watch the OpenReview thread for AC/reviewer messages.
- If reviewers ask for: (a) multi-seed on the N_outer=2/pct50 finding,
  (b) WikiText single-pass control, or (c) the saturation curve at
  $N_\text{outer} \in \{4, 5\}$ — those are the three runs I'd flag
  as next-on-deck in the situation report. Each is ~$0.20 on A40.
- If reviewers push back on 305M-as-toy: the response is in
  `sections/limitations.tex` ("controlled-scale characterisation,
  not capability bench").

### 4. Companion paper

The interpretability finding is strong enough to seed a follow-up
paper. AGENT_BRIEF_INTERPRETABILITY.md in the sfumato repo describes
Phase 4+5 work (causal steering, Neuronpedia self-host) that would
turn the by-depth result + Phase K mechanism into a standalone
mechanistic paper for a workshop or a second TMLR.

---

## Verification

To rebuild from source:
```bash
cd paper_C/
make                  # produces main.pdf (31 pages, ~457 KB)
```

Required: pdflatex + bibtex + natbib + pgfplots + hyperref.
Available in TeX Live 2026 basic install.

## Provenance

Both repos are pushed:
- code/results: `github.com/eren23/sfumato` HEAD `df40506` (or newer)
- paper: `github.com/eren23/sfumato_paper` HEAD with this commit
- artefacts: `huggingface.co/eren23/sfumato-composite-ckpts`
  (F10/F11 checkpoints + 22 SAEs)

Total compute spend for the paper: ~$60 (per CLAUDE.md ledger),
covering 5 months of phases T0–K plus the P.1–P.7 interpretability
layer. Reproducible end-to-end at this budget on A40 / RTX 4090.
