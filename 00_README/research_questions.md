# Research Questions

## RQ1: Conductivity-Machinability Relationship

**What is the quantitative relationship between electrical conductivity and machinability indicators (tool wear, cutting forces, surface roughness) in low-alloy steels?**

### Sub-questions
- RQ1a: Which machinability indicator (VB, Ra, Fc) correlates most strongly with conductivity?
- RQ1b: Is the relationship linear, monotonic, or non-linear?
- RQ1c: Does the relationship hold across different steel grades (AISI 1045, 4140, 4340)?
- RQ1d: What is the effect of cutting parameters (speed, feed, depth) on this relationship?

### Hypothesis
Electrical conductivity correlates negatively with cutting forces and positively with tool life for low-alloy steels in a given microstructural family, because higher conductivity indicates fewer lattice defects and lower hardness.

### Required Evidence
- Paired conductivity-machinability datasets for at least 3 steel grades
- Controlled cutting parameter sets (ISO 3685 compliant)
- Statistical correlation analysis (Pearson, Spearman)

### Success Criteria
- Correlation coefficient |r| > 0.7 for at least one machinability indicator
- Statistically significant (p < 0.05) across 2+ steel grades

---

## RQ2: Microstructural Mediation

**How do microstructural features (grain size, phase composition, precipitate distribution) mediate the conductivity-machinability relationship?**

### Sub-questions
- RQ2a: Which microstructural feature has the strongest independent effect on conductivity?
- RQ2b: Which microstructural feature has the strongest independent effect on machinability?
- RQ2c: Can mediating variables be quantified via a path analysis or structural equation model?
- RQ2d: Do different heat treatments (annealing, normalising, Q&T) produce distinct conductivity-machinability clusters?

### Hypothesis
Grain boundaries, phase boundaries, and precipitates scatter conduction electrons and simultaneously influence chip formation and tool-workpiece interaction, creating a shared microstructural basis for both properties.

### Required Evidence
- Metallographic characterisation (optical, SEM) paired with conductivity data
- Phase fraction quantification (XRD, EBSD)
- Grain size measurements (ASTM E112)
- Hardness maps correlated with conductivity

### Success Criteria
- Identified at least 2 mediating microstructural variables
- Mediation model explains >50% of conductivity-machinability variance

---

## RQ3: Measurement Methodology

**Which conductivity measurement techniques (4-probe DC, eddy current) provide the most reliable machinability prediction, and under what conditions?**

### Sub-questions
- RQ3a: What is the measurement uncertainty of each method for low-alloy steels?
- RQ3b: How does surface condition (roughness, oxide layer, residual stress) affect each method?
- RQ3c: Is eddy current viable for ferromagnetic steels despite permeability complications?
- RQ3d: What frequency range optimises eddy current sensitivity to machinability-relevant features?

### Hypothesis
Four-probe DC provides more accurate absolute conductivity values, but eddy current offers better practical utility for in-line monitoring; both can predict machinability within defined uncertainty bounds.

### Required Evidence
- Repeatability studies (min 10 measurements per specimen per method)
- Gauge R&R analysis
- Comparison against certified reference materials (ASTM B193, E1004)
- Surface condition sensitivity study

### Success Criteria
- Measurement uncertainty characterised for both methods
- Identified preferred method with uncertainty < 2% for prediction application

---

## RQ4: Predictive Model

**Can a validated predictive model estimate machinability from conductivity measurements, reducing machining trials?**

### Sub-questions
- RQ4a: Which modelling approach (regression, ANN, SVM, random forest) yields the best prediction?
- RQ4b: What is the minimum dataset size for reliable model training?
- RQ4c: How well does the model generalise across steel grades not in the training set?
- RQ4d: What is the practical prediction accuracy (RMSE, MAPE) for tool life and surface roughness?

### Hypothesis
A model incorporating conductivity, hardness, and composition as inputs can predict tool life (VB = 0.3 mm criterion) within +/- 15% and surface roughness Ra within +/- 0.3 um.

### Required Evidence
- Training dataset: min 50 data points across 3+ steel grades
- Validation dataset: min 15 data points (held out or cross-validated)
- Benchmark against composition-only and hardness-only models

### Success Criteria
- Prediction MAPE < 15% for tool life
- Model outperforms hardness-only baseline by > 10% relative improvement
- Cross-validation R^2 > 0.75
