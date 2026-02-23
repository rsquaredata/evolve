# EVOLVE – Inter-Annotator Agreement Analysis

## 1. Objective

The calibration phase evaluates annotation consistency using both quantitative metrics and structured qualitative analysis.

The goal is to:

- Quantify detection-level agreement
- Quantify spatial consistency
- Identify systematic disagreement patterns
- Refine annotation rules if necessary

Calibration is performed on a shared subset of 30 images independently annotated by both annotators.

---

## 2. Quantitative Agreement

Agreement is evaluated at two complementary levels:

1. Instance-level agreement (object presence)
2. Spatial agreement (bounding box overlap)

---

## 2.1 Instance Count Agreement

For each image and each class, we compute:

$$
\text{Count Difference Ratio} =
\frac{\left| n_A - n_B \right|}
{\max(n_A, n_B)}
$$

Where:

- $n_A$ is the number of instances annotated by annotator A
- $n_B$ is the number of instances annotated by annotator B

Interpretation:

- 0.00 → perfect agreement  
- < 0.15 → strong agreement  
- 0.15–0.30 → moderate discrepancy  
- > 0.30 → substantial disagreement  

This metric captures detection-level disagreement (missed or over-detected objects).

---

## 2.2 Spatial Agreement (IoU-Based Matching)

Bounding boxes are matched using an IoU threshold of 0.50.

The Intersection over Union (IoU) between two bounding boxes is defined as:

$$
\text{IoU}(B_A, B_B) = \frac{|B_A \cap B_B|}{|B_A \cup B_B|}
$$

Where:

- $B_A$ is the bounding box from annotator A
- $B_B$ is the bounding box from annotator B

For matched pairs, we compute:

$$
\text{Mean IoU} = \frac{1}{N} \sum_{i=1}^{N} \text{IoU}_i
$$

Where:

- $N$ is the number of matched bounding box pairs.

We also compute the matching rate:

$$
\text{Matching Rate} = \frac{N_{\text{matched}}}{N_{\text{total}}}
$$

Interpretation:

- Mean IoU ≥ 0.60 → high spatial consistency  
- 0.40–0.60 → acceptable tolerance variation  
- < 0.40 → inconsistent spatial definitions  

This metric evaluates spatial precision beyond simple object presence.

---

## 2.3 Acceptance Thresholds

Calibration is considered satisfactory if:

- Mean Count Difference Ratio ≤ 0.15 per class  
- Mean IoU ≥ 0.60  
- No systematic bias between annotators  
- No class exhibits persistent structural disagreement  

If thresholds are not met, annotation rules are refined and calibration is repeated.

---

## 3. Qualitative Disagreement Analysis

Quantitative metrics are complemented by structured manual review.

### 3.1 Disagreement Categories

| Category | Description |
|----------|------------|
| Missed detection | Object annotated by one annotator only |
| Over-detection | Spurious detection due to ambiguity |
| Box size variation | Different spatial tolerance |
| Class confusion | Misclassification between visually similar classes |
| Low-light ambiguity | Visibility threshold discrepancy |

---

### 3.2 Focus on Ambiguous Classes

Particular attention is given to:

- `mosh_pit`
- `hands_raised`
- `micro`

These classes are inherently more subjective under extreme lighting conditions.

---

## 4. Outcome

The calibration phase produces:

- Agreement summary tables  
- IoU distribution plots  
- Disagreement typology summary  
- Refined annotation guidelines (if required)  

---

## 5. Methodological Contribution

This structured calibration protocol:

- Explicitly quantifies annotation subjectivity  
- Reduces variance prior to full-scale labeling  
- Documents ambiguity in extreme visual conditions  
- Strengthens dataset reliability  

---

End of document