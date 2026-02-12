"""Standard plots for conductivity-machinability research."""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def scatter_with_regression(
    x: np.ndarray,
    y: np.ndarray,
    xlabel: str = "Electrical conductivity (%IACS)",
    ylabel: str = "Machinability metric",
    title: str | None = None,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Scatter plot with linear regression line and R² annotation.

    Parameters
    ----------
    x, y : array-like
        Data arrays.
    xlabel, ylabel : str
        Axis labels.
    title : str, optional
        Plot title.
    ax : matplotlib Axes, optional
        Axes to plot on. Created if not provided.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(x, y, alpha=0.7, edgecolors="k", linewidths=0.5)

    # Linear fit
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() > 2:
        coeffs = np.polyfit(x[mask], y[mask], 1)
        x_line = np.linspace(np.nanmin(x), np.nanmax(x), 100)
        ax.plot(x_line, np.polyval(coeffs, x_line), "r--", linewidth=1.5)

        # R²
        ss_res = np.sum((y[mask] - np.polyval(coeffs, x[mask])) ** 2)
        ss_tot = np.sum((y[mask] - np.mean(y[mask])) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        ax.annotate(f"R² = {r2:.3f}", xy=(0.05, 0.95), xycoords="axes fraction", fontsize=11)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    if title:
        ax.set_title(title, fontsize=13)
    ax.grid(True, alpha=0.3)

    return ax


def steel_grade_comparison(
    df,
    x_col: str,
    y_col: str,
    hue_col: str = "steel_grade",
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> plt.Figure:
    """Scatter plot comparing multiple steel grades.

    Parameters
    ----------
    df : pd.DataFrame
        Data with columns for x, y, and hue.
    x_col, y_col : str
        Column names for axes.
    hue_col : str
        Column for colour grouping (default: steel_grade).
    xlabel, ylabel : str, optional
        Axis labels (default: column names).

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col, style=hue_col, s=80, ax=ax)
    ax.set_xlabel(xlabel or x_col, fontsize=12)
    ax.set_ylabel(ylabel or y_col, fontsize=12)
    ax.legend(title=hue_col, fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig
