"""
EVOLVE – YOLO Label Instance Counter

This script counts the number of object instances per class from YOLO-format label files.

Each label file contains one object per line in the format:
    class_id x_center y_center width height

The script aggregates class frequencies for a given split
(e.g., train / val / test).

This is primarily used for:
- Dataset balance verification
- Post-annotation sanity checks
- Monitoring class imbalance
"""

import os
from collections import Counter


# ============================================================
# Configuration
# ============================================================

LABELS_DIR = "data/processed/labels/train"  # Change if needed


# ============================================================
# Instance counting
# ============================================================

class_counts = Counter()
total_instances = 0
total_files = 0

for filename in os.listdir(LABELS_DIR):

    # Process only YOLO label files
    if not filename.endswith(".txt"):
        continue

    total_files += 1

    with open(os.path.join(LABELS_DIR, filename), "r") as f:
        for line in f.readlines():

            # Skip empty lines (important safeguard)
            if not line.strip():
                continue

            class_id = int(line.split()[0])
            class_counts[class_id] += 1
            total_instances += 1


# ============================================================
# Results
# ============================================================

print("========================================")
print("YOLO Instance Distribution Summary")
print("========================================")
print(f"Label files processed: {total_files}")
print(f"Total object instances: {total_instances}")
print("----------------------------------------")

for class_id, count in sorted(class_counts.items()):
    print(f"Class {class_id}: {count} instances")

print("========================================")