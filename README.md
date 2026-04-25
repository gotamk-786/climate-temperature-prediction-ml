# Climate Change Predictions

This repository contains a complete Data Science course project on climate change analysis and city-level temperature prediction using machine learning. The implementation follows the project rules defined in `AGENT.md` and produces reproducible preprocessing, EDA, modeling, tuning, and final evaluation outputs.

## Dataset
- Source: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
- Main file: `GlobalLandTemperaturesByCity.csv`
- Local path: `data/raw/GlobalLandTemperaturesByCity.csv`
- Working analysis window: data from `1900` onward to focus on the modern climate record

## Implemented Highlights
- Regression-based temperature prediction for `AverageTemperature`
- Leakage-aware historical features such as lag values and historical city-month averages
- Global and South Asia analysis tracks
- Random split and chronological split comparison
- Baseline models:
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor
  - Gradient Boosting Regressor
  - XGBoost Regressor when available
- Hyperparameter tuning for:
  - Random Forest
  - Gradient Boosting

## Folder Overview
- `AGENT.md`: project instructions and acceptance criteria
- `src/`: reusable project modules
- `scripts/`: runnable pipeline scripts
- `notebooks/`: required notebooks for cleaning, EDA, modeling, and final evaluation
- `data/raw/`: raw Kaggle dataset
- `data/processed/`: cleaned data, South Asia subset, modeling sample, and train/test splits
- `outputs/figures/`: generated charts
- `outputs/tables/`: generated result tables
- `outputs/models/`: saved trained models
- `research-paper/`: report drafting material

## Run Order
1. `python scripts/run_preprocessing.py`
2. `python scripts/run_eda.py`
3. `python scripts/run_modeling.py`
4. `python scripts/run_final_evaluation.py`

## Notes
- The raw dataset is very large, so the pipeline keeps the cleaned full working dataset for analysis and creates a stratified modeling sample for practical training time.
- All report claims should be taken from the generated tables and figures inside `outputs/`.
