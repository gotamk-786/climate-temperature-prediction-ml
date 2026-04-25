# Climate Change Analysis and Temperature Prediction Using Machine Learning

## Abstract
This study investigates the use of machine learning for predicting city-level monthly land surface temperature using historical climate records. The project is based on the Berkeley Earth climate dataset from Kaggle, with the file `GlobalLandTemperaturesByCity.csv` used as the main source. The workflow includes data cleaning, datetime parsing, geographic conversion of latitude and longitude, feature engineering, exploratory data analysis, model training, hyperparameter tuning, and comparative evaluation. Multiple regression models were used to predict `AverageTemperature`, including Linear Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor, and XGBoost. The strongest chronological-split baseline model was Random Forest, which achieved an RMSE of `1.372` and an `R2 Score` of `0.980`, with XGBoost finishing very close behind at an RMSE of `1.376`. The study also includes anomaly-based climate interpretation and a South Asia case study, making the project more climate-focused than a standard regression benchmark.

## Keywords
Climate Change, Temperature Prediction, Machine Learning, Regression, South Asia, Temperature Anomaly, Data Science

## 1. Introduction
Climate change is one of the most important environmental issues of the modern era. Rising temperatures affect ecosystems, agriculture, water resources, health systems, and urban environments. Historical climate records provide an opportunity to analyze long-term temperature trends and build predictive models that can support environmental understanding and planning.

This project focuses on temperature prediction using machine learning. In addition to prediction accuracy, the study emphasizes analytical interpretation of temperature patterns across time and region. This makes the work more meaningful than a simple predictive benchmark.

## 2. Problem Statement
The research problem is to predict monthly city-level land surface temperature from historical records using temporal and geographic features, and to compare different machine learning models to determine which approach performs best.

## 3. Objectives
1. Analyze long-term temperature trends using historical data.
2. Preprocess the dataset for reliable model training.
3. Engineer meaningful temporal and geographic features.
4. Train and compare at least four machine learning regression models.
5. Tune selected models for improved performance.
6. Interpret results in the context of climate change.
7. Add novelty through anomaly analysis and a South Asia case study.

## 4. Literature Review
This section should summarize 5 to 10 related studies on:
- climate trend analysis
- temperature prediction using machine learning
- regression methods for environmental data
- anomaly-based climate interpretation
- regional climate studies in South Asia

Use the `literature_review_notes.md` file as the base for writing this section.

## 5. Dataset Description
The dataset used is `Climate Change: Earth Surface Temperature Data` from Berkeley Earth, accessed through Kaggle.

Main file:
- `GlobalLandTemperaturesByCity.csv`

Main columns:
- `dt`
- `AverageTemperature`
- `AverageTemperatureUncertainty`
- `City`
- `Country`
- `Latitude`
- `Longitude`

Why this dataset is suitable:
- real and citable
- large historical coverage
- strong climate relevance
- suitable for regression and feature engineering

## 6. Methodology
The project follows these steps:
1. Load and inspect the raw data
2. Handle missing values and duplicates
3. Parse date features
4. Convert geographic coordinates
5. Engineer features such as season, decade, hemisphere, rolling means, lag values, and temperature anomaly
6. Perform exploratory data analysis
7. Split the data for training and testing
8. Train multiple regression models
9. Tune selected models
10. Compare models using regression metrics
11. Interpret findings globally and for South Asia

## 7. Data Preprocessing
The raw dataset contained missing temperature values and uncertainty values. Rows missing the target variable `AverageTemperature` or the date field were removed, while `AverageTemperatureUncertainty` was retained and later imputed in the modeling pipeline using median imputation. Duplicate records were removed.

The date column `dt` was converted into a datetime feature. The analysis focused on records from `1900` onward to keep the study centered on the modern climate record and to reduce extreme sparsity from the earliest period. Temporal features such as `Year`, `Month`, `Quarter`, `Decade`, and `YearsSince1900` were created. Geographic coordinates were converted from directional strings into numeric latitude and longitude values.

Feature engineering included `Lag1Temperature`, `Lag12Temperature`, `Rolling12MeanTemperature`, `HistoricalCityMonthMean`, `TemperatureAnomaly`, and `ClimateRiskIndex`. A South Asia tag was also added to support focused regional analysis. For machine learning, numeric variables were scaled with `StandardScaler`, categorical variables were encoded with `OneHotEncoder`, and the final evaluation emphasized chronological train-test splitting to avoid temporal leakage.

## 8. Exploratory Data Analysis
EDA showed that missing values were concentrated mainly in temperature and uncertainty columns in the raw dataset. The cleaned target distribution remained broad and multi-modal, which is expected for a global dataset containing both cold and hot climate zones.

The yearly global trend plot shows a long-run upward movement in average temperature across the twentieth century and beyond. Seasonal boxplots confirmed consistent seasonal structure, while region-based outlier analysis showed strong spread caused by the diversity of global climates. The global versus South Asia comparison indicated that South Asia maintains a warmer baseline than the global aggregate across most years.

Correlation analysis showed that the strongest direct modeling features were historical climate features rather than simple calendar variables alone. In particular, `HistoricalCityMonthMean`, `Lag12Temperature`, and rolling historical averages carried most of the predictive signal.

