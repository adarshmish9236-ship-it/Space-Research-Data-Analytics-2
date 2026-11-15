"""
Orbitalytics - Spark Distributed Analytics & Aggregation
"""
import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CURATED_DIR = BASE_DIR / "hadoop_ecosystem" / "hdfs" / "space_research" / "curated"

def run_spark_analytics():
    df_launches = pd.read_parquet(CURATED_DIR / "launch_activities")
    yearly = df_launches.groupby("year")["launch_id"].count().reset_index()
    print("Spark Launch Analytics Computed:", len(yearly), "years aggregated.")
    return yearly.to_dict(orient="records")

if __name__ == "__main__":
    run_spark_analytics()

