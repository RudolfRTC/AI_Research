# Formal Hypotheses

This document states the formal hypotheses for each research question, including null and alternative hypotheses, statistical tests, and required sample sizes.

---

## H1: Conductivity–Machinability Correlation (RQ1)

### H1a: Conductivity vs. Tool Life

| | Statement |
|---|---|
| **H₀** | There is no significant linear correlation between electrical conductivity (%IACS) and tool life (min) for low-alloy steels: ρ = 0 |
| **H₁** | There is a significant correlation between electrical conductivity and tool life: ρ ≠ 0 |
| **Test** | Pearson correlation (if normal) / Spearman rank correlation (if non-normal) |
| **Significance** | α = 0.05 |
| **Effect size target** | \|r\| > 0.7 |
| **Required n** | ≥ 15 paired observations (power = 0.80, α = 0.05, \|r\| = 0.7) |

### H1b: Conductivity vs. Surface Roughness (Ra)

| | Statement |
|---|---|
| **H₀** | No significant correlation between conductivity and Ra: ρ = 0 |
| **H₁** | Significant correlation exists: ρ ≠ 0 |
| **Test** | Pearson / Spearman correlation |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 15 paired observations |

### H1c: Conductivity vs. Cutting Force (Fc)

| | Statement |
|---|---|
| **H₀** | No significant correlation between conductivity and Fc: ρ = 0 |
| **H₁** | Higher conductivity correlates with lower cutting forces: ρ < 0 |
| **Test** | One-tailed Pearson / Spearman correlation |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 15 paired observations |

### H1d: Cross-grade consistency

| | Statement |
|---|---|
| **H₀** | The conductivity–machinability relationship does not hold across steel grades |
| **H₁** | The relationship is consistent across AISI 1045, 4140, and 4340 |
| **Test** | Fisher's z-transformation to compare correlation coefficients across groups |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 10 per steel grade (3 grades minimum) |

---

## H2: Microstructural Mediation (RQ2)

### H2a: Microstructure → Conductivity pathway

| | Statement |
|---|---|
| **H₀** | Microstructural features (grain size, phase fraction) do not significantly predict conductivity |
| **H₁** | At least one microstructural feature significantly predicts conductivity (p < 0.05) |
| **Test** | Multiple linear regression; F-test for overall significance |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 30 specimens with paired metallographic + conductivity data |

### H2b: Mediation model

| | Statement |
|---|---|
| **H₀** | Microstructure does not mediate the conductivity–machinability relationship (indirect effect = 0) |
| **H₁** | Microstructure significantly mediates the relationship (indirect effect ≠ 0) |
| **Test** | Baron & Kenny mediation steps + Sobel test / bootstrap confidence interval |
| **Significance** | 95% bootstrap CI for indirect effect excludes zero |
| **Effect size target** | Mediation model explains >50% of conductivity–machinability variance |
| **Required n** | ≥ 50 specimens |

### H2c: Heat treatment clustering

| | Statement |
|---|---|
| **H₀** | Different heat treatments (annealed, normalised, Q&T) do not form distinct conductivity–machinability clusters |
| **H₁** | Heat treatments produce statistically separable clusters in conductivity–machinability space |
| **Test** | MANOVA or permutation-based MANOVA on 2D (conductivity, machinability) space |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 10 specimens per heat treatment condition (minimum 3 conditions) |

---

## H3: Measurement Method Comparison (RQ3)

### H3a: Method agreement

| | Statement |
|---|---|
| **H₀** | Four-probe DC and eddy current methods produce equivalent conductivity values (mean difference = 0) |
| **H₁** | There is a systematic bias between the two methods |
| **Test** | Paired t-test / Bland-Altman analysis |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 30 specimens measured with both methods |

### H3b: Predictive accuracy comparison

| | Statement |
|---|---|
| **H₀** | Both methods yield equal machinability prediction accuracy (MAPE_4probe = MAPE_eddy) |
| **H₁** | One method yields significantly better prediction accuracy |
| **Test** | Paired comparison of prediction errors (Wilcoxon signed-rank test) |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 20 prediction pairs |

### H3c: Measurement uncertainty

| | Statement |
|---|---|
| **H₀** | Neither method achieves measurement uncertainty < 2% |
| **H₁** | At least one method achieves expanded uncertainty U < 2% of measured value |
| **Test** | GUM (Guide to Uncertainty in Measurement) uncertainty budget |
| **Criterion** | U₉₅ < 2% for the preferred method |
| **Required n** | ≥ 10 repeated measurements per specimen, ≥ 5 specimens |

---

## H4: Predictive Model Performance (RQ4)

### H4a: Model vs. hardness-only baseline

| | Statement |
|---|---|
| **H₀** | The conductivity-based model does not outperform the hardness-only baseline (MAPE_model ≥ MAPE_baseline) |
| **H₁** | The conductivity-based model outperforms the baseline by >10% relative improvement |
| **Test** | Paired comparison of cross-validated errors; one-tailed Wilcoxon signed-rank test |
| **Significance** | α = 0.05 |
| **Required n** | ≥ 50 data points, 5-fold cross-validation |

### H4b: Tool life prediction accuracy

| | Statement |
|---|---|
| **H₀** | The model cannot predict tool life with MAPE < 15% |
| **H₁** | The model achieves MAPE < 15% for tool life prediction |
| **Test** | 5-fold or leave-one-group-out cross-validation |
| **Criterion** | Mean MAPE across folds < 15% |
| **Required n** | ≥ 50 data points across 3+ steel grades |

### H4c: Cross-grade generalisation

| | Statement |
|---|---|
| **H₀** | The model does not generalise to steel grades not in the training set (R² ≤ 0) |
| **H₁** | The model generalises to unseen grades with R² > 0.5 |
| **Test** | Leave-one-grade-out cross-validation |
| **Criterion** | R² > 0.5 on the held-out grade |
| **Required n** | Data from ≥ 4 steel grades (3 train, 1 test, rotated) |

### H4d: Model selection

| | Statement |
|---|---|
| **Candidates** | Linear Regression, SVR, Random Forest, Gradient Boosting, ANN |
| **Comparison** | Nested cross-validation (outer: model evaluation, inner: hyperparameter tuning) |
| **Metric** | MAPE (primary), R² (secondary) |
| **Selection criterion** | Lowest mean MAPE across outer folds; if within 1%, prefer simpler model |

---

## Summary Table

| Hypothesis | RQ | Primary test | n required | Success criterion |
|---|---|---|---|---|
| H1a–c | RQ1 | Pearson/Spearman | ≥ 15 | \|r\| > 0.7, p < 0.05 |
| H1d | RQ1 | Fisher z-test | ≥ 30 total | Consistent across grades |
| H2a | RQ2 | Multiple regression | ≥ 30 | p < 0.05 for ≥1 predictor |
| H2b | RQ2 | Mediation/bootstrap | ≥ 50 | CI excludes 0, >50% variance |
| H2c | RQ2 | MANOVA | ≥ 30 | p < 0.05 |
| H3a | RQ3 | Bland-Altman | ≥ 30 | Bias characterised |
| H3b | RQ3 | Wilcoxon | ≥ 20 | p < 0.05 |
| H3c | RQ3 | GUM budget | ≥ 50 meas. | U < 2% |
| H4a | RQ4 | Paired Wilcoxon | ≥ 50 | >10% improvement |
| H4b | RQ4 | Cross-validation | ≥ 50 | MAPE < 15% |
| H4c | RQ4 | LOGO-CV | ≥ 4 grades | R² > 0.5 |