For clarity, the EDA was not handled in a sampled-only way. Full cleaned data was used for summary statistics, missing-value counts, yearly trend analysis, and the global versus South Asia comparison. For computationally expensive visualizations such as histograms, boxplots, and heatmaps, a large random sample was used so that the workflow remained practical while still preserving representative patterns.

## 9. Machine Learning Models
Planned models:
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor
5. XGBoost Regressor

The first four models satisfy the minimum course requirement, while XGBoost strengthens the comparative analysis by adding a widely used boosting-based regression model.

## 10. Hyperparameter Tuning
`RandomizedSearchCV` was used for two models:
- Random Forest
- Gradient Boosting

The search process tested combinations of estimator count, depth, learning rate, subsampling, and leaf-size settings. Tuning improved model selection rigor, but in this implementation the untuned chronological Random Forest still remained the best overall model. The tuned Gradient Boosting model matched the untuned Gradient Boosting RMSE of `1.458`, while the tuned Random Forest produced an RMSE of `1.493`, which was slightly worse than the strongest baseline Random Forest. The best-parameter outputs were saved separately so the final report can clearly show what was tried and what settings were selected.

## 11. Evaluation Metrics
The project uses regression metrics because the target variable is continuous. The main metrics were:

- `MAE` to measure average absolute prediction error
- `MSE` to penalize larger errors more strongly
- `RMSE` to express prediction error in temperature units
- `R2 Score` to show how much variance in temperature was explained by the model

These metrics are appropriate for temperature prediction and are better suited than classification metrics such as accuracy or F1-score.

## 12. Results and Discussion
Chronological split results are reported below because they provide the more realistic evaluation for climate time-series style data.

| Model | MAE | MSE | RMSE | R2 Score |
|-------|-----|-----|------|----------|
| Random Forest | 0.927 | 1.882 | 1.372 | 0.980 |
| XGBoost | 0.932 | 1.894 | 1.376 | 0.980 |
| Gradient Boosting | 0.965 | 2.126 | 1.458 | 0.978 |
| Gradient Boosting Tuned | 0.960 | 2.126 | 1.458 | 0.978 |
| Random Forest Tuned | 0.982 | 2.231 | 1.493 | 0.977 |
| Linear Regression | 1.009 | 2.391 | 1.546 | 0.975 |
| Decision Tree | 1.040 | 2.425 | 1.557 | 0.975 |

The best chronological model was Random Forest, with XGBoost performing almost equally well. An RMSE of `1.372` means the model's prediction error is roughly 1.37 degrees Celsius on average in squared-error terms, which is strong performance for a global city-level climate dataset with substantial geographic variation.

Feature importance analysis showed that `HistoricalCityMonthMean` dominated model performance, followed by `Lag12Temperature`, `Lag1Temperature`, and `Rolling12MeanTemperature`. This confirms that long-term city-specific seasonal patterns are central to accurate monthly temperature prediction.

## 13. Comparative Analysis
Discuss:
- Best RMSE: Random Forest under chronological split with `1.372`
- Best R2: Random Forest under chronological split with `0.980`
- Best generalization: Random Forest remained strongest even when evaluated under the more realistic chronological split, while XGBoost provided a competitive second-best result
- Complexity versus performance: Linear Regression performed well and remained interpretable, but tree ensembles captured nonlinear patterns more effectively
- Important features: `HistoricalCityMonthMean`, `Lag12Temperature`, `Lag1Temperature`, and `Rolling12MeanTemperature`
- Random versus chronological split: random split produced an average RMSE of `1.449`, while chronological split produced an average RMSE of `1.481`, showing that random evaluation is slightly optimistic

The before-versus-after tuning comparison also showed that tuning did not always improve the final test metrics. This is an important finding because it demonstrates that stronger methodology does not automatically mean better generalization on unseen chronological data.

## 14. Novelty of the Study
The novelty of this study lies in combining city-level temperature prediction with anomaly-based climate interpretation, time-aware validation, and a focused South Asia case study to improve both methodological realism and regional relevance.

## 15. Conclusion
This project successfully built a full climate change regression pipeline using a real global temperature dataset. The objectives of preprocessing, EDA, feature engineering, multi-model training, hyperparameter tuning, and comparative analysis were achieved.

The strongest model was Random Forest under chronological evaluation, with an RMSE of `1.372` and an `R2 Score` of `0.980`. The results show that historical seasonal context and lag-based city temperature signals are more useful than simple calendar information alone. The South Asia analysis also added local relevance and supported discussion of warming patterns in the region.

## 16. Future Work
Possible future extensions:
- use satellite or remote sensing data
- integrate Google Earth Engine based features
- include urban heat island variables
- build a climate dashboard
- test deep learning models for long-range forecasting

## 17. Limitations
This project uses a strong historical climate dataset, but it still has some limitations. The dataset does not directly include related explanatory variables such as rainfall, humidity, land cover, or urbanization. Some visually heavy EDA plots were based on large random samples rather than every row, although the main summary and trend analyses were still done on the full cleaned dataset. The source data also includes uncertainty values, which means the observations themselves are not perfectly exact.

## 18. References
Use the sources listed in `references.md`.
