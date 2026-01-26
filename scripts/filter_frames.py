import cv2
import numpy as np
from pathlib import Path
import shutil

# ==============================
# Configuration
# ==============================

INPUT_DIR = Path("data/raw/images/youtube/frames")
OUTPUT_DIR = Path("data/raw/images/youtube/pre_filtered")

MIN_BRIGHTNESS = 25      # trop sombre si < 25
MIN_SHARPNESS = 40       # variance du Laplacien (flou si < 40)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# Helper functions
# ==============================

def is_too_dark(img_gray):
    return img_gray.mean() < MIN_BRIGHTNESS

def is_too_blurry(img_gray):
    lap = cv2.Laplacian(img_gray, cv2.CV_64F).var()
    return lap < MIN_SHARPNESS

# ==============================
# Main loop
# ==============================

kept, discarded = 0, 0

for video_dir in INPUT_DIR.iterdir():
    if not video_dir.is_dir():
        continue

    out_video_dir = OUTPUT_DIR / video_dir.name
    out_video_dir.mkdir(exist_ok=True)

    for img_path in video_dir.glob("*.jpg"):
        img = cv2.imread(str(img_path))
        if img is None:
            discarded += 1
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if is_too_dark(gray) or is_too_blurry(gray):
            discarded += 1
            continue

        shutil.copy(img_path, out_video_dir / img_path.name)
        kept += 1

print("✅ Pre-filtering completed")
print(f"✔ Kept images     : {kept}")
print(f"✖ Discarded images: {discarded}")
