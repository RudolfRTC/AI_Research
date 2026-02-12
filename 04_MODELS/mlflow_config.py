"""MLflow experiment tracking setup for machinability prediction models.

Usage in notebooks or scripts:
    from machinability_models.mlflow_config import init_tracking
    init_tracking()

    with mlflow.start_run(run_name="rf-v200-f015"):
        mlflow.log_params({"model": "RandomForest", "n_estimators": 100})
        mlflow.log_metrics({"r2": 0.85, "mape": 0.12, "rmse": 2.3})
"""

import mlflow

from src.machinability.utils.config import MLFLOW_EXPERIMENT_NAME, MLFLOW_TRACKING_URI


def init_tracking(
    tracking_uri: str = MLFLOW_TRACKING_URI,
    experiment_name: str = MLFLOW_EXPERIMENT_NAME,
) -> str:
    """Initialise MLflow tracking for this project.

    Parameters
    ----------
    tracking_uri : str
        MLflow tracking URI (default: local file store in mlruns/).
    experiment_name : str
        Experiment name.

    Returns
    -------
    str
        Experiment ID.
    """
    mlflow.set_tracking_uri(tracking_uri)
    experiment = mlflow.set_experiment(experiment_name)
    return experiment.experiment_id


# Standard parameter sets for logging
CUTTING_PARAMS_SCHEMA = {
    "cutting_speed_m_min": "Cutting speed (m/min)",
    "feed_mm_rev": "Feed rate (mm/rev)",
    "depth_mm": "Depth of cut (mm)",
    "tool_material": "Tool material / ISO code",
    "coolant": "Coolant type (dry, flood, MQL)",
}

MODEL_PARAMS_SCHEMA = {
    "model_type": "Algorithm name (RF, SVR, ANN, LinearRegression, etc.)",
    "target_metric": "Target variable (tool_life_min, Ra_um, VB_mm, Fc_N)",
    "features": "Input features used (comma-separated)",
    "cv_folds": "Number of cross-validation folds",
    "steel_grades_train": "Steel grades in training set",
}
