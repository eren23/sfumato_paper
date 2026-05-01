# Sfumato Paper 1 — Video Companion

Silent Manim companion to the paper. ~5-6 minutes at 1080p60, 11 scenes.

## Render

```bash
cd video
./render_story.sh -ql        # quick low-quality preview (480p15)
./render_story.sh -qh        # final 1080p60 render
```

Each scene is rendered separately and concatenated with ffmpeg. Output:
`final_story_480p15.mp4` or `final_story_1080p60.mp4`.

## Review individual scenes

After rendering, extract frames at 25/50/75/100% of every scene to scan for
text-overlap, clipping, or off-screen content:

```bash
./review_frames.sh 480p15            # all scenes
./review_frames.sh 480p15 scene05    # just scene05
```

Frames land in `media/frames/<resolution>/<scene>/frame_*.png`.

## Text non-overlap discipline

The hard rule for this video is: **no two text mobjects on screen at the same
time may overlap.** See `storyboard.md` for the full rule list. The summary:

1. Always position text via `.move_to()` or `.next_to()` *before* `self.add()`
   or `self.play()`.
2. At most 1 title + 1 body block on screen at once. Multi-row content uses
   `comparison_table()` or `VGroup.arrange(DOWN, buff=0.35)`.
3. `fade_out_all(self)` between sub-sections.
4. Always run `./review_frames.sh` after rendering and visually scan.
5. No font smaller than size 16.
6. Every new scene calls `assert_no_overlap(...)` from `utils.layout` once
   per phase as a defensive check at construction time.
