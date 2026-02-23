"""
EVOLVE – Copy Selected Annotation Pool

This script copies the 700 selected images from their original locations to a dedicated annotation directory.

The operation is reproducible and safe.
"""

import os
import shutil
import pandas as pd

INPUT_CSV = "data/interim/selected_700.csv"
DEST_DIR = "data/processed/annotation_pool_700"

# Create destination directory if it does not exist
os.makedirs(DEST_DIR, exist_ok=True)

df = pd.read_csv(INPUT_CSV)

print("Copying", len(df), "images...")

for _, row in df.iterrows():
    src = row["full_path"]
    dst = os.path.join(DEST_DIR, row["filename"])

    if not os.path.exists(dst):  # Avoid duplicate copy
        shutil.copy(src, dst)

print("Copy complete.")
print("Destination:", DEST_DIR)