#!/usr/bin/env python3
"""
ORBITALYTICS Phase 7 — Task 4: Feature Engineering Pipeline
Generates time-series lag features, rolling statistics, and ML-ready features
for equipment demand forecasting. All features use only historically-available
information at the prediction timestamp — no future leakage.

Feature schema (per year-agency-component observation):
  - Temporal: year, years_since_start, is_recent_period
  - Target:   annual_units_demanded
  - Lag features: lag_1_units, lag_2_units, lag_3_units, lag_4_units, lag_1_value
  - Rolling stats: rolling_3yr_mean, rolling_3yr_std
  - Growth: yoy_growth_pct, growth_3yr_pct
  - Fulfillment: fulfillment_rate_pct
  - Activity counts: prev_yr_mission_count, prev_yr_launch_count, prev_yr_satellite_deploy_count
"""

import sys
import time
import json
from datetime import datetime

sys.path.insert(0, "/opt/spark_analytics")
from spark_session import get_spark_session, stop_spark, SILVER_BASE, GOLD_BASE

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType, DoubleType, StringType


FEATURE_GOLD_PATH = f"{GOLD_BASE}/forecast_features/equipment_demand_features"
TRAIN_GOLD_PATH   = f"{GOLD_BASE}/forecast_features/train_dataset"
TEST_GOLD_PATH    = f"{GOLD_BASE}/forecast_features/test_dataset"

TRAIN_CUTOFF_YEAR = 2023  # 2010-2023 = training, 2024-2026 = test


def build_annual_demand_base(spark):
    """Step 1: Build annual component-agency demand aggregation."""
    ed = spark.read.parquet(f"{SILVER_BASE}/equipment_demand")
    ed = ed.withColumn("year", F.col("year").cast(IntegerType())) \
           .withColumn("units_demanded", F.col("units_demanded").cast(DoubleType())) \
           .withColumn("units_manufactured", F.col("units_manufactured").cast(DoubleType())) \
           .withColumn("units_procured", F.col("units_procured").cast(DoubleType())) \
           .withColumn("lead_time_days", F.col("lead_time_days").cast(IntegerType())) \
           .withColumn("total_demand_value_m_usd", F.col("total_demand_value_million_usd").cast(DoubleType()))

    base = (
        ed.groupBy("year", "agency_id", "component_id", "component_category")
          .agg(
              F.round(F.sum("units_demanded"), 1).alias("annual_units_demanded"),
              F.round(F.sum("total_demand_value_m_usd"), 2).alias("annual_demand_value_m_usd"),
              F.round(F.avg("lead_time_days"), 1).alias("avg_lead_time_days"),
              F.round(F.sum("units_manufactured"), 1).alias("annual_units_manufactured"),
              F.round(F.sum("units_procured"), 1).alias("annual_units_procured")
          )
    )
    print(f"  Base demand observations: {base.count():,}")
    return base


def add_lag_features(base):
    """Step 2: Add lag features (1-4 years) using Window partitioned by agency+component."""
    entity_window = Window.partitionBy("agency_id", "component_id").orderBy("year")

    with_lags = (
        base
        .withColumn("lag_1_units", F.lag("annual_units_demanded", 1).over(entity_window))
        .withColumn("lag_2_units", F.lag("annual_units_demanded", 2).over(entity_window))
        .withColumn("lag_3_units", F.lag("annual_units_demanded", 3).over(entity_window))
        .withColumn("lag_4_units", F.lag("annual_units_demanded", 4).over(entity_window))
        .withColumn("lag_1_value", F.lag("annual_demand_value_m_usd", 1).over(entity_window))
    )
    return with_lags


def add_rolling_stats(df):
    """Step 3: Add rolling window statistics (3-year mean and std)."""
    entity_window = Window.partitionBy("agency_id", "component_id").orderBy("year")
    rolling_window = entity_window.rowsBetween(-3, -1)

    with_rolling = (
        df
        .withColumn("rolling_3yr_mean",
            F.round(F.avg("annual_units_demanded").over(rolling_window), 2))
        .withColumn("rolling_3yr_std",
            F.round(F.stddev("annual_units_demanded").over(rolling_window), 2))
    )
    return with_rolling


