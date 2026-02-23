# EVOLVE – Calibration Protocol (v1.1)


## 1. Purpose

The calibration phase aims to:

- Reduce inter-annotator subjectivity
- Harmonize bounding box definitions
- Clarify ambiguous class boundaries
- Establish reproducible annotation standards

Calibration is conducted on a shared subset of 30 images independently annotated by both annotators.

The subset is stratified by luminance category:

- 10 very_low
- 10 low
- 10 medium

This ensures that calibration reflects lighting variability inherent to the dataset.

---

## 2. Annotation Setup

- Tool: CVAT
- Export format: YOLO
- Annotation type: Rectangle only
- No attributes
- Identical zoom policy

Labels:

- amp
- guitar
- drums
- micro
- mosh_pit
- hands_raised

Refer to `annotation_guidelines.md` for full semantic definitions.

---

## 3. Global Operational Rules

### 3.1. Zoom Policy

- Default zoom: 100–150%
- Maximum zoom: 300%
- Pixel-level micro-interpretation is forbidden

Rationale: maintain consistent perceptual scale and avoid artificial precision.


### 3.2. Bounding Box Tightness Rule

Bounding boxes must:

- Enclose the visible object extent
- Avoid excessive background
- Allow slight tolerance for motion blur

Forbidden:

- Oversized safety margins
- Over-tight cropping that amputates visible object edges

### 3.3 Minimum Visibility Rule

An object is annotated only if:

- Its structural identity is inferable
- At least ~30% of its shape is visible

Do not annotate:

- Pure silhouette fragments
- Light reflections
- Indistinct color blobs

### 3.4 Partial Object Rule

If partially occluded:

- Annotate only the visible region
- Do not hallucinate hidden structure
- Do not extrapolate invisible geometry

---

## 4. Class-Specific Rules

### 2.4. Class-Specific Calibration Rules

`amp`:
- Box cabinet body only
- Ignore cables and floor

`guitar`:
- Neck + body must be identifiable
- Do not confuse with microphone stands
- If only neck silhouette visible → do not annotate

`drums`:
- Prefer one box around full kit
- If kit split visually → multiple boxes allowed

`micro`:
- Tight vertical box
- No extra background
- Ignore reflections

`mosh_pit` (**CRITICAL CLASS**):
- Annotate only if:
  - Coordinated collective movement visible
  - Spatial cluster exists
  - Clear dynamic pattern
- Do NOT annotate:
  - Dense but static crowd
  - Isolated jumping individual
- Box must:
  - Enclose active region
  - Avoid large static periphery

`hands_raised`:
- Annotate cluster, not individual hands.
- Minimum threshold:
  - At least 3 raised arms visible
  - Clear upward posture
- Do not annotate:
  - Single isolated arm
  - Ambiguous blur

---

## 5. Calibration Procedure

1. Independent annotation of 30 shared images
2. Quantitative agreement analysis
3. Identification of divergent cases
4. Joint qualitative review
5. Rule refinement (if required)
6. Freeze protocol as v1.1

---

## 6. Acceptance Criteria

Calibration is considered satisfactory if:

- ≤ 15% average count difference per class
- No systematic bias between annotators
- No persistent high disagreement for critical classes

If not satisfied, protocol refinement is performed before full dataset annotation.

---

## 7. Deliverables

- Inter-annotator agreement report
- Before/after visual examples
- Updated annotation rules (if applicable)

---

End of document
