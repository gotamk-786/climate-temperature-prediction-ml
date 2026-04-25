# AGENT.md

## Project Title
Climate Change Analysis and Temperature Prediction Using Machine Learning

## Project Purpose
This file is the execution guide for the Data Science course project. It defines the research problem, dataset, workflow, modeling plan, evaluation strategy, research paper structure, and bonus-oriented novelty.

## Course Alignment Status
This project fulfills the teacher's project description if implemented as written.

Requirement coverage:
- Problem definition: covered
- Real dataset: covered
- Data preprocessing: covered
- EDA with visualizations: covered
- At least 4 machine learning models: covered
- Hyperparameter tuning: covered
- Evaluation and comparative analysis: covered
- Research paper with implementation and results: covered
- Climate change bonus domain: covered

Important note:
- The official course format is group-based. Final submission should be prepared as a group project of 3 to 4 students.

---

## Core Goal
Build a complete climate change data science project that predicts city-level monthly temperature using historical, temporal, and geographic features. The project must include preprocessing, EDA, at least 4 machine learning models, hyperparameter tuning, comparative evaluation, a research paper, and slides.

## Recommended Problem Statement
Global and regional temperature patterns are changing over time due to climate change. The aim of this project is to analyze long-term city-level temperature records and build machine learning models that predict monthly temperature while also generating meaningful climate interpretation from the results.

## Refined Research Problem
How accurately can machine learning models predict city-level monthly land surface temperature from historical climate records, and which feature engineering and modeling strategy provides the best balance between performance, interpretability, and climate relevance?

## Research Questions
1. Which temporal and geographic features most improve temperature prediction?
2. Which regression model performs best on unseen data?
3. Does time-aware validation provide a more realistic estimate than random split evaluation?
4. Can a South Asia focused analysis add local relevance and stronger climate interpretation?
5. Does anomaly-based analysis make the project more research-oriented than raw temperature prediction alone?

---

## Why Regression and Not Classification
Regression is the correct choice because:
- The target variable is continuous: `AverageTemperature`
- The project predicts actual temperature values, not categories
- The teacher's allowed metrics include regression metrics such as RMSE
- Classification would only make sense if the target were classes like hot, cold, or normal

Evaluation metrics to use:
- MAE
- MSE
- RMSE
- R2 Score

---

## Dataset Selected

### Dataset Name
Climate Change: Earth Surface Temperature Data

### Source
Kaggle - Berkeley Earth Climate Data
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

### Primary File
`GlobalLandTemperaturesByCity.csv`

### Dataset Download Location
Store the dataset here after download:
`data/raw/GlobalLandTemperaturesByCity.csv`

### Official Dataset Link for Submission
Use this exact link in the report and README:
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

### Why This Dataset
- Real and publicly available
- Directly relevant to climate change
- Large enough for meaningful analysis
- Contains temporal and geographic information
- Suitable for regression and feature engineering
- Strong fit for bonus marks under the climate change domain

### Dataset Columns
| Column | Description |
|--------|-------------|
| dt | Date of record |
| AverageTemperature | Monthly average land surface temperature in Celsius |
| AverageTemperatureUncertainty | Uncertainty range of the estimate |
| City | City name |
| Country | Country name |
| Latitude | Latitude as string |
| Longitude | Longitude as string |

### Citation
Berkeley Earth. (2017). Climate Change: Earth Surface Temperature Data. Kaggle.
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

---

## Research Objectives
1. Analyze global and regional temperature trends.
2. Clean and preprocess the dataset for reproducible modeling.
3. Engineer strong temporal and geographic features.
4. Train and compare at least 4 regression models.
5. Tune at least 2 models using hyperparameter search.
6. Evaluate models using proper regression metrics.
7. Interpret model results in the context of climate change.
8. Add novelty through anomaly analysis, time-aware validation, and a South Asia case study.

---

## Project Type
Regression

Target variable:
`AverageTemperature`

Optional analytical secondary target:
`TemperatureAnomaly`

Definition:
`TemperatureAnomaly = AverageTemperature - long_term_city_month_average`

---

## What Must Be Built

### 1. Problem Definition
- Clearly state the research problem
- Explain why climate change and temperature prediction matter
- Define target variable and objectives
- Justify regression over classification

### 2. Dataset Section
- Describe the source, file, columns, and suitability
- Mention dataset scale
- Cite the source properly

