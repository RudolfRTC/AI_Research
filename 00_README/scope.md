# Research Repository Scope

## What This Repository Is

This repository organises all research materials for a PhD dissertation on **"Determining machinability of low-alloy steels via electrical conductivity measurements."** It serves as the single source of truth for literature, evidence, methods, models, and the dissertation itself.

## How to Use This Repository

### Folder Guide

| Folder | Contents |
|--------|----------|
| `00_README/` | Scope, research questions, search keywords, meta-documentation |
| `01_LITERATURE/` | BibTeX library (`library.bib`), per-paper notes (`notes/`), raw PDFs (`papers/`) |
| `02_EVIDENCE_MATRIX/` | Structured CSV linking papers to steels, methods, and machinability data |
| `03_METHODS/` | Conductivity measurement protocols, machining metrics definitions |
| `04_MODELS/` | Hypotheses, statistical models, ML approaches |
| `05_DISSERTATION/` | Chapter outline, drafts, figures |
| `06_NEWS_WATCH/` | Alert setup, monthly digests, conference calendar |

### Reading Workflow

1. **Search** — Use keyword strings from `00_README/keywords_queries.md` across databases.
2. **Screen** — Title/abstract screening against research questions in `00_README/research_questions.md`.
3. **Store** — Add BibTeX entry to `01_LITERATURE/library.bib` using naming convention `authorlastname_year_keyword`.
4. **Note** — Create a per-paper note from `01_LITERATURE/notes/PAPER_NOTE_TEMPLATE.md`.
5. **Extract** — Add a row to `02_EVIDENCE_MATRIX/evidence_matrix.csv` with quantitative data.
6. **Link** — Update relevance scores and cross-references in the note file.

### Evidence Tracking Workflow

1. Each paper gets a unique BibTeX key (e.g., `shaw_2005_machinability`).
2. The same key is used in the note filename, the evidence matrix `paper_id` column, and dissertation citations.
3. The evidence matrix tracks which papers provide data for which steel grades, measurement methods, and machinability metrics.
4. Gaps in the matrix reveal where additional literature or experimental work is needed.

### Conventions

- BibTeX key format: `authorlastname_year_keyword`
- Note filename format: `authorlastname_year_keyword.md`
- All conductivity values normalised to %IACS or S/m with temperature noted
- Machinability metrics follow ISO 3685 definitions where applicable
- Papers without verified full-text access are marked `NEEDS_FULLTEXT`
