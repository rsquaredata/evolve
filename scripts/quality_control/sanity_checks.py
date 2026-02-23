"""
EVOLVE – Dataset Integrity Sanity Checks

This script verifies structural consistency between images and labels for YOLO-format dataset splits (train/val/test).

Checks performed:
1. Missing label files for existing images
2. Missing image files for existing labels
3. Empty label files (no objects annotated)

This script should be executed after annotation export.
"""

import os


# ============================================================
# Configuration
# ============================================================

IMAGES_DIR = "data/processed/images"
LABELS_DIR = "data/processed/labels"

SPLITS = ["train", "val", "test"]


# ============================================================
# Sanity checks
# ============================================================

for split in SPLITS:

    img_dir = os.path.join(IMAGES_DIR, split)
    lbl_dir = os.path.join(LABELS_DIR, split)

    if not os.path.exists(img_dir) or not os.path.exists(lbl_dir):
        print(f"[WARNING] Missing directory for split: {split}")
        continue

    images = {os.path.splitext(f)[0] for f in os.listdir(img_dir)}
    labels = {os.path.splitext(f)[0] for f in os.listdir(lbl_dir)}

    missing_labels = images - labels
    missing_images = labels - images

    # Detect empty label files
    empty_labels = []

    for label_file in os.listdir(lbl_dir):
        if not label_file.endswith(".txt"):
            continue

        path = os.path.join(lbl_dir, label_file)

        if os.path.getsize(path) == 0:
            empty_labels.append(label_file)

    print("========================================")
    print(f"SPLIT: {split.upper()}")
    print("========================================")
    print(f"Total images: {len(images)}")
    print(f"Total labels: {len(labels)}")
    print("----------------------------------------")
    print(f"Missing labels: {len(missing_labels)}")
    print(f"Missing images: {len(missing_images)}")
    print(f"Empty label files: {len(empty_labels)}")
    print("========================================\n")
