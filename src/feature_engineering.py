from __future__ import annotations

import numpy as np
import pandas as pd

from .preprocessing import SOUTH_ASIA_COUNTRIES


def build_south_asia_subset(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Country"].isin(SOUTH_ASIA_COUNTRIES)].copy()


def compute_warming_rate_by_country(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for country in countries:
        country_data = df[df["Country"].astype(str) == country]
        yearly = (
            country_data.groupby("Year", observed=True)["AverageTemperature"]
            .mean()
            .dropna()
            .reset_index()
        )
        if len(yearly) < 10:
            continue
        slope, intercept = np.polyfit(yearly["Year"], yearly["AverageTemperature"], 1)
        rows.append(
            {
                "Country": country,
                "WarmingRatePerYear": float(slope),
                "WarmingRatePerDecade": float(slope * 10),
                "Intercept": float(intercept),
            }
        )

    return pd.DataFrame(rows).sort_values("WarmingRatePerDecade", ascending=False)
