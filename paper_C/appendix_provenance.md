# Paper C — provenance ledger

Every numerical claim in `main.pdf` traced to its source. Internal
reference; not user-facing supplementary material.

## Notation
- `git:<sha>` — file in github.com/eren23/sfumato at that commit
- `hf:<path>` — file in huggingface.co/eren23/sfumato-composite-ckpts

## §3 Data-Efficiency Curve

| Claim | Source |
|---|---|
| Composite at 500p AR-NLL −0.40 ($5.7\sigma$) | `git:e5/results/d3_perplexity_raw.json` |
| Composite at 7,473p AR-NLL +0.22 | `git:e5/results/probes_raw.json` (`f1_composite_seed*`) |
| Crossover near 1,000 problems | `git:e5/results/T0_PROBES_FINAL.md` Phase D3 table |

## §4 Compute-Matched Diffusion-Axis Win

| Claim | Source |
|---|---|
| Composite-3k vs pure-diff-6k at 200M: −0.69 NLL | `git:e5/results/perplexity_processed.json` |
| Replication at 60M / 120M / 300M | same file, `f2_*` rows |

## §5 Mode-Switching Inference

| Claim | Source |
|---|---|
| n=8 seeds, mean lift Δ | `git:e5/results/overnight_pull/evals/probe_diff_draft_ar_refill_n50.json` |

## §6 Honest Negatives (incl. Phase L SFT + Phase N.1 XSA)

| Claim | Source |
|---|---|
| OOD NLL +0.1–0.2 per scale | `git:e5/results/d4_d5_raw.json` |
| ECE table | `git:e5/results/d4_d5_raw.json` |
| Phase L SFT loss 2.84→1.0 | `git:e5/results/f10_sft_gsm8k/train.log` |
| Phase L SFT acc 0–6% | `git:e5/results/f10_sft_gsm8k/probe5_eval.json`, `probe5_greedy.json` |
| XSA A/B (60M, USE_XSA=1 vs 0) | `git:e5/results/f13_xsa_60m/composite/k2_sweep_n100.json`, `git:e5/results/f13_baseline_60m/composite/k2_sweep_n100.json` |

## §7 Sample-Quality Investigation (F9, F10)

| Claim | Source |
|---|---|
| F9 free-run 0/50 GSM8K-dev | `git:e5/results/f9_300m_coherent/composite/samples.md` |
| F10 final val_ar_nll 1.155 | `git:e5/results/f10_mixed/composite/summary.json` (also `score.json`) |
| Decoder fixes (Tier 0 + Tier 0.5) | `git:e5/scripts/probe5_mode_switch.py` (count-based rep_pen) |

## §8 Interleaved Routing (incl. I.3 router)

| Claim | Source |
|---|---|
| I.0 interleaved schedule table on F9 / F10@10k | `git:e5/results/overnight_pull/evals/probe_interleaved_*.json` |
| I.1 heuristic router table | `git:e5/results/overnight_pull/evals/probe_router_heuristic_*.json` |
| I.3 router REINFORCE: loop 0.69→0.00, acc=0 | `git:e5/results/f10_mixed/router_i3/router_v1.log.jsonl`, `router_v1.train.log` |

## §9 Phase K + K.2.1 + K.2.2

| Claim | Source |
|---|---|
| Single-round K.2 N=200, pct50=11.98 | `git:e5/results/f10_mixed/composite/k2_pct50_n200.json` |
| Iterated n_outer=2 N=100, pct50=11.86 | `git:e5/results/f10_mixed/composite/k2_iterated2_n100.json` |
| F10@step35k control pct50=11.84 | `git:e5/results/f10_mixed/composite/k2_step35k.json` |
| F11 fine-tune pct50=11.40 | `git:e5/results/f11_diff_heavy/composite_fixed_30/k2_sweep_n100.json`, `hf:f11_fine_tune/k2_sweep_n100.json` |
| F11 ar_only acc 6% | `git:e5/results/f11_diff_heavy/composite_fixed_30/probe5_eval.json` |
| F12-α20 pct50=11.25 | `git:e5/results/f12_alpha20/composite_fixed_20/k2_sweep_n100.json` |
| F12-α40 pct50=11.55 | `git:e5/results/f12_alpha40/composite_fixed_40/k2_sweep_n100.json` |
| F11+ extended pct50=11.26 | `git:e5/results/f11_extended/composite_fixed_30/k2_sweep_n100.json` |
| K.2 on WikiText-2 (generalisation) | `git:e5/results/f10_mixed/composite/k2_wikitext_n50.json` |

## Phase J (in §8 sub-section)

| Claim | Source |
|---|---|
| 5.43× parallel-decode speedup | `git:e5/results/f10_mixed/probe_speed_n20.json` |
| FIM AR-with-suffix == AR-no-suffix | `git:e5/results/f10_mixed/probe_infill_n50.json` |
| Revision NLL −0.74 / −2.20 in revise band | `git:e5/results/f10_mixed/probe_revision_nll_n50.json` |

## Model checkpoints

All slim ckpts:
- F10 final → `hf:f10_mixed/model_slim_final.pt`
- F11 final → `hf:f11_fine_tune/model_slim.pt`
- F11+ extended, F12-α20, F12-α40 → `hf:f11_extended/`, `hf:f12_alpha20/`, `hf:f12_alpha40/`
- F13-XSA, F13-baseline 60M → only intermediate `model_step*.pt` on HF; final ckpts local in `git:e5/results/f13_xsa_60m/`, `f13_baseline_60m/`
