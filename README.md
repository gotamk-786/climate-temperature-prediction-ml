# Climate Change Temperature Prediction

GitHub Repository: https://github.com/gotamk-786/climate-temperature-prediction-ml

This repository contains a complete Data Science course project on climate change analysis and city-level temperature prediction using machine learning. The project studies long-term temperature behavior from the Berkeley Earth dataset and builds regression models to predict `AverageTemperature`.

The work is prepared for academic submission through self-contained Jupyter notebooks, generated result tables, visualizations, a final research paper, presentation slides, and a short presentation video.

## Project Objective

The main objective is to analyze climate change patterns and predict city-level average temperature using historical climate records.

The project focuses on:

- defining a real climate-related prediction problem
- cleaning and preparing a large real-world dataset
- performing exploratory data analysis with visualizations
- engineering meaningful temporal and geographic features
- training and comparing multiple machine learning models
- tuning selected models
- evaluating performance using regression metrics
- interpreting the results in a research-paper format

## Dataset Details

- Dataset source: Berkeley Earth Climate Change: Earth Surface Temperature Data
- Kaggle link: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
- Main raw file: `GlobalLandTemperaturesByCity.csv`
- Target variable: `AverageTemperature`
- Unit: temperature in Celsius
- Main columns used:
  - `dt`
  - `AverageTemperature`
  - `AverageTemperatureUncertainty`
  - `City`
  - `Country`
  - `Latitude`
  - `Longitude`

The dataset contains historical city-level temperature records from many countries. For this project, records from year `1900` onward are used to focus on the modern climate period and reduce the effect of very old sparse records.

## Preprocessing Work

The preprocessing notebook handles:

- converting date values into proper datetime format
- extracting `Year`, `Month`, `Quarter`, `Decade`, and `YearsSince1900`
- removing rows with missing target temperature values
- removing duplicate rows
- converting latitude and longitude values from direction format into signed numeric coordinates
- creating season labels such as Winter, Spring, Summer, and Autumn
- tagging hemisphere based on latitude
- tagging South Asian countries for regional climate analysis
- preparing a modeling dataset from the cleaned climate records

Missing values are checked before and after cleaning. The modeling dataset removes rows where required model features are not available.

## Feature Engineering

Several climate-aware features were created to improve model performance and interpretation:

- `Lag1Temperature`: previous monthly temperature for the same city
- `Lag12Temperature`: temperature from the same month in the previous year
- `Rolling12MeanTemperature`: rolling yearly mean based on previous observations
- `HistoricalCityMonthMean`: historical average for each city-month combination
- `TemperatureAnomaly`: difference from the historical city-month mean
- `CityYearMeanTemperature`: yearly average temperature for each city
- `DecadeMeanTemperature`: average temperature by decade
- `ClimateRiskIndex`: combined standardized signal based on anomaly, uncertainty, and decade trend

These features help the models learn seasonality, long-term trends, and location-specific climate behavior.

## Exploratory Data Analysis

The EDA notebook includes:

- missing-value summary
- descriptive statistics
- temperature distribution plot
- global temperature trend over time
- seasonal temperature variation
- country-level temperature comparison
- global vs South Asia temperature trend
- Pakistan vs global trend
- Pakistan city-level trend comparison
- correlation heatmap
- outlier inspection
- South Asia warming-rate comparison

The EDA is used to support the research paper discussion with visual evidence rather than relying only on model accuracy.

## Machine Learning Models

This is a regression problem because the target value is a continuous temperature value.

The following models were implemented and compared:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor

The project compares both random split and chronological split results. The chronological split is important because climate data is time-based, and future prediction should be tested on later records.

## Hyperparameter Tuning

Hyperparameter tuning was performed for:

- Random Forest Regressor
- Gradient Boosting Regressor

Randomized search with cross-validation was used to test different parameter combinations. The tuning results are saved in:

- `outputs/tables/best_hyperparameters.csv`
- `outputs/tables/tuning_before_after_comparison.csv`

## Evaluation Metrics

The models were evaluated using:

- MAE
- MSE
- RMSE
- MAPE
- R2 Score

The main comparison table is saved in:

- `outputs/tables/model_comparison_results.csv`

## Main Results

The best chronological baseline result was achieved by Random Forest:

- MAE: `0.927`
- RMSE: `1.372`
- R2 Score: `0.980`

XGBoost also performed strongly:

- RMSE: `1.376`
- R2 Score: `0.980`

The feature-importance analysis showed that `HistoricalCityMonthMean` was the most influential feature, followed by lag and rolling temperature features. This confirms that historical city-specific seasonality is highly important for temperature prediction.

South Asia warming-rate analysis showed warming trends across selected countries. In this project output, Pakistan shows an estimated warming rate of about `0.110 C per decade`.

## Research Paper Work

The research paper is based on the complete data science workflow:

- problem definition and objectives
- dataset description and source citation
- preprocessing methodology
- feature engineering explanation
- EDA findings with generated plots
- machine learning model implementation
- hyperparameter tuning
- experimental results
- comparative model analysis
- final conclusion and limitations

Final paper files are available in:

- `research paper/research_paper_final.docx`

## Repository Structure

- `notebooks/`: self-contained Jupyter notebooks for the complete workflow
- `data/raw/`: raw dataset note and local raw data location
- `data/processed/`: final modeling dataset and processed-data notes
- `outputs/figures/`: generated charts used in analysis and report
- `outputs/tables/`: generated metric tables and result summaries
- `research paper/`: final IEEE-format research paper
- `video and slide/`: final presentation slides and recorded presentation video
- `requirements.txt`: Python package requirements

## Notebook Order

Run or review the notebooks in this order:

1. `notebooks/01_data_cleaning.ipynb`
2. `notebooks/02_eda.ipynb`
3. `notebooks/03_modeling.ipynb`
4. `notebooks/04_final_evaluation.ipynb`

The notebooks are self-contained, so the main project logic required for marking is included inside the notebooks.

## Submission Files

For teacher submission, the important files are:

- Dataset: `data/raw/GlobalLandTemperaturesByCity.csv`
- Notebooks:
  - `notebooks/01_data_cleaning.ipynb`
  - `notebooks/02_eda.ipynb`
  - `notebooks/03_modeling.ipynb`
  - `notebooks/04_final_evaluation.ipynb`
- Research paper:
  - `research paper/research_paper_final.docx`
- Presentation slides:
  - `video and slide/climate_change_prediction_presentation.pptx`
- Presentation video:
  - `video and slide/video1484401397.mp4`

## Notes

- The raw dataset is included because the submission requires the data file used for the project.
- All claims in the paper are supported by generated tables and figures inside `outputs/`.
- This project is related to the climate change bonus topic. Some extra features such as lag temperature, rolling mean, anomaly, and regional comparison were also used.
