"""Baseline models for machinability prediction (RQ4).

These serve as benchmarks against which more complex models are compared.
"""

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error, r2_score


class HardnessOnlyBaseline(BaseEstimator, RegressorMixin):
    """Baseline: predict machinability from hardness alone.

    This is the model to beat — if conductivity-based models cannot
    outperform hardness-only prediction, the approach has limited value.
    """

    def __init__(self):
        self.model_ = LinearRegression()

    def fit(self, X, y):
        """Fit linear regression on hardness feature.

        Parameters
        ----------
        X : array-like of shape (n_samples, 1)
            Hardness values (HV, HRC, or HB).
        y : array-like of shape (n_samples,)
            Machinability target (tool life, Ra, etc.).
        """
        self.model_.fit(X, y)
        return self

    def predict(self, X):
        return self.model_.predict(X)

    def score(self, X, y):
        y_pred = self.predict(X)
        return r2_score(y, y_pred)


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Compute standard evaluation metrics.

    Parameters
    ----------
    y_true : array-like
        True target values.
    y_pred : array-like
        Predicted target values.

    Returns
    -------
    dict
        Dictionary with R², MAPE, RMSE.
    """
    return {
        "r2": r2_score(y_true, y_pred),
        "mape": mean_absolute_percentage_error(y_true, y_pred),
        "rmse": float(np.sqrt(np.mean((y_true - y_pred) ** 2))),
    }
