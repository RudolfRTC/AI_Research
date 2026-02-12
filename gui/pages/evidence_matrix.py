"""Streamlit page for viewing and editing the evidence matrix.

Provides an interactive data table with sidebar filters, a form for adding
new entries, a data-quality summary with completeness heatmap and gap
analysis, and a CSV export button.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent.parent  # gui/pages -> gui -> AI_Research
_CSV_PATH = _PROJECT_ROOT / "02_EVIDENCE_MATRIX" / "evidence_matrix.csv"

# ---------------------------------------------------------------------------
# Pre-filled option lists
# ---------------------------------------------------------------------------

_STEEL_GRADES = ["AISI 1045", "AISI 4140", "AISI 4340", "other"]
_CONDUCTIVITY_METHODS = ["4-probe DC", "eddy current", "PEC", "calculated", "literature"]
_MACHINING_PROCESSES = ["turning", "milling", "drilling", "N/A"]

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _load_csv() -> pd.DataFrame:
    """Read the evidence matrix CSV from disk.

    Returns an empty DataFrame with the expected columns when the file
    cannot be found so that the rest of the page still renders.
    """
    if _CSV_PATH.exists():
        df = pd.read_csv(_CSV_PATH, dtype=str)
        # Coerce numeric columns where possible
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
        if "temp_C" in df.columns:
            df["temp_C"] = pd.to_numeric(df["temp_C"], errors="coerce")
        return df

    st.warning(f"CSV not found at `{_CSV_PATH}`. Starting with an empty matrix.")
    return pd.DataFrame(
        columns=[
            "paper_id",
            "year",
            "steel_grade",
            "composition",
            "heat_treatment",
            "microstructure",
            "conductivity_method",
            "conductivity_value_units",
            "temp_C",
            "uncertainty",
            "machining_process",
            "tool",
            "cutting_params",
            "machinability_metric",
            "key_findings",
            "tags",
            "link_or_doi",
        ]
    )


def _unique_sorted(series: pd.Series) -> list[str]:
    """Return sorted unique non-null string values from a Series."""
    vals = series.dropna().astype(str).unique().tolist()
    vals = [v.strip() for v in vals if v.strip()]
    return sorted(set(vals))


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------


def _render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Build sidebar filter widgets and return the filtered DataFrame."""
    st.sidebar.header("Filters")

    # --- Steel grade dropdown ---
    all_grades = _unique_sorted(df["steel_grade"]) if "steel_grade" in df.columns else []
    grade_options = ["All"] + all_grades
    selected_grade = st.sidebar.selectbox("Steel grade", grade_options, index=0)

    # --- Year range slider ---
    if "year" in df.columns:
        numeric_years = df["year"].dropna()
        if not numeric_years.empty:
            min_year = int(numeric_years.min())
            max_year = int(numeric_years.max())
            if min_year < max_year:
                year_range = st.sidebar.slider(
                    "Year range",
                    min_value=min_year,
                    max_value=max_year,
                    value=(min_year, max_year),
                )
            else:
                year_range = (min_year, max_year)
                st.sidebar.info(f"Only one year present: {min_year}")
        else:
            year_range = None
    else:
        year_range = None

    # --- Conductivity method multiselect ---
    all_methods = (
        _unique_sorted(df["conductivity_method"])
        if "conductivity_method" in df.columns
        else []
    )
    selected_methods = st.sidebar.multiselect(
        "Conductivity method",
        options=all_methods,
        default=[],
        help="Leave empty to show all methods.",
    )

    # --- Machining process multiselect ---
    all_processes = (
        _unique_sorted(df["machining_process"])
        if "machining_process" in df.columns
        else []
    )
    selected_processes = st.sidebar.multiselect(
        "Machining process",
        options=all_processes,
        default=[],
        help="Leave empty to show all processes.",
    )

    # --- Apply filters ---
    mask = pd.Series(True, index=df.index)

    if selected_grade != "All" and "steel_grade" in df.columns:
        mask &= df["steel_grade"].astype(str).str.strip() == selected_grade

    if year_range is not None and "year" in df.columns:
        mask &= (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])

    if selected_methods and "conductivity_method" in df.columns:
        mask &= df["conductivity_method"].astype(str).str.strip().isin(selected_methods)

    if selected_processes and "machining_process" in df.columns:
        mask &= df["machining_process"].astype(str).str.strip().isin(selected_processes)

    return df.loc[mask].reset_index(drop=True)


