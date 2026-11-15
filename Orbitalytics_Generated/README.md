# ORBITALYTICS 2.0: Space Research Big Data Analytics Platform

> **A Distributed Hadoop Ecosystem Approach to Demand Forecasting and Supply Chain Optimization for Space Exploration Resources and Satellite Hardware.**

---

## 🛰️ Executive Overview

**ORBITALYTICS 2.0** is an enterprise-grade Big Data Analytics, Predictive Forecasting, and Resource Allocation Platform engineered specifically for space exploration, orbital mechanics telemetry, satellite manufacturing, and mission logistics. The platform synthesizes classical distributed computing paradigms—**Apache Hadoop HDFS**, **YARN**, **Hadoop Streaming MapReduce**, **Apache Pig Latin**, **Apache Hive Data Warehouse**, and **Apache Spark / PySpark**—with modern time-series forecasting, Mixed-Integer Linear Programming (MILP), and high-performance asynchronous web microservices.

---

## 🏛️ System Architecture

```
+---------------------------------------------------------------------------------------------------+
|                                   ORBITALYTICS 2.0 ARCHITECTURE                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ LAYER 1: DATA INGESTION & DISCOVERY (BRONZE) ]                                                  |
|  * 9 Canonical Datasets (CSV/JSON) -> Schema & Primary/Foreign Key Validation                      |
|  * Automated SHA-256 Checksums & Provenance Lineage Tracking                                      |
|                                                                                                   |
|  [ LAYER 2: DISTRIBUTED STORAGE — APACHE HADOOP HDFS ]                                            |
|  * NameNode (Port 9000/9870) + DataNode (Port 9864)                                               |
|  * 7-Tier Medallion Storage: Raw, Bronze, Silver, Gold, Curated, Forecasts, Warehouse               |
|                                                                                                   |
|  [ LAYER 3: DISTRIBUTED BATCH & ETL COMPUTING ]                                                   |
|  * Apache Pig Latin: 9 declarative ETL dataflow scripts emitting Snappy-compressed Parquet        |
|  * Hadoop MapReduce: 7 Python mapper/reducer pairs with distributed YARN shuffle-and-sort         |
|  * Apache PySpark: In-memory Catalyst joins, rolling window aggregates, and MLlib ensembles       |
|                                                                                                   |
|  [ LAYER 4: DATA WAREHOUSING — APACHE HIVE ]                                                      |
|  * HiveServer2 (Port 10000) & Hive Metastore backed by PostgreSQL 13                              |
|  * Dimensional Star-Schema: 7 Dimension Tables & 5 Partitioned Fact Tables (year=YYYY)            |
|  * 16 Pre-compiled Analytical SQL Queries demonstrating partition pruning                         |
|                                                                                                   |
|  [ LAYER 5: PREDICTIVE FORECASTING & OPERATIONS RESEARCH ]                                        |
|  * 13 Forecasting Models (Baseline, ARIMA, SARIMA, Holt-Winters, Random Forest, XGBoost, MLlib)   |
|  * Chronological rolling-origin backtesting without lookahead leakage                             |
|  * SciPy HiGHS Mixed-Integer Linear Programming (MILP) Procurement Optimizer                      |
|                                                                                                   |
|  [ LAYER 6: APPLICATION GATEWAY & CLIENT INTERFACE ]                                              |
|  * FastAPI Asynchronous REST Engine with 38 versioned endpoints (/api/v1/)                         |
|  * Single-Page Application (SPA) with Dual-Layer Navigation: Research Intelligence & Engineering  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## ⚡ Quick-Start Installation

### Prerequisites
- **Docker Desktop** (v4.20+) with Docker Compose v2
- **Python 3.10 – 3.14**
- **Git**

### 1. Launch the 9-Container Hadoop Ecosystem
```bash
cd docker
docker compose up -d
docker compose ps
```

### 2. Install Python Dependencies
```powershell
python -m pip install -r backend/requirements.txt
```

### 3. Run End-to-End System Audit (14 Stages)
```powershell
python scripts/run_e2e_pipeline.py
```

### 4. Start Backend Server & Open Dashboard
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
- **Web Dashboard:** [http://localhost:8000/](http://localhost:8000/)
- **Swagger REST API:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **HDFS NameNode UI:** [http://localhost:9870/](http://localhost:9870/)
- **YARN Resource Manager:** [http://localhost:8088/](http://localhost:8088/)
- **Spark Cluster UI:** [http://localhost:8080/](http://localhost:8080/)

---

## 🧪 Comprehensive Automated Testing

The platform includes 80 automated unit and integration tests covering the complete platform:
```powershell
python -m pytest tests/phase_12 -v
```
**Test Result:** `80 passed in 7.22s (100.0% Pass Rate)`

---

## 📚 Technical Documentation Index

| Documentation File | Description |
| :--- | :--- |
| [`docs/system_architecture.md`](file:///E:/PROJECTS/BDT/docs/system_architecture.md) | Six-layer architecture, Medallion Lakehouse tiers, and cluster ports |
| [`docs/installation_guide.md`](file:///E:/PROJECTS/BDT/docs/installation_guide.md) | Step-by-step developer deployment guide |
| [`docs/hadoop_setup_guide.md`](file:///E:/PROJECTS/BDT/docs/hadoop_setup_guide.md) | Hadoop container configuration, XML parameters, and cluster maintenance |
| [`docs/dataset_documentation.md`](file:///E:/PROJECTS/BDT/docs/dataset_documentation.md) | Schema dictionaries, primary keys, partitions, and quality rules |
| [`docs/hdfs_documentation.md`](file:///E:/PROJECTS/BDT/docs/hdfs_documentation.md) | HDFS storage tiers, block size policies (128 MB), and directory tree |
| [`docs/pig_etl_documentation.md`](file:///E:/PROJECTS/BDT/docs/pig_etl_documentation.md) | Apache Pig Latin script inventory, type transformations, and execution |
| [`docs/mapreduce_documentation.md`](file:///E:/PROJECTS/BDT/docs/mapreduce_documentation.md) | Streaming mapper/reducer pairs, YARN shuffle-and-sort, and aggregations |
| [`docs/hive_sql_documentation.md`](file:///E:/PROJECTS/BDT/docs/hive_sql_documentation.md) | Star-schema DDL, partition pruning execution plans, and 16 SQL queries |
| [`docs/spark_documentation.md`](file:///E:/PROJECTS/BDT/docs/spark_documentation.md) | PySpark in-memory execution, Catalyst joins, and MLlib tree ensembles |
| [`docs/forecasting_methodology.md`](file:///E:/PROJECTS/BDT/docs/forecasting_methodology.md) | Mathematical formulation, 13 models, rolling backtesting, and 95% CIs |
| [`docs/benchmarking_methodology.md`](file:///E:/PROJECTS/BDT/docs/benchmarking_methodology.md) | 75-trial empirical comparison across Pandas, Spark, Hive, MR, and Pig |
| [`docs/api_documentation.md`](file:///E:/PROJECTS/BDT/docs/api_documentation.md) | Complete OpenAPI catalog of all 38 REST endpoints under `/api/v1/` |
| [`docs/testing_report.md`](file:///E:/PROJECTS/BDT/docs/testing_report.md) | Detailed QA report across all 80 automated unit and integration tests |
| [`docs/known_limitations.md`](file:///E:/PROJECTS/BDT/docs/known_limitations.md) | Explicit disclosure of containerization, runtime, and dataset boundaries |
| [`docs/troubleshooting_guide.md`](file:///E:/PROJECTS/BDT/docs/troubleshooting_guide.md) | Operational runbook for port conflicts, SafeMode, and Docker pipes |
| [`docs/academic_project_report.md`](file:///E:/PROJECTS/BDT/docs/academic_project_report.md) | Publication-grade formal 21-section technical report with citations |
| [`docs/final_delivery_report.md`](file:///E:/PROJECTS/BDT/docs/final_delivery_report.md) | Final acceptance matrix, sign-off, and release audit |

---

## 🎬 Live Interactive Demonstration

To run the interactive 13-stage system demonstration sequence:
```powershell
python demonstration/run_orbitalytics_demo.py
```
or double-click `demonstration/run_orbitalytics_demo.bat`.

---

## ⚖️ License & Academic Disclosure

Distributed under the Apache 2.0 License. Developed for research and educational purposes in Big Data Technologies, Distributed Computing, and Aerospace Logistics Analytics.
