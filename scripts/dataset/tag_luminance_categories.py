"""
EVOLVE – Luminance Category Tagging

This script assigns illumination categories to each frame based on its mean grayscale luminance.

Categories:
    - very_low  : mean_luminance < 50
    - low       : 50 <= mean_luminance < 125
    - medium    : mean_luminance >= 125

These categories are used for:
    - Dataset analysis
    - Stratified sampling
    - Difficulty characterization
"""

import pandas as pd


# ============================================================
# Configuration
# ============================================================

INPUT_CSV = "data/interim/luminosity_stats.csv"
OUTPUT_CSV = "data/interim/luminosity_tagged.csv"

VERY_LOW_THRESHOLD = 50
LOW_THRESHOLD = 125


# ============================================================
# Load data
# ============================================================

df = pd.read_csv(INPUT_CSV)


# ============================================================
# Categorization function
# ============================================================

def categorize_luminance(x):
    """
    Assign luminance category based on predefined thresholds.
    """
    if x < VERY_LOW_THRESHOLD:
        return "very_low"
    elif x < LOW_THRESHOLD:
        return "low"
    else:
        return "medium"


# Apply categorization
df["lum_category"] = df["mean_luminance"].apply(categorize_luminance)


# ============================================================
# Save result
# ============================================================

df.to_csv(OUTPUT_CSV, index=False)

print("Luminance tagging complete.")
print("Distribution:")
print(df["lum_category"].value_counts())