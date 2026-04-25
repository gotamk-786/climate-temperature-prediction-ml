from __future__ import annotations

import re
from typing import Iterable

import numpy as np
import pandas as pd


LAT_LONG_PATTERN = re.compile(r"^\s*([0-9.]+)\s*([NSEW])\s*$", re.IGNORECASE)
SOUTH_ASIA_COUNTRIES = {
    "Afghanistan",
    "Bangladesh",
    "Bhutan",
    "India",
    "Maldives",
    "Nepal",
    "Pakistan",
    "Sri Lanka",
}


def convert_coordinate(value: str) -> float:
    match = LAT_LONG_PATTERN.match(str(value))
    if not match:
        raise ValueError(f"Invalid coordinate value: {value}")

    magnitude = float(match.group(1))
    direction = match.group(2).upper()
    if direction in {"S", "W"}:
        return -magnitude
    return magnitude


def season_from_month(month: int) -> str:
    if month in {12, 1, 2}:
        return "Winter"
    if month in {3, 4, 5}:
        return "Spring"
    if month in {6, 7, 8}:
        return "Summer"
    return "Autumn"


def _z_score(series: pd.Series) -> pd.Series:
    std = series.std(ddof=0)
    if pd.isna(std) or std == 0:
        return pd.Series(np.zeros(len(series)), index=series.index, dtype="float32")
    return ((series - series.mean()) / std).astype("float32")


def clean_temperature_data(df: pd.DataFrame, min_year: int = 1900) -> pd.DataFrame:
    data = df.copy()
    data["dt"] = pd.to_datetime(data["dt"], errors="coerce")
    data["AverageTemperature"] = pd.to_numeric(data["AverageTemperature"], errors="coerce")
    data["AverageTemperatureUncertainty"] = pd.to_numeric(
        data["AverageTemperatureUncertainty"],
        errors="coerce",
    )

    data = data.dropna(subset=["dt", "AverageTemperature"]).drop_duplicates()
    data = data[data["dt"].dt.year >= min_year].copy()

    data["LatitudeValue"] = data["Latitude"].apply(convert_coordinate).astype("float32")
    data["LongitudeValue"] = data["Longitude"].apply(convert_coordinate).astype("float32")
    data["Year"] = data["dt"].dt.year.astype("int16")
    data["Month"] = data["dt"].dt.month.astype("int8")
    data["Quarter"] = data["dt"].dt.quarter.astype("int8")
    data["Season"] = data["Month"].apply(season_from_month)
    data["Hemisphere"] = np.where(data["LatitudeValue"] >= 0, "Northern", "Southern")
    data["Decade"] = ((data["Year"] // 10) * 10).astype("int16")
    data["YearsSince1900"] = (data["Year"] - min_year).astype("int16")
    data["RegionTag"] = np.where(
        data["Country"].isin(SOUTH_ASIA_COUNTRIES),
        "South Asia",
        "Global",
    )

    data = data.sort_values(["City", "dt"]).reset_index(drop=True)
    data["Lag1Temperature"] = (
        data.groupby("City", sort=False)["AverageTemperature"].shift(1).astype("float32")
    )
    data["Lag12Temperature"] = (
        data.groupby("City", sort=False)["AverageTemperature"].shift(12).astype("float32")
    )
    data["Rolling12MeanTemperature"] = (
        data.groupby("City", sort=False)["AverageTemperature"]
        .transform(lambda values: values.shift(1).rolling(window=12, min_periods=6).mean())
        .astype("float32")
    )

    month_groups = data.groupby(["City", "Month"], sort=False)["AverageTemperature"]
    cumulative_sum = month_groups.cumsum() - data["AverageTemperature"]
    observation_index = month_groups.cumcount()
    historical_mean = cumulative_sum / observation_index.replace(0, np.nan)
    data["HistoricalCityMonthMean"] = historical_mean.astype("float32")
    data["TemperatureAnomaly"] = (
        data["AverageTemperature"] - data["HistoricalCityMonthMean"]
    ).astype("float32")

    city_year_mean = data.groupby(["City", "Year"], sort=False)["AverageTemperature"].transform("mean")
    data["CityYearMeanTemperature"] = city_year_mean.astype("float32")
    decade_mean = data.groupby("Decade", sort=False)["AverageTemperature"].transform("mean")
    data["DecadeMeanTemperature"] = decade_mean.astype("float32")

    anomaly_z = _z_score(data["TemperatureAnomaly"].fillna(0))
    uncertainty_z = _z_score(data["AverageTemperatureUncertainty"].fillna(data["AverageTemperatureUncertainty"].median()))
    decade_z = _z_score(data["DecadeMeanTemperature"])
    data["ClimateRiskIndex"] = (anomaly_z + uncertainty_z + decade_z).astype("float32")

    category_columns = ["City", "Country", "Season", "Hemisphere", "RegionTag", "Latitude", "Longitude"]
    for column in category_columns:
        data[column] = data[column].astype("category")

    float_columns = [
        "AverageTemperature",
        "AverageTemperatureUncertainty",
        "LatitudeValue",
        "LongitudeValue",
        "Lag1Temperature",
        "Lag12Temperature",
        "Rolling12MeanTemperature",
        "HistoricalCityMonthMean",
        "TemperatureAnomaly",
        "CityYearMeanTemperature",
        "DecadeMeanTemperature",
        "ClimateRiskIndex",
    ]
    for column in float_columns:
        data[column] = data[column].astype("float32")

    return data


def build_modeling_dataset(
    df: pd.DataFrame,
    sample_size: int = 75_000,
    random_state: int = 42,
) -> pd.DataFrame:
    required_columns: Iterable[str] = (
        "AverageTemperature",
        "AverageTemperatureUncertainty",
        "Lag1Temperature",
        "Lag12Temperature",
        "Rolling12MeanTemperature",
        "HistoricalCityMonthMean",
    )
    eligible = df.dropna(subset=list(required_columns)).copy()
    eligible["SamplingGroup"] = (
        eligible["Decade"].astype(str) + "_" + eligible["RegionTag"].astype(str)
    )

    if len(eligible) <= sample_size:
        return eligible.drop(columns=["SamplingGroup"]).sort_values("dt").reset_index(drop=True)

    sampled_parts: list[pd.DataFrame] = []
    total_rows = len(eligible)
    for _, group in eligible.groupby("SamplingGroup", observed=True, sort=False):
        group_share = len(group) / total_rows
        group_target = max(250, int(round(group_share * sample_size)))
        sampled_parts.append(
            group.sample(
                n=min(len(group), group_target),
                random_state=random_state,
            )
        )

    sampled = pd.concat(sampled_parts, ignore_index=True)
    if len(sampled) > sample_size:
        sampled = sampled.sample(n=sample_size, random_state=random_state)

    return sampled.drop(columns=["SamplingGroup"]).sort_values("dt").reset_index(drop=True)
