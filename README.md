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

**EVOLVE** is a structured object detection study focused on visually challenging real-world environments, using live metal concert imagery as a representative challenging domain.

These environments combine:

- Low and uneven illumination
- Rapid and colored lighting shifts
- Motion blur
- Dense crowds
- Frequent occlusions
- Handheld instability

Such conditions introduce significant variability in visual scene properties.

Beyond measuring detection performance under these conditions, EVOLVE investigates the following question:

> How does object detection performance vary across visually challenging environments, and can this variability be explained by measurable scene properties?

The project studies the statistical relationship between scene-level descriptors (visual and structural) and detection performance metrics.

---

## Research Orientation

EVOLVE combines;

- Dataset construction and annotation calibration  
- Controlled luminance stratification  
- Structured quality control  
- Quantitative analysis of performance variability 

A central objective is to determine whether measurable scene properties (e.g., luminance distribution, blur, spatial density) account for systematic differences in detection outcomes.

The emphasis is placed on experimental control, measurement rigor, and reproducible analysis.

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
