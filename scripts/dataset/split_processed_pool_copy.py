"""
EVOLVE - Video-level train/val/test split (COPY) from a flat annotated pool.

Input (flat):
  data/processed/images/   -> 700 images
  data/processed/labels/   -> 700 YOLO txt (same stem)

Output (copy):
  data/processed/yolo/
    images/{train,val,test}/
    labels/{train,val,test}/

Split is done at video_id level (all frames from same video in same split)
to reduce leakage. A split log is saved in metadata/splits_v1.json.

Filename rule:
- Prefer pattern "-<videoid>_frame_" (e.g. ...-TfdpwD3Y3J4_frame_0001.jpg)
- Else fallback to prefix before "_frame_"
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

POOL_IMAGES_DIR = Path("data/processed/images")
POOL_LABELS_DIR = Path("data/processed/labels")

OUT_BASE = Path("data/processed/yolo")
OUT_IMAGES = OUT_BASE / "images"
OUT_LABELS = OUT_BASE / "labels"

SPLIT_LOG_PATH = Path("metadata") / "splits_v1.json"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


# =========================
# Helpers
# =========================
def list_pool_images(images_dir: Path):
    files = []
    for p in images_dir.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            files.append(p)
    return sorted(files)

def extract_video_id(filename: str) -> str:
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

    return {
        "train": items[:n_train],
        "val": items[n_train:n_train + n_val],
        "test": items[n_train + n_val:],
    }

def ensure_dirs():
    for split in ("train", "val", "test"):
        (OUT_IMAGES / split).mkdir(parents=True, exist_ok=True)
        (OUT_LABELS / split).mkdir(parents=True, exist_ok=True)
    Path("metadata").mkdir(parents=True, exist_ok=True)

def copy_file(src: Path, dst: Path):
    shutil.copy2(str(src), str(dst))


# =========================
# Main
# =========================
def main():
    pool_images = list_pool_images(POOL_IMAGES_DIR)
    if len(pool_images) == 0:
        raise RuntimeError(
            "No images found in data/processed/images/. "
            "Make sure the 700 images are directly inside this folder (flat)."
        )

    # Check labels exist and group by video_id
    video_to_images = {}
    missing_labels = []

    for img_path in pool_images:
        lbl_path = POOL_LABELS_DIR / (img_path.stem + ".txt")
        if not lbl_path.exists():
            missing_labels.append(img_path.name)

        vid = extract_video_id(img_path.name)
        video_to_images.setdefault(vid, []).append(img_path)

    if missing_labels:
        print("ERROR: Missing labels for some images (showing up to 20):")
        for x in missing_labels[:20]:
            print(" -", x)
        raise RuntimeError(f"Missing labels: {len(missing_labels)}. Fix before splitting.")

    all_video_ids = sorted(video_to_images.keys())

    print(f"Pool images: {len(pool_images)}")
    print(f"Video groups: {len(all_video_ids)}")

    splits = split_list(all_video_ids, SPLIT_RATIOS, RANDOM_STATE)

    ensure_dirs()

    counts = {"train": 0, "val": 0, "test": 0}

    for split_name, vids in splits.items():
        for vid in vids:
            for img_path in video_to_images[vid]:
                # copy image
                dst_img = OUT_IMAGES / split_name / img_path.name
                copy_file(img_path, dst_img)

                # copy label
                src_lbl = POOL_LABELS_DIR / (img_path.stem + ".txt")
                dst_lbl = OUT_LABELS / split_name / (img_path.stem + ".txt")
                copy_file(src_lbl, dst_lbl)

                counts[split_name] += 1

    payload = {
        "random_state": RANDOM_STATE,
        "ratios": SPLIT_RATIOS,
        "mode": "copy",
        "video_id_rule": "regex -<videoid>_frame_ else prefix before _frame_",
        "n_images": len(pool_images),
        "n_videos": len(all_video_ids),
        "images_per_split": counts,
        "splits": splits,
    }

    with open(SPLIT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("Split complete:")
    for s in ("train", "val", "test"):
        print(f"  {s}: {counts[s]} images")
    print(f"Saved split log: {SPLIT_LOG_PATH}")
    print(f"Output dataset: {OUT_BASE}")


if __name__ == "__main__":
    main()
