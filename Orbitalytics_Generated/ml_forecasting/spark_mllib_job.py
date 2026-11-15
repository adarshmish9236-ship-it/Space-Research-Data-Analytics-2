#!/usr/bin/env python3
"""
ORBITALYTICS Phase 8 — Task 4: Distributed Spark MLlib Training Job
Trains distributed RandomForestRegressor and GBTRegressor directly on the Spark cluster
using the Gold Layer feature datasets persisted in HDFS:
  - Train: hdfs://namenode:9000/orbitalytics/gold/forecast_features/train_dataset
  - Test:  hdfs://namenode:9000/orbitalytics/gold/forecast_features/test_dataset
"""

import sys
import json
import time
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator

SPARK_MASTER = "spark://spark-master:7077"
HDFS_BASE = "hdfs://namenode:9000/orbitalytics/gold/forecast_features"
OUTPUT_MANIFEST = "/tmp/phase8_spark_mllib_manifest.json"

FEATURE_COLS = [
    "avg_lead_time_days",
    "annual_units_manufactured",
    "annual_units_procured",
    "lag_1_units",
    "lag_2_units",
    "lag_3_units",
    "lag_4_units",
    "lag_1_value",
    "rolling_3yr_mean",
    "rolling_3yr_std",
    "fulfillment_rate_pct",
    "prev_yr_mission_count",
    "prev_yr_launch_count",
    "prev_yr_satellite_deploy_count",
    "years_since_start",
    "is_recent_period"
]


def run_spark_mllib_pipeline():
    print("\n" + "="*80)
    print("ORBITALYTICS PHASE 8 — DISTRIBUTED SPARK MLLIB TRAINING PIPELINE")
    print("="*80)

    spark = (
        SparkSession.builder
        .master(SPARK_MASTER)
        .appName("ORBITALYTICS-P8-SparkMLlib")
        .config("spark.executor.memory", "1536m")
        .config("spark.driver.memory", "1024m")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        train_path = f"{HDFS_BASE}/train_dataset"
        test_path  = f"{HDFS_BASE}/test_dataset"

        print(f"[DATA] Loading train partition from HDFS: {train_path}")
        train_df = spark.read.parquet(train_path)
        print(f"[DATA] Loading test partition from HDFS:  {test_path}")
        test_df  = spark.read.parquet(test_path)

        train_count = train_df.count()
        test_count  = test_df.count()
        print(f"  Training records: {train_count:,}")
        print(f"  Test records:     {test_count:,}")

        # Fill any missing feature values with 0.0 for robust MLlib vector assembly
        for c in FEATURE_COLS:
            train_df = train_df.withColumn(c, F.coalesce(F.col(c).cast("double"), F.lit(0.0)))
            test_df  = test_df.withColumn(c,  F.coalesce(F.col(c).cast("double"), F.lit(0.0)))

        train_df = train_df.withColumn("label", F.col("annual_units_demanded").cast("double"))
        test_df  = test_df.withColumn("label",  F.col("annual_units_demanded").cast("double"))

        # VectorAssembler
        assembler = VectorAssembler(inputCols=FEATURE_COLS, outputCol="features")
        train_vec = assembler.transform(train_df).select("features", "label")
        test_vec  = assembler.transform(test_df).select("features", "label")

        # Cache assembled vectors
        train_vec.cache()
        test_vec.cache()

        results = []

        # 1. Distributed Random Forest Regressor
        print("\n--- Training Distributed Spark MLlib RandomForestRegressor ---")
        t0 = time.time()
        rf = RandomForestRegressor(featuresCol="features", labelCol="label", numTrees=50, maxDepth=5, seed=42)
        rf_model = rf.fit(train_vec)
        rf_train_time = round(time.time() - t0, 2)

        rf_preds = rf_model.transform(test_vec)
        evaluator_rmse = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
        evaluator_r2   = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="r2")
        evaluator_mae  = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="mae")

        rf_rmse = round(float(evaluator_rmse.evaluate(rf_preds)), 2)
        rf_r2   = round(float(evaluator_r2.evaluate(rf_preds)), 4)
        rf_mae  = round(float(evaluator_mae.evaluate(rf_preds)), 2)
        print(f"  RF Model trained in {rf_train_time}s | Test RMSE: {rf_rmse} | R2: {rf_r2} | MAE: {rf_mae}")

        results.append({
            "model_name": "Spark_MLlib_RandomForestRegressor",
            "train_time_seconds": rf_train_time,
            "trees": 50,
            "max_depth": 5,
            "test_rmse": rf_rmse,
            "test_r2": rf_r2,
            "test_mae": rf_mae
        })

        # 2. Distributed Gradient-Boosted Trees (GBTRegressor)
        print("\n--- Training Distributed Spark MLlib GBTRegressor ---")
        t0 = time.time()
        gbt = GBTRegressor(featuresCol="features", labelCol="label", maxIter=30, maxDepth=4, seed=42)
        gbt_model = gbt.fit(train_vec)
        gbt_train_time = round(time.time() - t0, 2)

        gbt_preds = gbt_model.transform(test_vec)
        gbt_rmse = round(float(evaluator_rmse.evaluate(gbt_preds)), 2)
        gbt_r2   = round(float(evaluator_r2.evaluate(gbt_preds)), 4)
        gbt_mae  = round(float(evaluator_mae.evaluate(gbt_preds)), 2)
        print(f"  GBT Model trained in {gbt_train_time}s | Test RMSE: {gbt_rmse} | R2: {gbt_r2} | MAE: {gbt_mae}")

        results.append({
            "model_name": "Spark_MLlib_GBTRegressor",
            "train_time_seconds": gbt_train_time,
            "max_iter": 30,
            "max_depth": 4,
            "test_rmse": gbt_rmse,
            "test_r2": gbt_r2,
            "test_mae": gbt_mae
        })

        manifest = {
            "phase": 8,
            "component": "Spark_MLlib_Distributed_Training",
            "timestamp": datetime.now().isoformat(),
            "spark_master": SPARK_MASTER,
            "train_records": train_count,
            "test_records": test_count,
            "feature_count": len(FEATURE_COLS),
            "features": FEATURE_COLS,
            "models_evaluated": results
        }

        with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"\nManifest saved to {OUTPUT_MANIFEST}")
        print("="*80 + "\n")

    finally:
        spark.stop()


if __name__ == "__main__":
    run_spark_mllib_pipeline()
