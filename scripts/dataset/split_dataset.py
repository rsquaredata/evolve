"""
EVOLVE – Video-Level Train/Val/Test Split Script

This script performs a video-level split of the dataset to avoid data leakage between training and evaluation sets.

Key principles:
- Splitting is performed at video level (not frame level).
- All frames from a given video belong to the same split.
- Reproducibility ensured via fixed random seed.

Output structure:
    data/processed/images/
        ├── train/
        ├── val/
        └── test/
"""

import os
import random
import shutil


# ============================================================
# Configuration
# ============================================================

RANDOM_STATE = 42
random.seed(RANDOM_STATE)

FRAMES_DIR = "data/interim/frames"
OUTPUT_IMAGES = "data/processed/images"

SOURCES = ["youtube", "personal"]

SPLIT_RATIOS = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15
}


# ============================================================
# Helper function
# ============================================================

def split_videos(video_list):
    """
    Splits a list of videos into train/val/test subsets.

    Args:
        video_list (list): List of video identifiers.

    Returns:
        dict: Mapping split name -> list of videos.
    """
    random.shuffle(video_list)
    n = len(video_list)

    train_end = int(n * SPLIT_RATIOS["train"])
    val_end = train_end + int(n * SPLIT_RATIOS["val"])

    return {
        "train": video_list[:train_end],
        "val": video_list[train_end:val_end],
        "test": video_list[val_end:]
    }


# ============================================================
# Collect videos
# ============================================================

all_videos = []

for source in SOURCES:
    source_path = os.path.join(FRAMES_DIR, source)

    if not os.path.exists(source_path):
        continue

    videos = [
        os.path.join(source, v)
        for v in os.listdir(source_path)
        if os.path.isdir(os.path.join(source_path, v))
    ]

    all_videos.extend(videos)

print(f"Total videos found: {len(all_videos)}")


# ============================================================
# Perform split
# ============================================================

splits = split_videos(all_videos)

for split_name, video_subset in splits.items():
    os.makedirs(os.path.join(OUTPUT_IMAGES, split_name), exist_ok=True)

    for video in video_subset:
        source, video_name = video.split(os.sep)
        video_path = os.path.join(FRAMES_DIR, source, video_name)

        for img in os.listdir(video_path):
            src = os.path.join(video_path, img)

            # Rename to avoid filename collisions across videos
            new_name = f"{video_name}_{img}"
            dst = os.path.join(OUTPUT_IMAGES, split_name, new_name)

            shutil.copy(src, dst)


# ============================================================
# Summary
# ============================================================

for split in ["train", "val", "test"]:
    split_path = os.path.join(OUTPUT_IMAGES, split)
    n_images = len(os.listdir(split_path))
    print(f"{split}: {n_images} images")

print("Video-level split complete.")