# Dissertation Outline

**Title:** Determining Machinability of Low-Alloy Steels via Electrical Conductivity Measurements

**Candidate:** [Name]
**Supervisor(s):** [Name(s)]
**Programme:** [Doctoral Programme, University]
**Estimated total length:** 200--250 pages (excluding appendices)

---

## Chapter 1: Introduction

**Estimated length:** 15--20 pages

### 1.1 Background and Motivation
- Economic cost of machining trials in the steel supply chain
- The need for rapid, non-destructive machinability screening
- Electrical conductivity as a physically motivated proxy property

### 1.2 Problem Statement
- No validated, quantitative link between conductivity and machinability for low-alloy steels
- Existing machinability indices rely on destructive or empirical methods
- Gap between microstructure--property science and shop-floor prediction tools

### 1.3 Research Aim and Objectives
- Aim: develop and validate a conductivity-based machinability prediction framework
- Objective 1: Quantify conductivity--machinability correlations (RQ1)
- Objective 2: Identify microstructural mediating mechanisms (RQ2)
- Objective 3: Evaluate and compare measurement methods (RQ3)
- Objective 4: Build and validate a predictive model (RQ4)

### 1.4 Research Questions
- RQ1--RQ4 with sub-questions (reference to `00_README/research_questions.md`)

### 1.5 Scope and Delimitations
- Steel grades: AISI 1045, 4140, 4340
- Heat treatment conditions: annealed, normalised, quenched & tempered
- Machining process: longitudinal turning (ISO 3685 framework)
- Conductivity methods: four-probe DC and eddy current

### 1.6 Contributions of This Work
- First systematic paired conductivity--machinability dataset for three low-alloy steel grades
- Mediation model linking microstructure to both properties
- Validated ML prediction model with practical accuracy targets
- Measurement method recommendation for industrial adoption

### 1.7 Dissertation Structure
- Chapter-by-chapter roadmap

**Key figures/tables:**
- Table 1.1: Summary of research questions, methods, and success criteria
- Figure 1.1: Conceptual diagram of the conductivity--microstructure--machinability chain

---

## Chapter 2: Literature Review

**Estimated length:** 45--55 pages

### 2.1 Machinability of Low-Alloy Steels
#### 2.1.1 Definitions and Metrics
- Tool wear (VB, crater wear), surface roughness (Ra), cutting forces (Fc)
- Tool life criteria per ISO 3685
- Machinability indices and rating systems (AISI B1112 = 100% baseline)
#### 2.1.2 Machinability of AISI 1045, 4140, and 4340
- Composition--property relationships
- Effect of heat treatment on machinability
- Published machinability data and benchmarks
#### 2.1.3 Factors Influencing Machinability
- Workpiece hardness, strength, and ductility
- Microstructural features: grain size, phase fractions, inclusions
- Cutting parameters: speed, feed, depth of cut
- Tool material and geometry

### 2.2 Electrical Conductivity and Microstructure of Steels
#### 2.2.1 Electron Transport in Metals
- Drude--Sommerfeld model; Bloch--Gruneisen theory
- Matthiessen's rule: contributions of phonons, impurities, grain boundaries, dislocations
#### 2.2.2 Effect of Alloying Elements
- Solid-solution scattering (C, Mn, Cr, Mo, Ni)
- Precipitate scattering (carbides, nitrides)
#### 2.2.3 Effect of Microstructure and Heat Treatment
- Ferrite, pearlite, bainite, martensite: conductivity ranges
- Grain size dependence (grain boundary scattering)
- Tempering effects on conductivity recovery
#### 2.2.4 Conductivity as a Non-Destructive Indicator
- Prior work correlating conductivity with hardness and mechanical properties
- Gaps: lack of direct conductivity--machinability studies

