# Climate Change Predictions

This repository contains a complete Data Science course project on climate change analysis and city-level temperature prediction using machine learning. The notebooks include preprocessing, EDA, modeling, hyperparameter tuning, evaluation, and interpretation for the final submission.

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
- `notebooks/`: self-contained notebooks for cleaning, EDA, modeling, and final evaluation
- `src/`: reusable project modules kept for reference
- `data/raw/`: raw Kaggle dataset
- `data/processed/`: cleaned data, South Asia subset, modeling sample, and train/test splits
- `outputs/figures/`: generated charts
- `outputs/tables/`: generated result tables
- `outputs/models/`: saved trained models
- `paper/`: final research paper and proposal files
- `slides/`: final presentation material

## Notebook Order
1. `notebooks/01_data_cleaning.ipynb`
2. `notebooks/02_eda.ipynb`
3. `notebooks/03_modeling.ipynb`
4. `notebooks/04_final_evaluation.ipynb`

## Notes
- The raw dataset is very large, so the pipeline keeps the cleaned full working dataset for analysis and creates a stratified modeling sample for practical training time.
- All report claims should be taken from the generated tables and figures inside `outputs/`.
