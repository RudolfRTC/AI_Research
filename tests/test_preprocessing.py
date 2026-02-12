"""Tests for data preprocessing utilities."""

import numpy as np
import pytest

from src.machinability.data.preprocessing import (
    iacs_to_ms_per_m,
    ms_per_m_to_iacs,
    resistivity_to_conductivity,
)


class TestUnitConversions:
    def test_iacs_100_percent(self):
        """100% IACS should equal 58.0 MS/m (annealed copper)."""
        assert iacs_to_ms_per_m(100.0) == pytest.approx(58.0)

    def test_iacs_roundtrip(self):
        """Converting IACS -> MS/m -> IACS should be identity."""
        original = 3.5
        converted = ms_per_m_to_iacs(iacs_to_ms_per_m(original))
        assert converted == pytest.approx(original)

    def test_resistivity_to_conductivity(self):
        """Known value: copper ~1.68 micro-ohm-cm -> ~59.5 MS/m."""
        result = resistivity_to_conductivity(1.68)
        assert result == pytest.approx(0.0595, rel=0.01)

    def test_iacs_array(self):
        """Should work with numpy arrays."""
        arr = np.array([1.0, 2.0, 3.0])
        result = iacs_to_ms_per_m(arr)
        expected = np.array([0.58, 1.16, 1.74])
        np.testing.assert_allclose(result, expected)
