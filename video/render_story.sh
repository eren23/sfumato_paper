#!/bin/bash
set -e
cd "$(dirname "$0")"

PYTHON="${PYTHON:-/usr/bin/python3}"
QUALITY="${1:--ql}"
MANIFEST="${MANIFEST:-scene_manifest.yml}"

case "$QUALITY" in
    -ql) RES_DIR="480p15" ;;
    -qm) RES_DIR="720p30" ;;
    -qh) RES_DIR="1080p60" ;;
    *)   RES_DIR="480p15" ;;
esac

SCENES=$(awk '/^[[:space:]]*file:/ {print $2}' "$MANIFEST")
CONCAT_FILE="concat_story_${RES_DIR}.txt"
> "$CONCAT_FILE"

echo "Rendering Sfumato paper video at quality: $QUALITY"
for scene in $SCENES; do
    echo "Rendering $scene"
    "$PYTHON" -m manim render "$scene" "$QUALITY" --format mp4

    basename=$(basename "$scene" .py)
    found=$(find "media/videos/$basename/$RES_DIR/" -maxdepth 1 -name "*.mp4" 2>/dev/null \
        | xargs -I{} stat -f "%m %N" {} 2>/dev/null \
        | sort -rn | head -1 | awk '{print $2}')
    if [ -z "$found" ]; then
        echo "Missing render output for $scene"
        exit 1
    fi
    echo "file '$found'" >> "$CONCAT_FILE"
done

ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c copy "final_story_${RES_DIR}.mp4"
echo "Done: final_story_${RES_DIR}.mp4"
