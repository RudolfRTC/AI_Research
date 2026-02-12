"""Data preprocessing and unit conversion utilities."""

import numpy as np
import pandas as pd


# Conversion constants
IACS_100_PERCENT_MS_PER_M = 58.0  # 100% IACS = 58.0 MS/m (annealed copper at 20°C)


def iacs_to_ms_per_m(iacs_percent: float | np.ndarray) -> float | np.ndarray:
    """Convert %IACS to MS/m."""
    return iacs_percent / 100.0 * IACS_100_PERCENT_MS_PER_M


def ms_per_m_to_iacs(ms_per_m: float | np.ndarray) -> float | np.ndarray:
    """Convert MS/m to %IACS."""
    return ms_per_m / IACS_100_PERCENT_MS_PER_M * 100.0


def resistivity_to_conductivity(resistivity_uohm_cm: float | np.ndarray) -> float | np.ndarray:
    """Convert resistivity (micro-ohm-cm) to conductivity (MS/m).

    conductivity (MS/m) = 0.1 / resistivity (micro-ohm-cm)
    """
    return 0.1 / resistivity_uohm_cm


def merge_conductivity_machining(
    conductivity_df: pd.DataFrame,
    machining_df: pd.DataFrame,
    on: str = "specimen_id",
) -> pd.DataFrame:
    """Merge conductivity and machining datasets on specimen identifier.

    Parameters
    ----------
    conductivity_df : pd.DataFrame
        Conductivity measurement data.
    machining_df : pd.DataFrame
        Machining test data.
    on : str
        Column name to join on.

    Returns
    -------
    pd.DataFrame
        Merged dataset.
    """
    return pd.merge(conductivity_df, machining_df, on=on, how="inner")
