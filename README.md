<div align="center">

# EVOLVE

### *Extreme Vision Over Low-light and Volatile Environments*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange.svg)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

*Master 2 SISE Project - Computer Vision*  
*Université Lumière Lyon 2 | 2025–2026*

---

</div>


## Overview

**EVOLVE** is a structured object detection study focused on **extreme low-light and volatile real-world environments**, using live metal concert imagery as a representative challenging domain.

These environments combine:

- Very low illumination
- Rapid and colored lighting shifts
- Motion blur
- Dense crowds
- Frequent occlusions
- Handheld instability

Such conditions remain underrepresented in standard computer vision benchmarks.

EVOLVE investigates:

> How do modern object detection models behave when deployed in visually extreme, low-visibility scenarios?

The project examines performance variation, degradation patterns, and failure modes under controlled lighting stratification.

---

## Research Orientation

EVOLVE is both a modeling project and a **dataset construction and annotation calibration study**.

Key methodological components:

- Controlled luminance stratification  
- Explicit inter-annotator calibration  
- Structured quality control pipeline  
- Performance analysis across lighting conditions  

The emphasis is placed on measurement, documentation, and controlled experimental design.

---

## Dataset Construction

The dataset is built through a structured multi-stage pipeline:

```
Raw video collection
↓
Frame extraction
↓
Luminance computation
↓
Stratified sampling
↓
Calibration subset creation
↓
Manual annotation (CVAT)
↓
Quality control
↓
Train / validation split
```

Full details are documented in:

- `doc/dataset_pipeline.md`
- `doc/calibration_protocol.md`
- `doc/inter_annotator_analysis.md`

### Data Sources

- Personal concert footage
- Public YouTube videos (research use only)

The dataset itself is **not distributed** due to licensing constraints.

---

## Target Classes

| Class | Description |
|-------|------------|
| `amp` | Stage amplifiers or monitors |
| `guitar` | Guitar or bass instruments |
| `drums` | Drum kit or drum elements |
| `micro` | Vocal microphones |
| `mosh_pit` | Collective dynamic crowd movement |
| `hands_raised` | Clusters of raised arms |

---

## Modeling

- Framework: PyTorch  
- Detector: YOLOv8 (Ultralytics)  
- Training approach: transfer learning from COCO pre-trained weights  
- Evaluation stratified by luminance categories  

---

## Evaluation Strategy

### Quantitative Metrics

- mAP
- Precision / Recall per class
- IoU
- Performance comparison across luminance strata  

### Qualitative Analysis

- Error typology
- Failure case inspection
- Lighting-specific degradation patterns
- Ambiguity analysis in dense and dynamic scenes  

---

## Project Structure

```
EVOLVE/
├── configs/
├── data/
│ ├── raw/
│ ├── interim/
│ └── processed/
├── doc/
│ ├── dataset_pipeline.md
│ ├── calibration_protocol.md
│ └── inter_annotator_analysis.md
├── metadata/
├── notebooks/
├── results/
├── scripts/
└── README.md
```

The repository emphasizes:

- reproducibility
- traceability
- structured dataset governance

---

## Limitations

- Limited dataset size
- Domain specificity (concert imagery)
- Residual annotation subjectivity
- Extreme lighting variability  

---

## Perspective

Future work may include:

- Larger-scale dataset extension
- Domain adaptation experiments
- Controlled ablation on lighting preprocessing
- Cross-model comparative analysis

---

## License

Academic project - non-commercial use only.

---

## A Reality Check

Building real-world computer vision systems often looks glamorous. However large-scale manual annotation remains a central bottleneck.

In EVOLVE, annotation is treated as a structured, calibrated and measurable process rather than a hidden cost.

---

<div align="center">

EVOLVE - Extreme Vision Under Extreme Conditions

</div>
