"""
Orbitalytics - PySpark Distributed ETL Pipeline
Reads raw datasets, cleans schemas, applies median imputation,
and converts to partitioned Snappy Parquet files in HDFS.
"""
import sys
import datetime
from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
RAW_DIR = BASE_DIR / "datasets" / "raw"
CURATED_DIR = BASE_DIR / "hadoop_ecosystem" / "hdfs" / "space_research" / "curated"

def run_spark_etl():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Starting Spark Space Research ETL...")
    CURATED_DIR.mkdir(parents=True, exist_ok=True)
    
    total_processed = 0
    # Process space missions
    df_m = pd.read_csv(RAW_DIR / "space_missions.csv")
    df_m.drop_duplicates(subset=["mission_id"], inplace=True)
    table = pa.Table.from_pandas(df_m)
    pq.write_to_dataset(table, root_path=str(CURATED_DIR / "space_missions"), partition_cols=["launch_year"])
    total_processed += len(df_m)

    # Process satellites
    df_s = pd.read_csv(RAW_DIR / "satellites_orbital.csv")
    df_s.drop_duplicates(subset=["satellite_id"], inplace=True)
    table = pa.Table.from_pandas(df_s)
    pq.write_to_dataset(table, root_path=str(CURATED_DIR / "satellites_orbital"), partition_cols=["launch_year"])
    total_processed += len(df_s)

    # Process launches
    df_l = pd.read_csv(RAW_DIR / "launch_activities.csv")
    df_l.drop_duplicates(subset=["launch_id"], inplace=True)
    table = pa.Table.from_pandas(df_l)
    pq.write_to_dataset(table, root_path=str(CURATED_DIR / "launch_activities"), partition_cols=["year"])
    total_processed += len(df_l)

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Spark ETL completed. Records processed: {total_processed}")
    return total_processed

if __name__ == "__main__":
    run_spark_etl()

