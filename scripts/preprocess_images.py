from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/yolo/images/all")

OUT_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (640, 640)  # YOLO native size

def preprocess_image(img_path):
    img = cv2.imread(str(img_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE, interpolation=cv2.INTER_AREA)
    return img

counter = 0

for img_path in tqdm(list(RAW_DIR.rglob("*.jpg"))):
    img = preprocess_image(img_path)
    out_path = OUT_DIR / f"img_{counter:06d}.jpg"

    cv2.imwrite(
        str(out_path),
        cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    )
    counter += 1

print(f"✔ Processed {counter} images.")
