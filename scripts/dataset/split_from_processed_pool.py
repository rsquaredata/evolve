"""
EVOLVE — Video-level train/val/test split from a flat annotated pool.

Input (flat):
  data/processed/images/   -> 700 images (jpg/png)
  data/processed/labels/   -> 700 YOLO txt files (same stem)

Output:
  data/processed/images/{train,val,test}/
  data/processed/labels/{train,val,test}/

Key principles:
- Split at "video_id" level to reduce leakage (all frames from same video in same split)
- Reproducible via fixed seed
- Moves or copies BOTH image and label
- Saves splits to metadata/splits_v*.json

Assumption about filenames:
- Most files look like: "...-VIDEOID_frame_0123.jpg"
  -> video_id extracted as the token after the last "-" and before "_frame_"
If pattern not found, fallback to prefix before "_frame_".
"""

import os
import re
import json
import random
import shutil
from pathlib import Path


# =========================
# Configuration
# =========================
RANDOM_STATE = 42
SPLIT_RATIOS = {"train": 0.7, "val": 0.15, "test": 0.15}

IMAGES_DIR = Path("data/processed/images")
LABELS_DIR = Path("data/processed/labels")

OUTPUT_IMAGES = Path("data/processed/images")
OUTPUT_LABELS = Path("data/processed/labels")

SPLIT_LOG_DIR = Path("metadata")
SPLIT_LOG_PATH = SPLIT_LOG_DIR / "splits_v1.json"

# If True: move files into split folders (cleaner, avoids duplicates)
# If False: copy files (safer if you want to keep original flat pool)
MOVE_FILES = True

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


# =========================
# Helpers
# =========================
def is_split_dir(p: Path) -> bool:
    return p.name in ("train", "val", "test") and p.is_dir()

def list_pool_images(images_dir: Path):
    files = []
    for p in images_dir.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            files.append(p)
    return sorted(files)

def extract_video_id(filename: str) -> str:
    """
    Try to extract video_id for grouping:
    1) pattern: "-<videoid>_frame_" (common in your names)
    2) fallback: everything before "_frame_"
    3) fallback: stem itself
    """
    # Example: "...-TfdpwD3Y3J4_frame_0001.jpg" -> "TfdpwD3Y3J4"
    m = re.search(r"-([A-Za-z0-9_]+)_frame_", filename)
    if m:
        return m.group(1)

    if "_frame_" in filename:
        return filename.split("_frame_")[0]

    return Path(filename).stem

def split_list(items, ratios, seed):
    rnd = random.Random(seed)
    items = list(items)
    rnd.shuffle(items)

    n = len(items)
    n_train = int(n * ratios["train"])
    n_val = int(n * ratios["val"])
    train_items = items[:n_train]
    val_items = items[n_train:n_train + n_val]
    test_items = items[n_train + n_val:]
    return {"train": train_items, "val": val_items, "test": test_items}

def ensure_dirs():
    for split in ("train", "val", "test"):
        (OUTPUT_IMAGES / split).mkdir(parents=True, exist_ok=True)
        (OUTPUT_LABELS / split).mkdir(parents=True, exist_ok=True)
    SPLIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

def transfer(src: Path, dst: Path, move: bool):
    if move:
        shutil.move(str(src), str(dst))
    else:
        shutil.copy2(str(src), str(dst))


# =========================
# Main
# =========================
def main():
    # Safety: if split dirs already exist and contain files, warn early
    for split in ("train", "val", "test"):
        img_split_dir = OUTPUT_IMAGES / split
        if img_split_dir.exists() and any(img_split_dir.iterdir()):
            raise RuntimeError(
                f"Split folder not empty: {img_split_dir}. "
                "Clean it or set MOVE_FILES=False with different output."
            )
        lbl_split_dir = OUTPUT_LABELS / split
        if lbl_split_dir.exists() and any(lbl_split_dir.iterdir()):
            raise RuntimeError(
                f"Split folder not empty: {lbl_split_dir}. "
                "Clean it or set MOVE_FILES=False with different output."
            )

    # Pool images are only those at the root of images_dir (not already split)
    pool_images = list_pool_images(IMAGES_DIR)

    if len(pool_images) == 0:
        raise RuntimeError(
            "No images found in data/processed/images/. "
            "Make sure the 700 images are directly inside that folder (flat)."
        )

    # Build mapping video_id -> list of image paths
    video_to_images = {}
    missing_labels = []

    for img_path in pool_images:
        video_id = extract_video_id(img_path.name)
        video_to_images.setdefault(video_id, []).append(img_path)

        # Check corresponding label exists
        label_path = LABELS_DIR / (img_path.stem + ".txt")
        if not label_path.exists():
            missing_labels.append(img_path.name)

    if missing_labels:
        print("WARNING: Some images have no matching .txt label:")
        print("\n".join(missing_labels[:20]))
        print(f"... total missing labels: {len(missing_labels)}")
        raise RuntimeError("Fix missing labels before splitting.")

    all_video_ids = sorted(video_to_images.keys())
    print(f"Total images in pool: {len(pool_images)}")
    print(f"Total video groups: {len(all_video_ids)}")

    splits = split_list(all_video_ids, SPLIT_RATIOS, RANDOM_STATE)

    ensure_dirs()

    # Move/copy grouped images+labels
    moved_counts = {s: 0 for s in ("train", "val", "test")}
    for split_name, video_ids in splits.items():
        for vid in video_ids:
            for img_path in video_to_images[vid]:
                dst_img = OUTPUT_IMAGES / split_name / img_path.name
                transfer(img_path, dst_img, MOVE_FILES)

                src_lbl = LABELS_DIR / (img_path.stem + ".txt")
                dst_lbl = OUTPUT_LABELS / split_name / (img_path.stem + ".txt")
                transfer(src_lbl, dst_lbl, MOVE_FILES)

                moved_counts[split_name] += 1

    # Save split mapping
    split_payload = {
        "random_state": RANDOM_STATE,
        "ratios": SPLIT_RATIOS,
        "move_files": MOVE_FILES,
        "video_id_rule": "regex -<videoid>_frame_ else prefix before _frame_",
        "n_images": len(pool_images),
        "n_videos": len(all_video_ids),
        "splits": splits,
        "images_per_split": moved_counts,
    }

    with open(SPLIT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(split_payload, f, indent=2)

    print("Split complete.")
    for split in ("train", "val", "test"):
        print(f"{split}: {moved_counts[split]} images")
    print(f"Saved: {SPLIT_LOG_PATH}")


if __name__ == "__main__":
    main()
