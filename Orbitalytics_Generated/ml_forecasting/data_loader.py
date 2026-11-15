"""
ORBITALYTICS Phase 8 — Time-Series Data Loader & Feature Builder
Constructs continuous quarterly and annual time series for:
  - Target 1: Space Equipment & Component Demand (8 component types + aggregate)
  - Target 2: Space Research Resource Consumption (7 resource types + aggregate)
  - Secondary: Launch cadence and Agency R&D expenditures

Enforces strict chronological ordering and leakage-safe feature engineering.
"""

import os
import math
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "datasets" / "processed"
GOLD_DIR = PROJECT_ROOT / "datasets" / "gold"


class TimeSeriesDataLoader:
    def __init__(self):
        self.processed_dir = PROCESSED_DIR
        self.gold_dir = GOLD_DIR

    def load_equipment_demand_series(self, equipment_type: Optional[str] = None) -> pd.DataFrame:
        """
        Loads continuous monthly equipment demand and aggregates to quarterly series.
        Quarterly frequency is optimal: 67 continuous quarters (2010 Q1 - 2026 Q3).
        """
        csv_path = self.processed_dir / "equipment_component_demand_cleaned.csv"
        df = pd.read_csv(csv_path)
        df["date"] = pd.to_datetime(df["date"])

        if equipment_type and equipment_type != "All":
            df = df[df["equipment_type"] == equipment_type]

        # Aggregate monthly to quarterly
        df["year"] = df["date"].dt.year
        df["quarter"] = df["date"].dt.quarter
        df["period"] = df["year"].astype(str) + "Q" + df["quarter"].astype(str)

        # Filter for complete quarters only (all 3 calendar months present)
        # Prevents artificial cliff drops in partial trailing quarters (e.g., 2026Q4 with only October)
        month_counts = df.groupby(["year", "quarter"])["date"].apply(lambda s: s.dt.month.nunique())
        complete_q = month_counts[month_counts == 3].index

        quarterly = (
            df.groupby(["year", "quarter", "period"], as_index=False)
              .agg(
                  units_demanded=("units_demanded", "sum"),
                  total_value_m_usd=("total_demand_value_million_usd", "sum"),
                  avg_lead_time_days=("lead_time_days", "mean")
              )
              .sort_values(["year", "quarter"])
        )
        quarterly = quarterly[quarterly.set_index(["year", "quarter"]).index.isin(complete_q)].reset_index(drop=True)
        quarterly["target"] = quarterly["units_demanded"]
        return quarterly

    def load_resource_consumption_series(self, resource_name: Optional[str] = None) -> pd.DataFrame:
        """
        Loads continuous monthly resource consumption and aggregates to quarterly series.
        """
        csv_path = self.processed_dir / "resource_consumption_cleaned.csv"
        df = pd.read_csv(csv_path)
        df["date"] = pd.to_datetime(df["date"])

        if resource_name and resource_name != "All":
            df = df[df["resource_name"] == resource_name]

        df["year"] = df["date"].dt.year
        df["quarter"] = df["date"].dt.quarter
        df["period"] = df["year"].astype(str) + "Q" + df["quarter"].astype(str)

        # Filter for complete quarters only (all 3 calendar months present)
        month_counts = df.groupby(["year", "quarter"])["date"].apply(lambda s: s.dt.month.nunique())
        complete_q = month_counts[month_counts == 3].index

        quarterly = (
            df.groupby(["year", "quarter", "period"], as_index=False)
              .agg(
                  quantity_consumed=("quantity_consumed", "sum"),
                  total_cost_k_usd=("procurement_cost_k_usd", "sum")
              )
              .sort_values(["year", "quarter"])
        )
        quarterly = quarterly[quarterly.set_index(["year", "quarter"]).index.isin(complete_q)].reset_index(drop=True)
        quarterly["target"] = quarterly["quantity_consumed"]
        return quarterly

    def get_equipment_types(self) -> List[str]:
        """Returns all 8 component equipment categories."""
        csv_path = self.processed_dir / "equipment_component_demand_cleaned.csv"
        df = pd.read_csv(csv_path)
        return sorted(df["equipment_type"].unique().tolist())

    def get_resource_types(self) -> List[str]:
        """Returns all 7 resource categories."""
        csv_path = self.processed_dir / "resource_consumption_cleaned.csv"
        df = pd.read_csv(csv_path)
        return sorted(df["resource_name"].unique().tolist())

    def build_feature_matrix(self, df: pd.DataFrame, lags: int = 4) -> pd.DataFrame:
        """
        Constructs leakage-safe feature matrix from a quarterly series:
          - Lags: 1, 2, 3, 4 (prior quarters)
          - Rolling stats: rolling 4-quarter mean and std (shifted by 1 to exclude current period)
          - Seasonal cyclical encoding: sin_q, cos_q (m=4)
          - Linear trend: time_index (1, 2, ...)
          - YoY difference: lag_1 - lag_5 (or growth rate)
        """
        data = df.copy()
        data["time_index"] = np.arange(len(data)) + 1

        # Cyclic encoding of quarter (1-4)
        data["sin_q"] = np.sin(2 * np.pi * data["quarter"] / 4.0)
        data["cos_q"] = np.cos(2 * np.pi * data["quarter"] / 4.0)

        # One-hot quarter indicators for regression
        for q in [1, 2, 3, 4]:
            data[f"q_{q}"] = (data["quarter"] == q).astype(int)

        # Lags strictly from historical periods
        for l in range(1, lags + 1):
            data[f"lag_{l}"] = data["target"].shift(l)

        # Rolling statistics strictly ending at t-1
        data["rolling_mean_4"] = data["target"].shift(1).rolling(window=4).mean()
        data["rolling_std_4"] = data["target"].shift(1).rolling(window=4).std()
        data["rolling_mean_2"] = data["target"].shift(1).rolling(window=2).mean()

        # YoY seasonal lag
        data["seasonal_lag_4"] = data["target"].shift(4)

        # Growth rate from t-2 to t-1
        data["prior_growth_rate"] = np.where(
            data["lag_2"] > 0,
            (data["lag_1"] - data["lag_2"]) / data["lag_2"],
            0.0
        )

        # Drop initial NaN rows created by shift(4) to ensure clean training
        clean_data = data.dropna().reset_index(drop=True)
        return clean_data
