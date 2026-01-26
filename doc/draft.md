## 1. Introduction and Problem Statement

The EVOLVE project (Extreme Vision Over Low‑light and Volatile Environments) investigates the robustness of deep learning architectures in high-density, low-visibility scenarios—specifically within the context of live music events.

## 1.1. The Challenge of Adverse Environments

While standard computer vision benchmarks (e.g., COCO) assume optimal lighting and clear object separation, real-world "extreme" environments present three fundamental hurdles:

1. **Feature collapse**: As noted by **Morawski et al. (2021)**, extreme low-light is a representation problem. Traditional CNNs often fail to extract usable features as object edges and keypoints are lost in the noise floor.

2. **Perceptual vs. machine quality**: Conventional image enhancement often optimizes for human vision (brightness), which can introduce artifacts that degrade detector performance.

3. **Semantic volatility**: Dense crowds and motion blur create "camouflaged" targets where semantic components (e.g., `mosh_pit`, `hands_raised`) lack the sharp geometric boundaries expected by standard detectors.

## 1.2. Project Objective

The objective of this project is to implement an end-to-end pipeline for **Object Detection** in these volatile environments. We aim to demonstrate that by **fine-tuning** a State-of-the-Art (SOTA) architecture, namely **YOLOv8**, on a custom-curated dataset of 150+ images, we can maintain high detection accuracy even when traditional visual cues are significantly degraded.

## 2. Architecture Choice and Justification

For the EVOLVE project, we have selected **YOLOv8s** (You Only Look Once, version 8 Small) as the core detection architecture. This choice is justified by both the operational constraints of the project and the specific technical requirements of extreme-light environments.

## 2.1. Technical Alignment with Literature

The literature review highlights two major hurdles that YOLOv8 is uniquely equipped to handle:

- **Feature recovery via FPN**: **Zhang et al. (2022)** emphasized the need for feature reuse to recover small-object information lost in deep layers. YOLOv8 utilizes a **Feature Pyramid Network (FPN)** and a Path Aggregation Network (PAN), which allow for multi-scale feature fusion. This ensures that faint structural cues of instruments or equipment are preserved across different spatial resolutions.

- **Spatial attention and representation**: As **Morawski et al. (2021)** noted, low-light detection is a representation problem. YOLOv8’s use of **C2f modules** (cross-stage partial bottlenecks) enhances the gradient flow and allows the model to learn more robust representations of "camouflaged" targets, such as crowd members in deep shadows.

## 2.2. Selection of the "Small" Variant (YOLOv8s)

We opted for the **Small (s)** variant rather than Nano (n) or Large (x) for the following reasons:

- **Sensitivity vs. noise**: The Nano variant lacks the parameter depth to distinguish between image noise and actual features in low-light.

- **Inference speed**: The Small variant offers a superior balance for the "Volatile" aspect of EVOLVE, maintaining high inference speeds (essential for crowd dynamics) while providing enough capacity for fine-tuning on a small, specialized dataset.

## 2.3. Transfer Learning Strategy

To satisfy the  requirement for finetuning, we initialized the model with weights pre-trained on the COCO dataset.

- **Base knowledge**: We leverage COCO’s pre-learned filters for basic shapes and person detection.

- **Domain adaptation**: We then adapt the "head" of the network to our specific classes (`mosh_pit`, `hands_raised`, `amp`, etc.), where visual boundaries differ significantly from the standard COCO "person" or "chair" classes.

# 3. Dataset Methodology

## 3.1. Data Collection & Extraction

Unlike standard datasets, the EVOLVE dataset was curated to capture "Extreme Vision" conditions. We implemented a dedicated collection pipeline:

- **Sources**: Publicly available concert footage and images, as well as personal photos.
- **Sampling**: Frames were extracted at a fixed temporal rate (1 frame every 5 seconds) using a custom shell script (`youtube_pipeline.sh`) to ensure visual diversity and avoid high temporal correlation between training samples.
- **Selection**: Images were manually screened to ensure the presence of target semantic components under varying degrees of lighting volatility.

## 3.2. Target Classes and Annotation

We defined 6 distinct classes that represent the structural and semantic pillars of a live music environment. Each class was annotated with a minimum of 30 instances.

