from __future__ import annotations

from dataclasses import dataclass
import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

try:
    from xgboost import XGBRegressor
except ImportError:  # pragma: no cover - optional dependency
    XGBRegressor = None


NUMERIC_FEATURES = [
    "Year",
    "Month",
    "Quarter",
    "YearsSince1900",
    "LatitudeValue",
    "LongitudeValue",
    "AverageTemperatureUncertainty",
    "HistoricalCityMonthMean",
    "Lag1Temperature",
    "Lag12Temperature",
    "Rolling12MeanTemperature",
]
CATEGORICAL_FEATURES = ["Country", "Season", "Hemisphere", "RegionTag"]
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = "AverageTemperature"


@dataclass
class ExperimentResult:
    split_strategy: str
    model: str
    tuned: str
    mae: float
    mse: float
    rmse: float
    mape: float
    r2: float


BASELINE_TO_TUNED = {
    "Random Forest": "Random Forest Tuned",
    "Gradient Boosting": "Gradient Boosting Tuned",
}


def build_feature_pipeline() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def prepare_model_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=NUMERIC_FEATURES + [TARGET_COLUMN]).copy()


def split_random(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
    return train_df.copy(), test_df.copy()


def split_chronological(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ordered = df.sort_values("dt").reset_index(drop=True)
    split_index = int(len(ordered) * 0.8)
    train_df = ordered.iloc[:split_index].copy()
    test_df = ordered.iloc[split_index:].copy()
    return train_df, test_df


def _model_catalog() -> dict[str, object]:
    models: dict[str, object] = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=14, min_samples_leaf=8, random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=120,
            max_depth=16,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=3,
            random_state=42,
        ),
    }
    if XGBRegressor is not None:
        models["XGBoost"] = XGBRegressor(
            objective="reg:squarederror",
            n_estimators=120,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            tree_method="hist",
            n_jobs=-1,
            random_state=42,
        )
    return models


def evaluate_predictions(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    denominator = np.maximum(np.abs(np.asarray(y_true, dtype="float64")), 1e-3)
    mape = np.mean(np.abs((np.asarray(y_pred, dtype="float64") - np.asarray(y_true, dtype="float64")) / denominator)) * 100
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": float(mse),
        "rmse": float(np.sqrt(mse)),
        "mape": float(mape),
        "r2": float(r2_score(y_true, y_pred)),
    }


def fit_model(train_df: pd.DataFrame, estimator: object) -> Pipeline:
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_feature_pipeline()),
            ("model", estimator),
        ]
    )
    pipeline.fit(train_df[FEATURE_COLUMNS], train_df[TARGET_COLUMN])
    return pipeline


def run_model_suite(df: pd.DataFrame, split_strategy: str) -> tuple[pd.DataFrame, dict[str, Pipeline]]:
    prepared = prepare_model_frame(df)
    if split_strategy == "chronological":
        train_df, test_df = split_chronological(prepared)
    else:
        train_df, test_df = split_random(prepared)

    results: list[ExperimentResult] = []
    fitted_models: dict[str, Pipeline] = {}
    for model_name, estimator in _model_catalog().items():
        pipeline = fit_model(train_df, estimator)
        predictions = pipeline.predict(test_df[FEATURE_COLUMNS])
        metrics = evaluate_predictions(test_df[TARGET_COLUMN], predictions)
        fitted_models[model_name] = pipeline
        results.append(
            ExperimentResult(
                split_strategy=split_strategy,
                model=model_name,
                tuned="No",
                **metrics,
            )
        )

    results_df = pd.DataFrame([result.__dict__ for result in results]).sort_values(
        ["split_strategy", "rmse", "r2"],
        ascending=[True, True, False],
    )
    return results_df, fitted_models


