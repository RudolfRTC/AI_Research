"""
Data Visualization & Correlation Analysis Page (RQ1).

Provides interactive exploration of the relationship between electrical
conductivity and machinability metrics for low-alloy steels.

Usage:
    import gui.pages.analysis as analysis_page
    analysis_page.render()
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_EVIDENCE_CSV = Path(__file__).resolve().parents[2] / "02_EVIDENCE_MATRIX" / "evidence_matrix.csv"

_STEEL_GRADES = ["AISI 1045", "AISI 4140", "AISI 4340"]

_NUMERIC_COLS = [
    "conductivity_%IACS",
    "tool_life_min",
    "Ra_um",
    "Fc_N",
    "hardness_HV",
]

_COL_LABELS: dict[str, str] = {
    "conductivity_%IACS": "Conductivity (%IACS)",
    "tool_life_min": "Tool Life (min)",
    "Ra_um": "Surface Roughness Ra (\u03bcm)",
    "Fc_N": "Cutting Force Fc (N)",
    "hardness_HV": "Hardness (HV)",
    "steel_grade": "Steel Grade",
}

_RNG_SEED = 42

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------


def _load_real_data() -> pd.DataFrame | None:
    """Attempt to load evidence_matrix.csv and return it if it has enough
    numeric rows for meaningful correlation analysis (>= 5 rows with at least
    two numeric columns)."""
    if not _EVIDENCE_CSV.exists():
        return None
    try:
        df = pd.read_csv(_EVIDENCE_CSV)
    except Exception:
        return None

    numeric_df = df.select_dtypes(include="number")
    if numeric_df.dropna(how="all").shape[0] < 5 or numeric_df.shape[1] < 2:
        return None
    return df


def _generate_demo_data(n: int = 50) -> pd.DataFrame:
    """Generate physically-plausible synthetic data for three steel grades.

    The synthetic relationships mirror established metallurgical trends:
    * Higher-alloy steels (4340) have lower conductivity and are harder to
      machine (lower tool life, higher forces, rougher surfaces).
    * Conductivity is inversely correlated with hardness within each grade.
    * Tool life drops with conductivity (harder material -> lower conductivity
      -> shorter tool life) with realistic scatter.
    """
    rng = np.random.default_rng(_RNG_SEED)

    grade_params: dict[str, dict[str, tuple[float, float]]] = {
        "AISI 1045": {
            "conductivity": (5.5, 0.50),
            "hardness": (210, 20),
        },
        "AISI 4140": {
            "conductivity": (4.0, 0.45),
            "hardness": (290, 25),
        },
        "AISI 4340": {
            "conductivity": (3.0, 0.40),
            "hardness": (350, 30),
        },
    }

    rows: list[dict] = []
    per_grade = n // len(_STEEL_GRADES)
    remainder = n - per_grade * len(_STEEL_GRADES)

    for idx, grade in enumerate(_STEEL_GRADES):
        count = per_grade + (1 if idx < remainder else 0)
        p = grade_params[grade]

        cond = rng.normal(p["conductivity"][0], p["conductivity"][1], size=count)
        cond = np.clip(cond, 2.0, 7.0)

        hv = rng.normal(p["hardness"][0], p["hardness"][1], size=count)
        hv = np.clip(hv, 150, 450)

        # Tool life inversely related to hardness (and thus to lower conductivity)
        tool_life = 80 - 0.15 * hv + rng.normal(0, 3.5, size=count)
        tool_life = np.clip(tool_life, 5, 70)

        # Surface roughness increases with hardness
        ra = 0.3 + 0.004 * hv + rng.normal(0, 0.18, size=count)
        ra = np.clip(ra, 0.3, 3.5)

        # Cutting force increases with hardness
        fc = 200 + 1.8 * hv + rng.normal(0, 40, size=count)
        fc = np.clip(fc, 200, 1200)

        for i in range(count):
            rows.append(
                {
                    "steel_grade": grade,
                    "conductivity_%IACS": round(float(cond[i]), 2),
                    "tool_life_min": round(float(tool_life[i]), 1),
                    "Ra_um": round(float(ra[i]), 2),
                    "Fc_N": round(float(fc[i]), 1),
                    "hardness_HV": round(float(hv[i]), 0),
                }
            )

    return pd.DataFrame(rows)


def _get_data(use_demo: bool) -> pd.DataFrame:
    """Return the appropriate dataframe based on user toggle."""
    if use_demo:
        return _generate_demo_data()
    real = _load_real_data()
    if real is not None:
        return real
    return _generate_demo_data()


def _friendly(col: str) -> str:
    """Return a human-readable label for a column name."""
    return _COL_LABELS.get(col, col)


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------


def _render_data_toggle() -> bool:
    """Show a toggle switch and return whether demo data should be used."""
    real_available = _load_real_data() is not None

    if real_available:
        label = "Use demo data (synthetic 50-specimen dataset)"
    else:
        label = (
            "Use demo data  \u2014  *real data in `evidence_matrix.csv` has "
            "insufficient numeric rows; demo data is active by default*"
        )

    use_demo = st.toggle(label, value=True)
    return use_demo


def _render_scatter(df: pd.DataFrame) -> None:
    """Interactive scatter plot with selectable axes, trendline, and
    Pearson statistics."""
    st.subheader("Interactive Scatter Plots")

    col_left, col_right = st.columns(2)
    x_options = [c for c in _NUMERIC_COLS if c in df.columns]
    y_options = [c for c in _NUMERIC_COLS if c in df.columns]

    with col_left:
        x_col = st.selectbox(
            "X axis",
            options=x_options,
            format_func=_friendly,
            index=0,
            key="scatter_x",
        )
    with col_right:
        default_y = 1 if len(y_options) > 1 else 0
        y_col = st.selectbox(
            "Y axis",
            options=y_options,
            format_func=_friendly,
            index=default_y,
            key="scatter_y",
        )

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color="steel_grade",
        trendline="ols",
        labels={x_col: _friendly(x_col), y_col: _friendly(y_col), "steel_grade": "Steel Grade"},
        title=f"{_friendly(y_col)} vs {_friendly(x_col)}",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hover_data={c: True for c in _NUMERIC_COLS if c in df.columns},
    )
    fig.update_layout(
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Pearson r and p-value (overall)
    valid = df[[x_col, y_col]].dropna()
    if len(valid) >= 3:
        r_val, p_val = stats.pearsonr(valid[x_col], valid[y_col])
        significance = (
            "significant" if p_val < 0.05 else "not significant"
        )
        st.markdown(
            f"**Overall Pearson r = {r_val:.3f}**, "
            f"p-value = {p_val:.2e} ({significance} at \u03b1 = 0.05)"
        )

        # Per-grade statistics
        per_grade_parts: list[str] = []
        for grade in sorted(df["steel_grade"].unique()):
            subset = df.loc[df["steel_grade"] == grade, [x_col, y_col]].dropna()
            if len(subset) >= 3:
                r_g, p_g = stats.pearsonr(subset[x_col], subset[y_col])
                per_grade_parts.append(f"{grade}: r={r_g:.3f} (p={p_g:.2e})")
        if per_grade_parts:
            st.caption("Per-grade: " + " | ".join(per_grade_parts))
    else:
        st.info("Not enough valid data points to compute Pearson correlation.")


def _render_heatmap(df: pd.DataFrame) -> None:
    """Correlation heatmap for all numeric columns."""
    st.subheader("Correlation Heatmap")

    numeric_df = df[[c for c in _NUMERIC_COLS if c in df.columns]].dropna()
    if numeric_df.shape[0] < 3:
        st.warning("Not enough data to compute correlations.")
        return

    corr = numeric_df.corr(method="pearson")

    labels = [_friendly(c) for c in corr.columns]

    # Build annotation text matrix
    text_matrix = [[f"{corr.iloc[i, j]:.2f}" for j in range(corr.shape[1])] for i in range(corr.shape[0])]

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=labels,
            y=labels,
            text=text_matrix,
            texttemplate="%{text}",
            textfont=dict(size=13),
            colorscale="RdBu_r",
            zmid=0,
            zmin=-1,
            zmax=1,
            colorbar=dict(title="r"),
        )
    )
    fig.update_layout(
        title="Pearson Correlation Matrix",
        template="plotly_white",
        width=700,
        height=600,
        xaxis=dict(tickangle=-40),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_distributions(df: pd.DataFrame) -> None:
    """Histograms and box plots for each numeric variable, grouped by steel
    grade."""
    st.subheader("Distribution Plots")

    plot_type = st.radio(
        "Plot type",
        options=["Histogram", "Box plot"],
        horizontal=True,
        key="dist_plot_type",
    )

    cols_present = [c for c in _NUMERIC_COLS if c in df.columns]
    # Show two plots per row
    for i in range(0, len(cols_present), 2):
        row_cols = st.columns(2)
        for j, st_col in enumerate(row_cols):
            idx = i + j
            if idx >= len(cols_present):
                break
            col_name = cols_present[idx]
            with st_col:
                if plot_type == "Histogram":
                    fig = px.histogram(
                        df,
                        x=col_name,
                        color="steel_grade",
                        barmode="overlay",
                        opacity=0.7,
                        nbins=20,
                        labels={col_name: _friendly(col_name), "steel_grade": "Steel Grade"},
                        title=_friendly(col_name),
                        color_discrete_sequence=px.colors.qualitative.Set2,
                    )
                else:
                    fig = px.box(
                        df,
                        x="steel_grade",
                        y=col_name,
                        color="steel_grade",
                        labels={
                            col_name: _friendly(col_name),
                            "steel_grade": "Steel Grade",
                        },
                        title=_friendly(col_name),
                        color_discrete_sequence=px.colors.qualitative.Set2,
                    )
                fig.update_layout(
                    template="plotly_white",
                    showlegend=False,
                    height=350,
                )
                st.plotly_chart(fig, use_container_width=True)


def _render_summary_table(df: pd.DataFrame) -> None:
    """Descriptive statistics per variable per steel grade, displayed as a
    styled dataframe."""
    st.subheader("Statistical Summary Table")

    cols_present = [c for c in _NUMERIC_COLS if c in df.columns]
    if not cols_present:
        st.warning("No numeric columns available for summary.")
        return

    summary_parts: list[pd.DataFrame] = []
    for col_name in cols_present:
        grouped = (
            df.groupby("steel_grade")[col_name]
            .agg(["mean", "std", "min", "max", "count"])
            .reset_index()
        )
        grouped.insert(0, "variable", _friendly(col_name))
        grouped = grouped.rename(
            columns={
                "steel_grade": "Steel Grade",
                "mean": "Mean",
                "std": "Std",
                "min": "Min",
                "max": "Max",
                "count": "Count",
            }
        )
        summary_parts.append(grouped)

    summary = pd.concat(summary_parts, ignore_index=True)

    # Style: round floats, highlight min/max per group
    def _style_fn(s: pd.Series) -> list[str]:
        """Highlight the max value in green and min value in red within each
        column."""
        styles = [""] * len(s)
        if s.dtype.kind == "f":
            max_idx = s.idxmax()
            min_idx = s.idxmin()
            styles[s.index.get_loc(max_idx)] = "background-color: #d4edda"
            styles[s.index.get_loc(min_idx)] = "background-color: #f8d7da"
        return styles

    styled = (
        summary.style
        .format(
            {
                "Mean": "{:.2f}",
                "Std": "{:.2f}",
                "Min": "{:.2f}",
                "Max": "{:.2f}",
                "Count": "{:.0f}",
            }
        )
        .apply(_style_fn, subset=["Mean", "Std", "Min", "Max"])
    )

    st.dataframe(styled, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Main render entry point
# ---------------------------------------------------------------------------


def render() -> None:
    """Render the full Data Visualization & Correlation Analysis page.

    This is the single entry point called by the Streamlit app shell.
    """
    st.title("Data Visualization & Correlation Analysis")
    st.markdown(
        "Explore relationships between **electrical conductivity** and "
        "**machinability metrics** (tool life, surface roughness, cutting "
        "force) across low-alloy steel grades (RQ1)."
    )

    st.divider()

    # --- Data source toggle ---------------------------------------------------
    use_demo = _render_data_toggle()
    df = _get_data(use_demo)

    if use_demo:
        st.info(
            f"Showing **synthetic demo data** with {len(df)} specimens across "
            f"{', '.join(_STEEL_GRADES)}.",
            icon="\U0001f9ea",
        )
    else:
        st.success(
            f"Loaded **real data** from `evidence_matrix.csv` ({len(df)} rows).",
            icon="\u2705",
        )

    # Quick data preview (collapsed)
    with st.expander("Preview raw data"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # --- Sections -------------------------------------------------------------
    _render_scatter(df)
    st.divider()
    _render_heatmap(df)
    st.divider()
    _render_distributions(df)
    st.divider()
    _render_summary_table(df)
