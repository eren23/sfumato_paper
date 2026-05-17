# Paper C — video

Companion video for `paper_C/` (composite AR + discrete-diffusion
training at toy scale). Silent, ~8m30s, 1080p60, sixteen Manim scenes.

See `storyboard.md` for the full scene-by-scene script + claim
discipline.

## Status

- [x] Storyboard
- [ ] Scene 0 — title card
- [ ] Scene 1 — composite arch diagram
- [ ] Scene 2 — toy-scale envelope
- [ ] Scene 3 — symmetric trade-off bars (F3 + E3b)
- [ ] Scene 4 — data-efficiency crossover (E3c)
- [ ] Scene 5 — honest negatives (OOD + ECE)
- [ ] Scene 6 — mode-switch lift (E3a)
- [ ] Scene 7 — F-series montage
- [ ] Scene 8 — the F9 loop shock
- [ ] Scene 9 — teacher-forced vs free-run NLL gap
- [ ] Scene 10 — three independent root causes
- [ ] Scene 11 — Tier 0 AR-side fix
- [ ] Scene 12 — set-based vs count-based rep_pen (animation)
- [ ] Scene 13 — Tier 0.5 results bar chart
- [ ] Scene 14 — before/after sample text
- [ ] Scene 15 — F10 in flight + close

## Layout

```
paper_C/video/
├── README.md            # this file
├── storyboard.md        # scene-by-scene script
├── scenes/              # one .py per scene
│   ├── scene00_title.py
│   ├── scene01_arch.py
│   └── ...
├── media/               # figures / images referenced by scenes
│   └── figures/         # generated from e5/scripts/loop_rate.py etc.
└── manim.cfg            # to be created when first scene compiles
```

## Reuse

The existing `paper_C/../video/` (paper-1) Manim scaffold:
- `utils/theme_shim.py` — color constants, body/title text helpers
- `utils/layout.py` — `assert_no_overlap` and friends
- `render_story.sh` — orchestrates all scenes into one concat-video

Copy / symlink as needed when first scene is implemented.

## Build prerequisites for figures

Scene 13 needs `media/figures/loop_rate_bar.pdf`. Generate from the
F9 probe5 JSONs:

```
python3 -c "
import json
P = '../../../../sfumato/e5/results/f9_300m_coherent'
greedy = {'ar_only': 1.0, 'mode_switch_96_32': 1.0,
          'mode_switch_64_32': 1.0, 'paired_64_64': 1.0}
tier0 = json.load(open(P + '/probe5_tier0_n50.json'))
tier05 = json.load(open(P + '/probe5_tier05count_n50.json'))
# emit pgfplots data ...
"
```

(Or generate the PDF via matplotlib; the storyboard does not constrain
the figure backend.)
