"""
EVOLVE – Sample Visualization Script

This script randomly visualizes a grid of images from a given split (train / val / test) for quick qualitative inspection.

Useful for:
- Dataset sanity check
- Visual inspection before training
- Reporting examples in documentation
"""

import os
import random
import cv2
import matplotlib.pyplot as plt


# ============================================================
# Configuration
# ============================================================

SPLIT = "train"  # Change to "val" or "test" if needed
IMAGES_DIR = f"data/processed/images/{SPLIT}"

GRID_SIZE = 3
N_IMAGES = GRID_SIZE * GRID_SIZE
RANDOM_STATE = 42

random.seed(RANDOM_STATE)


# ============================================================
# Load image list
# ============================================================

if not os.path.exists(IMAGES_DIR):
    raise FileNotFoundError(f"Directory not found: {IMAGES_DIR}")

image_files = [
    f for f in os.listdir(IMAGES_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if len(image_files) == 0:
    raise ValueError("No images found in directory.")

sample_images = random.sample(
    image_files,
    min(N_IMAGES, len(image_files))
)


# ============================================================
# Visualization
# ============================================================

plt.figure(figsize=(10, 10))

for i, img_name in enumerate(sample_images):

    img_path = os.path.join(IMAGES_DIR, img_name)
    img = cv2.imread(img_path)

    if img is None:
        continue

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.subplot(GRID_SIZE, GRID_SIZE, i + 1)
    plt.imshow(img)
    plt.axis("off")

plt.suptitle(f"Random Samples from {SPLIT} Split", fontsize=14)
plt.tight_layout()
plt.show()