### 2.3 Conductivity Measurement Methods
#### 2.3.1 Four-Probe DC Method
- Principle, ASTM B193 standard
- Advantages: absolute measurement, well-characterised uncertainty
- Limitations: contact resistance, specimen preparation
#### 2.3.2 Eddy Current Method
- Principle, ASTM E1004 standard
- Advantages: non-contact, speed, portability
- Complications: magnetic permeability in ferromagnetic steels, lift-off, frequency selection
#### 2.3.3 Emerging Techniques
- Pulsed eddy current (PEC), terahertz conductivity
- Contactless methods for in-line monitoring
#### 2.3.4 Measurement Uncertainty and Traceability
- Sources of error, calibration, reference materials

### 2.4 Machine Learning in Manufacturing and Machinability Prediction
#### 2.4.1 Overview of ML Approaches
- Supervised learning: regression (linear, SVR, ANN, RF, gradient boosting)
- Feature engineering for materials data
#### 2.4.2 ML for Tool Wear and Surface Roughness Prediction
- Sensor-based approaches (force, vibration, AE)
- Composition-based and property-based models
#### 2.4.3 ML for Conductivity--Property Relationships
- Prior work using conductivity as an input feature
#### 2.4.4 Model Validation and Generalisation
- Cross-validation, leave-one-group-out, extrapolation risk

### 2.5 Research Gaps and Positioning
- Summary table mapping literature to RQ1--RQ4
- Identification of specific gaps this dissertation addresses

**Key figures/tables:**
- Table 2.1: Machinability data for AISI 1045, 4140, 4340 from published literature
- Table 2.2: Electrical conductivity ranges for different steel microstructures
- Table 2.3: Comparison of conductivity measurement methods
- Table 2.4: Summary of ML models used in machinability prediction literature
- Figure 2.1: Schematic of electron scattering mechanisms in low-alloy steels
- Figure 2.2: Literature map showing research gap at conductivity--machinability intersection
- Figure 2.3: Evidence matrix heat map (papers vs. research questions)

---

## Chapter 3: Theoretical Framework

**Estimated length:** 20--25 pages

### 3.1 The Conductivity--Microstructure--Machinability Chain
- Physical reasoning: microstructure as the common causal factor
- Conductivity path: lattice defects, grain boundaries, phase boundaries, precipitates scatter electrons
- Machinability path: the same features control deformation, chip formation, friction, and tool wear
- Conceptual causal diagram

### 3.2 Electron Scattering and Matthiessen's Rule
- Decomposition of resistivity: rho = rho_phonon + rho_impurity + rho_GB + rho_dislocation + rho_precipitate
- Quantitative estimates for each contribution in low-alloy steels
- Temperature normalisation strategy

### 3.3 Microstructure--Machinability Relationships
- Grain size: Hall--Petch strengthening and its effect on cutting forces
- Phase composition: hardness, ductility, and chip morphology
- Precipitates: abrasive wear mechanism on tool flank
- Theoretical linking functions between microstructural descriptors and machinability indicators

### 3.4 Mediation and Path Analysis Framework
- Statistical mediation: conductivity -> microstructure -> machinability
- Baron and Kenny conditions for mediation
- Structural equation modelling (SEM) approach for multi-mediator models
- Expected path coefficients and testable implications

### 3.5 Predictive Modelling Framework
- Input feature space: conductivity, hardness, composition
- Target outputs: tool life, Ra, Fc
- Model selection rationale: interpretable vs. black-box trade-off
- Baseline models: hardness-only, composition-only

### 3.6 Summary of Testable Hypotheses
- Cross-reference to `04_MODELS/hypotheses.md`
- Visual summary of hypotheses mapped to the causal chain

**Key figures/tables:**
- Figure 3.1: Causal diagram: composition -> heat treatment -> microstructure -> {conductivity, machinability}
- Figure 3.2: Matthiessen's rule decomposition for a representative AISI 4140 sample
- Figure 3.3: Mediation model diagram with expected sign of each path
- Figure 3.4: Predictive modelling pipeline schematic
- Table 3.1: Summary of theoretical predictions for each hypothesis

---

## Chapter 4: Experimental Methods

**Estimated length:** 30--35 pages

