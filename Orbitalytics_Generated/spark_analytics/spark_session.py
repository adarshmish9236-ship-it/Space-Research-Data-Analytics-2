#!/usr/bin/env python3
"""
ORBITALYTICS Phase 7 — PySpark SparkSession Factory
Provides a reusable, production-configured SparkSession connected to:
  - Hadoop HDFS (hdfs://namenode:9000)
  - Spark Master (spark://spark-master:7077)
  - Hive Metastore (optional)
"""

import os
import logging
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("orbitalytics.spark_session")

SPARK_MASTER = os.getenv("SPARK_MASTER", "spark://spark-master:7077")
HDFS_NAMENODE = os.getenv("HDFS_NAMENODE", "hdfs://namenode:9000")
APP_NAME = "ORBITALYTICS-Phase7"

SILVER_BASE = f"{HDFS_NAMENODE}/orbitalytics/silver"
GOLD_BASE   = f"{HDFS_NAMENODE}/orbitalytics/gold"


def get_spark_session(app_name: str = APP_NAME, master: str = SPARK_MASTER) -> SparkSession:
    """
    Build and return a production SparkSession for ORBITALYTICS Phase 7.
    Configuration:
      - Executor memory: 1536m (safe for 4 GB NodeManager)
      - Driver memory:   1024m
      - Serializer:      KryoSerializer (faster than Java default)
      - Parquet compression: snappy
      - Adaptive Query Execution: enabled (Spark 3+)
      - Log level: WARN (suppress verbose INFO from HDFS/Spark internals)
    """
    spark = (
        SparkSession.builder
        .master(master)
        .appName(app_name)
        .config("spark.executor.memory", "1536m")
        .config("spark.driver.memory", "1024m")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.parquet.compression.codec", "snappy")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.hadoop.fs.defaultFS", HDFS_NAMENODE)
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.default.parallelism", "8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    logger.info(f"SparkSession active: {spark.version} | master={master}")
    logger.info(f"HDFS base: {HDFS_NAMENODE}")
    return spark


def stop_spark(spark: SparkSession):
    """Gracefully stop the SparkSession and log execution metrics summary."""
    sc = spark.sparkContext
    logger.info(f"Stopping SparkSession | AppId={sc.applicationId}")
    spark.stop()
