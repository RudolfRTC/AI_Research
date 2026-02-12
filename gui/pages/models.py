"""ML Model Training & Evaluation page (RQ4).

Provides an interactive Streamlit interface for training regression models
on machinability data, comparing them against the HardnessOnly baseline,
and evaluating research hypotheses H4a-H4d.
"""

import time

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.svm import SVR

from src.machinability.models.baseline import HardnessOnlyBaseline, evaluate_model


# ---------------------------------------------------------------------------
# Synthetic data generation
# ---------------------------------------------------------------------------

def _generate_synthetic_data(n: int = 80, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic machinability data for demonstration.

    Produces *n* specimens spread across three AISI steel grades with
    realistic correlations between features and targets.

    Parameters
    ----------
    n : int
        Number of specimens (default 80).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: steel_grade, conductivity, hardness,
        composition_C, composition_Mn, composition_Cr, tool_life, Ra, Fc.
    """
    rng = np.random.default_rng(seed)

    grades = np.array(["AISI 1045", "AISI 4140", "AISI 4340"])
    grade_assignment = rng.choice(grades, size=n)

    # Grade-specific base properties
    grade_props = {
        "AISI 1045": {"cond": 7.5, "hard": 200, "C": 0.45, "Mn": 0.75, "Cr": 0.04},
        "AISI 4140": {"cond": 5.1, "hard": 280, "C": 0.40, "Mn": 0.87, "Cr": 1.00},
        "AISI 4340": {"cond": 4.3, "hard": 320, "C": 0.40, "Mn": 0.70, "Cr": 0.80},
    }

    records = []
    for i in range(n):
        g = grade_assignment[i]
        p = grade_props[g]

        conductivity = p["cond"] + rng.normal(0, 0.4)
        hardness = p["hard"] + rng.normal(0, 15)
        comp_C = np.clip(p["C"] + rng.normal(0, 0.02), 0.10, 0.70)
        comp_Mn = np.clip(p["Mn"] + rng.normal(0, 0.05), 0.30, 1.20)
        comp_Cr = np.clip(p["Cr"] + rng.normal(0, 0.05), 0.0, 1.50)

        # Targets with realistic correlations
        tool_life = (
            120
            + 8.0 * conductivity
            - 0.35 * hardness
            - 40 * comp_C
            + 10 * comp_Mn
            - 15 * comp_Cr
            + rng.normal(0, 6)
        )
        Ra = (
            0.3
            - 0.03 * conductivity
            + 0.003 * hardness
            + 0.5 * comp_C
            + rng.normal(0, 0.08)
        )
        Fc = (
            300
            - 12 * conductivity
            + 1.5 * hardness
            + 100 * comp_C
            + 50 * comp_Cr
            + rng.normal(0, 20)
        )

        records.append(
            {
                "steel_grade": g,
                "conductivity": round(conductivity, 3),
                "hardness": round(hardness, 1),
                "composition_C": round(comp_C, 4),
                "composition_Mn": round(comp_Mn, 4),
                "composition_Cr": round(comp_Cr, 4),
                "tool_life": round(max(tool_life, 5), 2),
                "Ra": round(max(Ra, 0.05), 4),
                "Fc": round(max(Fc, 50), 2),
            }
        )

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Model factory
# ---------------------------------------------------------------------------

_MODEL_MAP = {
    "Linear Regression": LinearRegression,
    "SVR": SVR,
    "Random Forest": RandomForestRegressor,
    "Gradient Boosting": GradientBoostingRegressor,
}


def _make_model(name: str):
    """Instantiate an sklearn estimator by display name."""
    cls = _MODEL_MAP[name]
    if name == "SVR":
        return cls(kernel="rbf", C=10.0, epsilon=0.1)
    if name == "Random Forest":
        return cls(n_estimators=100, random_state=42)
    if name == "Gradient Boosting":
        return cls(n_estimators=100, learning_rate=0.1, random_state=42)
    return cls()


# ---------------------------------------------------------------------------
# Hypothesis criteria (RQ4)
# ---------------------------------------------------------------------------

_HYPOTHESES = {
    "H4a": {
        "description": (
            "Conductivity-based features improve predictive accuracy for "
            "tool life beyond hardness-only baselines."
        ),
        "criterion": "MAPE < 15% AND R\u00b2 > 0.75 for tool_life target",
    },
    "H4b": {
        "description": (
            "ML models incorporating conductivity achieve > 10% lower MAPE "
            "than the HardnessOnly baseline."
        ),
        "criterion": "Relative MAPE improvement > 10% vs baseline",
    },
    "H4c": {
        "description": (
            "Random Forest or Gradient Boosting outperforms linear models "
            "when conductivity features are included."
        ),
        "criterion": "Non-linear model R\u00b2 exceeds linear model R\u00b2",
    },
    "H4d": {
        "description": (
            "Feature importance analysis ranks conductivity among the top-3 "
            "predictors."
        ),
        "criterion": "Conductivity in top-3 features by importance",
    },
}


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    """Render the ML Model Training & Evaluation page."""

    st.header("ML Model Training & Evaluation")
    st.markdown(
        "Train regression models on machinability data and compare against "
        "the **HardnessOnly** baseline (RQ4)."
    )

    # Initialise session state for model comparison history
    if "model_results" not in st.session_state:
        st.session_state["model_results"] = []

    # ------------------------------------------------------------------
    # Sidebar: Model configuration
    # ------------------------------------------------------------------
    st.subheader("Model Configuration")

    col_cfg1, col_cfg2 = st.columns(2)

    with col_cfg1:
        model_name = st.selectbox(
            "Model type",
            list(_MODEL_MAP.keys()),
            help="Choose the regression algorithm to train.",
        )

        all_features = [
            "conductivity",
            "hardness",
            "composition_C",
            "composition_Mn",
            "composition_Cr",
        ]
        selected_features = st.multiselect(
            "Input features",
            all_features,
            default=all_features,
            help="Select one or more features to use as predictors.",
        )

    with col_cfg2:
        target_variable = st.selectbox(
            "Target variable",
            ["tool_life", "Ra", "Fc"],
            help="Machinability metric to predict.",
        )

        test_size = st.slider(
            "Test split ratio",
            min_value=0.1,
            max_value=0.4,
            value=0.2,
            step=0.05,
        )

        cv_folds = st.slider(
            "CV folds",
            min_value=3,
            max_value=10,
            value=5,
            step=1,
        )

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    st.divider()
    train_clicked = st.button("Train Model", type="primary", use_container_width=True)

    if train_clicked:
        if not selected_features:
            st.error("Please select at least one input feature.")
            return

        # --- Load or generate data ---
        progress = st.progress(0, text="Preparing data...")
        df = _generate_synthetic_data()
        time.sleep(0.15)
        progress.progress(10, text="Data ready. Splitting...")

        X = df[selected_features].values
        y = df[target_variable].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        progress.progress(20, text="Training model...")

        # --- Train selected model ---
        model = _make_model(model_name)
        model.fit(X_train, y_train)
        progress.progress(50, text="Generating predictions...")

        y_pred = model.predict(X_test)
        metrics = evaluate_model(y_test, y_pred)
        progress.progress(65, text="Cross-validating...")

        # --- Cross-validation ---
        cv_scores = cross_val_score(
            _make_model(model_name), X, y, cv=cv_folds, scoring="r2"
        )
        progress.progress(80, text="Training baseline...")

        # --- Baseline comparison ---
        if "hardness" in selected_features:
            hardness_idx = selected_features.index("hardness")
            X_hard_train = X_train[:, hardness_idx].reshape(-1, 1)
            X_hard_test = X_test[:, hardness_idx].reshape(-1, 1)
        else:
            # Use hardness column from full dataframe for baseline regardless
            hard_all = df["hardness"].values
            hard_train, hard_test = train_test_split(
                hard_all, test_size=test_size, random_state=42
            )
            X_hard_train = hard_train.reshape(-1, 1)
            X_hard_test = hard_test.reshape(-1, 1)

        baseline = HardnessOnlyBaseline()
        baseline.fit(X_hard_train, y_train)
        y_pred_base = baseline.predict(X_hard_test)
        baseline_metrics = evaluate_model(y_test, y_pred_base)

        progress.progress(100, text="Done!")
        time.sleep(0.25)
        progress.empty()

        # ----------------------------------------------------------
        # Store results
        # ----------------------------------------------------------
        result = {
            "model": model_name,
            "features": ", ".join(selected_features),
            "target": target_variable,
            "R2": round(metrics["r2"], 4),
            "MAPE": round(metrics["mape"] * 100, 2),
            "RMSE": round(metrics["rmse"], 4),
            "CV_mean_R2": round(float(np.mean(cv_scores)), 4),
            "Baseline_R2": round(baseline_metrics["r2"], 4),
            "Baseline_MAPE": round(baseline_metrics["mape"] * 100, 2),
        }

        # Avoid exact duplicates
        existing_keys = [
            (r["model"], r["features"], r["target"])
            for r in st.session_state["model_results"]
        ]
        key = (result["model"], result["features"], result["target"])
        if key in existing_keys:
            idx = existing_keys.index(key)
            st.session_state["model_results"][idx] = result
        else:
            st.session_state["model_results"].append(result)

        # ----------------------------------------------------------
        # Metrics cards
        # ----------------------------------------------------------
        st.subheader("Performance Metrics")

        m1, m2, m3 = st.columns(3)
        m1.metric(
            "R\u00b2",
            f"{metrics['r2']:.4f}",
            delta=f"{metrics['r2'] - baseline_metrics['r2']:+.4f} vs baseline",
        )
        m2.metric(
            "MAPE",
            f"{metrics['mape'] * 100:.2f}%",
            delta=f"{(metrics['mape'] - baseline_metrics['mape']) * 100:+.2f}pp vs baseline",
            delta_color="inverse",
        )
        m3.metric(
            "RMSE",
            f"{metrics['rmse']:.4f}",
            delta=f"{metrics['rmse'] - baseline_metrics['rmse']:+.4f} vs baseline",
            delta_color="inverse",
        )

        # ----------------------------------------------------------
        # Results Visualization
        # ----------------------------------------------------------
        st.subheader("Results Visualization")

        tab_pred, tab_resid, tab_imp, tab_cv = st.tabs(
            ["Actual vs Predicted", "Residuals", "Feature Importance", "CV Scores"]
        )

        # --- Actual vs Predicted scatter ---
        with tab_pred:
            fig_pred = px.scatter(
                x=y_test,
                y=y_pred,
                labels={"x": f"Actual {target_variable}", "y": f"Predicted {target_variable}"},
                title=f"Actual vs Predicted - {model_name}",
                opacity=0.7,
            )
            # Perfect prediction line
            axis_min = min(float(y_test.min()), float(y_pred.min()))
            axis_max = max(float(y_test.max()), float(y_pred.max()))
            fig_pred.add_trace(
                go.Scatter(
                    x=[axis_min, axis_max],
                    y=[axis_min, axis_max],
                    mode="lines",
                    line=dict(dash="dash", color="red"),
                    name="Perfect prediction",
                )
            )
            fig_pred.update_layout(showlegend=True)
            st.plotly_chart(fig_pred, use_container_width=True)

        # --- Residuals plot ---
        with tab_resid:
            residuals = y_test - y_pred
            fig_resid = px.scatter(
                x=y_pred,
                y=residuals,
                labels={"x": f"Predicted {target_variable}", "y": "Residual"},
                title=f"Residuals - {model_name}",
                opacity=0.7,
            )
            fig_resid.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig_resid, use_container_width=True)

        # --- Feature importance (RF / GB only) ---
        with tab_imp:
            if model_name in ("Random Forest", "Gradient Boosting"):
                importances = model.feature_importances_
                imp_df = pd.DataFrame(
                    {"feature": selected_features, "importance": importances}
                ).sort_values("importance", ascending=True)

                fig_imp = px.bar(
                    imp_df,
                    x="importance",
                    y="feature",
                    orientation="h",
                    title=f"Feature Importance - {model_name}",
                    labels={"importance": "Importance", "feature": "Feature"},
                )
                fig_imp.update_layout(yaxis=dict(categoryorder="total ascending"))
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                st.info(
                    "Feature importance is available for **Random Forest** and "
                    "**Gradient Boosting** models only."
                )

        # --- Cross-validation scores box plot ---
        with tab_cv:
            cv_df = pd.DataFrame(
                {"fold": [f"Fold {i+1}" for i in range(len(cv_scores))], "R2": cv_scores}
            )
            fig_cv = px.box(
                cv_df,
                y="R2",
                points="all",
                title=f"Cross-Validation R\u00b2 ({cv_folds}-fold) - {model_name}",
                labels={"R2": "R\u00b2 Score"},
            )
            fig_cv.update_layout(showlegend=False)
            st.plotly_chart(fig_cv, use_container_width=True)

            st.caption(
                f"Mean R\u00b2 = {np.mean(cv_scores):.4f}  |  "
                f"Std = {np.std(cv_scores):.4f}"
            )

    # ------------------------------------------------------------------
    # Model Comparison (always visible if results exist)
    # ------------------------------------------------------------------
    if st.session_state["model_results"]:
        st.divider()
        st.subheader("Model Comparison")

        comp_df = pd.DataFrame(st.session_state["model_results"])
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        # --- Comparison bar charts ---
        comp_col1, comp_col2 = st.columns(2)

        with comp_col1:
            fig_r2 = px.bar(
                comp_df,
                x="model",
                y="R2",
                color="target",
                barmode="group",
                title="R\u00b2 Comparison",
                labels={"R2": "R\u00b2", "model": "Model"},
            )
            fig_r2.add_hline(
                y=0.75, line_dash="dot", line_color="green",
                annotation_text="H4a threshold (0.75)",
            )
            st.plotly_chart(fig_r2, use_container_width=True)

        with comp_col2:
            fig_mape = px.bar(
                comp_df,
                x="model",
                y="MAPE",
                color="target",
                barmode="group",
                title="MAPE Comparison (%)",
                labels={"MAPE": "MAPE (%)", "model": "Model"},
            )
            fig_mape.add_hline(
                y=15, line_dash="dot", line_color="green",
                annotation_text="H4a threshold (15%)",
            )
            st.plotly_chart(fig_mape, use_container_width=True)

        # --- Clear history button ---
        if st.button("Clear comparison history"):
            st.session_state["model_results"] = []
            st.rerun()

    # ------------------------------------------------------------------
    # Hypotheses Status (RQ4)
    # ------------------------------------------------------------------
    st.divider()
    st.subheader("Hypotheses Status (RQ4)")

    # Gather best results per hypothesis check
    results = st.session_state["model_results"]

    for hyp_id, hyp in _HYPOTHESES.items():
        with st.expander(f"{hyp_id}: {hyp['description']}", expanded=True):
            st.caption(f"Criterion: {hyp['criterion']}")

            if not results:
                st.warning("No models trained yet. Train a model to evaluate hypotheses.")
                continue

            if hyp_id == "H4a":
                # MAPE < 15% AND R2 > 0.75 for tool_life
                tool_life_results = [r for r in results if r["target"] == "tool_life"]
                if not tool_life_results:
                    st.warning("No models trained on tool_life target yet.")
                else:
                    best = min(tool_life_results, key=lambda r: r["MAPE"])
                    passed = best["MAPE"] < 15.0 and best["R2"] > 0.75
                    if passed:
                        st.success(
                            f"SUPPORTED -- Best model ({best['model']}): "
                            f"MAPE = {best['MAPE']:.2f}%, R\u00b2 = {best['R2']:.4f}"
                        )
                    else:
                        st.error(
                            f"NOT SUPPORTED -- Best model ({best['model']}): "
                            f"MAPE = {best['MAPE']:.2f}%, R\u00b2 = {best['R2']:.4f}"
                        )

            elif hyp_id == "H4b":
                # > 10% relative MAPE improvement vs baseline
                improvements = []
                for r in results:
                    if r["Baseline_MAPE"] > 0:
                        rel_imp = (r["Baseline_MAPE"] - r["MAPE"]) / r["Baseline_MAPE"] * 100
                        improvements.append((r, rel_imp))
                if not improvements:
                    st.warning("No baseline comparisons available.")
                else:
                    best_r, best_imp = max(improvements, key=lambda x: x[1])
                    passed = best_imp > 10.0
                    if passed:
                        st.success(
                            f"SUPPORTED -- Best improvement ({best_r['model']} on "
                            f"{best_r['target']}): {best_imp:.1f}% MAPE reduction "
                            f"vs baseline"
                        )
                    else:
                        st.error(
                            f"NOT SUPPORTED -- Best improvement ({best_r['model']} on "
                            f"{best_r['target']}): {best_imp:.1f}% MAPE reduction "
                            f"vs baseline (need > 10%)"
                        )

            elif hyp_id == "H4c":
                # Non-linear model R2 > linear model R2
                linear_results = [
                    r for r in results if r["model"] in ("Linear Regression", "SVR")
                ]
                nonlinear_results = [
                    r for r in results
                    if r["model"] in ("Random Forest", "Gradient Boosting")
                ]
                if not linear_results or not nonlinear_results:
                    st.warning(
                        "Need at least one linear model (Linear Regression/SVR) and "
                        "one non-linear model (Random Forest/Gradient Boosting) "
                        "trained on the same target to evaluate."
                    )
                else:
                    best_linear = max(linear_results, key=lambda r: r["R2"])
                    best_nonlinear = max(nonlinear_results, key=lambda r: r["R2"])
                    passed = best_nonlinear["R2"] > best_linear["R2"]
                    if passed:
                        st.success(
                            f"SUPPORTED -- {best_nonlinear['model']} "
                            f"(R\u00b2 = {best_nonlinear['R2']:.4f}) > "
                            f"{best_linear['model']} "
                            f"(R\u00b2 = {best_linear['R2']:.4f})"
                        )
                    else:
                        st.error(
                            f"NOT SUPPORTED -- {best_nonlinear['model']} "
                            f"(R\u00b2 = {best_nonlinear['R2']:.4f}) <= "
                            f"{best_linear['model']} "
                            f"(R\u00b2 = {best_linear['R2']:.4f})"
                        )

            elif hyp_id == "H4d":
                # Conductivity in top-3 features by importance
                tree_results = [
                    r for r in results
                    if r["model"] in ("Random Forest", "Gradient Boosting")
                    and "conductivity" in r["features"]
                ]
                if not tree_results:
                    st.warning(
                        "Need a Random Forest or Gradient Boosting model trained "
                        "with conductivity in the feature set to evaluate."
                    )
                else:
                    # Re-train the best tree model to extract importance
                    best_tree = max(tree_results, key=lambda r: r["R2"])
                    feats = [f.strip() for f in best_tree["features"].split(",")]
                    df_synth = _generate_synthetic_data()
                    X_all = df_synth[feats].values
                    y_all = df_synth[best_tree["target"]].values
                    temp_model = _make_model(best_tree["model"])
                    temp_model.fit(X_all, y_all)
                    imp_order = np.argsort(temp_model.feature_importances_)[::-1]
                    top3_features = [feats[i] for i in imp_order[:3]]
                    passed = "conductivity" in top3_features
                    if passed:
                        st.success(
                            f"SUPPORTED -- Top-3 features for "
                            f"{best_tree['model']}: {top3_features}"
                        )
                    else:
                        st.error(
                            f"NOT SUPPORTED -- Top-3 features for "
                            f"{best_tree['model']}: {top3_features} "
                            f"(conductivity not in top 3)"
                        )
