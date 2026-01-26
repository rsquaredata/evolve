## Introduction & Problem Statement

The **EVOLVE project** (Extreme Vision Over Low‑light and Volatile Environments) addresses the critical failure of standard computer vision pipelines in high-density, low-visibility scenarios, specifically within the context of **live concerts and large-scale crowd events**.

### The Problem

Traditional object detection models are trained on datasets with clear luminosity and distinct object-background separation. In extreme low-light environments:

1. **Feature collapse:** Standard CNNs fail to extract usable features as object edges and keypoints disappear into the noise floor.
2. **Perceptual bias:** Conventional image enhancement (LLE) focuses on making images "look better" for humans, often introducing artifacts that further degrade machine-level detection accuracy.
3. **Dynamic volatility:** Dense crowds create high occlusion and "camouflaged" targets where individuals are visually indistinguishable from the background shadows.

### The EVOLVE Approach

EVOLVE moves beyond simple preprocessing by treating extreme vision as a **representation and contextual reasoning challenge**.

* **Machine-centric representation:** Instead of human-readable brightening, we focus on aligning low-light feature clusters with standard detection manifolds.
* **Spatio-temporal fusion:** By extracting **Motion Information Images (MII)** from video sources, we provide the static image detector with a secondary "motion-aware" spatial channel. This channel highlights direction and magnitude of flow, serving as a proxy for presence when appearance is lost.
* **Contextual fallback:** We utilize scene-level and crowd-level context to maintain detection confidence, effectively identifying "camouflaged" individuals through their environmental relationships rather than isolated pixel data.

