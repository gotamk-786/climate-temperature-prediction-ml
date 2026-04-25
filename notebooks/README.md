# Notebooks

This folder contains the main working notebooks used in the project. The notebooks follow the same order as the project workflow, so it is better to open and run them from top to bottom.

## Notebook Order

### `01_data_cleaning.ipynb`
This notebook shows the raw dataset, checks missing values and duplicates, performs cleaning, creates new features, and saves the processed files needed for the next steps.

### `02_eda.ipynb`
This notebook is for exploratory data analysis. It includes summary statistics, missing-value analysis, temperature distribution, long-term trend plots, seasonal patterns, regional comparison, and correlation analysis.

### `03_modeling.ipynb`
This notebook trains the machine learning models, compares random and chronological split results, performs tuning for selected models, and saves the best model outputs.

### `04_final_evaluation.ipynb`
This notebook is used for final result checking. It generates prediction outputs, residual analysis, actual vs predicted plots, feature importance, and split-strategy comparison.

## Suggested Use

If the processed files already exist, the notebooks can be opened directly for review. If not, run them in sequence so that each stage creates the files required by the next one.

## Note

The figures and tables generated in these notebooks are the same ones that should be used in the report and presentation.
