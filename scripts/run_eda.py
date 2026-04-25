from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import FIGURES_DIR, PROCESSED_DIR, RAW_DATASET_PATH, TABLES_DIR
from src.data_loader import load_temperature_data
from src.eda import generate_eda_outputs
from src.utils import ensure_directories


def main() -> None:
    cleaned_path = PROCESSED_DIR / "cleaned_temperature_data.csv"
    south_asia_path = PROCESSED_DIR / "south_asia_subset.csv"
    if not cleaned_path.exists() or not south_asia_path.exists():
        raise SystemExit("Processed files not found. Run scripts/run_preprocessing.py first.")

    ensure_directories(FIGURES_DIR, TABLES_DIR)

    raw_df = load_temperature_data(RAW_DATASET_PATH)
    cleaned_df = pd.read_csv(cleaned_path, parse_dates=["dt"])
    south_asia_df = pd.read_csv(south_asia_path, parse_dates=["dt"])

    generate_eda_outputs(
        raw_df=raw_df,
        cleaned_df=cleaned_df,
        south_asia_df=south_asia_df,
        figures_dir=FIGURES_DIR,
        tables_dir=TABLES_DIR,
    )
    print("EDA outputs generated successfully.")


if __name__ == "__main__":
    main()
