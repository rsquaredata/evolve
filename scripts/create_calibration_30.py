"""
EVOLVE – Calibration Subset Creation

This script creates a balanced calibration subset of 30 images from the previously selected 700-image annotation pool.

The subset contains:
    - 10 very_low luminance images
    - 10 low luminance images
    - 10 medium luminance images

This calibration set is used to:
    - Align annotation guidelines between annotators
    - Reduce inter-annotator disagreement
    - Validate bounding box consistency

The process is reproducible via a fixed random seed.
"""

import pandas as pd

# ============================================================
# Configuration
# ============================================================

INPUT_PATH = "data/interim/selected_700.csv"
OUTPUT_PATH = "data/interim/calibration_30.csv"

N_PER_CATEGORY = 10
RANDOM_STATE = 42  # Ensures reproducibility

# ============================================================
# Load selected dataset
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("Loaded dataset:", len(df), "images")

# ============================================================
# Stratified sampling by luminance category
# ============================================================

calibration_subsets = []

for category in ["very_low", "low", "medium"]:
    subset = df[df["lum_category"] == category].sample(
        n=N_PER_CATEGORY,
        random_state=RANDOM_STATE
    )
    calibration_subsets.append(subset)

# Concatenate selected subsets
calibration_df = pd.concat(calibration_subsets).reset_index(drop=True)

# ============================================================
# Save calibration subset
# ============================================================

calibration_df.to_csv(OUTPUT_PATH, index=False)

# ============================================================
# Summary output
# ============================================================

print("Calibration set created.")
print("Total images:", len(calibration_df))
print("Luminance distribution:")
print(calibration_df["lum_category"].value_counts())
print("Unique videos represented:",
      calibration_df["video_name"].nunique())
print("Saved to:", OUTPUT_PATH)