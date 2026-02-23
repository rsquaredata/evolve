"""
EVOLVE – Near-Duplicate Frame Detection

This script computes a simple perceptual hash for each image in order to detect visually similar (near-duplicate) frames.

Purpose:
- Identify redundant frames extracted from videos
- Reduce dataset redundancy
- Improve annotation efficiency

Current method:
- Resize image to 32x32
- Convert to grayscale
- Compute perceptual hash using mean thresholding
"""

import os
import cv2
import numpy as np
from tqdm import tqdm


# ============================================================
# Configuration
# ============================================================

FRAMES_DIR = "data/interim/frames/youtube"
HASH_SIZE = 32


# ============================================================
# Perceptual hash function (average hash - aHash)
# ============================================================

def compute_ahash(image):
    """
    Compute a simple average hash (aHash).

    Steps:
    - Resize image to HASH_SIZE x HASH_SIZE
    - Convert to grayscale
    - Compute mean pixel value
    - Create binary hash based on threshold

    Returns:
        np.ndarray: Flattened binary hash vector
    """

    resized = cv2.resize(image, (HASH_SIZE, HASH_SIZE))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    mean_val = np.mean(gray)
    binary_hash = (gray > mean_val).astype(np.uint8)

    return binary_hash.flatten()


# ============================================================
# Compute hashes
# ============================================================

hashes = {}

for root, _, files in os.walk(FRAMES_DIR):
    for file in tqdm(files):

        if not file.lower().endswith(".jpg"):
            continue

        path = os.path.join(root, file)
        img = cv2.imread(path)

        if img is None:
            continue

        h = compute_ahash(img)
        hashes[path] = h

print("Hash computation complete.")
print(f"Total images processed: {len(hashes)}")