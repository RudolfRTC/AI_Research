"""Tests for correlation analysis functions."""

import pandas as pd
import pytest

from src.machinability.analysis.correlation import (
    correlation_matrix,
    pearson_correlation,
    spearman_correlation,
)


class TestCorrelation:
    def test_perfect_positive_pearson(self):
        x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
        result = pearson_correlation(x, y)
        assert result["r"] == pytest.approx(1.0)
        assert result["n"] == 5

    def test_perfect_negative_spearman(self):
        x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        y = pd.Series([10.0, 8.0, 6.0, 4.0, 2.0])
        result = spearman_correlation(x, y)
        assert result["rho"] == pytest.approx(-1.0)

    def test_handles_nan(self):
        x = pd.Series([1.0, 2.0, None, 4.0, 5.0])
        y = pd.Series([2.0, 4.0, 6.0, None, 10.0])
        result = pearson_correlation(x, y)
        assert result["n"] == 3  # Only rows where both are non-null

    def test_correlation_matrix_shape(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        result = correlation_matrix(df)
        assert result.shape == (3, 3)
