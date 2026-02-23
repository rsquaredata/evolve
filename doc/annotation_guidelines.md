# EVOLVE – Annotation Guidelines

Version: 1.0  
Project: EVOLVE (Extreme Vision Over Low-light and Volatile Environments)  
Authors: Rina Razafimahefa, Anne-Camille Vial 
Date: 2026-02-22  

---

## 1. General Principles

The EVOLVE dataset focuses on object detection in extreme concert environments characterized by:

- Low and very low illumination
- Strong chromatic bias (red/blue lighting)
- High density crowd scenes
- Motion blur and occlusion

Annotations follow the YOLO bounding box format.

All bounding boxes must:

- Enclose the visible extent of the object
- Avoid including excessive background
- Remain consistent across similar cases

---

## 2. Class Definitions

### 0 — `amp`

**Definition:**  
Guitar or bass amplifiers visible on stage.

**Include:**
- Full amplifier cabinets
- Partial amplifiers if identifiable

**Exclude:**
- Speakers from venue ceiling
- Unidentifiable black boxes

**Annotation rule:**  
Box should cover the cabinet body, not surrounding stage floor.

---

### 1 — `guitar`

**Definition:**  
String instruments (guitar or bass), whether being played or resting.

**Include:**
- Clearly visible instrument body
- Partial guitar if neck + body identifiable

**Exclude:**
- Microphone stands mistaken for neck
- Cables

**Common confusion:**  
Vertical silhouettes may resemble `micro`. If no instrument body is visible → do not label as guitar.

---

### 2 — `drums`

**Definition:**  
Drum kits or identifiable drum components (kick, toms, cymbals).

**Include:**
- Visible drum shells
- Partial drum kit if structure is clear

**Exclude:**
- Isolated cymbal reflections with no structure

**Annotation rule:**  
Prefer a single bounding box around the entire kit unless clearly separated.

---

### 3 — `micro`

**Definition:**  
Microphones and microphone stands.

**Include:**
- Handheld microphone
- Microphone on stand

**Challenge:**  
Thin geometry and low contrast.

**Annotation rule:**  
Bounding box must tightly follow the vertical structure without excessive background.

---

### 4 — `mosh_pit`

**Definition:**  
Any coordinated collective crowd movement typical of high-energy metal concerts.

This includes, but is not limited to:

- Circle pits
- Wall of death
- Pogo (synchronized jumping)
- Rowing (crowd sitting and simulating rowing)
- Crowd surfing clusters
- Sudden coordinated forward/backward surges

**Nature:**  
This class represents *collective behavior*, not individuals.

**Annotation rule:**  
Draw a bounding box around the active crowd movement zone.

The box should:
- Enclose the region where coordinated motion is visible
- Avoid including large static background areas
- Prioritize spatial coherence over perfect geometric fit

**Important:**  
Do not annotate isolated individuals as `mosh_pit`.  
There must be observable collective dynamics.

---

### 5 — `hands_raised`

**Definition:**  
Visible crowd silhouettes with raised arms toward the stage.

This includes:
- "Devil horns" gesture ( \m/ )
- Open hands raised
- Arms extended upward
- Grouped raised hands forming foreground silhouettes

**Exclude:**
- Single blurred arm without clear silhouette
- Partially visible limb with no clear upward orientation

**Annotation rule:**  
Bounding box should capture the silhouette cluster rather than individual fingers.

The objective is not gesture classification, but detection of vertical expressive crowd posture.

---

## 3. Edge Cases and Ambiguities

### Extreme Low-Light

If object is barely visible but structurally identifiable → annotate.

If object cannot be confidently identified → do not annotate.

---

### Occlusion

Partial occlusion is acceptable if the object identity is inferable.

---

### Motion Blur

Blur alone is not a reason for exclusion.

---

## 4. Annotation Consistency Strategy

To reduce subjectivity:

- Use consistent zoom level during annotation.
- Revisit earlier annotations after completing 50 images.
- Maintain minimum 30 instances per class.
- Perform final sanity check with class distribution script.

---

## 5. Quality Control

After annotation:

- Run `count_instances.py`
- Verify no empty label files
- Visually inspect 20 random samples
- Check class imbalance

---

## 6. Known Limitations

- `mosh_pit` bounding boxes are inherently subjective.
- Small objects (`micro`) may be underrepresented.
- Dataset cannot be redistributed due to source constraints.

---

## 7. Ethical and Legal Note

Images extracted from publicly available YouTube videos are used strictly for academic purposes.  
The dataset is not redistributed publicly.  
Only metadata and training code are shared.

---

End of document.