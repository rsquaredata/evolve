from pathlib import Path
from collections import Counter

LABEL_DIR = Path("data/yolo/labels")

counter = Counter()

for split in ["train", "val", "test"]:
    for label_file in (LABEL_DIR / split).glob("*.txt"):
        with open(label_file) as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    counter[class_id] += 1

print("Instance count per class:")
for k, v in sorted(counter.items()):
    print(f"Class {k}: {v}")
