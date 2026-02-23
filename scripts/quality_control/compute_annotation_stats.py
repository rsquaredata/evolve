"""
EVOLVE – Annotation Statistics Computation

This script computes descriptive statistics for the annotated YOLO dataset.

It provides:

- Total number of annotated images
- Total number of bounding boxes
- Average number of boxes per image
- Per-class instance distribution

Outputs:
- Console summary
- CSV table saved to results/tables/annotation_statistics.csv

Assumptions:
- YOLO format: one .txt file per image
- Each line in a .txt file corresponds to one bounding box
- Format per line:
    class_id x_center y_center width height
"""

import os
import glob
import pandas as pd
from collections import Counter


# =========================================================
# Configuration
# =========================================================

# Directory containing YOLO label files
LABELS_DIR = "data/processed/labels"

# Class mapping file (id -> class name)
CLASS_MAPPING_PATH = "metadata/class_mapping.txt"

# Output CSV file
OUTPUT_PATH = "results/tables/annotation_statistics.csv"


# =========================================================
# Utility Functions
# =========================================================

def load_class_mapping(path):
    """
    Load class mapping from metadata/class_mapping.txt.

    Expected format:
        0 amp
        1 guitar
        ...

    Returns:
        dict: {class_id (int): class_name (str)}
    """
    mapping = {}

    if not os.path.exists(path):
        raise FileNotFoundError(f"Class mapping file not found: {path}")

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) >= 2:
                class_id = int(parts[0])
                class_name = parts[1]
                mapping[class_id] = class_name

    return mapping


def compute_annotation_statistics():
    """
    Iterate over all YOLO label files and compute:

    - Number of annotated images
    - Total number of bounding boxes
    - Per-class instance counts

    Returns:
        total_boxes (int)
        image_count (int)
        class_counter (Counter)
    """

    # Recursively find all .txt files in LABELS_DIR
    label_files = glob.glob(
        os.path.join(LABELS_DIR, "**/*.txt"),
        recursive=True
    )

    total_boxes = 0
    image_count = 0
    class_counter = Counter()

    for file_path in label_files:

        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Count as annotated image only if at least one box
        if len(lines) > 0:
            image_count += 1

        # Update total box count
        total_boxes += len(lines)

        # Count per-class instances
        for line in lines:
            parts = line.split()
            class_id = int(parts[0])
            class_counter[class_id] += 1

    return total_boxes, image_count, class_counter


# =========================================================
# Main Execution
# =========================================================

def main():

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Load class mapping
    class_mapping = load_class_mapping(CLASS_MAPPING_PATH)

    # Compute statistics
    total_boxes, image_count, class_counter = compute_annotation_statistics()

    # Compute derived metric
    avg_boxes_per_image = (
        total_boxes / image_count if image_count > 0 else 0
    )

    # Prepare dataframe
    rows = []

    for class_id, count in sorted(class_counter.items()):
        rows.append({
            "class_id": class_id,
            "class_name": class_mapping.get(class_id, "unknown"),
            "num_instances": count
        })

    df = pd.DataFrame(rows)

    # Add total row
    df.loc[len(df)] = {
        "class_id": "TOTAL",
        "class_name": "",
        "num_instances": total_boxes
    }

    # Save CSV
    df.to_csv(OUTPUT_PATH, index=False)

    # Print summary
    print("\n=== EVOLVE Annotation Statistics ===")
    print(f"Annotated images: {image_count}")
    print(f"Total bounding boxes: {total_boxes}")
    print(f"Average boxes per image: {avg_boxes_per_image:.2f}")
    print("\nPer-class distribution:")
    print(df)


if __name__ == "__main__":
    main()