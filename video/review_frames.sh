#!/bin/bash
# Extract review frames at 25/50/75/100% of each rendered scene.
# Usage:
#   ./review_frames.sh                  # default 480p15, all scenes
#   ./review_frames.sh 1080p60          # specific resolution
#   ./review_frames.sh 480p15 scene04   # specific scene basename
set -e
cd "$(dirname "$0")"

QUALITY_DIR="${1:-480p15}"
ONLY="${2:-}"
MANIFEST="${MANIFEST:-scene_manifest.yml}"
OUT_DIR="${OUT_DIR:-media/frames/$QUALITY_DIR}"

mkdir -p "$OUT_DIR"

SCENES=$(awk '/^[[:space:]]*file:/ {print $2}' "$MANIFEST")
for scene in $SCENES; do
    basename=$(basename "$scene" .py)
    if [ -n "$ONLY" ] && [[ "$basename" != *"$ONLY"* ]]; then
        continue
    fi
    mp4=$(find "media/videos/$basename/$QUALITY_DIR/" -maxdepth 1 -name "*.mp4" 2>/dev/null \
        | xargs -I{} stat -f "%m %N" {} 2>/dev/null \
        | sort -rn | head -1 | awk '{print $2}')

    if [ -z "$mp4" ]; then
        echo "Skipping $basename: no $QUALITY_DIR render"
        continue
    fi

    scene_out="$OUT_DIR/$basename"
    mkdir -p "$scene_out"
    duration=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$mp4")

    for pct in 0.25 0.50 0.75 1.00; do
        ts=$(awk -v d="$duration" -v p="$pct" 'BEGIN { t=d*p; if (t>=d) t=d-0.05; if (t<0) t=0; printf "%.3f", t }')
        label=$(awk -v p="$pct" 'BEGIN { printf "%03d", p * 100 }')
        ffmpeg -y -ss "$ts" -i "$mp4" -frames:v 1 "$scene_out/frame_${label}.png" >/dev/null 2>&1
    done
    echo "Wrote review frames for $basename -> $scene_out"
done
