<div align="center">

# EVOLVE

### *Extreme Vision Over Low-light and Volatile Environments*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange.svg)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

*Master 2 SISE Project – Computer Vision*  
*Université Lumière Lyon 2 | 2025-2026*

[Overview](#overview) • [Academic Context](#academic-context) • [Objectives](#objectives) • [Methodology](#methodology) • [Dataset](#dataset) • [Modeling](#modeling) • [Evaluation](#evaluation)

---

</div>

## Table of Contents

- [Overview](#overview)
- [Academic Context](#academic-context)
- [Objectives](#objectives)
- [Project Highlights](#project-highlights)
- [Methodology](#methodology)
- [Dataset](#dataset)
- [Modeling](#modeling)
- [Evaluation](#evaluation)
- [Limitations and Perspectives](#limitations-and-perspectives)
- [Project Structure](#project-structure)
- [License](#license)

---

</div>

## Overview

**EVOLVE** (*Extreme Vision Over Low-light and Volatile Environments*) is a computer vision project dedicated to **object detection in extreme real-world visual environments**, with a specific focus on **live metal concert imagery**.

Such environments combine several challenging conditions for vision systems:

- **very low illumination**
- **strong and rapidly changing colored lighting**
- **motion blur**
- **dense crowds**
- **frequent occlusions**
- **handheld camera instability**


These conditions are rarely represented in standard computer vision benchmarks, yet they are common in real-world applications.


The objective of EVOLVE is to **study the behavior, robustness, and failure modes of modern object detection models** when applied to such extreme and unconstrained scenes.

---

## Academic Context

This project is carried out as part of the **Master 2 SISE – Statistics and Computer Science for Data Science**  
Université Lumière Lyon 2 | Academic year 2025–2026

Course: **Computer Vision & Deep Learning**

---

## Objectives

- Study **object detection under degraded visual conditions**
- Fine-tune a modern detection model using **transfer learning**
- Analyze **robustness and limitations** of pre-trained models
- Identify **typical failure modes** in low-light and high-motion scenes
- Provide a **qualitative and quantitative analysis** beyond raw performance metrics

---

## Project Highlights

- Real-world (*in-the-wild*) data, not synthetic
- Extreme and rarely studied visual conditions
- Rigorous and reproducible experimental pipeline
- Qualitative analysis beyond raw performance metrics
- Strong alignment with the course content

---

## Methodology

The project follows a classical object detection experimental pipeline:

```
Data collection (real-world images)
        ↓
Exploratory dataset analysis
        ↓
Manual annotation (YOLO bounding boxes)
        ↓
Fine-tuning a pre-trained detection model
        ↓
Quantitative evaluation (mAP, precision, recall)
        ↓
Qualitative error analysis and discussion
```

---

## Dataset

### Data sources

- Personal photographs taken during live metal concerts
- Frames extracted from publicly available YouTube videos
- Images collected from online image search engines

All data are used strictly for **academic and non-commercial purposes**.

### Annotation format

- **YOLO format** (normalized bounding boxes)
- Manual annotation using CVAT or Roboflow
- Coarse bounding boxes allowed (focus on robustness, not pixel-perfect accuracy)

### Target classes

The dataset includes **six object classes**:


| Class name | Description |
|-----------------|-------------|
| `amp` | Stage amplifiers or monitors |
| `guitar` | Guitar or bass instruments |
| `drums` | Drum kit or drum elements |
| `micro` | Vocal microphones |
| `mosh_pit` | Areas of intense collective crowd movement |
| `hands_raised` | Groups of raised hands in the crowd |

> ⚠️ Due to size and licensing constraints, the dataset itself is **not distributed** in this repository.

---

## Modeling

- Framework: **PyTorch**
- Detection library: **YOLOv8 (Ultralytics)**
- Approach: **transfer learning**
- Starting point: YOLOv8 model pre-trained on COCO
- Fine-tuning performed on the EVOLVE dataset

YOLO was selected for:
- strong performance in diverse visual conditions
- robustness to scale variations
- ease of fine-tuning and evaluation
- widespread adoption in applied computer vision

---

## Evaluation

Evaluation is performed using:

### Quantitative metrics
- mean Average Precision (mAP)
- Precision and Recall per class
- Intersection over Union (IoU)

### Qualitative analysis
- visualization of correct detections
- analysis of false positives and false negatives
- inspection of failure cases related to:
    - low-light conditions
    - motion blur
    - occlusions
    - dense crowd dynamics

---

## Limitations and Perspectives

### Limitations
- Limited dataset size
- Subjective and coarse annotations
- High intra-class variability
- Strong domain shift with respect to standard benchmarks

### Perspectives
- Targeted data augmentation strategies
- Comparison across YOLO model sizes
- Ablation studies on preprocessing choices
- Extension to other extreme visual environments (clubs, festivals, protests)

---

## Project Structure

```
evolve/
├── doc/
│   └── notebooks/ 
│           ├── evolve_workbook.qmd        # Project definition, task, classes, annotation protocol
│           ├── evolve_training.ipynb      # YOLO training (GPU / Colab)
│           └── evolve_evaluation.ipynb    # Quantitative & qualitative evaluation
│
├── data/
│   ├── raw/
│   │   └── images/
│   │       ├── youtube/
│   │       │   ├── videos/        # Downloaded YouTube videos (.mp4)
│   │       │   └── frames/        # Extracted video frames (.jpg)
│   │       │
│   │       ├── personal/
│   │       │   └── photos/        # Personal concert photographs
│   │       │
│   │       └── web/
│   │           └── images/        # Images scraped from web search engines
│   │
│   ├── processed/
│   │   └── images/                # Preprocessed images (EDA / visualization only)
│   │
│   ├── annotations/
│   │   ├── raw/                   # CVAT / Roboflow exports (original format)
│   │   └── yolo/
│   │       ├── images/
│   │       │   └── all/            # Images selected for annotation
│   │       └── labels/
│   │           └── all/            # YOLO labels (before splitting)
│   │
│   └── yolo/
│       ├── images/
│       │   ├── train/              # Training images
│       │   ├── val/                # Validation images
│       │   └── test/               # Test images
│       │
│       ├── labels/
│       │   ├── train/              # Training labels
│       │   ├── val/                # Validation labels
│       │   └── test/               # Test labels
│       │
│       └── dataset.yaml            # YOLO dataset configuration
│
├── scripts/
│   ├── youtube_pipeline.sh         # YouTube scraping & frame extraction
│   ├── prepare_yolo_dataset.py     # Train/val/test split for YOLO
│   ├── count_instances.py          # Class instance statistics
│   ├── sanity_checks.py            # Image/label consistency checks
│   └── utils/
│       └── preprocess_images.py    # Optional preprocessing (EDA only)
│
├── runs/
│   └── detect/                     # YOLO training outputs (weights, metrics, predictions)
│
├── logs/
│   ├── ytdlp.log                   # yt-dlp logs
│   └── ffmpeg.log                  # ffmpeg logs
│
├── README.md
└── LICENSE
```

The final YOLO-ready dataset located in `data/yolo/` is automatically generated from the manually annotated data stored in `data/annotations/yolo/` using a dedicated preparation script.  
Raw images are never modified in-place, ensuring full traceability and reproducibility of the dataset construction process.

---

## License

This project is developed in an **academic context**.  
For **educational and non-commercial use only**.

---

<div align="center">

*EVOLVE — Extreme Vision Over Low-light and Volatile Environments*

</div>
