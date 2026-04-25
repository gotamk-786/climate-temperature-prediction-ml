from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_temperature_data(csv_path: str | Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            "Download GlobalLandTemperaturesByCity.csv into data/raw first."
        )
    return pd.read_csv(csv_path)
