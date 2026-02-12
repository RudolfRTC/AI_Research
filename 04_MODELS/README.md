# 04_MODELS

Hypotheses, statistical models, and machine learning approaches for predicting machinability from conductivity.

## Structure

| Subfolder | Description |
|-----------|-------------|
| `statistical/` | Correlation analysis, regression, mediation models |
| `ml/` | ML model configs, hyperparameter searches, saved results |
| `hypotheses.md` | Formal hypothesis statements and testing criteria |

## Modelling Approaches (RQ4)

- Linear/polynomial regression
- Support Vector Regression (SVR)
- Random Forest / Gradient Boosting
- Artificial Neural Networks (ANN)
- Mediation / path analysis (RQ2)

## Success Criteria

- Prediction MAPE < 15% for tool life
- Cross-validation R² > 0.75
- Model outperforms hardness-only baseline by > 10%