def tune_models(
    train_df: pd.DataFrame,
    sample_size: int = 18_000,
) -> tuple[dict[str, Pipeline], pd.DataFrame]:
    tune_source = train_df.copy()
    if len(tune_source) > sample_size:
        tune_source = tune_source.sample(n=sample_size, random_state=42)

    search_spaces: dict[str, tuple[object, dict[str, list[object]]]] = {
        "Random Forest Tuned": (
            RandomForestRegressor(random_state=42, n_jobs=-1),
            {
                "model__n_estimators": [150, 220, 300],
                "model__max_depth": [12, 16, None],
                "model__min_samples_leaf": [2, 4, 8],
                "model__max_features": ["sqrt", 0.8, None],
            },
        ),
        "Gradient Boosting Tuned": (
            GradientBoostingRegressor(random_state=42),
            {
                "model__n_estimators": [120, 180, 240],
                "model__learning_rate": [0.03, 0.05, 0.08],
                "model__max_depth": [2, 3, 4],
                "model__subsample": [0.8, 1.0],
            },
        ),
    }

    tuned_models: dict[str, Pipeline] = {}
    tuning_rows: list[dict[str, object]] = []
    for model_name, (estimator, params) in search_spaces.items():
        search = RandomizedSearchCV(
            estimator=Pipeline(
                steps=[
                    ("preprocessor", build_feature_pipeline()),
                    ("model", estimator),
                ]
            ),
            param_distributions=params,
            n_iter=4,
            scoring="neg_root_mean_squared_error",
            cv=3,
            random_state=42,
            n_jobs=-1,
            verbose=0,
        )
        search.fit(tune_source[FEATURE_COLUMNS], tune_source[TARGET_COLUMN])
        tuned_models[model_name] = search.best_estimator_
        tuning_rows.append(
            {
                "Model": model_name,
                "Search Method": "RandomizedSearchCV",
                "CV Folds": 3,
                "Iterations": 4,
                "Best CV RMSE": round(float(-search.best_score_), 4),
                "Best Parameters": json.dumps(search.best_params_, sort_keys=True),
            }
        )

    tuning_details = pd.DataFrame(tuning_rows).sort_values("Best CV RMSE").reset_index(drop=True)
    return tuned_models, tuning_details


def evaluate_tuned_models(
    df: pd.DataFrame,
    split_strategy: str,
) -> tuple[pd.DataFrame, dict[str, Pipeline], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    prepared = prepare_model_frame(df)
    if split_strategy == "chronological":
        train_df, test_df = split_chronological(prepared)
    else:
        train_df, test_df = split_random(prepared)

    tuned_models, tuning_details = tune_models(train_df)
    results: list[ExperimentResult] = []
    for model_name, pipeline in tuned_models.items():
        predictions = pipeline.predict(test_df[FEATURE_COLUMNS])
        metrics = evaluate_predictions(test_df[TARGET_COLUMN], predictions)
        results.append(
            ExperimentResult(
                split_strategy=split_strategy,
                model=model_name,
                tuned="Yes",
                **metrics,
            )
        )

    results_df = pd.DataFrame([result.__dict__ for result in results]).sort_values("rmse")
    return results_df, tuned_models, train_df, test_df, tuning_details


def build_cross_validation_summary(
    df: pd.DataFrame,
    sample_size: int = 18_000,
    folds: int = 5,
) -> pd.DataFrame:
    prepared = prepare_model_frame(df)
    cv_source = prepared.copy()
    if len(cv_source) > sample_size:
        cv_source = cv_source.sample(n=sample_size, random_state=42)

    cv = KFold(n_splits=folds, shuffle=True, random_state=42)
    rows: list[dict[str, object]] = []
    scoring = {
        "mae": "neg_mean_absolute_error",
        "rmse": "neg_root_mean_squared_error",
        "r2": "r2",
    }

    for model_name, estimator in _model_catalog().items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_feature_pipeline()),
                ("model", estimator),
            ]
        )
        scores = cross_validate(
            pipeline,
            cv_source[FEATURE_COLUMNS],
            cv_source[TARGET_COLUMN],
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )
        rows.append(
            {
                "Model": model_name,
                "CV Folds": folds,
                "Rows Used": len(cv_source),
                "CV Mean MAE": round(float(-scores["test_mae"].mean()), 4),
                "CV Std MAE": round(float(scores["test_mae"].std()), 4),
                "CV Mean RMSE": round(float(-scores["test_rmse"].mean()), 4),
                "CV Std RMSE": round(float(scores["test_rmse"].std()), 4),
                "CV Mean R2": round(float(scores["test_r2"].mean()), 4),
                "CV Std R2": round(float(scores["test_r2"].std()), 4),
            }
        )

    return pd.DataFrame(rows).sort_values("CV Mean RMSE").reset_index(drop=True)


