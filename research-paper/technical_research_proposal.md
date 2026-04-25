# Technical Research Proposal

## Title
Climate Change Analysis and Temperature Prediction Using Machine Learning

## 1. Background
Climate change has become one of the most important global challenges because long-term temperature shifts affect agriculture, water resources, ecosystems, human health, and urban planning. Historical climate records make it possible to study these changes systematically and to build predictive models that can support evidence-based analysis.

This project focuses on monthly city-level temperature prediction using machine learning. The study is not limited to prediction only. It also includes climate interpretation through anomaly analysis, chronological validation, and a South Asia focused regional case study.

## 2. Problem Statement
The research problem is to predict monthly city-level land surface temperature from historical records using temporal and geographic features, and to identify which machine learning model gives the best balance between predictive performance, realism, and interpretability.

## 3. Research Objectives
1. Analyze long-term temperature trends using a real climate dataset.
2. Clean and preprocess the dataset for machine learning.
3. Engineer relevant temporal and geographic features.
4. Train and compare multiple regression models.
5. Tune selected models to test whether performance improves.
6. Evaluate the models using suitable regression metrics.
7. Interpret the findings in the context of climate change and South Asia.

## 4. Research Questions
1. Which features contribute most strongly to monthly temperature prediction?
2. Which regression model performs best on unseen data?
3. Does chronological validation provide a more realistic estimate than random splitting?
4. Can anomaly-based analysis and South Asia focused results improve the research value of the project?

## 5. Dataset
The project uses the `Climate Change: Earth Surface Temperature Data` dataset from Kaggle, originally based on Berkeley Earth records.

### Main File
`GlobalLandTemperaturesByCity.csv`

### Source
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

## 6. Proposed Methodology
The project will follow these technical steps:

1. Load and inspect the raw dataset.
2. Handle missing values and remove duplicates where needed.
3. Convert the date column into usable time-based attributes.
4. Convert latitude and longitude into numeric form.
5. Engineer features such as season, decade, lag temperature, rolling mean, anomaly, and region tags.
6. Perform exploratory data analysis with plots and summary tables.
7. Create train-test splits, with special emphasis on chronological validation.
8. Train multiple machine learning regression models.
9. Tune selected models using `RandomizedSearchCV`.
10. Evaluate models using `MAE`, `MSE`, `RMSE`, and `R2 Score`.
11. Compare the results and identify the strongest model.

## 7. Proposed Models
The main models selected for this study are:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor

## 8. Evaluation Plan
Since the target variable is continuous, the study uses regression metrics:
- MAE
- MSE
- RMSE
- R2 Score

The final analysis will compare:
- model-wise performance
- random split versus chronological split
- tuned versus untuned models
- important features in the best model

## 9. Expected Contribution
This project is expected to produce:
- a reproducible climate data preprocessing pipeline
- a comparative regression modeling study
- a climate interpretation layer through anomaly analysis
- a South Asia case study for local relevance

## 10. Novelty of the Study
The novelty of this work lies in combining city-level temperature prediction with anomaly-based interpretation, time-aware validation, and South Asia focused climate analysis instead of presenting only a simple multi-model benchmark.

## 11. Expected Deliverables
- processed dataset files
- EDA figures and summary tables
- trained machine learning models
- evaluation and comparison tables
- final research paper
- presentation slides

## 12. Conclusion
This proposal presents a data science project that is technically feasible, relevant to climate change, and suitable for both course submission and refinement from a TBW topic into a complete machine learning research paper.
