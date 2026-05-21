# TMLR readiness assessment — Paper C

## Verdict

**Cleanly TMLR after Phase M + N hardening.** Previously "TMLR with
caveats / strong workshop" (post-Phase E); each of the caveats has
since shrunk:

| Caveat | Status |
|---|---|
| D1 mode-switch was n=3 (lucky seed?) | Phase J replaces it — three measured composite-specific wins on F10 ($5.43\times$ speed, FIM, $-0.74$ NLL revision) |
| Phase K result was N=50 (-0.90 NLL) | Hardened to N=200 (-0.58 NLL, still positive, still composite-specific) |
| No α-sensitivity data | Phase M α-sweep ($0.20 / 0.30 / 0.40$) provides the curve |
| F11 was from-scratch (driver bug) | Phase N's redo trained F11 properly via resume-from-F10 |
| Phase L SFT untested | Phase L + N.1 add two more honest negatives |
| No transfer test beyond GSM8K | K.2.2 WikiText-2 generalisation: pct50 still optimum on prose |

## TMLR rubric self-score

**1. Claim well-defined?** Yes.
- Central claim: composite training maps a Pareto trade-off between
  AR-axis cost and diff-axis benefit, with an inference-deployable
  routing recipe (Phase K) that converts the diff-axis advantage
  into a measurable per-token NLL + wall-clock win.

**2. Evidence sufficient?**
- Multi-scale training: 60M / 120M / 200M / 300M / 305M.
- Multi-α α-sweep: 0.20 / 0.30 / 0.40 fixed + 1.0→0.5 schedule.
- Per-token routing recipe at N=200 with control (F10@step35k) and
  fine-tune (F11) variants.
- Cross-substrate transfer (WikiText-2) for the K.2 routing pattern.
- Honest-negative ledger: OOD, ECE, SFT, I.3 router, XSA all
  documented with data.

**3. Negative ledger honest?**
- 5 documented negatives (OOD, ECE, SFT, I.3 router, XSA) with
  explicit "did not help" framings and reasoning.

**4. Limits scoped?**
- Toy / undertrained scale (305M / 3B vs Chinchilla 6B for 305M)
- Single dominant substrate (GSM8K + small WikiText-2 transfer test)
- N=50–200 per K.2 measurement (binomial floor explicitly called out)
- α-sweep is n=1 per α (single seed each) — see "Likely reviewer
  complaints" below

## Likely reviewer complaints (and our responses)

| Complaint | Response |
|---|---|
| "α-sweep is single-seed" | Concede. Add Phase O.4 multi-seed if a reviewer requests it (~\$15 budget). |
| "Why GSM8K only?" | K.2.2 generalisation table on WikiText-2 already in §9 |
| "Toy scale results don't transfer" | Position the paper explicitly as a small-scale characterisation. Future work section flags 1B+ scaling. |
| "Why no FIM/comparison to BD3-LMs?" | BD3-LMs is block-AR + block-diff; our composite is per-step α-mix. Cite + position. |
| "Sample quality at FineWeb-Edu scale crashes" | Documented in §7 with three root causes and two decoder-side fixes. Cleanly framed as a diagnostic finding, not a model failure. |
| "Why 305M specifically?" | Chinchilla budget gate + pod-availability gate. Documented. |
| "XSA test was 60M only" | N.1 negative was anti-escalation: 60M result was \emph{worse} on K.2 NLL, so 305M XSA retrain not justified by N.1's gate. Documented. |

## Remaining blockers (none)

The paper is ready to draft a cover letter and submit. Items below
are NOT blockers, but quality-of-life improvements:

- Phase O.4 multi-seed α-sweep ($\$10$-$15$, 5h) — reviewer-armor.
- Cover letter draft (~30 min writing) — to be written after this
  readiness verdict is approved.
- Optional figures: α-sweep curve plot, K.2 percentile curve plot.

## What we do NOT claim

- That composite training is universally better than separated.
- That composite scales to 1B+ — explicitly out of scope.
- That K.2 routing transfers to non-math substrates at frontier
  quality (we have a small NLL-shape transfer test on WikiText-2,
  not a fluency contest).
- That XSA is universally bad — we tested 60M, short context, our
  recipe; the XSA paper's reported gains may be specific to their
  scale and context.

## Recommendation

Ship as TMLR. Cover letter next. Optional multi-seed if budget allows.