def add_growth_features(df):
    """Step 4: Add YoY growth rate and 3-year compounded growth rate."""
    with_growth = (
        df
        .withColumn("yoy_growth_pct",
            F.when(F.col("lag_1_units").isNotNull() & (F.col("lag_1_units") > 0),
                F.round((F.col("annual_units_demanded") - F.col("lag_1_units"))
                        / F.col("lag_1_units") * 100.0, 3))
            .otherwise(F.lit(None)))
        .withColumn("growth_3yr_pct",
            F.when(F.col("lag_3_units").isNotNull() & (F.col("lag_3_units") > 0),
                F.round((F.col("annual_units_demanded") - F.col("lag_3_units"))
                        / F.col("lag_3_units") * 100.0, 3))
            .otherwise(F.lit(None)))
        .withColumn("fulfillment_rate_pct",
            F.when(F.col("annual_units_demanded") > 0,
                F.round((F.col("annual_units_manufactured") + F.col("annual_units_procured"))
                        / F.col("annual_units_demanded") * 100.0, 2))
            .otherwise(F.lit(100.0)))
    )
    return with_growth


def add_activity_context_features(df, spark):
    """
    Step 5: Join annual mission count, launch count, satellite deployment count
    from prior year as contextual features (no future leakage).
    """
    # Annual mission count per agency
    missions = spark.read.parquet(f"{SILVER_BASE}/missions") \
                    .withColumn("year", F.col("year").cast(IntegerType()))
    mission_counts = (
        missions.groupBy("agency_id", "year")
                .agg(F.count("mission_id").alias("mission_count"))
                .withColumnRenamed("year", "context_year")
                .withColumnRenamed("agency_id", "m_agency_id")
    )

    # Annual launch count (global industry volume)
    launches = spark.read.parquet(f"{SILVER_BASE}/launches") \
                    .withColumn("year", F.col("year").cast(IntegerType()))
    launch_counts = (
        launches.groupBy("year")
                .agg(F.count("launch_id").alias("launch_count"))
                .withColumnRenamed("year", "context_year")
    )

    # Annual satellite deployment count (global)
    satellites = spark.read.parquet(f"{SILVER_BASE}/satellites") \
                      .withColumn("launch_year", F.col("launch_year").cast(IntegerType()))
    sat_counts = (
        satellites.groupBy("launch_year")
                  .agg(F.count("satellite_id").alias("satellite_deploy_count"))
                  .withColumnRenamed("launch_year", "context_year")
    )

    # Join: activity counts from (year - 1) = prior year context
    df_with_context = (
        df
        .join(F.broadcast(mission_counts),
              (df["agency_id"] == mission_counts["m_agency_id"]) &
              (df["year"] == mission_counts["context_year"] + 1),
              how="left")
        .drop("m_agency_id", "context_year")
        .join(F.broadcast(launch_counts),
              df["year"] == launch_counts["context_year"] + 1,
              how="left")
        .drop("context_year")
        .join(F.broadcast(sat_counts),
              df["year"] == sat_counts["context_year"] + 1,
              how="left")
        .drop("context_year")
        .withColumnRenamed("mission_count", "prev_yr_mission_count")
        .withColumnRenamed("launch_count", "prev_yr_launch_count")
        .withColumnRenamed("satellite_deploy_count", "prev_yr_satellite_deploy_count")
    )
    return df_with_context


def add_temporal_features(df):
    """Step 6: Add derived temporal features for ML models."""
    return (
        df
        .withColumn("years_since_start", F.col("year") - 2010)
        .withColumn("is_recent_period", F.when(F.col("year") >= 2020, 1).otherwise(0))
    )


def perform_train_test_split(df, cutoff_year):
    """
    Step 7: Time-aware train/test split.
    Training: 2010 to cutoff_year (inclusive).
    Test: cutoff_year + 1 to max year.
    """
    df_valid = df.filter(F.col("lag_1_units").isNotNull())
    train = df_valid.filter(F.col("year") <= cutoff_year)
    test  = df_valid.filter(F.col("year") >  cutoff_year)
    return train, test


