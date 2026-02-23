"""
EVOLVE – Luminance Computation Script

This script computes the mean grayscale luminance for each extracted frame in the dataset.

For every image (.jpg) located under: data/interim/frames/{source}/{video_name}/

It calculates:
    - Mean grayscale luminance

The resulting statistics are saved to:
    data/interim/luminosity_stats.csv

These values are later used for:
    - Illumination distribution analysis
    - Stratified sampling
    - Dataset difficulty characterization
"""

import os
import cv2
import numpy as np
import pandas as pd


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

FRAMES_DIR = "data/interim/frames"
OUTPUT_CSV = "data/interim/luminosity_stats.csv"

# Sources included in the dataset
SOURCES = ["youtube", "personal"]


# ------------------------------------------------------------------
# Luminance computation
# ------------------------------------------------------------------

records = []

for source in SOURCES:
    source_path = os.path.join(FRAMES_DIR, source)

    # Skip if source folder does not exist
    if not os.path.exists(source_path):
        continue

    for video_name in os.listdir(source_path):
        video_folder = os.path.join(source_path, video_name)

        # Ensure we only process directories
        if not os.path.isdir(video_folder):
            continue

        for filename in os.listdir(video_folder):

            # Only process JPG images
            if not filename.lower().endswith(".jpg"):
                continue

            img_path = os.path.join(video_folder, filename)

            # Load image
            img = cv2.imread(img_path)

            # Skip corrupted or unreadable images
            if img is None:
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Compute mean luminance
            mean_luminance = float(np.mean(gray))

            # Store metadata and luminance value
            records.append({
                "filename": filename,
                "full_path": img_path,
                "source": source,
                "video_name": video_name,
                "mean_luminance": mean_luminance
            })


# ------------------------------------------------------------------
# Save results
# ------------------------------------------------------------------

df = pd.DataFrame(records)
df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved {len(df)} luminance records to {OUTPUT_CSV}")