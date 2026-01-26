from pathlib import Path

IMG_DIR = Path("data/yolo/images")
LBL_DIR = Path("data/yolo/labels")

for split in ["train", "val", "test"]:
    img_dir = IMG_DIR / split
    lbl_dir = LBL_DIR / split

    imgs = list(img_dir.glob("*.jpg"))
    lbls = list(lbl_dir.glob("*.txt"))

    print(f"\n[{split.upper()}]")
    print(f"Images: {len(imgs)}")
    print(f"Labels: {len(lbls)}")

    # Image without label
    missing_labels = [
        img.name for img in imgs
        if not (lbl_dir / f"{img.stem}.txt").exists()
    ]

    # Label without image
    orphan_labels = [
        lbl.name for lbl in lbls
        if not (img_dir / f"{lbl.stem}.jpg").exists()
    ]

    # Empty label files
    empty_labels = [
        lbl.name for lbl in lbls
        if lbl.read_text().strip() == ""
    ]

    if missing_labels:
        print(f"⚠ Images without labels: {len(missing_labels)}")
    else:
        print("✔ All images have label files")

    if orphan_labels:
        print(f"⚠ Labels without images: {len(orphan_labels)}")

    if empty_labels:
        print(f"⚠ Empty label files: {len(empty_labels)}")