### 4.1 Materials
#### 4.1.1 Steel Grade Selection
- AISI 1045 (plain carbon baseline), 4140 (Cr-Mo), 4340 (Ni-Cr-Mo)
- Justification: range of alloying content, wide industrial use, availability
#### 4.1.2 Chemical Composition
- Spectrometric analysis (OES) of as-received stock
- Comparison to nominal specifications
#### 4.1.3 Heat Treatment Matrix
- Annealed, normalised, quenched & tempered (3 tempering temperatures)
- Minimum 5 conditions per grade = 15+ material conditions total
- Furnace parameters, quench media, holding times
#### 4.1.4 Specimen Preparation
- Bar stock dimensions for machining tests (diameter, length)
- Disc specimens for conductivity and metallography
- Surface preparation protocols

### 4.2 Conductivity Measurements
#### 4.2.1 Four-Probe DC Setup
- Equipment: Keithley 2182A nanovoltmeter + 6220 current source (or equivalent)
- Probe spacing, current level, measurement sequence
- ASTM B193 compliance
#### 4.2.2 Eddy Current Setup
- Equipment: impedance analyser or commercial EC instrument
- Frequency range: 100 Hz -- 10 MHz (RQ3d investigation)
- Lift-off control, probe calibration
- ASTM E1004 compliance
#### 4.2.3 Calibration and Reference Materials
- Certified conductivity standards (copper, aluminium, steel references)
- Temperature monitoring and correction to 20 degC
#### 4.2.4 Repeatability and Uncertainty Protocol
- 10 measurements per specimen per method (RQ3a requirement)
- Gauge R&R study design
- Uncertainty budget following GUM

### 4.3 Machining Tests
#### 4.3.1 Turning Setup
- Lathe specification (CNC vs. engine lathe)
- Tool: coated carbide insert, ISO designation (e.g., CNMG 120408)
- Dry or controlled coolant conditions
#### 4.3.2 Cutting Parameter Matrix
- Cutting speed: 3 levels (e.g., 150, 200, 250 m/min)
- Feed: 3 levels (e.g., 0.10, 0.15, 0.20 mm/rev)
- Depth of cut: fixed at 1.5 mm (or 2 levels)
- Factorial or fractional factorial design
#### 4.3.3 Tool Wear Measurement
- Flank wear VB measured via toolmaker's microscope at defined intervals
- Tool life criterion: VB = 0.3 mm (ISO 3685)
#### 4.3.4 Cutting Force Measurement
- Three-component dynamometer (Kistler 9257B or equivalent)
- Fc, Ff, Fp acquisition and processing
#### 4.3.5 Surface Roughness Measurement
- Stylus profilometer, Ra evaluation length per ISO 4287
- Measurement positions along workpiece length

### 4.4 Microstructural Characterisation
#### 4.4.1 Optical Metallography
- Mounting, polishing (up to 0.05 um alumina or colloidal silica)
- Etchants: 2% Nital, Picral, Vilella's reagent (as appropriate)
#### 4.4.2 Grain Size Measurement
- ASTM E112 linear intercept method
- Automated image analysis
#### 4.4.3 Phase Quantification
- X-ray diffraction (XRD) for phase fractions (austenite, ferrite, cementite)
- EBSD for grain orientation and phase mapping (selected specimens)
#### 4.4.4 Hardness Testing
- Vickers microhardness (HV0.5 or HV1) maps
- Bulk Rockwell or Brinell hardness
#### 4.4.5 SEM and EDS
- Precipitate imaging and semi-quantitative composition
- Fractography of chips (selected conditions)

### 4.5 Experimental Design and Sample Size
- Full test matrix: grades x heat treatments x cutting parameters
- Minimum sample sizes justified per power analysis (reference `04_MODELS/hypotheses.md`)
- Randomisation and blocking strategy

### 4.6 Data Management
- Data recording, file naming conventions
- Integration with MLflow experiment tracking
- Quality assurance checks

