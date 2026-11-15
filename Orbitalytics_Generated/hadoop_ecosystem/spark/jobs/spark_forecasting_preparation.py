"""
Orbitalytics - Spark Feature Engineering & Forecasting Preparation Job
Builds lag, rolling statistics, calendar seasonality, and trend features.
"""
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CURATED_DIR = BASE_DIR / "hadoop_ecosystem" / "hdfs" / "space_research" / "curated"

def prepare_features():
    df_demand = pd.read_parquet(CURATED_DIR / "equipment_component_demand")
    monthly = df_demand.groupby("date")["units_demanded"].sum().reset_index()
    monthly["date"] = pd.to_datetime(monthly["date"])
    monthly = monthly.sort_values("date").reset_index(drop=True)
    
    # Chronological features
    monthly["month"] = monthly["date"].dt.month
    monthly["quarter"] = monthly["date"].dt.quarter
    monthly["sin_month"] = np.sin(2 * np.pi * monthly["month"] / 12.0)
    monthly["cos_month"] = np.cos(2 * np.pi * monthly["month"] / 12.0)
    monthly["lag_1"] = monthly["units_demanded"].shift(1)
    monthly["lag_2"] = monthly["units_demanded"].shift(2)
    monthly["rolling_3"] = monthly["units_demanded"].shift(1).rolling(3).mean()
    monthly.bfill(inplace=True)
    print("Spark Forecasting Preparation complete. Feature rows:", len(monthly))
    return monthly

if __name__ == "__main__":
    prepare_features()

