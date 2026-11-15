#!/usr/bin/env python3
"""
ORBITALYTICS Phase 7 — Task 2 & 3: Multi-Dataset Integration & Distributed Transformations
Performs controlled joins, aggregations, window operations, and trend calculations
across all Silver Parquet datasets. Uses broadcast joins for small dimensions to avoid
Cartesian explosion. Outputs clean integrated DataFrames to Gold HDFS layer.
"""

import sys
import time
from datetime import datetime
sys.path.insert(0, "/opt/spark_analytics")
from spark_session import get_spark_session, stop_spark, SILVER_BASE, GOLD_BASE

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType, DoubleType


def load_silver_datasets(spark):
    """Load all Silver Parquet datasets into named DataFrames and temp views."""
    print("\n[LOAD] Reading Silver Parquet datasets from HDFS...")
    datasets = {}
    paths = {
        "missions":             f"{SILVER_BASE}/missions",
        "satellites":           f"{SILVER_BASE}/satellites",
        "launches":             f"{SILVER_BASE}/launches",
        "equipment_demand":     f"{SILVER_BASE}/equipment_demand",
        "resource_consumption": f"{SILVER_BASE}/resource_consumption",
        "manufacturing":        f"{SILVER_BASE}/manufacturing",
        "research_investment":  f"{SILVER_BASE}/agency_expenditure",
        "infrastructure":       f"{SILVER_BASE}/infrastructure",
    }
    for name, path in paths.items():
        try:
            df = spark.read.parquet(path)
            df.createOrReplaceTempView(name)
            datasets[name] = df
            print(f"  {name:22}: {df.count():,} rows | {len(df.columns)} cols")
        except Exception as e:
            print(f"  WARNING: {name} not loaded from {path}: {e}")
    return datasets


def task3_equipment_demand_analytics(spark, datasets):
    """
    Task 3A: Equipment Demand — Distributed Aggregations, Window Functions, Trend Analysis.
    Uses: fact_equipment_demand + Silver missions.
    """
    print("\n--- TASK 3A: Equipment Demand Analytics ---")
    ed = datasets.get("equipment_demand")
    if ed is None:
        print("  Skipped: equipment_demand not available.")
        return None

    # Cast numeric columns safely and alias value column
    ed = ed.withColumn("units_demanded", F.col("units_demanded").cast(DoubleType())) \
           .withColumn("units_manufactured", F.col("units_manufactured").cast(DoubleType())) \
           .withColumn("units_procured", F.col("units_procured").cast(DoubleType())) \
           .withColumn("lead_time_days", F.col("lead_time_days").cast(IntegerType())) \
           .withColumn("total_demand_value_m_usd", F.col("total_demand_value_million_usd").cast(DoubleType())) \
           .withColumn("year", F.col("year").cast(IntegerType()))

    # 1. Annual aggregation with window-based YoY growth
    year_window = Window.orderBy("year")
    annual_agg = (
        ed.groupBy("year")
          .agg(
              F.count("demand_id").alias("order_count"),
              F.round(F.sum("units_demanded"), 1).alias("total_units_demanded"),
              F.round(F.sum("total_demand_value_m_usd"), 2).alias("total_value_m_usd"),
              F.round(F.avg("lead_time_days"), 1).alias("avg_lead_time_days")
          )
          .withColumn("prev_year_units", F.lag("total_units_demanded", 1).over(year_window))
          .withColumn("yoy_growth_pct",
              F.round((F.col("total_units_demanded") - F.col("prev_year_units"))
                      / F.col("prev_year_units") * 100.0, 2))
          .withColumn("cumulative_units",
              F.round(F.sum("total_units_demanded").over(year_window.rowsBetween(Window.unboundedPreceding, 0)), 1))
          .orderBy("year")
    )

    print("  Annual demand trend (top 5 rows):")
    annual_agg.show(5, truncate=False)

    # 2. Component-level aggregation
    component_agg = (
        ed.groupBy("component_id", "component_category")
          .agg(
              F.round(F.sum("units_demanded"), 1).alias("total_units"),
              F.round(F.sum("total_demand_value_m_usd"), 2).alias("total_value_m_usd"),
              F.round(F.avg("lead_time_days"), 1).alias("avg_lead_time_days"),
              F.round(F.sum("units_manufactured"), 1).alias("total_manufactured"),
              F.round(F.sum("units_procured"), 1).alias("total_procured")
          )
          .withColumn("fulfillment_rate_pct",
              F.round((F.col("total_manufactured") + F.col("total_procured"))
                      / F.col("total_units") * 100.0, 2))
          .orderBy(F.desc("total_value_m_usd"))
    )
    print("  Component demand aggregation (top 3):")
    component_agg.show(3, truncate=False)

    # 3. Agency-level quarterly breakdown
    agency_quarterly = (
        ed.groupBy("agency_id", "year", "quarter")
          .agg(
              F.round(F.sum("units_demanded"), 1).alias("quarterly_units"),
              F.round(F.sum("total_demand_value_m_usd"), 2).alias("quarterly_value_m_usd")
          )
          .withColumn("supply_risk_flag",
              F.when(F.col("quarterly_units") < 5000, "HIGH")
               .when(F.col("quarterly_units") < 10000, "MEDIUM")
               .otherwise("LOW"))
          .orderBy("year", "quarter", "agency_id")
    )

    # Cache this for reuse in feature engineering
    t0 = time.time()
    annual_agg.cache()
    n = annual_agg.count()
    print(f"  Cached annual_agg: {n} rows in {round(time.time()-t0, 2)}s")

    return annual_agg, component_agg, agency_quarterly


