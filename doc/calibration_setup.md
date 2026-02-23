# EVOLVE - Calibration Setup in CVAT

## 1. Setup

Create 2 tasks based on 30 images from the 700 sample (stratified sampling by luminance category):
- 10 "very low"
- 10 "low"
- 10 "medium"

### Task description:
1. Same zoom level
2. Bounding box: tight but not amutated
3. Don't annotate unidentifiable objects
4. mosh_pit = visible collective dynamic, not juste a dense crows
5. hands_raised = cluster, not an isolated arm

### Create labels

Refer to `annotation_guidelines` for full labels descriptions.

Type = Rectangle.

| label name   | color  |
|--------------|--------|
| amp          | 9E9E9E |
| guitar       | 1E88E5 |
| drums        | 8E24AA |
| micro        | FDD835 |
| mosh_pit     | FB8C00 |
| hands_raised | 00ACC1 |

Raw version:

```
[
  {
    "name": "amp",
    "id": 14,
    "color": "#9e9e9e",
    "type": "rectangle",
    "attributes": []
  },
  {
    "name": "guitar",
    "id": 15,
    "color": "#1e88e5",
    "type": "rectangle",
    "attributes": []
  },
  {
    "name": "drums",
    "id": 16,
    "color": "#8e24aa",
    "type": "rectangle",
    "attributes": []
  },
  {
    "name": "micro",
    "id": 17,
    "color": "#fdd835",
    "type": "rectangle",
    "attributes": []
  },
  {
    "name": "mosh_pit",
    "id": 18,
    "color": "#fb8c00",
    "type": "rectangle",
    "attributes": []
  },
  {
    "name": "hands_raised",
    "id": 19,
    "color": "#00acc1",
    "type": "rectangle",
    "attributes": []
  }
]
```