### 3. Data Preprocessing
Must include:
- Missing value handling
- Duplicate removal if needed
- Datetime parsing
- Year and month extraction
- Latitude and longitude conversion to numeric form
- Scaling or normalization
- Feature engineering
- Train-test split
- Prefer chronological split in final evaluation to avoid leakage

### 4. Exploratory Data Analysis
Must include:
- Summary statistics
- Missing value analysis
- Distribution of target variable
- Temperature trends over time
- Seasonal variation
- Country or region comparison
- Correlation analysis
- Outlier inspection

### 5. Model Building
Minimum required models:
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor

Recommended stronger addition:
5. XGBoost Regressor

### 6. Hyperparameter Tuning
Must include:
- GridSearchCV or RandomizedSearchCV on at least 2 models
- Best parameter reporting
- Before and after tuning comparison

### 7. Evaluation
Use:
- MAE
- MSE
- RMSE
- R2 Score

Must include:
- Comparison table for all models
- Best model identification
- Error interpretation
- Discussion of generalization

### 8. Research Paper
Paper must include actual implementation, results, and comparative analysis.

### 9. Presentation
Must include:
- Problem
- Dataset
- Workflow
- EDA
- Models
- Results table
- Best model
- Conclusion and future work

---

## Recommended Folder Structure

```text
climate-change-predictions/
|-- AGENT.md
|-- README.md
|-- data/
|   |-- raw/
|   |   `-- GlobalLandTemperaturesByCity.csv
|   `-- processed/
|       `-- cleaned_data.csv
|-- notebooks/
|   |-- 01_data_cleaning.ipynb
|   |-- 02_eda.ipynb
|   |-- 03_modeling.ipynb
|   `-- 04_final_evaluation.ipynb
|-- src/
|   |-- data_loader.py
|   |-- preprocessing.py
|   |-- feature_engineering.py
|   |-- train.py
|   |-- evaluate.py
|   `-- utils.py
|-- outputs/
|   |-- figures/
|   |-- tables/
|   `-- models/
|-- paper/
|   `-- research_paper.pdf
`-- slides/
    `-- presentation.pptx