**Key figures/tables:**
- Table 4.1: Chemical composition of as-received steel stock
- Table 4.2: Heat treatment matrix (grade x condition x parameters)
- Table 4.3: Cutting parameter matrix (full factorial design)
- Table 4.4: Measurement uncertainty budget for four-probe DC and eddy current
- Figure 4.1: Photographs of experimental setups (conductivity, turning, metallography)
- Figure 4.2: Schematic of four-probe DC measurement arrangement
- Figure 4.3: Eddy current probe configuration and frequency sweep plan
- Figure 4.4: Experimental flowchart from specimen preparation to data analysis

---

## Chapter 5: Results and Discussion

**Estimated length:** 50--60 pages

### 5.1 Material Characterisation Summary
- Verified compositions (OES results)
- Microstructures achieved per heat treatment condition (optical micrographs)
- Hardness results across all conditions
- Table of material conditions tested

### 5.2 Results for RQ1: Conductivity--Machinability Relationship
#### 5.2.1 Conductivity Measurements Across All Conditions
- Conductivity values (%IACS and MS/m) for all grade--heat-treatment combinations
- Observed trends: effect of alloying and heat treatment on conductivity
#### 5.2.2 Machinability Results
- Tool life, cutting forces, and surface roughness for all conditions
- Taylor tool life curves
#### 5.2.3 Correlation Analysis
- Pearson and Spearman correlation coefficients for conductivity vs. VB, Ra, Fc
- Identification of strongest correlated indicator (RQ1a)
- Scatter plots with regression fits
#### 5.2.4 Linearity and Functional Form (RQ1b)
- Linear, logarithmic, power-law, and polynomial fits
- Model comparison via AIC/BIC
#### 5.2.5 Cross-Grade Consistency (RQ1c)
- Comparison of correlation coefficients across AISI 1045, 4140, 4340
- ANCOVA or interaction analysis
#### 5.2.6 Effect of Cutting Parameters (RQ1d)
- How speed, feed, and depth of cut moderate the conductivity--machinability relationship
- Interaction plots

### 5.3 Results for RQ2: Microstructural Mediation
#### 5.3.1 Grain Size and Conductivity
- Grain size vs. conductivity scatter plots
- Regression and ANOVA by heat treatment group
#### 5.3.2 Phase Composition and Conductivity
- XRD/EBSD phase fractions vs. conductivity
- Ferrite--pearlite vs. tempered martensite clusters
#### 5.3.3 Grain Size and Phase Effects on Machinability
- Grain size vs. cutting forces, tool life, Ra
- Phase composition vs. machinability indicators
#### 5.3.4 Mediation Analysis (RQ2c)
- Path analysis results: direct and indirect effects
- Proportion of conductivity--machinability correlation explained by microstructure
- SEM model fit statistics (CFI, RMSEA, SRMR)
#### 5.3.5 Heat Treatment Clusters (RQ2d)
- Discriminant analysis or cluster analysis of conductivity--machinability space
- Distinct regions for annealed, normalised, Q&T conditions

### 5.4 Results for RQ3: Measurement Method Comparison
#### 5.4.1 Repeatability and Reproducibility
- Gauge R&R results for four-probe DC and eddy current
- Measurement uncertainty (expanded uncertainty, k = 2)
#### 5.4.2 Accuracy Against Reference Standards (RQ3a)
- Deviation from certified reference materials
- Systematic bias assessment
#### 5.4.3 Surface Condition Sensitivity (RQ3b)
- Effect of surface roughness, oxide layer, residual stress on each method
- Robustness comparison
#### 5.4.4 Eddy Current for Ferromagnetic Steels (RQ3c)
- Permeability compensation strategies
- Achievable accuracy for relative conductivity ranking
#### 5.4.5 Frequency Optimisation (RQ3d)
- Sensitivity vs. frequency plots
- Optimal frequency range for machinability-relevant features
#### 5.4.6 Method Recommendation
- Decision matrix: accuracy, practicality, cost, in-line capability
- Recommended method and conditions for industrial adoption

### 5.5 Integrated Discussion
- Synthesis across RQ1--RQ3
- Comparison with published literature
- Physical interpretation of key findings
- Limitations and caveats

