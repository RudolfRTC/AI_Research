# AI_Research

**Determining machinability of low-alloy steels via electrical conductivity measurements**

Doctoral research repository for experimental development, statistical analysis, and machine learning-based prediction of machinability from electrical conductivity data.

## Research Focus

This project investigates the quantitative relationship between electrical conductivity and machinability indicators (tool wear, cutting forces, surface roughness) in low-alloy steels (AISI 1045, 4140, 4340). The goal is to develop a validated predictive model that reduces the need for costly machining trials.

**Research questions:**

- **RQ1:** What is the quantitative relationship between electrical conductivity and machinability?
- **RQ2:** How do microstructural features mediate this relationship?
- **RQ3:** Which measurement technique (4-probe DC, eddy current) is most reliable?
- **RQ4:** Can a predictive model estimate machinability from conductivity measurements?

See `00_README/research_questions.md` for detailed sub-questions, hypotheses, and success criteria.

## Repository Structure

```
AI_Research/
├── 00_README/              # Scope, research questions, search keywords
├── 01_LITERATURE/          # BibTeX library, per-paper notes, raw PDFs
├── 02_EVIDENCE_MATRIX/     # Structured CSV linking papers to data
├── 03_METHODS/             # Measurement protocols, machining procedures
├── 04_MODELS/              # Hypotheses, statistical & ML models, MLflow config
├── 05_DISSERTATION/        # Chapter outline, drafts, figures
├── 06_NEWS_WATCH/          # Alerts, monthly digests, conference calendar
├── data/                   # Raw, processed, and external datasets
│   ├── raw/
│   ├── processed/
│   └── external/
├── notebooks/              # Jupyter notebooks for experiments
├── src/machinability/      # Python package
│   ├── data/               # Data loading and preprocessing
│   ├── models/             # Baseline and predictive models
│   ├── analysis/           # Correlation and statistical analysis
│   ├── visualization/      # Plotting utilities
│   └── utils/              # Configuration and helpers
├── tests/                  # Unit tests
├── results/                # Outputs, metrics, visualisations
├── pyproject.toml          # Python project configuration
└── .gitignore
```

## Getting Started

```bash
# Clone the repository
git clone <repo-url>
cd AI_Research

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Launch Jupyter
jupyter lab
```

## Experiment Tracking

This project uses [MLflow](https://mlflow.org/) for experiment tracking. Results are stored locally in `mlruns/` (git-ignored).

```python
import mlflow
from src.machinability.utils.config import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("machinability-prediction")

with mlflow.start_run(run_name="experiment-name"):
    mlflow.log_params({"model": "RandomForest", "features": "conductivity,hardness"})
    mlflow.log_metrics({"r2": 0.85, "mape": 0.12})
```

View results: `mlflow ui` (opens at http://localhost:5000)

## Workflow

1. **Literature** — search, screen, store in `01_LITERATURE/`
2. **Evidence** — extract quantitative data to `02_EVIDENCE_MATRIX/evidence_matrix.csv`
3. **Analysis** — use notebooks and `src/` modules for correlation/modelling
4. **Track** — log all experiments with MLflow
5. **Document** — write findings in `05_DISSERTATION/`

See `00_README/scope.md` for the complete reading and evidence tracking workflow.