def _render_data_table(df_filtered: pd.DataFrame) -> None:
    """Display the filtered evidence matrix as an interactive table."""
    st.subheader("Evidence Matrix")
    st.caption(f"Showing **{len(df_filtered)}** row(s) after filtering.")
    st.dataframe(df_filtered, use_container_width=True)


def _render_add_entry_form(df: pd.DataFrame) -> pd.DataFrame | None:
    """Render the *Add New Entry* expander form.

    Returns the updated DataFrame when a row is successfully appended,
    or ``None`` when no submission occurred.
    """
    with st.expander("Add New Entry", expanded=False):
        with st.form("add_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                paper_id = st.text_input("paper_id *", help="BibTeX key from library.bib")

                year = st.number_input(
                    "year",
                    min_value=1900,
                    max_value=2100,
                    value=2024,
                    step=1,
                )

                grade_choice = st.selectbox(
                    "steel_grade",
                    options=_STEEL_GRADES,
                    index=0,
                )
                if grade_choice == "other":
                    steel_grade = st.text_input("Specify steel grade")
                else:
                    steel_grade = grade_choice

                composition = st.text_input(
                    "composition",
                    help="Key alloying elements, e.g. 0.40C-0.80Mn-1.0Cr",
                )
                heat_treatment = st.text_input(
                    "heat_treatment",
                    help="e.g. Q&T 600C, annealed, normalised",
                )
                microstructure = st.text_input(
                    "microstructure",
                    help="e.g. tempered martensite, ferrite+pearlite",
                )
                conductivity_method = st.selectbox(
                    "conductivity_method",
                    options=[""] + _CONDUCTIVITY_METHODS,
                    index=0,
                    help="Leave blank if not applicable.",
                )
                conductivity_value_units = st.text_input(
                    "conductivity_value_units",
                    help="e.g. 3.1 %IACS, 2.5 MS/m",
                )

            with col2:
                temp_c = st.text_input(
                    "temp_C",
                    help="Measurement temperature in C (leave blank if unknown)",
                )
                uncertainty = st.text_input(
                    "uncertainty",
                    help="e.g. +/- 0.1 %IACS",
                )
                machining_process = st.selectbox(
                    "machining_process",
                    options=[""] + _MACHINING_PROCESSES,
                    index=0,
                )
                tool = st.text_input(
                    "tool",
                    help="Tool material & geometry, e.g. coated carbide CNMG 120408",
                )
                cutting_params = st.text_input(
                    "cutting_params",
                    help="Format: v=X f=Y d=Z",
                )
                machinability_metric = st.text_input(
                    "machinability_metric",
                    help="e.g. VB=0.3mm at T=18min",
                )
                key_findings = st.text_area(
                    "key_findings",
                    help="1-3 sentence summary of main result.",
                )
                tags = st.text_input(
                    "tags",
                    help="Comma-separated tags: pillar, steel family, method, etc.",
                )
                link_or_doi = st.text_input(
                    "link_or_doi",
                    help="DOI (preferred) or URL.",
                )

            submitted = st.form_submit_button("Add entry")

        if submitted:
            if not paper_id.strip():
                st.error("**paper_id** is required.")
                return None

            new_row = {
                "paper_id": paper_id.strip(),
                "year": int(year),
                "steel_grade": steel_grade.strip(),
                "composition": composition.strip(),
                "heat_treatment": heat_treatment.strip(),
                "microstructure": microstructure.strip(),
                "conductivity_method": conductivity_method.strip() if conductivity_method else "",
                "conductivity_value_units": conductivity_value_units.strip(),
                "temp_C": temp_c.strip(),
                "uncertainty": uncertainty.strip(),
                "machining_process": machining_process.strip() if machining_process else "",
                "tool": tool.strip(),
                "cutting_params": cutting_params.strip(),
                "machinability_metric": machinability_metric.strip(),
                "key_findings": key_findings.strip(),
                "tags": tags.strip(),
                "link_or_doi": link_or_doi.strip(),
            }

            new_df = pd.DataFrame([new_row])
            updated = pd.concat([df, new_df], ignore_index=True)

            # Persist to disk
            _CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
            updated.to_csv(_CSV_PATH, index=False)

            st.success(f"Row for **{paper_id}** added successfully.")
            return updated

    return None


def _render_data_quality(df: pd.DataFrame) -> None:
    """Render the Data Quality Summary section."""
    st.subheader("Data Quality Summary")

    if df.empty:
        st.info("No data to analyse.")
        return

    # ---- Completeness heatmap ----
    st.markdown("#### Completeness Heatmap")
    st.caption(
        "Each cell is coloured green when data is present or red when missing."
    )

    # Build a boolean presence matrix (True = has data)
    presence = df.notna() & (df.astype(str).str.strip() != "")

    # We create a styled dataframe with green/red background.
    def _colour_cell(val: bool) -> str:
        if val:
            return "background-color: #2e7d32; color: white"  # green
        return "background-color: #c62828; color: white"  # red

    # Limit to first 200 rows to avoid excessive rendering
    display_presence = presence.head(200)

    # Use paper_id (+ index) as the row label for readability
    if "paper_id" in df.columns:
        labels = df["paper_id"].astype(str).head(200)
        display_presence = display_presence.copy()
        display_presence.index = labels

    styled = display_presence.style.map(_colour_cell)
    st.dataframe(styled, use_container_width=True)

    # ---- Missing data percentage per column ----
    st.markdown("#### Missing Data Percentage per Column")
    total_rows = len(df)
    missing_counts = total_rows - presence.sum()
    missing_pct = (missing_counts / total_rows * 100).round(1)
    missing_summary = pd.DataFrame(
        {"missing_count": missing_counts, "missing_pct": missing_pct}
    ).sort_values("missing_pct", ascending=False)

    st.dataframe(missing_summary, use_container_width=True)

    # ---- Gap analysis ----
    st.markdown("#### Gap Analysis")
    st.caption(
        "Identifies which steel grades and conductivity methods have the fewest data rows."
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Rows per steel grade**")
        if "steel_grade" in df.columns:
            grade_counts = (
                df["steel_grade"]
                .fillna("(blank)")
                .astype(str)
                .str.strip()
                .replace("", "(blank)")
                .value_counts()
                .sort_values()
            )
            st.bar_chart(grade_counts)
        else:
            st.info("No `steel_grade` column found.")

    with col_b:
        st.markdown("**Rows per conductivity method**")
        if "conductivity_method" in df.columns:
            method_counts = (
                df["conductivity_method"]
                .fillna("(blank)")
                .astype(str)
                .str.strip()
                .replace("", "(blank)")
                .value_counts()
                .sort_values()
            )
            st.bar_chart(method_counts)
        else:
            st.info("No `conductivity_method` column found.")

    # Cross-tab summary
    if "steel_grade" in df.columns and "conductivity_method" in df.columns:
        st.markdown("**Steel grade vs. conductivity method (row counts)**")
        cross = pd.crosstab(
            df["steel_grade"].fillna("(blank)").astype(str).str.strip().replace("", "(blank)"),
            df["conductivity_method"].fillna("(blank)").astype(str).str.strip().replace("", "(blank)"),
            margins=True,
        )
        st.dataframe(cross, use_container_width=True)


def _render_export(df_filtered: pd.DataFrame) -> None:
    """Provide a download button for the filtered data."""
    st.subheader("Export")

    csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_bytes,
        file_name="evidence_matrix_filtered.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def render() -> None:
    """Render the Evidence Matrix page.

    This is the sole public entry point and is designed to be called as
    ``render()`` from a Streamlit application host.
    """
    st.set_page_config(page_title="Evidence Matrix", layout="wide")
    st.title("Evidence Matrix Viewer")

    # Load data (may be refreshed after adding a row)
    df = _load_csv()

    # --- 1. Sidebar filters + data table ---
    df_filtered = _render_sidebar_filters(df)
    _render_data_table(df_filtered)

    st.divider()

    # --- 2. Add new entry ---
    updated = _render_add_entry_form(df)
    if updated is not None:
        # Re-run the page so the table reflects the new row
        st.rerun()

    st.divider()

    # --- 3. Data quality summary (based on *full* dataset) ---
    _render_data_quality(df)

    st.divider()

    # --- 4. Export filtered data ---
    _render_export(df_filtered)
