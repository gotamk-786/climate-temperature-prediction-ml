from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import RAW_DATASET_PATH, RAW_DIR


def main() -> None:
    try:
        import kagglehub
    except ImportError as exc:
        raise SystemExit(
            "kagglehub is not installed. Install it with `python -m pip install kagglehub`."
        ) from exc

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dataset_dir = Path(
        kagglehub.dataset_download(
            "berkeleyearth/climate-change-earth-surface-temperature-data"
        )
    )
    source_file = dataset_dir / "GlobalLandTemperaturesByCity.csv"
    if not source_file.exists():
        raise SystemExit(f"Expected file not found in download directory: {source_file}")

    shutil.copy2(source_file, RAW_DATASET_PATH)
    print(f"Dataset copied to: {RAW_DATASET_PATH}")


if __name__ == "__main__":
    main()
