# Metrics Definitions

Standard definitions for all metrics used in this research.

---

## Electrical Conductivity Metrics

### %IACS (International Annealed Copper Standard)

- **Definition:** Electrical conductivity expressed as a percentage of the conductivity of annealed copper at 20 °C.
- **Reference:** 100 %IACS = 58.0 MS/m = 1.7241 μΩ·cm resistivity
- **Typical range for low-alloy steels:** 2–8 %IACS

### MS/m (Mega-Siemens per metre)

- **Definition:** SI unit of electrical conductivity.
- **Conversion:** conductivity (MS/m) = %IACS × 0.58

### μΩ·cm (Micro-ohm centimetre)

- **Definition:** CGS unit of electrical resistivity.
- **Conversion:** conductivity (MS/m) = 0.1 / resistivity (μΩ·cm)

### Temperature Correction

- **Standard reference:** 20 °C
- **Coefficient:** For steels, approximately +0.4 %/°C (resistivity increases with temperature)
- **Formula:** ρ(T) = ρ₂₀ × [1 + α(T − 20)], where α ≈ 0.004 /°C for low-alloy steels

---

## Machinability Metrics

### VB — Flank Wear (mm)

- **Definition:** Width of the wear land on the flank face of the cutting tool, measured in the zone B (per ISO 3685).
- **Tool life criterion:** VB = 0.3 mm (uniform wear) or VBmax = 0.6 mm (localised wear)
- **Measurement:** Optical microscope or toolmaker's microscope at 20–50× magnification.

### Ra — Arithmetic Mean Surface Roughness (μm)

- **Definition:** Arithmetic average of absolute values of the profile deviations from the mean line, per ISO 4287.
- **Measurement:** Stylus profilometer with cut-off length λc = 0.8 mm (typical for turned surfaces).
- **Typical range:** 0.4–6.3 μm for finish turning of steels.

### Fc — Main Cutting Force (N)

- **Definition:** Component of the resultant cutting force in the direction of the cutting velocity vector.
- **Measurement:** 3-component piezoelectric dynamometer (e.g., Kistler 9257B).
- **Related:** Specific cutting energy kc = Fc / (f × ap) in N/mm².

### Tool Life T (min)

- **Definition:** Cutting time to reach the tool life criterion (VB = 0.3 mm).
- **Standard:** ISO 3685 for single-point turning tools.
- **Taylor equation:** VT^n = C, where V = cutting speed, n = Taylor exponent, C = constant.

### Machinability Index / Rating (%)

- **Definition:** Ratio of cutting speed of test material to cutting speed of reference material (AISI B1112 = 100%) for same tool life.
- **Formula:** MI = (V₆₀_test / V₆₀_ref) × 100%

---

## Statistical Metrics

### R² — Coefficient of Determination

- **Definition:** Proportion of variance in the dependent variable explained by the model.
- **Formula:** R² = 1 − (SS_res / SS_tot)
- **Range:** 0 to 1 (higher is better). Success criterion: R² > 0.75

### MAPE — Mean Absolute Percentage Error

- **Definition:** Average of absolute percentage errors between predicted and actual values.
- **Formula:** MAPE = (1/n) Σ |yᵢ − ŷᵢ| / |yᵢ| × 100%
- **Success criterion:** MAPE < 15% for tool life prediction

### RMSE — Root Mean Square Error

- **Definition:** Square root of the mean of squared residuals.
- **Formula:** RMSE = √[(1/n) Σ (yᵢ − ŷᵢ)²]
- **Units:** Same as the target variable.

### Pearson r — Pearson Correlation Coefficient

- **Definition:** Measure of linear correlation between two continuous variables.
- **Range:** −1 to +1
- **Success criterion:** |r| > 0.7 for at least one machinability indicator (RQ1)

### Spearman ρ — Spearman Rank Correlation

- **Definition:** Non-parametric measure of rank correlation (monotonic relationship).
- **Range:** −1 to +1
- **Use case:** When relationship may be monotonic but not necessarily linear.

### p-value

- **Definition:** Probability of observing the test statistic (or more extreme) under the null hypothesis.
- **Significance threshold:** p < 0.05 (used throughout this research)

---

## Measurement Uncertainty

### Gauge R&R (Repeatability and Reproducibility)

- **Repeatability:** Variation from repeated measurements by the same operator with the same equipment.
- **Reproducibility:** Variation from different operators or equipment.
- **Acceptable:** Total Gauge R&R < 10% of tolerance range.

### Expanded Uncertainty U

- **Definition:** Half-width of the confidence interval at 95% confidence level.
- **Formula:** U = k × u_c, where k = 2 (coverage factor) and u_c = combined standard uncertainty.
- **Target:** U < 2% of measured conductivity value (RQ3).
