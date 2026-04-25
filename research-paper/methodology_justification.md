# Methodology Justification

## Why Regression Was Used

The target variable in this project is `AverageTemperature`, which is a continuous numerical value. Because the goal is to predict actual temperature values rather than labels or categories, regression is the correct machine learning approach. A classification setup would only make sense if the temperatures were first converted into classes such as low, medium, and high, but that would reduce detail and weaken the climate interpretation of the study.

## Why Chronological Validation Was Used

Climate records are time-dependent, so random splitting can give an overly optimistic estimate of model performance. In a random split, older and newer observations may appear together in both training and testing sets. This can make prediction easier than it would be in a realistic future-forecasting situation.

For that reason, the final analysis emphasized chronological train-test splitting. The model was trained on earlier observations and tested on later observations. This makes the methodology more realistic and better aligned with the way climate data would be used in practice.

## Why Some EDA Plots Used Sampling

The cleaned dataset contains millions of rows. Full-data summary statistics, missing-value counts, yearly trend analysis, and regional trend comparisons were retained wherever correctness mattered most. For visually heavy plots such as histograms, boxplots, and correlation heatmaps, a large random sample was used. This keeps the plots readable and computationally practical while still preserving representative patterns in the data.

## Why South Asia Was Included

The South Asia case study was added to improve the regional relevance of the project. Since climate change affects regions differently, this focused analysis makes the project stronger than a purely global benchmark and supports more meaningful discussion in presentation and viva settings.
