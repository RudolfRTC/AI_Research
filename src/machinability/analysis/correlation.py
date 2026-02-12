"""Correlation analysis between conductivity and machinability indicators (RQ1)."""

import pandas as pd
from scipy import stats


def pearson_correlation(x: pd.Series, y: pd.Series) -> dict:
    """Compute Pearson correlation with p-value.

    Parameters
    ----------
    x, y : pd.Series
        Paired observations (NaN rows dropped automatically).

    Returns
    -------
    dict
        Keys: r, p_value, n
    """
    mask = x.notna() & y.notna()
    x_clean, y_clean = x[mask], y[mask]
    r, p = stats.pearsonr(x_clean, y_clean)
    return {"r": r, "p_value": p, "n": len(x_clean)}


def spearman_correlation(x: pd.Series, y: pd.Series) -> dict:
    """Compute Spearman rank correlation with p-value.

    Parameters
    ----------
    x, y : pd.Series
        Paired observations (NaN rows dropped automatically).

    Returns
    -------
    dict
        Keys: rho, p_value, n
    """
    mask = x.notna() & y.notna()
    x_clean, y_clean = x[mask], y[mask]
    rho, p = stats.spearmanr(x_clean, y_clean)
    return {"rho": rho, "p_value": p, "n": len(x_clean)}


def correlation_matrix(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Compute pairwise Pearson correlation matrix for selected numeric columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    columns : list of str, optional
        Columns to include. If None, uses all numeric columns.

    Returns
    -------
    pd.DataFrame
        Correlation matrix.
    """
    if columns:
        df = df[columns]
    return df.select_dtypes(include="number").corr(method="pearson")
