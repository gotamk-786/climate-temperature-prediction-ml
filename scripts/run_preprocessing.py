from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import PROCESSED_DIR, RAW_DATASET_PATH
from src.data_loader import load_temperature_data
from src.feature_engineering import build_south_asia_subset
from src.preprocessing import build_modeling_dataset, clean_temperature_data
from src.utils import ensure_directories


def main() -> None:
    ensure_directories(PROCESSED_DIR)

    raw_df = load_temperature_data(RAW_DATASET_PATH)
    cleaned_df = clean_temperature_data(raw_df, min_year=1900)
    south_asia_df = build_south_asia_subset(cleaned_df)
    modeling_df = build_modeling_dataset(cleaned_df)

    cleaned_path = PROCESSED_DIR / "cleaned_temperature_data.csv"
    south_asia_path = PROCESSED_DIR / "south_asia_subset.csv"
    modeling_path = PROCESSED_DIR / "modeling_dataset.csv"

    cleaned_df.to_csv(cleaned_path, index=False)
    south_asia_df.to_csv(south_asia_path, index=False)
    modeling_df.to_csv(modeling_path, index=False)

    print(f"Cleaned data saved to: {cleaned_path}")
    print(f"South Asia subset saved to: {south_asia_path}")
    print(f"Modeling dataset saved to: {modeling_path}")


if __name__ == "__main__":
    main()
