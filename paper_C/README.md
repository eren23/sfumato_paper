# Paper C — Composite AR + Discrete-Diffusion Training at Toy Scale

Third paper in the Sfumato program. Draft state: workshop-grade
skeleton awaiting E3a/E3b/E3c experimental results.

## Status

- Skeleton: complete (this directory).
- E3a (`probe-5 n=8`): pending GPU run.
- E3b (multi-scale D2): pending GPU run.
- E3c (D3 crossover localisation): pending GPU run.
- Once E3 lands, replace the `[TODO]` placeholders in
  `sections/results_curve.tex`, `results_compute_control.tex`, and
  `results_modeswitch.tex`.

## Decision rule

After E3 results land:

| E3a (n=8 mode-switch) | E3b (multi-scale control) | E3c (crossover) | Class |
|---|---|---|---|
| ≥+3pp SEM ≤1pp | Composite wins at all 3 scales | Localised | TMLR |
| ≥+2pp | Composite wins at 2/3 scales | Consistent | Strong workshop / TMLR with caveats |
| ≤+1pp | Mixed | Noisy | Workshop |

## Build

```
cd paper_C
make
```

(Requires `pdflatex`, `bibtex`, `natbib`.)

## Source data

All numerical results are derived from
`/Users/eren/Documents/ai/sfumato/e5/results/`. The canonical summary
document is `T0_PROBES_FINAL.md`. Paper-C draws from:

- `T0_PROBES_FINAL.md` for the headline numbers
- `d3_perplexity_raw.json` + `probe6_perplexity_raw.json` for the data
  curve
- `probes_raw.json` for compute-matched / FIM / position-strat
- `d4_d5_raw.json` for OOD and ECE
- `e3a_probe5_n8/summary.json` (forthcoming) for mode-switching $n=8$
- `e3b_multiscale_d2/summary.json` (forthcoming) for multi-scale control
- `e3c_d3_crossover/summary.json` (forthcoming) for crossover refinement
