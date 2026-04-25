from __future__ import annotations

import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import FIGURES_DIR, MODELS_DIR, PROCESSED_DIR, TABLES_DIR
from src.train import (
    build_error_by_decade,
    extract_feature_importance,
    prediction_frame,
)
from src.utils import ensure_directories


def _save_plot(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()


def main() -> None:
    ensure_directories(FIGURES_DIR, TABLES_DIR)

    baseline_model_path = MODELS_DIR / "best_baseline_model.joblib"
    tuned_model_path = MODELS_DIR / "best_tuned_model.joblib"
    test_path = PROCESSED_DIR / "chronological_test_split.csv"
    results_path = TABLES_DIR / "model_comparison_results.csv"
    if not baseline_model_path.exists() or not tuned_model_path.exists() or not test_path.exists() or not results_path.exists():
        raise SystemExit("Missing artifacts. Run preprocessing and modeling scripts first.")

    comparison_results = pd.read_csv(results_path)
    chrono_results = comparison_results[comparison_results["Split Strategy"] == "chronological"].copy()
    best_row = chrono_results.sort_values("RMSE").iloc[0]

    if str(best_row["Tuned"]).strip().lower() == "yes":
        selected_model_path = tuned_model_path
    else:
        selected_model_path = baseline_model_path

    best_model = joblib.load(selected_model_path)
    test_df = pd.read_csv(test_path, parse_dates=["dt"])

    best_predictions = prediction_frame(
        best_model,
        test_df=test_df,
        split_strategy="chronological",
        model_name=str(best_row["Model"]),
    )
    best_predictions.to_csv(TABLES_DIR / "best_model_predictions.csv", index=False)
    build_error_by_decade(best_predictions).to_csv(TABLES_DIR / "error_by_decade.csv", index=False)

    sample_predictions = best_predictions.sample(n=min(20_000, len(best_predictions)), random_state=42)
    plt.figure(figsize=(6, 6))
    sns.scatterplot(
        data=sample_predictions,
        x="AverageTemperature",
        y="PredictedTemperature",
        alpha=0.35,
        s=18,
        color="#0B6E4F",
    )
    limits = [
        min(sample_predictions["AverageTemperature"].min(), sample_predictions["PredictedTemperature"].min()),
        max(sample_predictions["AverageTemperature"].max(), sample_predictions["PredictedTemperature"].max()),
    ]
    plt.plot(limits, limits, linestyle="--", color="#BC4B51")
    plt.title("Actual vs Predicted Temperature")
    _save_plot(FIGURES_DIR / "actual_vs_predicted_best_model.png")

    plt.figure(figsize=(8, 4))
    sns.histplot(sample_predictions["Residual"], bins=40, kde=True, color="#355070")
    plt.title("Residual Distribution")
    _save_plot(FIGURES_DIR / "residual_plot.png")

    plt.figure(figsize=(9, 4))
    sns.barplot(data=comparison_results, x="Model", y="RMSE", hue="Split Strategy")
    plt.xticks(rotation=30, ha="right")
    plt.title("Model Comparison by RMSE")
    _save_plot(FIGURES_DIR / "model_comparison_bar_chart.png")

    feature_importance = extract_feature_importance(best_model, top_n=15)
    feature_importance.to_csv(TABLES_DIR / "best_model_feature_importance.csv", index=False)
    if not feature_importance.empty:
        plt.figure(figsize=(9, 5))
        sns.barplot(data=feature_importance, x="Importance", y="Feature", hue="Feature", palette="flare", legend=False)
        plt.title("Feature Importance for Best Model")
        _save_plot(FIGURES_DIR / "feature_importance_best_model.png")

    split_comparison = (
        comparison_results.groupby("Split Strategy", as_index=False)[["RMSE", "MAPE", "R2 Score"]]
        .mean()
        .sort_values("RMSE")
    )
    split_comparison.to_csv(TABLES_DIR / "split_strategy_summary.csv", index=False)
    print("Final evaluation artifacts generated successfully.")


if __name__ == "__main__":
    main()
