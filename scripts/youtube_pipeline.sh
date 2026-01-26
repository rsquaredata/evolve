#!/bin/bash
set -e

# ==================================================
# EVOLVE — YouTube data collection pipeline
# ==================================================
# - Downloads publicly available YouTube videos
# - Extracts frames at a fixed temporal rate
# - Intended for academic, non-commercial use only
# ==================================================

URL_FILE="data/raw/images/youtube/youtube_urls.txt"
VIDEO_DIR="data/raw/images/youtube/videos"
FRAME_DIR="data/raw/images/youtube/frames"
LOG_DIR="logs"

# --------------------------------------------------
# Sanity checks
# --------------------------------------------------

if [ ! -f "$URL_FILE" ]; then
  echo "❌ URL file not found: $URL_FILE"
  exit 1
fi

mkdir -p "$VIDEO_DIR" "$FRAME_DIR" "$LOG_DIR"

# --------------------------------------------------
# Download videos
# --------------------------------------------------

echo "▶ Downloading YouTube videos..."

yt-dlp \
  -f "bv*[height<=1080]" \
  -o "$VIDEO_DIR/%(uploader)s_%(id)s.%(ext)s" \
  -a "$URL_FILE" \
  --no-playlist \
  --restrict-filenames \
  --merge-output-format mp4 \
  --write-info-json \
  | tee "$LOG_DIR/ytdlp.log"

# --------------------------------------------------
# Extract frames
# --------------------------------------------------

echo "▶ Extracting frames (1 frame every 5 seconds)..."

shopt -s nullglob
for v in "$VIDEO_DIR"/*.mp4 "$VIDEO_DIR"/*.webm; do
  name=$(basename "$v" .mp4)
  mkdir -p "$FRAME_DIR/$name"

  ffmpeg -i "$v" -vf fps=1 \
    "$FRAME_DIR/$name/%04d.jpg" \
    2>> "$LOG_DIR/ffmpeg.log"
done
shopt -u nullglob

echo "✔ YouTube data collection pipeline completed."
