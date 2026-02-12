"""Project paths and configuration."""

from pathlib import Path

# Repository root (assumes this file is at src/machinability/utils/config.py)
REPO_ROOT = Path(__file__).resolve().parents[3]

# Standard paths
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
DATA_EXTERNAL = REPO_ROOT / "data" / "external"
EVIDENCE_MATRIX = REPO_ROOT / "02_EVIDENCE_MATRIX" / "evidence_matrix.csv"
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
RESULTS_DIR = REPO_ROOT / "results"
MODELS_DIR = REPO_ROOT / "04_MODELS"

# MLflow
MLFLOW_TRACKING_URI = f"file://{REPO_ROOT / 'mlruns'}"
MLFLOW_EXPERIMENT_NAME = "machinability-prediction"
