"""
Streamlit page for browsing PhD literature notes.

Provides:
    1. Literature Overview  -- searchable/filterable table of all paper notes
    2. Paper Reader         -- full markdown display of a selected note
    3. BibTeX Library       -- search and browse the .bib file
    4. RQ Coverage Matrix   -- papers x research-questions heatmap
    5. Tag Cloud / Summary  -- tag frequencies and pillar groupings
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_BASE = Path(__file__).resolve().parents[2]  # …/AI_Research
_NOTES_DIR = _BASE / "01_LITERATURE" / "notes"
_BIB_FILE = _BASE / "01_LITERATURE" / "library.bib"
_TEMPLATE = "PAPER_NOTE_TEMPLATE.md"

# Research questions
_RQS = ["RQ1", "RQ2", "RQ3", "RQ4"]
_RQ_LABELS = {
    "RQ1": "RQ1 (Conductivity-Machinability)",
    "RQ2": "RQ2 (Microstructural Mediation)",
    "RQ3": "RQ3 (Measurement Methods)",
    "RQ4": "RQ4 (Predictive Model)",
}

# Pillar definitions (from keywords_queries.md)
_PILLAR_LABELS = {
    "A": "Pillar A: Machinability of Low-Alloy Steels",
    "B": "Pillar B: Electrical Conductivity & Microstructure",
    "C": "Pillar C: Measurement Methods",
    "D": "Pillar D: Bridging & Predictive Models",
    "Multi": "Multi-Pillar / Bridging",
}

# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def _note_files() -> list[Path]:
    """Return all .md note files, excluding the template."""
    if not _NOTES_DIR.is_dir():
        return []
    return sorted(
        p for p in _NOTES_DIR.glob("*.md") if p.name != _TEMPLATE
    )


def _extract_field(text: str, field: str) -> str:
    """Extract a '- **Field:** value' line from markdown text."""
    pattern = rf"\*\*{re.escape(field)}:\*\*\s*(.*)"
    m = re.search(pattern, text)
    return m.group(1).strip() if m else ""


def _extract_rq_scores(text: str) -> dict[str, int]:
    """Parse 'RQ1: 4/5 | RQ2: 3/5 ...' into a dict of ints."""
    scores: dict[str, int] = {}
    relevance_line = _extract_field(text, "RQ Relevance")
    if not relevance_line:
        return {rq: 0 for rq in _RQS}
    for rq in _RQS:
        m = re.search(rf"{rq}:\s*(\d+)/5", relevance_line)
        scores[rq] = int(m.group(1)) if m else 0
    return scores


def _extract_tags(text: str) -> list[str]:
    """Extract backtick-delimited tags from the '## Tags' section."""
    m = re.search(r"## Tags\s*\n(.+)", text)
    if not m:
        return []
    return re.findall(r"`([^`]+)`", m.group(1))


def _extract_pillar(text: str) -> str:
    """Extract pillar letter(s) from the Classification section."""
    raw = _extract_field(text, "Pillar")
    if not raw:
        return ""
    # Normalise: "Multi (B + D)" -> "Multi", "A" -> "A"
    raw_upper = raw.strip().upper()
    if raw_upper.startswith("MULTI"):
        return "Multi"
    # Take the first single letter that matches known pillars
    for ch in "ABCD":
        if ch in raw_upper:
            return ch
    return raw.strip()


def _parse_note(path: Path) -> dict[str, Any]:
    """Parse a single paper note into a metadata dict."""
    text = path.read_text(encoding="utf-8")
    rq_scores = _extract_rq_scores(text)
    tags = _extract_tags(text)
    pillar = _extract_pillar(text)
    year_raw = _extract_field(text, "Year")
    # Try to pull a 4-digit year
    year_match = re.search(r"\d{4}", year_raw)
    year = int(year_match.group()) if year_match else None

    return {
        "file": path.name,
        "path": str(path),
        "title": _extract_field(text, "Title"),
        "authors": _extract_field(text, "Authors"),
        "year": year,
        "journal": _extract_field(text, "Journal/Publisher"),
        "pillar": pillar,
        "paper_type": _extract_field(text, "Paper Type"),
        **rq_scores,
        "relevance_total": sum(rq_scores.values()),
        "tags": tags,
        "tags_str": ", ".join(tags),
        "raw": text,
    }


@st.cache_data(show_spinner="Scanning literature notes...")
def _load_all_notes() -> pd.DataFrame:
    """Load and parse every paper note into a DataFrame."""
    files = _note_files()
    if not files:
        return pd.DataFrame()
    records = [_parse_note(p) for p in files]
    return pd.DataFrame(records)


@st.cache_data(show_spinner="Loading BibTeX library...")
def _load_bibtex() -> str:
    """Return the raw text of library.bib."""
    if _BIB_FILE.is_file():
        return _BIB_FILE.read_text(encoding="utf-8")
    return ""


def _parse_bib_entries(bib_text: str) -> list[dict[str, str]]:
    """Lightweight parser: split bib_text into individual entries."""
    entries: list[dict[str, str]] = []
    # Match each @type{key, ... } block
    pattern = re.compile(
        r"@(\w+)\{([^,]+),\s*(.*?)\n\}", re.DOTALL
    )
    for m in pattern.finditer(bib_text):
        entry_type = m.group(1)
        cite_key = m.group(2).strip()
        body = m.group(3)
        # Extract fields
        fields: dict[str, str] = {"type": entry_type, "key": cite_key}
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}", body, re.DOTALL):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        fields["_raw"] = m.group(0)
        entries.append(fields)
    return entries


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

def _section_overview(df: pd.DataFrame) -> None:
    """Section 1 -- Literature Overview."""
    st.header("Literature Overview")
    st.markdown(f"**{len(df)}** paper notes found in `01_LITERATURE/notes/`")

    # --- Filters ---
    col_search, col_pillar, col_year = st.columns([2, 1, 1])
    with col_search:
        search = st.text_input(
            "Search (title, authors, tags)",
            key="overview_search",
        )
    with col_pillar:
        pillar_opts = ["All"] + sorted(df["pillar"].dropna().unique().tolist())
        pillar_filter = st.selectbox("Pillar", pillar_opts, key="overview_pillar")
    with col_year:
        year_range = st.slider(
            "Year range",
            min_value=int(df["year"].min()) if df["year"].notna().any() else 1960,
            max_value=int(df["year"].max()) if df["year"].notna().any() else 2025,
            value=(
                int(df["year"].min()) if df["year"].notna().any() else 1960,
                int(df["year"].max()) if df["year"].notna().any() else 2025,
            ),
            key="overview_year",
        )

    view = df.copy()
    # Apply pillar filter
    if pillar_filter != "All":
        view = view[view["pillar"] == pillar_filter]
    # Apply year filter
    if view["year"].notna().any():
        view = view[
            view["year"].between(year_range[0], year_range[1])
            | view["year"].isna()
        ]
    # Apply text search
    if search:
        pat = search.lower()
        mask = (
            view["title"].str.lower().str.contains(pat, na=False)
            | view["authors"].str.lower().str.contains(pat, na=False)
            | view["tags_str"].str.lower().str.contains(pat, na=False)
        )
        view = view[mask]

    # --- Display table ---
    display_cols = [
        "file",
        "title",
        "authors",
        "year",
        "pillar",
        "paper_type",
        "RQ1",
        "RQ2",
        "RQ3",
        "RQ4",
        "relevance_total",
        "tags_str",
    ]
    rename_map = {
        "file": "File",
        "title": "Title",
        "authors": "Authors",
        "year": "Year",
        "pillar": "Pillar",
        "paper_type": "Type",
        "relevance_total": "Total",
        "tags_str": "Tags",
    }
    st.dataframe(
        view[display_cols].rename(columns=rename_map).reset_index(drop=True),
        use_container_width=True,
        height=min(400, 35 * len(view) + 38),
    )
    st.caption(f"Showing {len(view)} of {len(df)} papers")


def _section_paper_reader(df: pd.DataFrame) -> None:
    """Section 2 -- Paper Reader."""
    st.header("Paper Reader")
    if df.empty:
        st.info("No paper notes available.")
        return

    options = df["file"].tolist()
    selected = st.selectbox("Select a paper note", options, key="reader_select")
    row = df[df["file"] == selected].iloc[0]

    # Sidebar-style metadata in an expander
    with st.sidebar:
        st.subheader("Paper Metadata")
        st.markdown(f"**Title:** {row['title']}")
        st.markdown(f"**Authors:** {row['authors']}")
        st.markdown(f"**Year:** {row['year']}")
        st.markdown(f"**Journal:** {row['journal']}")
        st.markdown(f"**Pillar:** {row['pillar']}")
        st.markdown(f"**Type:** {row['paper_type']}")
        st.markdown("**RQ Relevance:**")
        for rq in _RQS:
            score = int(row[rq])
            bar = "\u2588" * score + "\u2591" * (5 - score)
            st.markdown(f"- {_RQ_LABELS[rq]}: `{bar}` {score}/5")
        if row["tags"]:
            st.markdown("**Tags:** " + " ".join(f"`{t}`" for t in row["tags"]))

    # Full content
    st.markdown(row["raw"])


def _section_bibtex(bib_text: str) -> None:
    """Section 3 -- BibTeX Library."""
    st.header("BibTeX Library")
    if not bib_text:
        st.warning("`01_LITERATURE/library.bib` not found.")
        return

    entries = _parse_bib_entries(bib_text)
    st.markdown(f"**{len(entries)}** entries in `library.bib`")

    search = st.text_input(
        "Search BibTeX (key, author, title, keywords)",
        key="bib_search",
    )

    filtered = entries
    if search:
        pat = search.lower()
        filtered = [
            e
            for e in entries
            if pat in e.get("key", "").lower()
            or pat in e.get("author", "").lower()
            or pat in e.get("title", "").lower()
            or pat in e.get("keywords", "").lower()
        ]
        st.caption(f"Showing {len(filtered)} of {len(entries)} entries")

    for entry in filtered:
        with st.expander(f"**{entry['key']}** ({entry['type']})"):
            st.code(entry.get("_raw", ""), language="bibtex")
            cols = st.columns(3)
            with cols[0]:
                st.markdown(f"**Author:** {entry.get('author', 'N/A')}")
            with cols[1]:
                st.markdown(f"**Year:** {entry.get('year', 'N/A')}")
            with cols[2]:
                st.markdown(f"**Keywords:** {entry.get('keywords', 'N/A')}")


def _section_rq_coverage(df: pd.DataFrame) -> None:
    """Section 4 -- Research Questions Coverage Matrix."""
    st.header("Research Questions Coverage")
    if df.empty:
        st.info("No paper notes available.")
        return

    # Build matrix
    matrix = df[["file"] + _RQS].set_index("file")
    matrix.index.name = "Paper"

    # Heatmap with plotly
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix.values,
            x=[_RQ_LABELS[rq] for rq in _RQS],
            y=matrix.index.tolist(),
            colorscale="YlOrRd",
            zmin=0,
            zmax=5,
            text=matrix.values,
            texttemplate="%{text}",
            hovertemplate="Paper: %{y}<br>%{x}: %{z}/5<extra></extra>",
            colorbar=dict(title="Score /5"),
        )
    )
    fig.update_layout(
        title="Paper-RQ Relevance Matrix",
        yaxis=dict(autorange="reversed", dtick=1),
        xaxis=dict(side="top"),
        height=max(400, 28 * len(matrix)),
        margin=dict(l=200),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gap analysis
    st.subheader("Gap Analysis")
    rq_totals = matrix.sum()
    rq_means = matrix.mean().round(2)
    gap_df = pd.DataFrame(
        {"Total Score": rq_totals, "Mean Score": rq_means, "Papers Scored > 0": (matrix > 0).sum()}
    )
    gap_df.index = [_RQ_LABELS[rq] for rq in _RQS]
    st.dataframe(gap_df, use_container_width=True)

    weakest = rq_means.idxmin()
    st.info(
        f"**{_RQ_LABELS[weakest]}** has the lowest average relevance score "
        f"({rq_means[weakest]}/5). Consider searching for more literature in this area."
    )

    # Papers with low total relevance
    low_threshold = 5
    low_papers = df[df["relevance_total"] <= low_threshold][["file", "title", "relevance_total"]]
    if not low_papers.empty:
        with st.expander(f"Papers with total relevance score <= {low_threshold}"):
            st.dataframe(low_papers.reset_index(drop=True), use_container_width=True)


def _section_tag_cloud(df: pd.DataFrame) -> None:
    """Section 5 -- Tag Cloud / Summary."""
    st.header("Tag Cloud & Summary")
    if df.empty:
        st.info("No paper notes available.")
        return

    # Collect all tags
    all_tags: list[str] = []
    for tags in df["tags"]:
        if tags:
            all_tags.extend(tags)
    tag_counts = Counter(all_tags)

    if not tag_counts:
        st.info("No tags found in paper notes.")
        return

    # Bar chart of tag frequencies
    tag_df = (
        pd.DataFrame(tag_counts.items(), columns=["Tag", "Count"])
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        tag_df,
        x="Count",
        y="Tag",
        orientation="h",
        title="Tag Frequencies Across All Papers",
        color="Count",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed", dtick=1),
        height=max(400, 25 * len(tag_df)),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Group papers by pillar
    st.subheader("Papers by Pillar")
    for pillar_key, pillar_label in _PILLAR_LABELS.items():
        pillar_papers = df[df["pillar"] == pillar_key]
        count = len(pillar_papers)
        with st.expander(f"{pillar_label} ({count} papers)"):
            if pillar_papers.empty:
                st.write("No papers assigned to this pillar.")
            else:
                for _, row in pillar_papers.iterrows():
                    tags_display = " ".join(f"`{t}`" for t in row["tags"]) if row["tags"] else ""
                    st.markdown(
                        f"- **{row['title']}** ({row['authors']}, {row['year']}) {tags_display}"
                    )

    # Year distribution
    st.subheader("Publication Year Distribution")
    year_df = df.dropna(subset=["year"]).copy()
    if not year_df.empty:
        year_df["year"] = year_df["year"].astype(int)
        fig_year = px.histogram(
            year_df,
            x="year",
            nbins=max(1, year_df["year"].nunique()),
            title="Papers by Publication Year",
            color="pillar",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"year": "Year", "pillar": "Pillar"},
        )
        fig_year.update_layout(bargap=0.1)
        st.plotly_chart(fig_year, use_container_width=True)


# ---------------------------------------------------------------------------
# Main render entry point
# ---------------------------------------------------------------------------

def render() -> None:
    """Render the Literature Browser page.

    This function is self-contained and designed to be called as ``render()``
    from a Streamlit application shell.
    """
    st.title("Literature Browser")
    st.markdown(
        "Browse, search, and analyse the literature notes for the PhD research on "
        "*Determining Machinability of Low-Alloy Steels via Electrical Conductivity Measurements*."
    )

    df = _load_all_notes()
    bib_text = _load_bibtex()

    if df.empty:
        st.error(
            f"No paper notes found in `{_NOTES_DIR}`. "
            "Ensure `.md` files exist (excluding the template)."
        )
        return

    tab_overview, tab_reader, tab_bib, tab_rq, tab_tags = st.tabs(
        [
            "Literature Overview",
            "Paper Reader",
            "BibTeX Library",
            "RQ Coverage Matrix",
            "Tag Cloud & Summary",
        ]
    )

    with tab_overview:
        _section_overview(df)

    with tab_reader:
        _section_paper_reader(df)

    with tab_bib:
        _section_bibtex(bib_text)

    with tab_rq:
        _section_rq_coverage(df)

    with tab_tags:
        _section_tag_cloud(df)
