"""Functions for loading and validating experimental data."""

from pathlib import Path

import pandas as pd

EVIDENCE_MATRIX_PATH = Path(__file__).resolve().parents[3] / "02_EVIDENCE_MATRIX" / "evidence_matrix.csv"


def load_evidence_matrix(path: Path | None = None) -> pd.DataFrame:
    """Load the evidence matrix CSV.

    Parameters
    ----------
    path : Path, optional
        Custom path to evidence matrix CSV. Defaults to the repository's
        ``02_EVIDENCE_MATRIX/evidence_matrix.csv``.

    Returns
    -------
    pd.DataFrame
    """
    path = path or EVIDENCE_MATRIX_PATH
    df = pd.read_csv(path)
    return df


def load_conductivity_data(path: Path) -> pd.DataFrame:
    """Load raw conductivity measurement data from a CSV file.

    Expected columns: specimen_id, measurement_method, value, unit, temp_C

    Parameters
    ----------
    path : Path
        Path to the conductivity data CSV.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_csv(path)
    required = {"specimen_id", "measurement_method", "value", "unit", "temp_C"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in conductivity data: {missing}")
    return df


def load_machining_data(path: Path) -> pd.DataFrame:
    """Load raw machining test data from a CSV file.

    Expected columns: specimen_id, tool, v_m_min, f_mm_rev, d_mm, metric, value

    Parameters
    ----------
    path : Path
        Path to the machining data CSV.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_csv(path)
    required = {"specimen_id", "tool", "v_m_min", "f_mm_rev", "d_mm", "metric", "value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in machining data: {missing}")
    return df
