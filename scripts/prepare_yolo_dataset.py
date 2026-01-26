#!/usr/bin/env python3
"""
EVOLVE — YOLO Dataset Preparation Script

- Splits annotated images into train / val / test
- Copies images and labels into YOLO directory structure
- Ensures image-label consistency
"""

import shutil
import random
from pathlib import Path
from tqdm import tqdm

# =========================
# Configuration
# =========================

RANDOM_SEED = 42

SPLIT_RATIO = {
    "train": 0.7,
    "val": 0.2,
    "test": 0.1,
}

SRC_IMAGES = Path("data/annotations/yolo/images")
SRC_LABELS = Path("data/annotations/yolo/labels")

DST_ROOT = Path("data/yolo")
DST_IMAGES = DST_ROOT / "images"
DST_LABELS = DST_ROOT / "labels"

# =========================
# Utilities
# =========================

def ensure_dirs():
    for split in SPLIT_RATIO:
        (DST_IMAGES / split).mkdir(parents=True, exist_ok=True)
        (DST_LABELS / split).mkdir(parents=True, exist_ok=True)


def get_valid_pairs():
    images = list(SRC_IMAGES.glob("*.jpg"))
    pairs = []

    for img in images:
        label = SRC_LABELS / f"{img.stem}.txt"
        if label.exists():
            pairs.append((img, label))

    return pairs


def split_dataset(pairs):
    random.seed(RANDOM_SEED)
    random.shuffle(pairs)

    n = len(pairs)
    n_train = int(n * SPLIT_RATIO["train"])
    n_val = int(n * SPLIT_RATIO["val"])

    train = pairs[:n_train]
    val = pairs[n_train:n_train + n_val]
    test = pairs[n_train + n_val:]

    return {
        "train": train,
        "val": val,
        "test": test,
    }


def copy_split(split_name, pairs):
    for img, label in tqdm(pairs, desc=f"Copying {split_name}"):
        shutil.copy(img, DST_IMAGES / split_name / img.name)
        shutil.copy(label, DST_LABELS / split_name / label.name)


# =========================
# Main
# =========================

def main():
    print("▶ Preparing YOLO dataset")

    ensure_dirs()

    pairs = get_valid_pairs()
    print(f"✔ Found {len(pairs)} valid image-label pairs")

    if len(pairs) == 0:
        raise RuntimeError("No valid image-label pairs found.")

    splits = split_dataset(pairs)

    for split_name, split_pairs in splits.items():
        print(f"▶ {split_name}: {len(split_pairs)} samples")
        copy_split(split_name, split_pairs)

    print("✔ YOLO dataset preparation completed successfully")


if __name__ == "__main__":
    main()