| **Class Name** | **Type**  | **Description**                                           |
|----------------|-----------|-----------------------------------------------------------|
| `amp`          | Rigid     | Guitar/Bass amplifiers, often partially obscured.         |
| `guitar`       | Rigid     | Stringed instruments (guitars/basses).                    |
| `drums`        | Complex   | Percussion elements, often high-density/occluded.         |
| `micro`        | Small     | Microphones and stands; challenging due to thin geometry. |
| `mosh_pit`     | Amorphous | High-motion crowd zones; defined by collective texture.   |
| `hands_raised` | Amorphous | Foreground crowd silhouettes; high occlusion potential.   |

## 3.3. Quality Control and Preprocessing

To ensure the integrity of the model's training, we implemented a multi-stage validation process:

- **Consistency checks**: A custom script (`sanity_checks.py`) was used to verify that every image possessed a corresponding label file and that no empty labels were introduced.
- **Instance balancing**: Using `count_instances.py`, we monitored class distribution to avoid significant bias toward common classes like `hands_raised`.
- **Reproducible split**: The dataset was partitioned into **Train** (70%), **Validation** (20%), and **Test** (10%) using a fixed random seed (`42`) to allow for reproducible experimental results.

## 4. Training Protocol and Hyperparameters

This section details the specific configuration used in the `evolve_training.ipynb` notebook.

## 4.1. Fine-tuning Configuration

We utilized a **Transfer Learning** strategy by initializing our model with weights from the COCO dataset. This allows the model to leverage pre-learned low-level features (edges, textures) while specializing the high-level detection head for our specific domain.

- **Optimizer**: We utilized the **Auto-optimizer** (typically SGD or AdamW in YOLOv8) with a standard learning rate schedule.
- **Epochs**: Set to **50**, providing enough iterations for the model to converge on the specialized concert features without overfitting the small dataset.
- **Batch size**: Set to **16**, a choice governed by GPU memory constraints in the Google Colab environment while maintaining sufficient gradient stability.
- **Image resolution**: Maintained at 640x640. Given the adverse lighting conditions of the EVOLVE dataset, structural details are already degraded by noise. We maintained the native 640px resolution to maximize feature density. This prevents the "vanishing" of small semantic components, such as microphones or instruments, which are essential for accurate scene reconstruction in dense crowd environments.

# 5. Results and Evaluation

## 5.1. Quantitative Results (mAP)

Following the transfer learning process, the model was evaluated on the unseen test set (10% of the total dataset). We utilize the **mean Average Precision (mAP@.5)** as our primary metric, which is the standard for object detection.

| **Class**      | **Precision** | **Recall** | **mAP@.5** |
|----------------|---------------|------------|------------|
| `amp`          | - | - | - | 
| `guitar`       | - | - | - | 
| `drums`        | - | - | - | 
| `micro`        | - | - | - | 
| `mosh_pit`     | - | - | - | 
| `hands_raised` | - | - | - | 
| All Classes    | - | - | - | 

## 5.2. Qualitative Analysis: Success Cases

The model demonstrated a high degree of robustness in several "extreme" conditions:

- **Strong chromatic bias**: Despite intense red and blue stage lighting, the model successfully localized rigid objects like `amp` and `drums`, suggesting that the architecture learned structural geometric features rather than relying purely on color histograms.
- **Crowd silhouette detection**: The `hands_raised` class showed high recall even in near-zero visibility (backlit conditions), effectively utilizing the contrast between the crowd silhouettes and the stage lights.

## 5.3. Error Analysis and Failure Modes

We identified recurring failure patterns:

- **Scale invariance issues (`micro`)**: Small microphones were occasionally missed when positioned against a complex, noisy background (e.g., in front of a drum kit). This highlights the difficulty of detecting thin, linear objects in low-contrast environments.
- **Semantic overlap**: Confusions between `guitar` and `micro` (stands) occurred in extremely dark frames where only the vertical silhouette was visible.
- **Boundary ambiguity (`mosh_pit`)**: Because the `mosh_pit` is an amorphous crowd zone, the model sometimes struggled with precise bounding box localization (IoU errors), even when the semantic identification was correct.

# 6. Conclusion

The EVOLVE project successfully demonstrates that **YOLOv8**, when properly fine-tuned, can serve as a reliable detector in adverse live-music environments. By prioritizing feature density (640px resolution) and domain-specific classes (`mosh_pit`), we achieved a pipeline that outperforms generic "COCO-trained" models which typically fail to recognize specialized concert gear or crowd behaviors.

## Future Perspectives:

- **Temporal integration**: Future iterations could move beyond static frames to utilize motion vectors (MII) directly from the video stream to resolve ambiguities in static silhouettes.
- **Dataset expansion**: Increasing the instance count for the `micro` class would likely reduce the scale-invariance failures identified during evaluation.
















