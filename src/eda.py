from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .feature_engineering import compute_warming_rate_by_country


sns.set_theme(style="whitegrid")


def _save_figure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()


def generate_eda_outputs(
    raw_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    south_asia_df: pd.DataFrame,
    figures_dir: Path,
    tables_dir: Path,
) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    missing_values = raw_df.isna().sum().sort_values(ascending=False).reset_index()
    missing_values.columns = ["Column", "MissingValues"]
    missing_values.to_csv(tables_dir / "missing_values_summary.csv", index=False)

    summary_stats = cleaned_df[["AverageTemperature", "AverageTemperatureUncertainty", "TemperatureAnomaly"]].describe()
    summary_stats.to_csv(tables_dir / "summary_statistics.csv")

    plt.figure(figsize=(8, 4))
    sns.barplot(data=missing_values, x="Column", y="MissingValues", hue="Column", palette="crest", legend=False)
    plt.xticks(rotation=25, ha="right")
    plt.title("Missing Values in Raw Dataset")
    _save_figure(figures_dir / "missing_values_chart.png")

    distribution_sample = cleaned_df.sample(n=min(80_000, len(cleaned_df)), random_state=42)
    plt.figure(figsize=(8, 4))
    sns.histplot(distribution_sample["AverageTemperature"], bins=45, kde=True, color="#16697A")
    plt.title("Distribution of Average Temperature")
    _save_figure(figures_dir / "temperature_distribution.png")

    yearly_global = cleaned_df.groupby("Year", observed=True)["AverageTemperature"].mean().reset_index()
    plt.figure(figsize=(10, 4))
    sns.lineplot(data=yearly_global, x="Year", y="AverageTemperature", color="#C44536", linewidth=2)
    plt.title("Global Temperature Trend Over Time")
    _save_figure(figures_dir / "global_temperature_trend.png")

    plt.figure(figsize=(8, 4))
    seasonal_sample = cleaned_df.sample(n=min(60_000, len(cleaned_df)), random_state=42)
    sns.boxplot(data=seasonal_sample, x="Season", y="AverageTemperature", hue="Season", palette="Set2", legend=False)
    plt.title("Seasonal Variation in Temperature")
    _save_figure(figures_dir / "seasonal_boxplot.png")

    numeric_columns = [
        "AverageTemperature",
        "AverageTemperatureUncertainty",
        "Year",
        "Month",
        "LatitudeValue",
        "LongitudeValue",
        "Lag1Temperature",
        "Lag12Temperature",
        "Rolling12MeanTemperature",
        "HistoricalCityMonthMean",
        "TemperatureAnomaly",
        "ClimateRiskIndex",
    ]
    correlation_sample = cleaned_df[numeric_columns].sample(
        n=min(40_000, len(cleaned_df)),
        random_state=42,
    )
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_sample.corr(numeric_only=True), cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap")
    _save_figure(figures_dir / "correlation_heatmap.png")

    country_order = (
        cleaned_df.groupby("Country", observed=True)["AverageTemperature"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    top_countries = cleaned_df[cleaned_df["Country"].isin(country_order)].copy()
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=top_countries, x="Country", y="AverageTemperature", hue="Country", palette="rocket", legend=False)
    plt.xticks(rotation=35, ha="right")
    plt.title("Temperature Comparison Across Selected Countries")
    _save_figure(figures_dir / "country_comparison.png")

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=distribution_sample, x="RegionTag", y="AverageTemperature", hue="RegionTag", palette="viridis", legend=False)
    plt.title("Outlier Inspection by Region")
    _save_figure(figures_dir / "outlier_boxplot.png")

    global_region = cleaned_df.groupby("Year", observed=True)["AverageTemperature"].mean().reset_index()
    south_asia_region = south_asia_df.groupby("Year", observed=True)["AverageTemperature"].mean().reset_index()
    global_region["Region"] = "Global"
    south_asia_region["Region"] = "South Asia"
    combined = pd.concat([global_region, south_asia_region], ignore_index=True)
    plt.figure(figsize=(10, 4))
    sns.lineplot(data=combined, x="Year", y="AverageTemperature", hue="Region", linewidth=2)
    plt.title("Global vs South Asia Temperature Trend")
    _save_figure(figures_dir / "global_vs_south_asia_trend.png")

    pakistan_df = cleaned_df[cleaned_df["Country"].astype(str) == "Pakistan"].copy()
    if not pakistan_df.empty:
        pakistan_yearly = pakistan_df.groupby("Year", observed=True)["AverageTemperature"].mean().reset_index()
        pakistan_yearly["Region"] = "Pakistan"
        pakistan_vs_global = pd.concat([global_region, pakistan_yearly], ignore_index=True)
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=pakistan_vs_global, x="Year", y="AverageTemperature", hue="Region", linewidth=2)
        plt.title("Pakistan vs Global Temperature Trend")
        _save_figure(figures_dir / "pakistan_vs_global_trend.png")

        pakistan_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Multan"]
        pakistan_city_data = pakistan_df[pakistan_df["City"].isin(pakistan_cities)].copy()
        if not pakistan_city_data.empty:
            pakistan_city_trends = (
                pakistan_city_data.groupby(["City", "Year"], observed=True)["AverageTemperature"]
                .mean()
                .reset_index()
            )
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=pakistan_city_trends, x="Year", y="AverageTemperature", hue="City", linewidth=2)
            plt.title("Pakistan City Temperature Trends")
            _save_figure(figures_dir / "pakistan_city_trends.png")

    anomaly_by_decade = (
        cleaned_df.groupby(["Decade", "RegionTag"], observed=True)["TemperatureAnomaly"]
        .mean()
        .reset_index()
    )
    anomaly_by_decade.to_csv(tables_dir / "anomaly_by_decade.csv", index=False)
    plt.figure(figsize=(10, 4))
    sns.lineplot(data=anomaly_by_decade, x="Decade", y="TemperatureAnomaly", hue="RegionTag", marker="o")
    plt.title("Temperature Anomaly Trend by Decade")
    _save_figure(figures_dir / "anomaly_trend_by_decade.png")

    warming_rates = compute_warming_rate_by_country(
        cleaned_df,
        ["Pakistan", "India", "Bangladesh", "Nepal", "Sri Lanka", "Afghanistan"],
    )
    warming_rates.to_csv(tables_dir / "south_asia_warming_rates.csv", index=False)
    if not warming_rates.empty:
        plt.figure(figsize=(8, 4))
        sns.barplot(data=warming_rates, x="Country", y="WarmingRatePerDecade", hue="Country", palette="magma", legend=False)
        plt.title("South Asia Warming Rate Per Decade")
        _save_figure(figures_dir / "country_warming_rate_comparison.png")

    city_candidates = ["Karachi", "Lahore", "Delhi", "Dhaka"]
    selected_cities = cleaned_df[cleaned_df["City"].isin(city_candidates)].copy()
    if not selected_cities.empty:
        city_trends = (
            selected_cities.groupby(["City", "Year"], observed=True)["AverageTemperature"]
            .mean()
            .reset_index()
        )
        city_trends["Rolling5YearMean"] = (
            city_trends.groupby("City", observed=True)["AverageTemperature"]
            .transform(lambda values: values.rolling(window=5, min_periods=1).mean())
        )
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=city_trends, x="Year", y="Rolling5YearMean", hue="City", linewidth=2)
        plt.title("Rolling Mean Temperature Trend for Selected Cities")
        _save_figure(figures_dir / "rolling_mean_selected_cities.png")
