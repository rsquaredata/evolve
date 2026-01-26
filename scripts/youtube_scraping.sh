#!/bin/bash
set -e

# ================================
# EVOLVE — YouTube scraping script
# ================================

URL_FILE="data/youtube/youtube_urls.txt"
VIDEO_DIR="data/raw/youtube_videos"
FRAME_DIR="data/raw/youtube_frames"
LOG_DIR="logs"

mkdir -p "$VIDEO_DIR" "$FRAME_DIR" "$LOG_DIR"

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

echo "▶ Extracting frames (1 frame every 5 seconds)..."

for v in "$VIDEO_DIR"/*.mp4; do
  name=$(basename "$v" .mp4)
  mkdir -p "$FRAME_DIR/$name"

  ffmpeg -i "$v" -vf fps=0.2 \
    "$FRAME_DIR/$name/%04d.jpg" \
    2>> "$LOG_DIR/ffmpeg.log"
done

echo "✔ YouTube scraping completed."
