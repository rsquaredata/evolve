from pathlib import Path

IMG_DIR = Path("data/yolo/images")
LBL_DIR = Path("data/yolo/labels")

for split in ["train", "val", "test"]:
    imgs = list((IMG_DIR / split).glob("*.jpg"))
    lbls = list((LBL_DIR / split).glob("*.txt"))

    print(f"\n[{split.upper()}]")
    print(f"Images: {len(imgs)}")
    print(f"Labels: {len(lbls)}")

    missing = []
    for img in imgs:
        if not (LBL_DIR / split / (img.stem + ".txt")).exists():
            missing.append(img.name)

    if missing:
        print(f"⚠ Missing labels for {len(missing)} images")
    else:
        print("✔ All images have label files")
