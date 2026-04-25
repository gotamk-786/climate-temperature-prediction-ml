from __future__ import annotations

from pathlib import Path

import pandas as pd


def format_results_table(results: pd.DataFrame) -> pd.DataFrame:
    ordered = results.copy()
    ordered["MAE"] = ordered["mae"].round(3)
    ordered["MSE"] = ordered["mse"].round(3)
    ordered["RMSE"] = ordered["rmse"].round(3)
    ordered["MAPE"] = ordered["mape"].round(3)
    ordered["R2 Score"] = ordered["r2"].round(3)
    ordered = ordered.rename(
        columns={
            "split_strategy": "Split Strategy",
            "model": "Model",
            "tuned": "Tuned",
        }
    )
    return ordered[["Split Strategy", "Model", "Tuned", "MAE", "MSE", "RMSE", "MAPE", "R2 Score"]]


def save_table(df: pd.DataFrame, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
