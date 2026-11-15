# Orbitalytics Phase 2: Hadoop Ecosystem Verification & Test Report

## 1. Executive Summary
**Project Title:** Space Research Data Analytics: A Hadoop Ecosystem Approach to Demand Forecasting  
**Phase:** Phase 2 — Hadoop Ecosystem Environment Setup & Distributed Cluster Verification  
**Evaluation Scope:** NameNode, DataNode, YARN ResourceManager, NodeManager, JobHistoryServer, Hive Metastore, PostgreSQL, HiveServer2, Spark Master/Worker, and Apache Pig.

---

## 2. Test Gates & Verification Methodology
The environment is verified through a 7-gate empirical verification protocol:

```
[Phase 2 Verification Workflow]
   ├── Gate 1: Docker Compose Orchestration & Health Probes
   ├── Gate 2: HDFS Distributed Storage (Read/Write, DfsAdmin Report)
   ├── Gate 3: YARN Resource Negotiation (NodeManager Heartbeat & vCores)
   ├── Gate 4: Hadoop MapReduce Workload (Distributed Example Jar)
   ├── Gate 5: Apache Hive Data Warehouse (PostgreSQL Metastore & SQL Query)
   ├── Gate 6: Apache Pig Latin Transformation (HDFS Dataflow Execution)
   └── Gate 7: Apache Spark Distributed Compute (Spark Master RPC & SparkPi)
```

---

## 3. Detailed Verification Results by Gate

### Gate 1: Docker Container Service Health
- **Target Containers:** `hadoop-namenode`, `hadoop-datanode`, `hadoop-resourcemanager`, `hadoop-nodemanager`, `hadoop-historyserver`, `hive-metastore-postgresql`, `hive-server`, `spark-master`, `spark-worker`.
- **Network Bridge:** `hadoop_ecosystem_default`
- **Result:** **PASSED** (All 9 distributed services operational).

### Gate 2: HDFS Distributed Storage Operations
- **Filesystem URI:** `hdfs://namenode:9000`
- **Block Size:** 128 MB (`dfs.blocksize = 134217728`)
- **Configured Replication:** `1` (Single DataNode development cluster).
- **Test Operations:**
  - `hdfs dfs -mkdir -p /space_research/test` -> **SUCCESS**
  - `hdfs dfs -put /tmp/test.csv /space_research/test/test.csv` -> **SUCCESS**
  - `hdfs dfs -cat /space_research/test/test.csv` -> **SUCCESS**
- **Result:** **PASSED** (Zero block corruption; WebHDFS active on port 9870).

### Gate 3: YARN Resource Negotiation
- **ResourceManager Endpoint:** `resourcemanager:8032` (WebUI: `http://localhost:8088/`)
- **Active NodeManagers:** 1 Registered NodeManager (`hadoop-nodemanager`).
- **Cluster Memory Pool:** 4,096 MB memory available.
- **Virtual Cores:** 4 vCores.
- **Auxiliary Services:** `mapreduce_shuffle` active.
- **Result:** **PASSED** (Cluster state: `RUNNING`).

### Gate 4: Hadoop MapReduce Batch Workload
- **Job Submitter:** Hadoop YARN Client.
- **Test Payload:** Text tokenization and frequency aggregation over HDFS-staged space research records.
- **Job Output:** `hdfs://namenode:9000/space_research/test/mr_out/part-r-00000`
- **Task Counters:** 1 Map Task, 1 Reduce Task executed successfully via YARN containers.
- **Result:** **PASSED**.

### Gate 5: Apache Hive Data Warehouse & PostgreSQL Metastore
- **Metastore Database:** PostgreSQL 13 (`jdbc:postgresql://hive-metastore-postgresql:5432/metastore`).
- **Database Catalog:** `metastore` (Persistent Docker named volume).
- **Thrift Port:** 9083 (Metastore), 10000 (HiveServer2).
- **Beeline Query Test:**
  ```sql
  CREATE DATABASE IF NOT EXISTS space_research_wh;
  SHOW DATABASES;
  ```
- **HDFS Warehouse Directory:** `hdfs://namenode:9000/user/hive/warehouse`
- **Result:** **PASSED** (Interactive SQL query execution verified).

### Gate 6: Apache Pig Latin Transformation
- **Script Location:** `hadoop_ecosystem/pig/demand_analysis.pig`
- **Dataflow Logic:** Filters hardware demand where `units_demanded > 0`, groups by category, computes aggregate component demand and average financial value, and stores tab-delimited output back to HDFS.
- **Result:** **PASSED**.

### Gate 7: Apache Spark In-Memory Distributed Processing
- **Spark Version:** 3.1.2 (Hadoop 3.2 binary distribution).
- **Spark Master URL:** `spark://spark-master:7077` (WebUI: `http://localhost:8080/`).
- **Worker Allocation:** 1 Worker registered with 1024 MB executor RAM.
- **Execution Test:** Distributed calculation of $\pi$ via Monte Carlo sampling (`SparkPi`).
- **Result:** **PASSED** (`Pi is roughly 3.141...` successfully calculated).

---

## 4. Acceptance Criteria & Readiness Sign-Off
All acceptance criteria for Phase 2 have been satisfied:
1. Docker Compose orchestrates the genuine Hadoop, HDFS, YARN, Hive, Pig, and Spark services.
2. No simulated or mocked metrics are used.
3. Persistent volumes preserve NameNode fsimage and PostgreSQL Hive catalog.
4. End-to-end connectivity across all 7 verification gates achieved **100% success**.

