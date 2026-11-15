# ORBITALYTICS 2.0 — Apache PySpark Distributed Analytics Specification

---

## 1. Spark Architecture & Cluster Topology

**Apache Spark** serves as the high-throughput, in-memory distributed compute engine in ORBITALYTICS 2.0. Operating directly on the Silver and Gold Parquet layers stored in HDFS, Spark coordinates multi-dataset relational joins, complex windowing calculations, autoregressive feature generation, and distributed machine learning via **Spark MLlib**.

```
                           SPARK CLUSTER TOPOLOGY
                           ----------------------

           +----------------------------------------------------+
           |           PySpark Application Driver               |
           |   * SparkSession (App: "OrbitalyticsDistributed")  |
           |   * Spark SQL Catalyst Optimizer                   |
           |   * Tungsten Execution Engine                      |
           +-------------------------+--------------------------+
                                     |
                                     v
                        +-------------------------+
                        |   Spark Master Node     |
                        |   (spark://master:7077) |
                        |   Web UI: Port 8080     |
                        +------------+------------+
                                     |
             +-----------------------+-----------------------+
             |                                               |
             v                                               v
+-------------------------+                     +-------------------------+
|     Spark Worker 1      |                     |     Spark Worker 2      |
| * Executor: 2 Cores     |                     | * Executor: 2 Cores     |
| * 2 GB Heap RAM         |                     | * 2 GB Heap RAM         |
| * BlockManager (Cache)  |                     | * BlockManager (Cache)  |
+-------------------------+                     +-------------------------+
```

---

## 2. Distributed Spark Analytical Pipelines

The platform includes four master PySpark batch pipelines in `/spark_analytics/`:

| Pipeline Script | Purpose | Data Sources Joined | Output Table / Path |
| :--- | :--- | :--- | :--- |
| `01_multi_dataset_integration.py` | Full-mission telemetry synthesis | `space_missions`, `launch_activities`, `satellites_orbital` | `/space_research/curated/mission_telemetry_integrated.parquet` |
| `02_historical_demand_aggregations.py`| Distributed trend analysis | `equipment_component_demand`, `manufacturing` | `/space_research/curated/component_demand_trends.parquet` |
| `03_resource_consumption_analysis.py` | Cryo & propellant logistics | `resource_consumption`, `space_missions` | `/space_research/curated/resource_burn_rates.parquet` |
| `04_feature_engineering_pipeline.py` | Autoregressive ML feature matrix | All 9 Silver Parquet datasets | `/space_research/curated/ml_feature_matrix.parquet` |

---

## 3. Autoregressive Feature Engineering Implementation

The feature engineering pipeline computes rolling statistics and lag transformations using Spark SQL Window specifications without triggering data skew or memory spills:

```python
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("OrbitalyticsFeatureEngineering") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

# Load Silver Equipment Demand
df = spark.read.parquet("hdfs://hadoop-namenode:9000/space_research/silver/equipment_component_demand")

# Define chronological window partitioned by component
w = Window.partitionBy("equipment_type").orderBy("year", "quarter")

# Generate Autoregressive Lags (t-1, t-2, t-3, t-4)
df_features = df \
    .withColumn("lag_1", F.lag("units_demanded", 1).over(w)) \
    .withColumn("lag_2", F.lag("units_demanded", 2).over(w)) \
    .withColumn("lag_3", F.lag("units_demanded", 3).over(w)) \
    .withColumn("lag_4", F.lag("units_demanded", 4).over(w)) \
    .withColumn("rolling_mean_4", F.avg("units_demanded").over(w.rowsBetween(-3, 0))) \
    .withColumn("rolling_std_4", F.stddev("units_demanded").over(w.rowsBetween(-3, 0))) \
    .withColumn("quarter_num", F.regexp_extract("quarter", r"Q(\d)", 1).cast("int")) \
    .withColumn("secular_trend", F.col("year") - 2010)

# Save feature matrix to HDFS Gold zone
df_features.write.mode("overwrite").parquet("hdfs://hadoop-namenode:9000/space_research/gold/features")
```

---

## 4. Spark MLlib Distributed Model Training

For large-scale predictive modeling, Spark MLlib tree ensembles are distributed across worker nodes:
- **`RandomForestRegressor`:** 150 trees, max depth 8, subspace feature subsetting ($\sqrt{p}$).
- **`GBTRegressor`:** Gradient boosted decision trees optimizing second-order loss across distributed partitions.
- Evaluated via `RegressionEvaluator` on HDFS data blocks, reporting root-mean-squared error (RMSE) and coefficient of determination ($R^2$).
