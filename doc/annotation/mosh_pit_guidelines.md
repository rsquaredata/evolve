# EVOLVE - `mosh_pit` Detailed Annotation Guidelines

---

## 1. Definition

`mosh_pit` refers to a localized structural rupture within an otherwise globally stage-oriented dense crowd.

The phenomenon is fundamentally spatio-temporal, but must be inferred from a single image using spatial configuration alone.

The class captures coordinated collective crowd behavior, not isolated individuals.

---

## 2. Positive Visual Indicators

Annotate `mosh_pit` when at least one of the following structural signals is clearly identifiable, and forms a localized contrast with the surrounding crowd.

## 2.1 Density Rupture
- Visible empty or semi-empty space within a dense crowd
- Clearly delimited separation between two crowd fronts
- Circular void surrounded by spectators

The void must be structurally identifiable (circular, linear, or clearly bounded), not a random compression gap.

---

## 2.2 Spatial Reorganization
- **Circle pit**: circular or annular arrangement of people
- **Wall of death**: two aligned fronts facing each other with central separation
- **Rowing**: visible seated or crouched group within a standing crowd
- **Pogo**: locally chaotic cluster with irregular spacing and orientation

The pattern must contrast with the surrounding crowd regularity.

---

## 2.3 Orientation Rupture
- Majority of surrounding crowd faces the stage
- Within the suspected region:
  - Multiple divergent orientations
  - Lateral body positioning
  - Reduced alignment consistency

Head orientation irregularity may be used as a proxy when bodies are occluded.

---

## 2.4 Vertical Anomaly — Crowd Surfing

Crowd surfing is annotated as `mosh_pit` when:
- A horizontally positioned body is visible above the crowd
- A visible support zone (raised arms, convergence of heads) is present

The bounding box must include:
- The crowd surfer
- The immediate supporting zone (arms / hands / nearby heads)

Do not annotate raised hands alone without visible horizontal body.

---

## 3. Negative Indicators (Do Not Annotate)

Do not annotate `mosh_pit` in the following cases:
- Dense but static crowd
- Diffuse agitation without localized structure
- Single individual jumping or moving
- Lighting artifacts or motion blur without structural pattern
- Random small density fluctuation without geometric coherence

---

## 4. Decision Rule

Annotate `mosh_pit` only if:
- The region forms a clearly localized structural rupture
- Collective dynamics can be reasonably inferred
- The anomaly is distinguishable from background crowd behavior

As a heuristic threshold, the phenomenon should involve multiple visible individuals (≥ 3–5 depending on image scale), or produce a clearly identifiable geometric configuration.

---

## 5. Bounding Box Rule

The bounding box must:
- Enclose the full structurally divergent region
- Include the core rupture and immediately involved surrounding crowd
- Remain as compact as possible
- Avoid large areas of unaffected static crowd

The objective is to capture the spatially coherent behavioral zone, not an abstract center point.

---

## 6. Expected Variability

`mosh_pit` is inherently contextual and structurally defined.

Expected consequences:
- Higher inter-annotator variability (lower IoU expected)
- Potential class rarity
- Model performance instability compared to rigid object classes

This is considered an intrinsic property of the phenomenon.

---

End of document
