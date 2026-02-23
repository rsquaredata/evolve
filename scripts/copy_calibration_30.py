"""
EVOLVE – Copy Calibration Images

This script copies the 30 calibration images from their original locations to a dedicated calibration directory.

Purpose:
    - Freeze the calibration subset
    - Prepare a clean upload folder for CVAT
    - Ensure reproducibility of the annotation setup

The operation is idempotent:
    Existing files are not duplicated.
"""

import os
import shutil
import pandas as pd

# ============================================================
# Configuration
# ============================================================

INPUT_CSV = "data/interim/calibration_30.csv"
DEST_DIR = "data/processed/calibration_30"

# ============================================================
# Load calibration metadata
# ============================================================

df = pd.read_csv(INPUT_CSV)

print("Loaded calibration subset:", len(df), "images")

# ============================================================
# Create destination directory
# ============================================================

os.makedirs(DEST_DIR, exist_ok=True)

print("Destination directory ready:", DEST_DIR)

# ============================================================
# Copy images
# ============================================================

copied_count = 0

for _, row in df.iterrows():
    src = row["full_path"]
    dst = os.path.join(DEST_DIR, row["filename"])

    # Avoid overwriting if script is run multiple times
    if not os.path.exists(dst):
        shutil.copy(src, dst)
        copied_count += 1

# ============================================================
# Final summary
# ============================================================

print("Copy complete.")
print("Newly copied files:", copied_count)
print("Total files expected:", len(df))
print("Calibration folder ready for CVAT upload.")