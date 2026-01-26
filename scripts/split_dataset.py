from pathlib import Path
import random
import shutil

random.seed(42)

IMG_DIR = Path("data/yolo/images/all")
LBL_DIR = Path("data/yolo/labels/all")

OUT_IMG = Path("data/yolo/images")
OUT_LBL = Path("data/yolo/labels")

splits = {
    "train": 0.7,
    "val": 0.2,
    "test": 0.1
}

images = list(IMG_DIR.glob("*.jpg"))
random.shuffle(images)

n = len(images)
train_end = int(splits["train"] * n)
val_end = train_end + int(splits["val"] * n)

split_map = {
    "train": images[:train_end],
    "val": images[train_end:val_end],
    "test": images[val_end:]
}

for split, imgs in split_map.items():
    (OUT_IMG / split).mkdir(parents=True, exist_ok=True)
    (OUT_LBL / split).mkdir(parents=True, exist_ok=True)

    for img_path in imgs:
        label_path = LBL_DIR / (img_path.stem + ".txt")

        shutil.copy(img_path, OUT_IMG / split / img_path.name)

        if label_path.exists():
            shutil.copy(label_path, OUT_LBL / split / label_path.name)
        else:
            # empty label file (allowed in YOLO)
            open(OUT_LBL / split / (img_path.stem + ".txt"), "w").close()

print("✔ Dataset split completed.")
