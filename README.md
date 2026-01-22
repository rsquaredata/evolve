<div align="center">

# EVOLVE

### *Extreme Vision Over Low-light and Volatile Environments*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![Detectron2](https://img.shields.io/badge/Detectron2-Object%20Detection-orange.svg)](https://github.com/facebookresearch/detectron2)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

*Master 2 SISE Project – Computer Vision*  
*Université Lumière Lyon 2 | 2025-2026*

[Overview](#overview) • [Methodology](#methodology) • [Dataset](#dataset) • [Models](#modeling) • [Evaluation](#evaluation)

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

## Overview

**EVOLVE** (*Extreme Vision Over Low-light and Volatile Environments*) is a computer vision project dedicated to the study of **object detection in extreme and unconstrained visual environments**.

The project focuses on real-world scenes characterized by:
- **low-light conditions**
- **rapid illumination variations**
- **strong motion dynamics**
- **frequent occlusions**
- **high crowd density**

The main objective is to analyze the **robustness and limitations** of deep learning–based object detectors under such challenging conditions.

---

## Academic Context

This project is carried out as part of the **Master 2 SISE – Statistics and Computer Science for Data Science**  
Université Lumière Lyon 2 | Academic year 2025–2026

Course: **Computer Vision & Deep Learning**

---

## Objectives

- Study **object detection under degraded visual conditions**
- Evaluate modern detection models on **real-world, unconstrained data**
- Analyze typical **failure modes** of convolutional neural networks
- Discuss the **limitations of standard supervised approaches**
- Propose **perspectives and improvements** for similar environments

---

## Project Highlights

- Real-world (*in-the-wild*) data, not synthetic
- Extreme and rarely studied visual conditions
- Rigorous and reproducible experimental pipeline
- Qualitative analysis beyond raw performance metrics
- Strong alignment with the course content

---

## Methodology

The project follows a classical computer vision experimental pipeline:

```
Data collection
        ↓
Exploratory dataset analysis
        ↓
Manual annotation (bounding boxes)
        ↓
Training object detection models
        ↓
Quantitative and qualitative evaluation
        ↓
Error analysis and discussion
```

---

## Dataset

- Images collected from **unconstrained real-world scenes**
- Visual conditions include:
  - low illumination
  - volatile and rapidly changing lighting
  - motion blur
  - dense crowds
- Annotations in **COCO format**
- Main object classes:
  - person
  - raised_arm
  - mobile_phone
  - microphone
  - guitar_bass

> ⚠️ Due to size and licensing constraints, the full dataset is not stored in this repository.

---

## Modeling

- Framework: **PyTorch**
- Library: **Detectron2**
- Models explored:
  - Faster R-CNN (ResNet backbone)
- Supervised training
- Hyperparameter tuning within the scope of the course

---

## Evaluation

- Standard object detection metrics:
  - mAP
  - Precision / Recall
- Per-class analysis
- Qualitative error analysis:
  - false positives
  - false negatives
  - errors related to lighting and occlusions

---

## Limitations and Perspectives

### Limitations
- Intentionally limited dataset size
- Costly manual annotation process
- High intra-class variability

### Perspectives
- Targeted data augmentation
- Exploration of more robust architectures
- Transfer to other extreme visual environments
- Comparison with one-stage detectors

---

## Project Structure

```
EVOLVE/
│
├── notebooks/          # Experiments and analyses
├── src/                # Utility scripts
├── configs/            # Detectron2 configurations
├── analysis/           # Analysis and visualizations
├── figures/            # Figures for the report
├── data/               # Data (structure only)
├── README.md
└── LICENSE
```

---

## License

This project is developed in an **academic context**.  
For educational use only.

---

<div align="center">

*EVOLVE — Extreme Vision Over Low-light and Volatile Environments*

</div>