**Key figures/tables:**
- Table 5.1: Conductivity and hardness for all material conditions
- Table 5.2: Machinability results summary (tool life, Ra, Fc) for all conditions
- Table 5.3: Correlation matrix (conductivity vs. machinability indicators)
- Table 5.4: Mediation analysis path coefficients and significance
- Table 5.5: Gauge R&R results for both measurement methods
- Table 5.6: Measurement method decision matrix
- Figure 5.1: Representative micrographs for each grade and heat treatment
- Figure 5.2: Conductivity vs. tool life scatter plots by grade
- Figure 5.3: Conductivity vs. cutting forces by grade
- Figure 5.4: Conductivity vs. surface roughness by grade
- Figure 5.5: Taylor tool life curves grouped by conductivity bands
- Figure 5.6: Mediation path diagram with estimated coefficients
- Figure 5.7: Heat treatment cluster plot in conductivity--machinability space
- Figure 5.8: Gauge R&R bar charts for each measurement method
- Figure 5.9: Eddy current sensitivity vs. frequency

---

## Chapter 6: Predictive Model Development (RQ4)

**Estimated length:** 30--35 pages

### 6.1 Feature Engineering and Data Preparation
#### 6.1.1 Input Features
- Primary: electrical conductivity (%IACS)
- Secondary: Vickers hardness, composition (C, Mn, Cr, Mo, Ni wt.%)
- Derived: conductivity x hardness interaction, conductivity/hardness ratio
#### 6.1.2 Target Variables
- Tool life (minutes to VB = 0.3 mm)
- Surface roughness Ra (um)
- Main cutting force Fc (N)
#### 6.1.3 Data Cleaning and Normalisation
- Outlier detection and handling
- Feature scaling (standardisation, min-max)
#### 6.1.4 Train--Validation--Test Split Strategy
- 70/15/15 split stratified by steel grade
- Leave-one-grade-out cross-validation for generalisation assessment (RQ4c)

### 6.2 Baseline Models
#### 6.2.1 Hardness-Only Model
- Linear and polynomial regression: hardness -> tool life, Ra, Fc
- Performance metrics: R^2, RMSE, MAPE
#### 6.2.2 Composition-Only Model
- Multiple regression: C, Mn, Cr, Mo, Ni -> targets
- Performance comparison

### 6.3 Conductivity-Augmented Models
#### 6.3.1 Linear and Polynomial Regression
- Conductivity + hardness + composition as inputs
- Comparison to baselines
#### 6.3.2 Support Vector Regression (SVR)
- Kernel selection (RBF, polynomial)
- Hyperparameter tuning (C, epsilon, gamma) via grid search with CV
#### 6.3.3 Random Forest and Gradient Boosting
- Tree-based ensemble models
- Hyperparameter tuning (n_estimators, max_depth, learning_rate)
- Feature importance analysis
#### 6.3.4 Artificial Neural Networks (ANN)
- Architecture: input--hidden--output layers
- Hyperparameter tuning (hidden units, layers, dropout, learning rate)
- Early stopping and regularisation

### 6.4 Model Comparison and Selection (RQ4a)
- Performance summary table (R^2, RMSE, MAPE for all models and targets)
- Statistical comparison (paired t-test on cross-validation folds)
- Trade-off: accuracy vs. interpretability vs. data efficiency
- Minimum dataset size analysis (RQ4b): learning curves

### 6.5 Generalisation Assessment (RQ4c)
- Leave-one-grade-out results
- Discussion of extrapolation risk
- Conditions for reliable out-of-sample prediction

### 6.6 Practical Prediction Accuracy (RQ4d)
- Final model RMSE and MAPE on held-out test set
- Tool life prediction: actual vs. predicted plots
- Surface roughness prediction: actual vs. predicted plots
- Comparison against target thresholds (+/- 15% tool life, +/- 0.3 um Ra)

### 6.7 Model Interpretation
- SHAP values or permutation importance for best model
- Physical consistency check: do feature effects align with theory?
- Partial dependence plots for conductivity

### 6.8 Implementation Considerations
- Input requirements for practical deployment
- Sensitivity analysis: effect of conductivity measurement uncertainty on prediction
- Recommended workflow for industrial users

