from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MODELS_DIR, PROCESSED_DIR, TABLES_DIR
from src.evaluate import format_results_table, save_table
from src.train import (
    build_cross_validation_summary,
    build_tuning_comparison,
    evaluate_tuned_models,
    run_model_suite,
)
from src.utils import ensure_directories


def main() -> None:
    modeling_path = PROCESSED_DIR / "modeling_dataset.csv"
    if not modeling_path.exists():
        raise SystemExit("Modeling dataset not found. Run scripts/run_preprocessing.py first.")

    ensure_directories(TABLES_DIR, MODELS_DIR)
    data = pd.read_csv(modeling_path, parse_dates=["dt"])

    random_results, random_models = run_model_suite(data, split_strategy="random")
    chrono_results, chrono_models = run_model_suite(data, split_strategy="chronological")
    tuned_results, tuned_models, train_df, test_df, tuning_details = evaluate_tuned_models(
        data,
        split_strategy="chronological",
    )

    combined_results = pd.concat(
        [random_results, chrono_results, tuned_results],
        ignore_index=True,
    ).sort_values(["split_strategy", "rmse", "r2"], ascending=[True, True, False])

    formatted = format_results_table(combined_results)
    save_table(formatted, TABLES_DIR / "model_comparison_results.csv")
    save_table(tuning_details, TABLES_DIR / "best_hyperparameters.csv")
    save_table(build_cross_validation_summary(data), TABLES_DIR / "cross_validation_summary.csv")

    chrono_baseline_subset = chrono_results[chrono_results["model"].isin(["Random Forest", "Gradient Boosting"])].copy()
    tuning_comparison = build_tuning_comparison(chrono_baseline_subset, tuned_results)
    save_table(tuning_comparison, TABLES_DIR / "tuning_before_after_comparison.csv")

    best_baseline_name = chrono_results.sort_values("rmse").iloc[0]["model"]
    best_baseline_model = chrono_models[best_baseline_name]
    joblib.dump(best_baseline_model, MODELS_DIR / "best_baseline_model.joblib")

    best_tuned_name = tuned_results.sort_values("rmse").iloc[0]["model"]
    best_tuned_model = tuned_models[best_tuned_name]
    joblib.dump(best_tuned_model, MODELS_DIR / "best_tuned_model.joblib")

    train_df.to_csv(PROCESSED_DIR / "chronological_train_split.csv", index=False)
    test_df.to_csv(PROCESSED_DIR / "chronological_test_split.csv", index=False)
    print(f"Saved model comparison table to: {TABLES_DIR / 'model_comparison_results.csv'}")
    print(f"Saved best hyperparameters table to: {TABLES_DIR / 'best_hyperparameters.csv'}")
    print(f"Saved cross-validation summary to: {TABLES_DIR / 'cross_validation_summary.csv'}")
    print(f"Saved before/after tuning table to: {TABLES_DIR / 'tuning_before_after_comparison.csv'}")
    print(f"Saved best baseline model: {MODELS_DIR / 'best_baseline_model.joblib'}")
    print(f"Saved best tuned model: {MODELS_DIR / 'best_tuned_model.joblib'}")


if __name__ == "__main__":
    main()
