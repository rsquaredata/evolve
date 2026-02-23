# EVOLVE – Dataset Construction Pipeline

## 1. Overview

EVOLVE is a structured object detection dataset built from extreme concert environments, characterized by:

- highly dynamic lighting conditions
- strong luminance contrasts
- motion blur
- occlusions
- smoke and visual noise

The dataset construction follows a controlled multi-stage pipeline designed to ensure:

- reproducibility
- controlled luminance stratification
- annotation consistency
- compatibility with YOLO training frameworks

---

## 2. Global Data Structure

```
data/
├── raw/
├── interim/
└── processed/
```

Each directory corresponds to a well-defined stage in the data lifecycle.

---

## 3. Stage 1 - Raw Data Collection

**Location**

```
data/raw/
```

**Sources**

- Personal concert recordings
- Public YouTube videos (used for research purposes only; not redistributed)

Raw videos are stored without modification.

---

## 4. Stage 2 - Frame Extraction

**Script**
```
scripts/dataset/extract_frames.sh
```

Frames are extracted at a controlled sampling rate to avoid redundancy while preserving lighting variability.

**Output**
```
data/interim/frames/
```


---

## 5. Stage 3 - Luminance Computation

To control lighting distribution, each frame undergoes luminance analysis.

**Scripts**
```
compute_luminosity.py
tag_luminance_categories.py
```

**Outputs**
```
data/interim/luminosity_stats.csv
data/interim/luminosity_tagged.csv
```

### Luminance Metric

Mean grayscale luminance is computed per frame.

Frames are categorized into luminance groups (e.g., `very_low`, `low`, `medium`, `high`) based on predefined thresholds.

This enables controlled stratified sampling.

---

## 6. Stage 4 - Stratified Sampling

A stratified subset of frames is selected to ensure:

- balanced lighting distribution
- scene diversity
- reduced redundancy

**Script**
```
scripts/dataset/select_700_stratified.py
```

**Output**
```
data/interim/selected_700.csv
```

---

## 7. Stage 5 - Annotation Pool Creation

Selected frames are copied into an annotation pool for CVAT.

**Script**
```
scripts/annotation/copy_annotation_pool.py
```

**Output**
```
data/processed/annotation_pool/
```

---

## 8. Stage 6 - Calibration Subset

A smaller calibration subset is created to measure inter-annotator agreement.

**Script**
```
scripts/calibration/create_calibration_30.py
```

**Output**
```
data/processed/calibration/
```

This subset is annotated independently by multiple annotators.

---

## 9. Stage 7 - Annotation in CVAT

Annotations are performed in CVAT.

Export format: YOLO

Final outputs:
```
data/processed/images/
data/processed/labels/
```

---

## 10. Stage 8 - Quality Control

Quality control ensures dataset integrity and annotation consistency.

**Scripts**

- `detect_near_duplicates.py`
- `sanity_checks.py`
- `count_instances.py`

Checks include:

- bounding box validity
- label consistency
- duplicate detection
- class distribution verification

---

## 11. Stage 9 - Train/Test Split

The final dataset is split into training and validation sets.

**Script**
```
scripts/dataset/split_dataset.py
```

Split parameters are defined in:
```
configs/dataset.yaml
```

---

## 12. Reproducibility Principles

The pipeline is designed to be:

- modular
- script-driven
- version-controlled
- deterministic when possible

All intermediate artifacts are logged in:
```
metadata
```

This ensures traceability of frame selection, calibration subsets, and splits.

---

## 13. Design Rationale

The dataset construction emphasizes:

1. Controlled lighting stratification
2. Explicit annotation calibration
3. Transparent data lineage
4. Minimal leakage between splits
5. Compatibility with standard detection frameworks

This design allows rigorous evaluation of detection robustness under extreme visual conditions.

---

End of document