def build_tuning_comparison(
    baseline_results: pd.DataFrame,
    tuned_results: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    baseline_lookup = baseline_results.set_index("model")
    tuned_lookup = tuned_results.set_index("model")

    for baseline_model, tuned_model in BASELINE_TO_TUNED.items():
        if baseline_model not in baseline_lookup.index or tuned_model not in tuned_lookup.index:
            continue

        baseline_rmse = float(baseline_lookup.loc[baseline_model, "rmse"])
        tuned_rmse = float(tuned_lookup.loc[tuned_model, "rmse"])
        baseline_r2 = float(baseline_lookup.loc[baseline_model, "r2"])
        tuned_r2 = float(tuned_lookup.loc[tuned_model, "r2"])

        rows.append(
            {
                "Baseline Model": baseline_model,
                "Tuned Model": tuned_model,
                "Baseline RMSE": round(baseline_rmse, 4),
                "Tuned RMSE": round(tuned_rmse, 4),
                "RMSE Change": round(tuned_rmse - baseline_rmse, 4),
                "Baseline R2": round(baseline_r2, 4),
                "Tuned R2": round(tuned_r2, 4),
                "R2 Change": round(tuned_r2 - baseline_r2, 4),
            }
        )

    return pd.DataFrame(rows)


def extract_feature_importance(pipeline: Pipeline, top_n: int = 15) -> pd.DataFrame:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()

    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    elif hasattr(model, "coef_"):
        values = np.abs(np.ravel(model.coef_))
    else:
        return pd.DataFrame(columns=["Feature", "Importance"])

    importance_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": np.asarray(values, dtype="float64"),
        }
    )
    return importance_df.sort_values("Importance", ascending=False).head(top_n).reset_index(drop=True)


def prediction_frame(
    pipeline: Pipeline,
    test_df: pd.DataFrame,
    split_strategy: str,
    model_name: str,
) -> pd.DataFrame:
    predictions = pipeline.predict(test_df[FEATURE_COLUMNS])
    output = test_df[["dt", "City", "Country", TARGET_COLUMN]].copy()
    output["PredictedTemperature"] = predictions
    output["Residual"] = output[TARGET_COLUMN] - output["PredictedTemperature"]
    output["SplitStrategy"] = split_strategy
    output["Model"] = model_name
    return output.reset_index(drop=True)


def build_error_by_decade(predictions_df: pd.DataFrame) -> pd.DataFrame:
    analysis = predictions_df.copy()
    analysis["Decade"] = ((analysis["dt"].dt.year // 10) * 10).astype(int)
    analysis["AbsoluteError"] = analysis["Residual"].abs()
    analysis["SquaredError"] = analysis["Residual"] ** 2

    grouped = (
        analysis.groupby("Decade", as_index=False)
        .agg(
            Rows=("Residual", "size"),
            MeanAbsoluteError=("AbsoluteError", "mean"),
            RootMeanSquaredError=("SquaredError", lambda values: float(np.sqrt(np.mean(values)))),
            MeanResidual=("Residual", "mean"),
        )
        .sort_values("Decade")
    )
    grouped["MeanAbsoluteError"] = grouped["MeanAbsoluteError"].round(4)
    grouped["RootMeanSquaredError"] = grouped["RootMeanSquaredError"].round(4)
    grouped["MeanResidual"] = grouped["MeanResidual"].round(4)
    return grouped.reset_index(drop=True)
