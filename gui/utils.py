"""Shared utilities for the Machinability Research Dashboard.

Provides helper functions for loading project data, computing statistics,
reading markdown files, and defining common styling constants.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_MATRIX_PATH = PROJECT_ROOT / "02_EVIDENCE_MATRIX" / "evidence_matrix.csv"
LITERATURE_NOTES_DIR = PROJECT_ROOT / "01_LITERATURE" / "notes"
README_DIR = PROJECT_ROOT / "00_README"

# ---------------------------------------------------------------------------
# Theme / styling constants
# ---------------------------------------------------------------------------
THEME = {
    "primary_color": "#1B4F72",
    "secondary_color": "#2E86C1",
    "accent_color": "#F39C12",
    "success_color": "#27AE60",
    "warning_color": "#E74C3C",
    "bg_card": "#F8F9FA",
    "text_dark": "#2C3E50",
    "text_muted": "#7F8C8D",
}

PILLAR_LABELS = {
    "pillar_A": "A -- Machinability & Cutting",
    "pillar_B": "B -- Physical Metallurgy & Conductivity",
    "pillar_C": "C -- Measurement Techniques",
    "pillar_D": "D -- Predictive Modelling / ML",
}

PILLAR_COLORS = {
    "pillar_A": "#E74C3C",
    "pillar_B": "#2E86C1",
    "pillar_C": "#27AE60",
    "pillar_D": "#F39C12",
}

STEEL_GRADES_OF_INTEREST = ["AISI 1045", "AISI 4140", "AISI 4340"]


# ---------------------------------------------------------------------------
# Data-loading helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_evidence_matrix() -> pd.DataFrame:
    """Load the evidence matrix CSV and return it as a DataFrame.

    Returns an empty DataFrame with expected columns if the file is missing.
    """
    if not EVIDENCE_MATRIX_PATH.exists():
        return pd.DataFrame(columns=[
            "paper_id", "year", "steel_grade", "composition",
            "heat_treatment", "microstructure", "conductivity_method",
            "conductivity_value_units", "temp_C", "uncertainty",
            "machining_process", "tool", "cutting_params",
            "machinability_metric", "key_findings", "tags", "link_or_doi",
        ])
    df = pd.read_csv(EVIDENCE_MATRIX_PATH)
    return df


def count_literature_notes() -> int:
    """Count markdown literature notes (excludes the template file)."""
    if not LITERATURE_NOTES_DIR.exists():
        return 0
    notes = [
        f for f in LITERATURE_NOTES_DIR.iterdir()
        if f.suffix == ".md" and "TEMPLATE" not in f.name
    ]
    return len(notes)


def list_literature_notes() -> list[str]:
    """Return sorted list of literature note filenames (without extension)."""
    if not LITERATURE_NOTES_DIR.exists():
        return []
    notes = sorted(
        f.stem
        for f in LITERATURE_NOTES_DIR.iterdir()
        if f.suffix == ".md" and "TEMPLATE" not in f.name
    )
    return notes


def get_unique_papers(df: pd.DataFrame | None = None) -> int:
    """Return the number of unique paper IDs in the evidence matrix."""
    if df is None:
        df = load_evidence_matrix()
    if df.empty:
        return 0
    return df["paper_id"].nunique()


def get_unique_steel_grades(df: pd.DataFrame | None = None) -> list[str]:
    """Return sorted list of unique steel grades present in the matrix."""
    if df is None:
        df = load_evidence_matrix()
    if df.empty or "steel_grade" not in df.columns:
        return []
    grades = df["steel_grade"].dropna().unique().tolist()
    return sorted(grades)


def get_pillar_counts(df: pd.DataFrame | None = None) -> dict[str, int]:
    """Count evidence-matrix rows tagged with each research pillar."""
    if df is None:
        df = load_evidence_matrix()
    counts: dict[str, int] = {}
    if df.empty or "tags" not in df.columns:
        return {p: 0 for p in PILLAR_LABELS}
    for pillar in PILLAR_LABELS:
        counts[pillar] = int(
            df["tags"].fillna("").str.contains(pillar, case=False).sum()
        )
    return counts


def get_year_range(df: pd.DataFrame | None = None) -> tuple[int, int] | None:
    """Return (min_year, max_year) from the evidence matrix."""
    if df is None:
        df = load_evidence_matrix()
    if df.empty or "year" not in df.columns:
        return None
    years = pd.to_numeric(df["year"], errors="coerce").dropna()
    if years.empty:
        return None
    return int(years.min()), int(years.max())


def get_project_stats() -> dict:
    """Aggregate key project statistics into a single dictionary."""
    df = load_evidence_matrix()
    note_count = count_literature_notes()
    unique_papers = get_unique_papers(df)
    steel_grades = get_unique_steel_grades(df)
    pillar_counts = get_pillar_counts(df)
    year_range = get_year_range(df)
    matrix_rows = len(df)

    # Count methods-related markdown files
    methods_dir = PROJECT_ROOT / "03_METHODS"
    methods_count = 0
    if methods_dir.exists():
        methods_count = sum(
            1 for f in methods_dir.iterdir()
            if f.suffix == ".md" and f.name != "README.md"
        )

    # Git status (last commit date)
    last_commit_date = _get_last_commit_date()

    return {
        "matrix_rows": matrix_rows,
        "unique_papers": unique_papers,
        "note_count": note_count,
        "steel_grades": steel_grades,
        "pillar_counts": pillar_counts,
        "year_range": year_range,
        "methods_count": methods_count,
        "last_commit_date": last_commit_date,
    }


def _get_last_commit_date() -> str:
    """Try to retrieve the last git commit date; return 'N/A' on failure."""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()[:10]  # YYYY-MM-DD
    except Exception:
        pass
    return "N/A"


# ---------------------------------------------------------------------------
# Markdown rendering helper
# ---------------------------------------------------------------------------
def read_markdown_file(filepath: str | Path) -> str:
    """Read a markdown file and return its contents as a string.

    Returns a placeholder message when the file does not exist.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        return f"*File not found: `{filepath}`*"
    return filepath.read_text(encoding="utf-8")


def display_markdown_file(filepath: str | Path) -> None:
    """Read a markdown file and render it in the Streamlit app."""
    content = read_markdown_file(filepath)
    st.markdown(content, unsafe_allow_html=False)


# ---------------------------------------------------------------------------
# Reusable UI components
# ---------------------------------------------------------------------------
def styled_metric_card(label: str, value, description: str = "") -> str:
    """Return an HTML snippet for a styled metric card.

    Use with ``st.markdown(card, unsafe_allow_html=True)``.
    """
    desc_html = (
        f'<p style="margin:0;font-size:0.8rem;color:{THEME["text_muted"]}">'
        f"{description}</p>"
        if description
        else ""
    )
    return f"""
    <div style="
        background: {THEME['bg_card']};
        border-left: 4px solid {THEME['secondary_color']};
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    ">
        <p style="margin:0 0 0.25rem 0;font-size:0.85rem;color:{THEME['text_muted']};
                  text-transform:uppercase;letter-spacing:0.05em;">
            {label}
        </p>
        <p style="margin:0;font-size:1.8rem;font-weight:700;color:{THEME['text_dark']};">
            {value}
        </p>
        {desc_html}
    </div>
    """


def apply_custom_css() -> None:
    """Inject lightweight custom CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
        /* Tighten default Streamlit padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Sidebar header styling */
        [data-testid="stSidebar"] {
            background-color: #1B4F72;
        }
        [data-testid="stSidebar"] * {
            color: #ECF0F1 !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            font-size: 1rem;
        }
        /* Metric cards inside st.metric */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
