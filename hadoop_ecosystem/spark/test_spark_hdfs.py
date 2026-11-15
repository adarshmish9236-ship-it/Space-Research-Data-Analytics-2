from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Orbitalytics-PySpark-HDFS-Verification") \
    .getOrCreate()

print("=" * 65)
print("   ORBITALYTICS PYSPARK DISTRIBUTED HDFS VERIFICATION")
print("=" * 65)

# Read directly from distributed HDFS
df = spark.read.csv(
    "hdfs://namenode:9000/space_research/raw/equipment_component_demand.csv",
    header=True,
    inferSchema=True
)

total_records = df.count()
print(f"\n[OK] Total HDFS Demand Records Read via PySpark: {total_records}")

print("\n--- Demand Aggregation by Component Category via PySpark ---")
summary_df = df.groupBy("component_category") \
    .agg({"units_demanded": "sum", "total_demand_value_million_usd": "avg"}) \
    .withColumnRenamed("sum(units_demanded)", "total_units_demanded") \
    .withColumnRenamed("avg(total_demand_value_million_usd)", "avg_value_m_usd")

summary_df.orderBy("total_units_demanded", ascending=False).show(truncate=False)

# Write output back to HDFS in Parquet format
output_hdfs_path = "hdfs://namenode:9000/space_research/analytics/pyspark_demand_summary.parquet"
summary_df.write.mode("overwrite").parquet(output_hdfs_path)
print(f"[SUCCESS] Distributed Parquet output written to: {output_hdfs_path}\n")

spark.stop()