**Key figures/tables:**
- Table 6.1: Input features and their sources
- Table 6.2: Baseline model performance (hardness-only, composition-only)
- Table 6.3: Full model comparison matrix (all models x all targets x metrics)
- Table 6.4: Leave-one-grade-out generalisation results
- Table 6.5: Best model hyperparameters and final test-set performance
- Figure 6.1: Feature importance bar chart (best model)
- Figure 6.2: Learning curves (performance vs. training set size)
- Figure 6.3: Actual vs. predicted scatter plots for tool life and Ra
- Figure 6.4: SHAP summary plot
- Figure 6.5: Partial dependence plots for conductivity, hardness, and composition
- Figure 6.6: Prediction error distribution (histogram and Q-Q plot)
- Figure 6.7: Practical deployment workflow diagram

---

## Chapter 7: Conclusions and Future Work

**Estimated length:** 10--15 pages

### 7.1 Summary of Findings
- RQ1: Nature and strength of conductivity--machinability relationship
- RQ2: Microstructural mediation mechanisms
- RQ3: Measurement method recommendation
- RQ4: Predictive model performance and practical utility

### 7.2 Contributions to Knowledge
- Empirical: first systematic paired dataset
- Theoretical: mediation model and causal framework
- Practical: validated prediction tool and measurement protocol
- Methodological: cross-grade generalisation assessment approach

### 7.3 Limitations
- Steel grade and heat treatment scope
- Single machining process (turning)
- Sample size constraints
- Measurement method limitations for ferromagnetic materials

### 7.4 Recommendations for Industry
- Measurement method selection guidelines
- Minimum data requirements for model deployment
- Integration into quality control workflow

### 7.5 Future Work
- Extension to additional steel families (stainless, tool steels, HSLA)
- Other machining processes (milling, drilling, grinding)
- In-line eddy current monitoring integration
- Deep learning with larger datasets
- Multi-objective optimisation (machinability + conductivity + mechanical properties)
- Temperature-dependent conductivity for hot machining prediction

### 7.6 Closing Remarks

**Key figures/tables:**
- Table 7.1: Summary of hypotheses and outcomes (accept/reject)
- Table 7.2: Contribution matrix (contribution x novelty x impact)
- Figure 7.1: Roadmap of future research directions

---

## Back Matter

### References
- Estimated 150--200 references
- Managed via BibTeX (`01_LITERATURE/library.bib`)

### Appendices
**Estimated length:** 20--30 pages

#### Appendix A: Raw Data Tables
- Complete conductivity measurements (all specimens, all methods)
- Complete machining test results

#### Appendix B: Statistical Analysis Details
- Full correlation matrices
- Mediation model diagnostics
- ANOVA tables

#### Appendix C: ML Model Hyperparameters and Training Logs
- Grid search results
- Learning curves for all models
- MLflow experiment summaries

#### Appendix D: Equipment Calibration Certificates and Uncertainty Budgets

#### Appendix E: Published Papers and Conference Contributions

---

## Page Count Summary

| Chapter | Estimated Pages |
|---------|----------------|
| Chapter 1: Introduction | 15--20 |
| Chapter 2: Literature Review | 45--55 |
| Chapter 3: Theoretical Framework | 20--25 |
| Chapter 4: Experimental Methods | 30--35 |
| Chapter 5: Results and Discussion | 50--60 |
| Chapter 6: Predictive Model Development | 30--35 |
| Chapter 7: Conclusions and Future Work | 10--15 |
| References | 10--15 |
| Appendices | 20--30 |
| **Total** | **230--290** |

## Figure and Table Count Estimate

| Chapter | Figures | Tables |
|---------|---------|--------|
| Chapter 1 | 1 | 1 |
| Chapter 2 | 3 | 4 |
| Chapter 3 | 4 | 1 |
| Chapter 4 | 4 | 4 |
| Chapter 5 | 9 | 6 |
| Chapter 6 | 7 | 5 |
| Chapter 7 | 1 | 2 |
| **Total** | **29** | **23** |