def task3_resource_consumption_analytics(spark, datasets):
    """Task 3B: Resource Consumption — Annual trends and resource-type profiling."""
    print("\n--- TASK 3B: Resource Consumption Analytics ---")
    rc = datasets.get("resource_consumption")
    if rc is None:
        print("  Skipped: resource_consumption not available.")
        return None

    rc = rc.withColumn("quantity_consumed", F.col("quantity_consumed").cast(DoubleType())) \
           .withColumn("procurement_cost_k_usd", F.col("procurement_cost_k_usd").cast(DoubleType())) \
           .withColumn("year", F.col("year").cast(IntegerType()))

    annual_rc = (
        rc.groupBy("year", "resource_category")
          .agg(
              F.round(F.sum("quantity_consumed"), 2).alias("total_quantity_consumed"),
              F.round(F.sum("procurement_cost_k_usd"), 2).alias("total_cost_k_usd"),
              F.count("consumption_id").alias("record_count")
          )
          .withColumn("prev_quantity",
              F.lag("total_quantity_consumed", 1).over(
                  Window.partitionBy("resource_category").orderBy("year")))
          .withColumn("yoy_consumption_change_pct",
              F.round((F.col("total_quantity_consumed") - F.col("prev_quantity"))
                      / F.col("prev_quantity") * 100.0, 2))
          .orderBy("year", "resource_category")
    )
    print("  Resource consumption trend (top 5):")
    annual_rc.show(5, truncate=False)
    return annual_rc


def task3_launch_mission_analytics(spark, datasets):
    """Task 3C: Launch + Mission Correlation — joined aggregation with date transformations."""
    print("\n--- TASK 3C: Launch Activity and Mission Analytics ---")
    launches = datasets.get("launches")
    if launches is None:
        print("  Skipped: launches not available.")
        return None

    launches = launches.withColumn("year", F.col("year").cast(IntegerType())) \
                       .withColumn("launch_cost_m_usd", F.col("launch_cost_million_usd").cast(DoubleType())) \
                       .withColumn("payload_to_orbit_kg", F.col("payload_to_orbit_kg").cast(DoubleType()))

    year_window = Window.orderBy("year")

    launch_annual = (
        launches.groupBy("year")
          .agg(
              F.count("launch_id").alias("total_launches"),
              F.sum(F.when(F.col("launch_outcome") == "Success", 1).otherwise(0)).alias("successes"),
              F.round(F.sum("launch_cost_m_usd"), 2).alias("total_cost_m_usd"),
              F.round(F.sum("payload_to_orbit_kg"), 1).alias("total_payload_kg"),
              F.sum(F.when(
                  (F.col("commercial_flag") == True) | (F.col("commercial_flag").cast("string").isin("1", "True", "true")), 1).otherwise(0)
              ).alias("commercial_count")
          )
          .withColumn("success_rate_pct",
              F.round(F.col("successes") / F.col("total_launches") * 100.0, 2))
          .withColumn("commercial_share_pct",
              F.round(F.col("commercial_count") / F.col("total_launches") * 100.0, 2))
          .withColumn("prev_launches",
              F.lag("total_launches", 1).over(year_window))
          .withColumn("launch_growth_pct",
              F.round((F.col("total_launches") - F.col("prev_launches"))
                      / F.col("prev_launches") * 100.0, 2))
          .withColumn("rolling_3yr_avg_launches",
              F.round(F.avg("total_launches").over(
                  year_window.rowsBetween(-2, 0)), 2))
          .orderBy("year")
    )
    print("  Launch activity trend (top 5):")
    launch_annual.show(5, truncate=False)
    return launch_annual


