# ORBITALYTICS 2.0 — System Architecture Specification

---

## 1. Executive Summary

**ORBITALYTICS 2.0** is an enterprise-grade Big Data Analytics, Predictive Forecasting, and Resource Allocation Platform engineered specifically for space exploration, orbital mechanics telemetry, satellite manufacturing, and mission logistics. The architecture synthesizes classical distributed computing paradigms—**Apache Hadoop HDFS**, **YARN**, **Hadoop Streaming MapReduce**, **Apache Pig Latin**, **Apache Hive Data Warehouse**, and **Apache Spark / PySpark**—with modern time-series forecasting, Mixed-Integer Linear Programming (MILP), and high-performance asynchronous web microservices.

```
+---------------------------------------------------------------------------------------------------+
|                                   ORBITALYTICS 2.0 SYSTEM ARCHITECTURE                            |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ LAYER 1: DATA INGESTION & DISCOVERY (BRONZE) ]                                                  |
|  * 9 Canonical Datasets (CSV/JSON) -> Schema & Primary/Foreign Key Validation                      |
|  * Automated SHA-256 Checksums & Provenance Lineage Tracking                                      |
|                                                                                                   |
|  [ LAYER 2: DISTRIBUTED STORAGE — APACHE HADOOP HDFS ]                                            |
|  * NameNode (Port 9000/9870) + DataNode (Port 9864)                                               |
|  * Medallion Storage Zones:                                                                       |
|      /space_research/raw/        -> Immutable source landing zone                                 |
|      /space_research/bronze/     -> Standardized, verified ingest                                 |
|      /space_research/silver/     -> Snappy-compressed columnar Parquet, partitioned by year       |
|      /space_research/gold/       -> Star-Schema Hive warehouse facts & dimensions                 |
|      /space_research/curated/    -> Pre-aggregated analytics & cross-domain joins                  |
|      /space_research/forecasts/  -> 4-Quarter projections with 95% Confidence Intervals           |
|      /space_research/warehouse/  -> Hive managed and external tables                              |
|                                                                                                   |
|  [ LAYER 3: DISTRIBUTED BATCH & ETL COMPUTING ]                                                   |
|  +---------------------------+---------------------------+-------------------------------------+  |
|  |     Apache Pig Latin      |  Hadoop MapReduce Stream  |       Apache PySpark Engine         |  |
|  | * 9 ETL transformation    | * 7 Mapper/Reducer pairs  | * Multi-dataset relational joins    |  |
|  |   scripts (.pig)          | * Distributed shuffle/sort| * Autoregressive feature pipelines  |  |
|  | * Null filtering & casts  | * Pure Unix pipes         | * Spark MLlib tree ensembles        |  |
|  +---------------------------+---------------------------+-------------------------------------+  |
|                                                                                                   |
|  [ LAYER 4: DATA WAREHOUSING — APACHE HIVE ]                                                      |
|  * HiveServer2 (Port 10000) & Hive Metastore backed by PostgreSQL 13                              |
|  * Dimensional Star-Schema:                                                                       |
|      Dimensions: dim_agency, dim_component, dim_resource, dim_mission, dim_satellite, dim_date    |
|      Facts:      fact_equipment_demand, fact_resource_consumption, fact_launch_activity,          |
|                  fact_manufacturing, fact_research_investment                                     |
|  * Dynamic Partitioning by Year (`year=YYYY`) & Partition Pruning Execution                       |
|                                                                                                   |
|  [ LAYER 5: PREDICTIVE FORECASTING & OPERATIONS RESEARCH ]                                        |
|  * 13 Forecasting Models (Baseline, Statistical ARIMA/SARIMA/Holt-Winters, ML RF/XGBoost, MLlib)  |
|  * Rolling-origin expanding-window backtesting without lookahead leakage                          |
|  * Shortage detection: max(0, Forecast Demand - Available Supply)                                 |
|  * SciPy HiGHS Mixed-Integer Linear Programming (MILP) Procurement Optimizer                      |
|                                                                                                   |
|  [ LAYER 6: APPLICATION GATEWAY & CLIENT INTERFACE ]                                              |
|  * FastAPI Asynchronous REST Engine with 38 versioned endpoints (/api/v1/)                         |
|  * Responsive Single-Page Application (SPA) with Dual-Layer Navigation:                           |
|      Layer A: Space Research Intelligence Dashboard (Executive KPIs, Missions, Satellites, etc.)   |
|      Layer B: Big Data Engineering Control Center (HDFS, YARN, Hive, Spark, Models, Benchmarks)  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Medallion Storage Architecture (HDFS)

The platform enforces the Medallion Data Lakehouse architecture across 7 logical HDFS directories:

| Zone | HDFS Path | Storage Format | Compression | Mutability | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Raw / Landing** | `/space_research/raw/` | Delimited CSV / JSON | Uncompressed | Write-Once | Original immutable telemetry & registry dumps |
| **Bronze** | `/space_research/bronze/` | Validated CSV | Gzip / None | Append-Only | Quality-screened records with schema validation |
| **Silver** | `/space_research/silver/` | Columnar Parquet | Snappy | Immutable | Cleaned, typed, partitioned by year (`year=YYYY`) |
| **Gold** | `/space_research/gold/` | Star-Schema Parquet | Snappy | Managed | Star-schema facts & dimensions for Hive & Spark |
| **Curated** | `/space_research/curated/` | Parquet / Directory | Snappy | Optimized | Feature-engineered analytical datasets |
| **Forecasts** | `/space_research/forecasts/` | JSON / Parquet | None / Snappy | Read-Heavy | Multi-horizon projections with 95% CIs |
| **Warehouse** | `/space_research/warehouse/` | Apache Hive Tables | Snappy / ORC | External/Managed| SQL analytics query layer for HiveServer2 |

---

## 3. Data Processing Engines & Workflows

### 3.1 Apache Pig Latin ETL
- **Location:** `pig_etl/`
- **Role:** Extract, clean, filter, and cast raw space telemetry into typed Silver records.
- **Execution:** Runs in Pig local/MapReduce mode; handles dirty values, missing agency strings, negative budgets, and writes to partitioned Parquet and intermediate CSVs.

### 3.2 Hadoop Streaming MapReduce
- **Location:** `mapreduce/`
- **Role:** Distributed batch aggregation on high-volume Silver datasets.
- **Mechanisms:** Pure Python mappers and reducers communicating via standard POSIX streams (`sys.stdin` -> `sys.stdout`). Hadoop YARN executes the true distributed shuffle-and-sort phase between map and reduce.

### 3.3 Apache Hive Data Warehouse
- **Location:** `hive_warehouse/`
- **Role:** ANSI SQL analytical querying across star-schema tables.
- **Components:** HiveServer2 thrift daemon, Hive Metastore connected to PostgreSQL, and 16 pre-compiled analytical SQL queries demonstrating partition pruning, window functions, and multi-table joins.

### 3.4 Apache PySpark Distributed Analytics
- **Location:** `spark_analytics/` and `ml_forecasting/`
- **Role:** Scalable distributed joins, rolling window aggregation, autoregressive feature generation, and distributed Spark MLlib Random Forest and Gradient Boosted Tree models.

---

## 4. Forecasting & Operations Research Engine

1. **Expanding Window Backtester:** Evaluates models across chronological folds without target leakage (`max(train_t) < min(test_t)`).
2. **Evaluator Metrics:** Computes RMSE, MAE, WAPE (%), MAPE (%), Bias (%), and $R^2$.
3. **Shortage Detection:** Identifies expected supply deficits across 32 component classes and 6 propellant commodities.
4. **HiGHS MILP Optimizer:** Formulates a mixed-integer linear program minimizing total acquisition cost subject to cleanroom throughput constraints, budget caps, safety stocks, and lead-time buffering.

---

## 5. Security, Networking & Port Allocation

| Component | Container Name | Internal Port | Host Port | Protocol | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hadoop NameNode** | `hadoop-namenode` | 9000 | 9000 | RPC | HDFS IPC Metadata Server |
| **HDFS Web UI** | `hadoop-namenode` | 9870 | 9870 | HTTP | HDFS File System Web Browser |
| **Hadoop DataNode** | `hadoop-datanode` | 9864 | 9864 | HTTP | Block Data Transfer & Status |
| **YARN ResourceManager** | `hadoop-resourcemanager` | 8032, 8088 | 8032, 8088 | RPC, HTTP | Cluster Resource Scheduling & UI |
| **YARN NodeManager** | `hadoop-nodemanager` | 8042 | 8042 | HTTP | Worker Container Management |
| **HiveServer2** | `hive-server` | 10000, 10002 | 10000, 10002 | Thrift, HTTP | JDBC/ODBC SQL Client Interface |
| **Hive Metastore DB** | `hive-metastore-postgresql` | 5432 | 5432 | PostgreSQL | Relational Metadata Catalog |
| **Spark Master** | `spark-master` | 7077, 8080 | 7077, 8080 | RPC, HTTP | PySpark Cluster Coordinator & UI |
| **Spark Worker** | `spark-worker` | 8081 | 8081 | HTTP | Worker Execution Telemetry |
| **FastAPI Backend** | Host / Container | 8000 | 8000 | HTTP | REST API Gateway & SPA Server |
