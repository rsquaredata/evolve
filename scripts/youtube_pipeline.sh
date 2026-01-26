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
# Dependency checks
# --------------------------------------------------

check_command () {
  command -v "$1" >/dev/null 2>&1
}

OS="$(uname -s)"

missing=0

if ! check_command yt-dlp; then
  echo "❌ yt-dlp is not installed."
  missing=1
fi

if ! check_command ffmpeg; then
  echo "❌ ffmpeg is not installed."
  missing=1
fi

if [ "$missing" -eq 1 ]; then
  echo ""
  echo "📦 Missing dependencies detected."
  echo "Please install them using the appropriate command:"
  echo ""

  case "$OS" in
    Darwin)
      echo "macOS (Homebrew):"
      echo "  brew install yt-dlp ffmpeg"
      ;;
    Linux)
      echo "Linux (APT):"
      echo "  sudo apt update && sudo apt install -y yt-dlp ffmpeg"
      ;;
    MINGW*|MSYS*|CYGWIN*)
      echo "Windows:"
      echo "  Option 1 (recommended): Use WSL"
      echo "    https://learn.microsoft.com/windows/wsl/"
      echo "  Option 2: Install binaries manually"
      echo "    yt-dlp:  https://github.com/yt-dlp/yt-dlp#installation"
      echo "    ffmpeg:  https://ffmpeg.org/download.html"
      ;;
    *)
      echo "Unknown OS. Please install yt-dlp and ffmpeg manually."
      ;;
  esac

  echo ""
  echo "🚫 Aborting pipeline."
  exit 1
fi

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

  ffmpeg -i "$v" -vf fps=0.2 \
    "$FRAME_DIR/$name/%04d.jpg" \
    2>> "$LOG_DIR/ffmpeg.log"
done
shopt -u nullglob

echo "✔ YouTube data collection pipeline completed."