```

---

## Feature Engineering Plan
Include these features:
- Year
- Month
- Season
- Latitude as float
- Longitude as float
- Hemisphere
- Decade
- Rolling temperature average
- Lag temperature features
- City monthly historical mean
- Temperature anomaly
- Region tag such as South Asia vs Global

---

## Model Plan
Recommended final set:
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor
5. XGBoost Regressor

Reason:
- Includes both baseline and advanced models
- Supports strong comparative analysis
- Improves research paper quality

---

## Evaluation Table Format

| Model | MAE | MSE | RMSE | R2 Score |
|-------|-----|-----|------|----------|
| Linear Regression | ... | ... | ... | ... |
| Decision Tree | ... | ... | ... | ... |
| Random Forest | ... | ... | ... | ... |
| Gradient Boosting | ... | ... | ... | ... |
| XGBoost | ... | ... | ... | ... |

---

## Graphs That Must Be Included
- Missing values chart
- Distribution plot of `AverageTemperature`
- Correlation heatmap
- Global temperature trend over time
- Seasonal boxplot
- Country or region comparison
- Outlier boxplots
- Actual vs predicted plot for the best model
- Residual plot
- Model comparison bar chart
- Feature importance chart for tree-based models

## Extra Graphs for Bonus
- Global vs South Asia trend comparison
- Temperature anomaly trend by decade
- Country-wise warming rate comparison
- Rolling mean trend for selected cities
- Random split vs chronological split performance comparison

---

## Strong Novelty Plan
To earn bonus marks, the project should not be a basic "four models on a CSV" submission. Add at least three meaningful extras.

### Novelty 1: Temperature Anomaly Analysis
Create anomaly-based analysis in addition to raw temperature prediction.

Formula:
`TemperatureAnomaly = current city temperature - long_term city average for that month`

Why this helps:
- More climate relevant
- Shows deeper analytical thinking
- Makes the paper look more like a research study

### Novelty 2: Time-Aware Validation
Use chronological train-test splitting in final experiments.

Why this helps:
- More realistic than random split
- Reduces temporal leakage
- Stronger methodology for a climate project

### Novelty 3: South Asia Case Study
Add a focused regional analysis for South Asia, especially Pakistan if data is available.

Why this helps:
- Adds local relevance
- Makes viva discussion stronger
- Improves presentation quality

### Optional Novelty 4: Climate Risk Index
Create a simple analytical index for interpretation:

`ClimateRiskIndex = z(anomaly) + z(decadal_trend) + z(uncertainty)`

Why this helps:
- Adds originality
- Converts prediction output into practical insight
- Strengthens the "problem-solving and analytical reasoning" part of the project

---

## Comparative Analysis Requirements
The final analysis must discuss:
- Which model has the lowest RMSE
- Which model has the highest R2
- Whether tuning improves performance
- Which model generalizes better
- Which features are most important
- Trade-off between complexity and performance
- Difference between random split and chronological split
- Difference between global and South Asia findings

---

## Research Paper Writing Guidance

### Required Sections
1. Title
2. Abstract
3. Keywords
4. Introduction
5. Problem Statement
6. Objectives
7. Literature Review
8. Dataset Description
9. Methodology
10. Data Preprocessing
11. Exploratory Data Analysis
12. Machine Learning Models
13. Hyperparameter Tuning
14. Results and Discussion
15. Comparative Analysis
16. Conclusion
17. Future Work
18. References

### Important Paper Rules
- Every claim must come from actual code output
- Avoid generic statements
- Cite dataset and references properly
- Explain why regression was used
- Add one paragraph titled `Novelty of the Study`

### Recommended Novelty Statement
Use a statement like this:

"The novelty of this project lies in combining city-level temperature prediction with anomaly-based climate interpretation, time-aware validation, and a focused South Asia case study to improve both methodological realism and regional relevance."

---

## Bonus Alignment
This project clearly fits the climate change bonus category.

To maximize bonus marks:
- Show strong climate relevance
- Add anomaly-based interpretation
- Use chronological validation
- Include South Asia or Pakistan focused analysis
- Provide meaningful model comparison
- Discuss real-world implications, not only metrics

---

## Deliverables Checklist

### Code
- [ ] `01_data_cleaning.ipynb`
- [ ] `02_eda.ipynb`
- [ ] `03_modeling.ipynb`
- [ ] `04_final_evaluation.ipynb`

### Dataset
- [ ] Raw dataset downloaded
- [ ] Processed dataset saved
- [ ] Dataset source linked

### Research Paper
- [ ] All required sections written
- [ ] Actual results included
- [ ] Comparative analysis included
- [ ] Novelty section included
- [ ] References cited
- [ ] PDF exported

### Presentation
- [ ] Problem slide
- [ ] Dataset slide
- [ ] EDA visuals
- [ ] Model comparison table
- [ ] Best model slide
- [ ] Novelty slide
- [ ] Conclusion slide

---

## Minimum Acceptance Criteria
The project is complete only if:
- [ ] Real dataset is used
- [ ] Problem is clearly defined
- [ ] Missing values are handled
- [ ] Scaling or normalization is applied
- [ ] Feature engineering is performed
- [ ] EDA is included
- [ ] At least 4 models are implemented
- [ ] Hyperparameter tuning is completed
- [ ] Regression metrics are reported
- [ ] Comparative analysis is written
- [ ] Paper and slides are prepared

---

## Group Work Plan
Suggested role split:
- Member 1: data cleaning and preprocessing
- Member 2: EDA and visualization
- Member 3: modeling and tuning
- Member 4: paper, slides, and integration

### Week 1
- Download dataset
- Create folders
- Complete cleaning notebook
- Complete EDA notebook
- Finalize anomaly feature and South Asia subset

### Week 2
- Train all models
- Tune at least 2 models
- Compare random and chronological split
- Save plots and results tables

### Week 3
- Write paper using actual results
- Prepare slides
- Recheck citations, visuals, and conclusions

---

## Immediate Next Steps
1. Download the Kaggle dataset
2. Create the folder structure
3. Place the CSV in `data/raw/`
4. Start `01_data_cleaning.ipynb`
5. Build basic features first
6. Add anomaly feature and South Asia subset
7. Train baseline models
8. Tune the strongest models
9. Write paper after metrics and figures are finalized

---

## Quality Rules
- No plagiarism
- Cite all sources
- Keep code reproducible
- Explain every preprocessing and modeling choice
- Focus on analysis and interpretation, not just accuracy

---

## Final Verdict
Yes, this project plan satisfies the teacher's description.

To make it stronger and bonus-worthy, the final submission must explicitly show:
- At least 4 trained and compared models
- Hyperparameter tuning on at least 2 models
- Proper regression metrics
- A real comparative analysis
- A clear novelty component:
  - anomaly analysis
  - chronological validation
  - South Asia case study