if __name__ == "__main__":
    spark = get_spark_session(app_name="ORBITALYTICS-P7-FeatureEngineering")
    try:
        print("\n" + "="*80)
        print("PHASE 7 — TASK 4: TIME-SERIES FEATURE ENGINEERING PIPELINE")
        print("="*80)

        # Step 1: Base demand aggregation
        print("\n[STEP 1] Building annual demand base...")
        base = build_annual_demand_base(spark)

        # Steps 2-6: Feature additions
        print("[STEP 2] Adding lag features (lag 1-4)...")
        t0 = time.time()
        df = add_lag_features(base)
        print(f"  Done in {round(time.time()-t0, 2)}s")

        print("[STEP 3] Adding rolling statistics (3yr window)...")
        t0 = time.time()
        df = add_rolling_stats(df)
        print(f"  Done in {round(time.time()-t0, 2)}s")

        print("[STEP 4] Adding growth rate features...")
        t0 = time.time()
        df = add_growth_features(df)
        print(f"  Done in {round(time.time()-t0, 2)}s")

        print("[STEP 5] Adding prior-year activity context features...")
        t0 = time.time()
        df = add_activity_context_features(df, spark)
        print(f"  Done in {round(time.time()-t0, 2)}s")

        print("[STEP 6] Adding temporal features...")
        df = add_temporal_features(df)

        # Repartition for efficient writes
        df = df.repartition(8, "year")

        # Cache before split to avoid recomputation
        print("\n[CACHE] Caching feature DataFrame before train/test split...")
        t0 = time.time()
        df.cache()
        total_rows = df.count()
        print(f"  Cached: {total_rows:,} rows in {round(time.time()-t0, 2)}s")

        # Sample feature output
        print("\n[SAMPLE] Feature DataFrame schema and sample:")
        df.printSchema()
        df.select("year", "agency_id", "component_id",
                  "annual_units_demanded", "lag_1_units", "lag_2_units",
                  "rolling_3yr_mean", "rolling_3yr_std",
                  "yoy_growth_pct", "fulfillment_rate_pct",
                  "prev_yr_mission_count", "prev_yr_launch_count"
                  ).show(5, truncate=True)

        # Step 7: Train/test split
        print(f"\n[STEP 7] Time-aware split: train <= {TRAIN_CUTOFF_YEAR}, test > {TRAIN_CUTOFF_YEAR}")
        train, test = perform_train_test_split(df, TRAIN_CUTOFF_YEAR)
        train_count = train.count()
        test_count  = test.count()
        print(f"  Training observations: {train_count:,}")
        print(f"  Test observations:     {test_count:,}")
        print(f"  Train ratio: {round(train_count / (train_count + test_count) * 100, 1)}%")

        # Task 7: Write Gold layer
        print("\n[GOLD] Writing feature datasets to HDFS Gold layer...")
        t0 = time.time()
        df.write.mode("overwrite").partitionBy("year") \
          .option("compression", "snappy").parquet(FEATURE_GOLD_PATH)
        print(f"  Full features: {FEATURE_GOLD_PATH}  ({round(time.time()-t0, 2)}s)")

        t0 = time.time()
        train.write.mode("overwrite").partitionBy("year") \
             .option("compression", "snappy").parquet(TRAIN_GOLD_PATH)
        print(f"  Train set:     {TRAIN_GOLD_PATH}  ({round(time.time()-t0, 2)}s)")

        t0 = time.time()
        test.write.mode("overwrite").partitionBy("year") \
            .option("compression", "snappy").parquet(TEST_GOLD_PATH)
        print(f"  Test set:      {TEST_GOLD_PATH}  ({round(time.time()-t0, 2)}s)")

        print("\n[COMPLETE] Feature engineering pipeline finished.")
        print(f"  Total features: {len(df.columns)}")
        print(f"  Feature columns: {df.columns}")
        print("="*80 + "\n")

    finally:
        stop_spark(spark)
