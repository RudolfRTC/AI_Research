"""Machinability Research Dashboard -- Main Entry Point.

Launch with:
    streamlit run app.py

A multi-page Streamlit dashboard for the PhD research project:
"Determining machinability of low-alloy steels via electrical conductivity measurements"
"""

from __future__ import annotations

import streamlit as st

from gui.utils import (
    PILLAR_COLORS,
    PILLAR_LABELS,
    STEEL_GRADES_OF_INTEREST,
    THEME,
    PROJECT_ROOT,
    README_DIR,
    apply_custom_css,
    display_markdown_file,
    get_project_stats,
    list_literature_notes,
    styled_metric_card,
)

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Machinability Research Dashboard",
    page_icon=":gear:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center;padding:0.5rem 0 1rem 0;">
            <span style="font-size:2.5rem;">&#9881;</span>
            <h2 style="margin:0.25rem 0 0 0;font-size:1.15rem;line-height:1.3;">
                Machinability Research<br>Dashboard
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    page = st.radio(
        "Navigation",
        options=[
            "Home",
            "Literature Notes",
            "Evidence Matrix",
            "Data Analysis",
            "ML Models",
            "Methods & Protocols",
            "Models & Hypotheses",
            "Dissertation",
        ],
        index=0,
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("PhD Research -- 2024-2028")
    st.caption("Electrical Conductivity & Machinability")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Home
# ═══════════════════════════════════════════════════════════════════════════
def render_home() -> None:
    """Render the Home / Overview page."""
    # ── Header ──────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <h1 style="color:{THEME['primary_color']};margin-bottom:0;">
            Determining Machinability of Low-Alloy Steels<br>
            via Electrical Conductivity Measurements
        </h1>
        <p style="font-size:1.1rem;color:{THEME['text_muted']};margin-top:0.25rem;">
            Doctoral Research Dashboard &mdash; Interactive overview of literature,
            evidence, methods, and modelling progress.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Quick Stats ─────────────────────────────────────────────────────
    stats = get_project_stats()

    st.subheader("Project at a Glance")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Papers in Evidence Matrix",
            value=stats["unique_papers"],
            help="Unique paper IDs in 02_EVIDENCE_MATRIX/evidence_matrix.csv",
        )
    with col2:
        st.metric(
            label="Literature Notes",
            value=stats["note_count"],
            help="Markdown notes in 01_LITERATURE/notes/",
        )
    with col3:
        st.metric(
            label="Evidence Matrix Rows",
            value=stats["matrix_rows"],
            help="Total rows (some papers have multiple rows for different steel grades)",
        )
    with col4:
        st.metric(
            label="Steel Grades Tracked",
            value=len(stats["steel_grades"]),
            help=", ".join(stats["steel_grades"]) if stats["steel_grades"] else "None yet",
        )

    # Second row of stats using styled HTML cards
    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        yr = stats["year_range"]
        yr_str = f"{yr[0]} -- {yr[1]}" if yr else "N/A"
        st.markdown(
            styled_metric_card("Publication Year Range", yr_str),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            styled_metric_card(
                "Method Protocols",
                stats["methods_count"],
                "Files in 03_METHODS/",
            ),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            styled_metric_card(
                "Last Commit",
                stats["last_commit_date"],
                "Git repository activity",
            ),
            unsafe_allow_html=True,
        )
    with c4:
        grades_str = ", ".join(STEEL_GRADES_OF_INTEREST)
        st.markdown(
            styled_metric_card("Target Grades", grades_str, "Primary steel grades under study"),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Research Questions ──────────────────────────────────────────────
    st.subheader("Research Questions")

    rq_data = [
        (
            "RQ1",
            "Conductivity-Machinability Relationship",
            "What is the quantitative relationship between electrical conductivity "
            "and machinability indicators (tool wear, cutting forces, surface roughness) "
            "in low-alloy steels?",
            "pillar_A",
        ),
        (
            "RQ2",
            "Microstructural Mediation",
            "How do microstructural features (grain size, phase composition, precipitate "
            "distribution) mediate the conductivity-machinability relationship?",
            "pillar_B",
        ),
        (
            "RQ3",
            "Measurement Methodology",
            "Which conductivity measurement techniques (4-probe DC, eddy current) provide "
            "the most reliable machinability prediction, and under what conditions?",
            "pillar_C",
        ),
        (
            "RQ4",
            "Predictive Model",
            "Can a validated predictive model estimate machinability from conductivity "
            "measurements, reducing machining trials?",
            "pillar_D",
        ),
    ]

    for rq_id, rq_title, rq_text, pillar in rq_data:
        color = PILLAR_COLORS.get(pillar, THEME["secondary_color"])
        pillar_label = PILLAR_LABELS.get(pillar, pillar)
        st.markdown(
            f"""
            <div style="
                background:{THEME['bg_card']};
                border-left:5px solid {color};
                border-radius:0.4rem;
                padding:1rem 1.25rem;
                margin-bottom:0.75rem;
            ">
                <strong style="font-size:1.05rem;color:{color};">
                    {rq_id}: {rq_title}
                </strong>
                <span style="float:right;font-size:0.8rem;color:{THEME['text_muted']};">
                    {pillar_label}
                </span>
                <p style="margin:0.5rem 0 0 0;color:{THEME['text_dark']};">
                    {rq_text}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Evidence by Pillar ──────────────────────────────────────────────
    st.subheader("Evidence Coverage by Research Pillar")

    pillar_counts = stats["pillar_counts"]
    pcols = st.columns(4)
    for idx, (pillar_key, pillar_label) in enumerate(PILLAR_LABELS.items()):
        with pcols[idx]:
            count = pillar_counts.get(pillar_key, 0)
            color = PILLAR_COLORS[pillar_key]
            short_label = pillar_label.split(" -- ")[0]
            desc = pillar_label.split(" -- ")[1] if " -- " in pillar_label else ""
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    background:{THEME['bg_card']};
                    border-top:4px solid {color};
                    border-radius:0.4rem;
                    padding:1.25rem 0.75rem;
                ">
                    <p style="margin:0;font-size:2rem;font-weight:700;color:{color};">
                        {count}
                    </p>
                    <p style="margin:0.25rem 0 0 0;font-size:0.95rem;font-weight:600;
                              color:{THEME['text_dark']};">
                        Pillar {short_label}
                    </p>
                    <p style="margin:0.15rem 0 0 0;font-size:0.8rem;color:{THEME['text_muted']};">
                        {desc}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Recent Activity / Progress ──────────────────────────────────────
    st.subheader("Recent Activity & Progress")

    prog_col1, prog_col2 = st.columns(2)

    with prog_col1:
        st.markdown("**Repository Status**")
        st.markdown(
            f"""
            | Item | Status |
            |------|--------|
            | Evidence Matrix | {stats['matrix_rows']} rows, {stats['unique_papers']} papers |
            | Literature Notes | {stats['note_count']} notes completed |
            | Method Protocols | {stats['methods_count']} protocols defined |
            | Last Git Commit | {stats['last_commit_date']} |
            | Steel Grades | {', '.join(stats['steel_grades']) if stats['steel_grades'] else 'None yet'} |
            """
        )

    with prog_col2:
        st.markdown("**Research Milestones**")
        milestones = [
            ("Literature search & screening", 0.75),
            ("Evidence matrix population", 0.60),
            ("Conductivity measurement protocol", 0.50),
            ("Machining experiment protocol", 0.45),
            ("Baseline correlation analysis", 0.30),
            ("Predictive model development", 0.10),
            ("Dissertation drafting", 0.10),
        ]
        for label, progress in milestones:
            st.markdown(f"*{label}*")
            st.progress(progress, text=f"{int(progress * 100)}%")

    st.markdown("---")

    # ── Section Links ───────────────────────────────────────────────────
    st.subheader("Dashboard Sections")

    sections = [
        (
            "Literature Notes",
            "Browse and search individual paper notes from 01_LITERATURE/notes/.",
            "1F4DA",
        ),
        (
            "Evidence Matrix",
            "Explore the structured evidence matrix linking papers to steels, "
            "methods, and machinability data.",
            "1F4CA",
        ),
        (
            "Methods & Protocols",
            "View conductivity measurement and machining experiment protocols.",
            "1F52C",
        ),
        (
            "Models & Hypotheses",
            "Review hypotheses, statistical approaches, and ML model configurations.",
            "1F9E0",
        ),
        (
            "Dissertation",
            "Track dissertation outline and chapter progress.",
            "1F4DD",
        ),
    ]

    link_cols = st.columns(3)
    for idx, (title, desc, _icon_code) in enumerate(sections):
        with link_cols[idx % 3]:
            st.markdown(
                f"""
                <div style="
                    background:{THEME['bg_card']};
                    border:1px solid #DEE2E6;
                    border-radius:0.5rem;
                    padding:1.25rem;
                    margin-bottom:0.75rem;
                    min-height:8rem;
                ">
                    <p style="margin:0 0 0.5rem 0;font-size:1.05rem;font-weight:600;
                              color:{THEME['primary_color']};">
                        {title}
                    </p>
                    <p style="margin:0;font-size:0.9rem;color:{THEME['text_muted']};">
                        {desc}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.info(
        "Use the sidebar navigation to switch between sections.",
        icon=":material/arrow_back:",
    )


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Literature Notes
# ═══════════════════════════════════════════════════════════════════════════
def render_literature_notes() -> None:
    """Render the Literature Notes browser page."""
    st.header("Literature Notes")
    st.markdown(
        "Browse per-paper notes stored in `01_LITERATURE/notes/`. "
        "Select a note from the dropdown to view its full contents."
    )

    notes = list_literature_notes()
    if not notes:
        st.warning("No literature notes found.")
        return

    selected = st.selectbox("Select a paper note", options=notes, index=0)
    if selected:
        note_path = PROJECT_ROOT / "01_LITERATURE" / "notes" / f"{selected}.md"
        st.markdown("---")
        display_markdown_file(note_path)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Evidence Matrix
# ═══════════════════════════════════════════════════════════════════════════
def render_evidence_matrix() -> None:
    """Render the Evidence Matrix explorer page."""
    from gui.utils import load_evidence_matrix

    st.header("Evidence Matrix")
    st.markdown(
        "The evidence matrix (`02_EVIDENCE_MATRIX/evidence_matrix.csv`) links each paper "
        "to the steel grades, measurement methods, and machinability data it provides."
    )

    df = load_evidence_matrix()
    if df.empty:
        st.warning("Evidence matrix is empty or not found.")
        return

    # Filters
    with st.expander("Filters", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            all_papers = sorted(df["paper_id"].dropna().unique())
            sel_papers = st.multiselect("Paper ID", options=all_papers, default=[])
        with fc2:
            all_grades = sorted(df["steel_grade"].dropna().unique())
            sel_grades = st.multiselect("Steel Grade", options=all_grades, default=[])
        with fc3:
            tag_search = st.text_input("Tag search (substring)", value="")

    filtered = df.copy()
    if sel_papers:
        filtered = filtered[filtered["paper_id"].isin(sel_papers)]
    if sel_grades:
        filtered = filtered[filtered["steel_grade"].isin(sel_grades)]
    if tag_search:
        filtered = filtered[
            filtered["tags"].fillna("").str.contains(tag_search, case=False)
        ]

    st.markdown(f"**Showing {len(filtered)} of {len(df)} rows**")
    st.dataframe(filtered, use_container_width=True, height=500)

    # Data dictionary link
    dd_path = PROJECT_ROOT / "02_EVIDENCE_MATRIX" / "data_dictionary.md"
    if dd_path.exists():
        with st.expander("Data Dictionary"):
            display_markdown_file(dd_path)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Methods & Protocols
# ═══════════════════════════════════════════════════════════════════════════
def render_methods() -> None:
    """Render the Methods & Protocols page."""
    st.header("Methods & Protocols")
    st.markdown("Experimental protocols and metrics definitions from `03_METHODS/`.")

    methods_dir = PROJECT_ROOT / "03_METHODS"
    if not methods_dir.exists():
        st.warning("03_METHODS directory not found.")
        return

    md_files = sorted(
        f for f in methods_dir.iterdir()
        if f.suffix == ".md" and f.name != "README.md"
    )
    if not md_files:
        st.info("No protocol files found in 03_METHODS/.")
        return

    selected = st.selectbox(
        "Select a protocol / document",
        options=[f.stem for f in md_files],
        index=0,
    )
    if selected:
        display_markdown_file(methods_dir / f"{selected}.md")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Models & Hypotheses
# ═══════════════════════════════════════════════════════════════════════════
def render_models() -> None:
    """Render the Models & Hypotheses page."""
    st.header("Models & Hypotheses")
    st.markdown("Review research hypotheses and modelling approaches from `04_MODELS/`.")

    models_dir = PROJECT_ROOT / "04_MODELS"
    if not models_dir.exists():
        st.warning("04_MODELS directory not found.")
        return

    md_files = sorted(
        f for f in models_dir.iterdir()
        if f.suffix == ".md" and f.name != "README.md"
    )
    if not md_files:
        st.info("No documents found in 04_MODELS/.")
        return

    selected = st.selectbox(
        "Select a document",
        options=[f.stem for f in md_files],
        index=0,
    )
    if selected:
        display_markdown_file(models_dir / f"{selected}.md")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Dissertation
# ═══════════════════════════════════════════════════════════════════════════
def render_dissertation() -> None:
    """Render the Dissertation progress page."""
    st.header("Dissertation")
    st.markdown("Track the dissertation outline and chapter drafts from `05_DISSERTATION/`.")

    diss_dir = PROJECT_ROOT / "05_DISSERTATION"
    if not diss_dir.exists():
        st.warning("05_DISSERTATION directory not found.")
        return

    md_files = sorted(
        f for f in diss_dir.iterdir()
        if f.suffix == ".md" and f.name != "README.md"
    )
    if not md_files:
        st.info("No documents found in 05_DISSERTATION/.")
        return

    selected = st.selectbox(
        "Select a document",
        options=[f.stem for f in md_files],
        index=0,
    )
    if selected:
        display_markdown_file(diss_dir / f"{selected}.md")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: Data Analysis (interactive plots & correlation)
# ═══════════════════════════════════════════════════════════════════════════
def render_data_analysis() -> None:
    """Render the interactive Data Analysis page (RQ1)."""
    from gui.pages.analysis import render
    render()


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: ML Models (training & evaluation)
# ═══════════════════════════════════════════════════════════════════════════
def render_ml_models() -> None:
    """Render the ML Model Training & Evaluation page (RQ4)."""
    from gui.pages.models import render
    render()


# ── Router ──────────────────────────────────────────────────────────────────
PAGE_MAP: dict[str, callable] = {
    "Home": render_home,
    "Literature Notes": render_literature_notes,
    "Evidence Matrix": render_evidence_matrix,
    "Data Analysis": render_data_analysis,
    "ML Models": render_ml_models,
    "Methods & Protocols": render_methods,
    "Models & Hypotheses": render_models,
    "Dissertation": render_dissertation,
}

PAGE_MAP[page]()