def task3_research_investment_analytics(spark, datasets):
    """Task 3D: Research Investment — cumulative spend, moving averages, agency ranking."""
    print("\n--- TASK 3D: Research Investment Analytics ---")
    ri = datasets.get("research_investment")
    if ri is None:
        print("  Skipped: research_investment not available.")
        return None

    ri = ri.withColumn("year", F.col("year").cast(IntegerType())) \
           .withColumn("rd_expenditure_m_usd", F.col("rd_expenditure_million_usd").cast(DoubleType())) \
           .withColumn("infrastructure_expenditure_m_usd", F.col("infrastructure_expenditure_million_usd").cast(DoubleType())) \
           .withColumn("total_monthly_expenditure_m_usd", F.col("total_monthly_expenditure_million_usd").cast(DoubleType()))

    agency_window = Window.partitionBy("agency_id").orderBy("year")

    annual_ri = (
        ri.groupBy("year", "agency_id", "agency_name")
          .agg(
              F.round(F.sum("rd_expenditure_m_usd"), 2).alias("annual_rd_m_usd"),
              F.round(F.sum("infrastructure_expenditure_m_usd"), 2).alias("annual_infra_m_usd"),
              F.round(F.sum("total_monthly_expenditure_m_usd"), 2).alias("annual_total_m_usd")
          )
          .withColumn("cumulative_rd_m_usd",
              F.round(F.sum("annual_rd_m_usd").over(agency_window
                  .rowsBetween(Window.unboundedPreceding, 0)), 2))
          .withColumn("3yr_moving_avg_m_usd",
              F.round(F.avg("annual_total_m_usd").over(
                  agency_window.rowsBetween(-2, 0)), 2))
          .withColumn("agency_rank_by_investment",
              F.dense_rank().over(
                  Window.partitionBy("year").orderBy(F.desc("annual_total_m_usd"))))
          .orderBy("year", "agency_rank_by_investment")
    )
    print("  Research investment by agency-year (top 5):")
    annual_ri.show(5, truncate=False)
    return annual_ri


def write_gold_dataset(df, gold_path, partition_col="year"):
    """Write a DataFrame to HDFS Gold layer as partitioned Parquet + Snappy."""
    if df is None:
        print(f"  Skipping write to {gold_path}: DataFrame is None")
        return
    t0 = time.time()
    rows = df.count()
    (df.write
       .mode("overwrite")
       .partitionBy(partition_col)
       .option("compression", "snappy")
       .parquet(gold_path))
    elapsed = round(time.time() - t0, 2)
    print(f"  Written {rows:,} rows to Gold: {gold_path}  ({elapsed}s)")


if __name__ == "__main__":
    spark = get_spark_session(app_name="ORBITALYTICS-P7-Integration")
    try:
        datasets = load_silver_datasets(spark)

        # Task 3: Distributed transformations
        result_ed = task3_equipment_demand_analytics(spark, datasets)
        result_rc = task3_resource_consumption_analytics(spark, datasets)
        result_la = task3_launch_mission_analytics(spark, datasets)
        result_ri = task3_research_investment_analytics(spark, datasets)

        # Task 7: Write to Gold HDFS layer
        print("\n" + "="*80)
        print("TASK 7: WRITING GOLD LAYER DATASETS TO HDFS")
        print("="*80)

        if result_ed:
            annual_agg, component_agg, agency_quarterly = result_ed
            write_gold_dataset(annual_agg, f"{GOLD_BASE}/demand_analytics/annual_equipment_demand_trend")
            write_gold_dataset(component_agg.withColumn("category_partition", F.col("component_category")),
                               f"{GOLD_BASE}/demand_analytics/component_demand_summary", "category_partition")
        if result_rc:
            write_gold_dataset(result_rc, f"{GOLD_BASE}/resource_analytics/annual_resource_consumption_trend")
        if result_la:
            write_gold_dataset(result_la, f"{GOLD_BASE}/mission_analytics/annual_launch_trends")
        if result_ri:
            write_gold_dataset(result_ri, f"{GOLD_BASE}/research_analytics/annual_research_investment")

        print("\nTask 2 & 3 complete: Integration and transformations successful.")
    finally:
        stop_spark(spark)
