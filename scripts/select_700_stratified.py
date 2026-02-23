"""
EVOLVE – Stratified and Balanced Selection Script

This script:
1. Stratifies images according to luminance category.
2. Applies a hard cap per video to avoid over-representation.
3. Iteratively refills until reaching TARGET_TOTAL without breaking the cap.
4. Saves a reproducible and balanced selection for annotation.
"""

import pandas as pd

# ============================================================
# Configuration
# ============================================================

INPUT_CSV = "data/interim/luminosity_tagged.csv"
OUTPUT_CSV = "data/interim/selected_700.csv"

TARGET_TOTAL = 700
MAX_PER_VIDEO = 40
RANDOM_STATE = 42

# ============================================================
# Load dataset
# ============================================================

df = pd.read_csv(INPUT_CSV)

print("Total available images:", len(df))
print("Initial luminance distribution:")
print(df["lum_category"].value_counts())
print("-" * 50)

# ============================================================
# Step 1 – Stratified sampling by luminance
# ============================================================

distribution = df["lum_category"].value_counts(normalize=True)

selected = []

for category, ratio in distribution.items():
    n_samples = int(TARGET_TOTAL * ratio)
    subset = df[df["lum_category"] == category].sample(
        n=n_samples,
        random_state=RANDOM_STATE
    )
    selected.append(subset)

final_df = pd.concat(selected).reset_index(drop=True)

print("After luminance stratification:", len(final_df))
print(final_df["lum_category"].value_counts())
print("-" * 50)

# ============================================================
# Step 2 – Apply hard cap per video
# ============================================================

balanced_groups = []

for video_name, group in final_df.groupby("video_name"):
    if len(group) > MAX_PER_VIDEO:
        balanced_groups.append(
            group.sample(n=MAX_PER_VIDEO, random_state=RANDOM_STATE)
        )
    else:
        balanced_groups.append(group)

final_df = pd.concat(balanced_groups).reset_index(drop=True)

print("After video cap:")
print("Total images:", len(final_df))
print("Max images per video:",
      final_df.groupby("video_name").size().max())
print("-" * 50)

# ============================================================
# Step 3 – Iterative refill while respecting video cap
# ============================================================

if len(final_df) < TARGET_TOTAL:

    remaining_pool = df[~df["full_path"].isin(final_df["full_path"])].copy()

    while len(final_df) < TARGET_TOTAL and len(remaining_pool) > 0:

        video_counts = final_df["video_name"].value_counts()

        allowed_videos = video_counts[video_counts < MAX_PER_VIDEO].index

        candidates = remaining_pool[
            remaining_pool["video_name"].isin(allowed_videos)
        ]

        if len(candidates) == 0:
            break

        new_sample = candidates.sample(
            n=1,
            random_state=RANDOM_STATE
        )

        final_df = pd.concat([final_df, new_sample]).reset_index(drop=True)

        remaining_pool = remaining_pool.drop(new_sample.index)

print("After refill:")
print("Final total:", len(final_df))
print("Max images per video:",
      final_df.groupby("video_name").size().max())
print("Unique videos:",
      final_df["video_name"].nunique())
print("-" * 50)

# ============================================================
# Final luminance distribution
# ============================================================

print("Final luminance distribution:")
print(final_df["lum_category"].value_counts())
print("-" * 50)

# ============================================================
# Save output
# ============================================================

final_df.to_csv(OUTPUT_CSV, index=False)

print("Selection saved to:", OUTPUT_CSV)