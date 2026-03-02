## 1. Introduction

The EVOLVE project (*Extreme Vision Over Low-light and Volatile Environments*) studies object detection under visually adverse real-world conditions.

Unlike standard benchmarks such as COCO, live concert environments simultaneously combine:
- Low and uneven illumination
- Chromatic bias (dominant red/blue lighting)
- Motion blur
- High crowd density

These factors degrade edge contrast, reduce feature separability, and introduce instability in bounding-box localization.

Rather than maximizing benchmark performance, EVOLVE investigates the following question:
> Can variations in detection performance be statistically associated with measurable scene-level properties?

## 2. Dataset

### 2.1. Collection Pipeline

The dataset was constructed through a structured multi-stage pipeline:

Raw video collection → Frame extraction → Luminance computation → Stratified sampling → Manual annotation → Quality control → Reproducible split

Initial extraction:
- 2650 frames from 16 publicly available YouTube videos
- 1888 additional frames extracted from personal concert recordings
- 798 retained after filtering
- Final curated dataset: **700 images**

The inclusion of both public and personally recorded material increases environmental variability (venues, lighting systems, camera sensors) while maintaining consistent annotation criteria.

For the EVOLVE project, we have selected **YOLOv8s** (You Only Look Once, version 8 Small) as the core detection architecture. This choice is justified by both the operational constraints of the project and the specific technical requirements of extreme-light environments.

### 2.2. Split

| Split      | Images |
| ---------- | ------ |
| Train      | 560    |
| Validation | 70     |
| Test       | 70     |

Random seed:42

### 2.3. Class Distribution (Global)

| Class        | Instances |
| ------------ | --------- |
| amp          | 879       |
| guitar       | 494       |
| drums        | 339       |
| micro        | 329       |
| mosh_pit     | 99        |
| hands_raised | 593       |

Minimum per class: 99 instances.

The dataset shows moderate imbalance, with `mosh_pit` being the least represented class.

## 3. Architecture and Training

We selected YOLOv8s for the following reasons:
- Multi-scale feature aggregation (FPN + PAN)
- Parameter capacity suitable for medium-sized datasets
- Efficient training with limited computational resources

Training configuration:
- Image resolution: 640×640
- Epochs: 30
- Batch size: 16
- Transfer learning from COCO
- Deterministic mode enabled

Two training regimes were compared:
- Fine-tuned COCO-pretrained model
- Training from scratch

## 4. Results

### 4.1. Quantitative Performance

#### Validation Performance

| Model                   | mAP@0.5:0.95 | mAP@0.5 |
| ----------------------- | ------------ | ------- |
| Pretrained (fine-tuned) | ~0.17        | ~0.30   |
| Scratch                 | ~0.03        | ~0.08   |

Training from scratch does not achieve comparable performance levels.  
Pretraining provides a substantial improvement in detection metrics under low-light conditions.

### 4.2? Scene-Level Correlation Analysis

For the pretrained model:

| Variable       | r      | R²    | p-value |
| -------------- | ------ | ----- | ------- |
| Luminance      | 0.391  | 0.153 | 0.001   |
| Blur           | -0.110 | 0.012 | 0.364   |
| Density        | -0.080 | 0.006 | 0.511   |
| Occupied ratio | -0.070 | 0.005 | 0.567   |

Only luminance shows a statistically significant association with recall (p = 0.001).

This indicates that detection variability is partially structured by illumination level, whereas blur and density do not show statistically significant effects in this dataset.

## 5. Qualitative Analysis

Observations from visual inspection:
- Rigid objects (`amp`, `drums`) are more frequently detected in higher-luminance frames.
- Thin structures (`micro`) are occasionally missed when contrast is low.
- `mosh_pit` bounding boxes show localization variability due to diffuse boundaries.

Failure cases often occur in frames with very low mean luminance (< 20 pixel intensity), where edge contrast is minimal.

## 6. Conclusion

The EVOLVE project shows that:
1. Transfer learning is necessary for detection in low-visibility concert environments.
2. Detection performance variation is statistically associated with scene luminance.
3. Amorphous crowd-based classes present intrinsic challenges for bounding-box-based detectors.

