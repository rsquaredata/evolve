from pathlib import Path
from collections import Counter, defaultdict

LABEL_DIR = Path("data/yolo/labels")

CLASS_NAMES = {
    0: "amp",
    1: "guitar",
    2: "drums",
    3: "micro",
    4: "mosh_pit",
    5: "hands_raised"
}

MIN_INSTANCES = 20

total_counter = Counter()
split_counter = defaultdict(Counter)

for split in ["train", "val", "test"]:
    for label_file in (LABEL_DIR / split).glob("*.txt"):
        with open(label_file) as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    total_counter[class_id] += 1
                    split_counter[split][class_id] += 1

print("\n=== Instance count per class (TOTAL) ===")
for class_id, count in sorted(total_counter.items()):
    name = CLASS_NAMES.get(class_id, f"class_{class_id}")
    status = "⚠️ LOW" if count < MIN_INSTANCES else "OK"
    print(f"{class_id:>2} ({name:<13}) : {count:>3}  [{status}]")

print("\n=== Instance count per split ===")
for split in ["train", "val", "test"]:
    print(f"\n[{split}]")
    for class_id, name in CLASS_NAMES.items():
        print(f"  {name:<13}: {split_counter[split][class_id]}")
