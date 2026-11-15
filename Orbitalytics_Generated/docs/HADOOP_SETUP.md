# Orbitalytics: Hadoop Ecosystem Setup Guide

Comprehensive setup and deployment documentation for the Hadoop Big Data stack (HDFS, Hive, YARN, MapReduce, PySpark).

---

## 1. Architecture Overview

Orbitalytics integrates the Apache Hadoop Big Data ecosystem to demonstrate practical distributed storage, data warehousing, and batch processing:

- **HDFS (Hadoop Distributed File System):** Manages multi-tiered lakehouse storage under `/space_research/` with standard 128 MB blocks and 3x replication factor.
- **Apache Hive 3.1.2:** Provides metastore cataloging, partition pruning, and structured SQL analytical querying against Parquet external tables.
- **Hadoop Streaming MapReduce:** Executes Python mappers and reducers on YARN, handling mapper line splitting, distributed shuffle-sort, and reducer group aggregation.
- **Apache Spark / PySpark 3.5.3:** High-performance distributed data cleaning, null median imputation, schema validation, and Snappy Parquet conversion.

---

## 2. Docker Compose Deployment (Optional Distributed Multi-Node Cluster)

For environments with Docker and Docker Compose installed:

```bash
cd Orbitalytics_Generated/hadoop_ecosystem
docker-compose up -d
```

### Cluster Services & Ports

| Service Daemon | Container Name | Port Mapping | Functionality |
| :--- | :--- | :--- | :--- |
| **NameNode** | `orbitalytics-namenode` | `9870`, `9000` | HDFS Master, Web UI, RPC Filesystem |
| **DataNode** | `orbitalytics-datanode` | `9864` | HDFS Block Storage & Replication |
| **ResourceManager** | `orbitalytics-resourcemanager` | `8088` | YARN Cluster Resource Allocation |
| **NodeManager** | `orbitalytics-nodemanager` | `8042` | YARN Task Execution Containers |
| **Hive Server 2** | `orbitalytics-hive-server` | `10000`, `10002` | Hive Thrift Server & SQL Query Engine |

### Checking Cluster Status
```bash
docker-compose ps
```

### Stopping the Cluster
```bash
docker-compose down
```

---

## 3. Local High-Performance Lakehouse Engine (No Docker Required)

If Docker is not installed or unavailable, Orbitalytics automatically uses its local high-performance lakehouse engine:
- HDFS zones are mirrored under `hadoop_ecosystem/hdfs/space_research/`.
- Hive SQL analytical queries execute directly against partitioned Parquet datasets using PyArrow predicate pushdown.
- MapReduce jobs execute via Python subprocess streaming pipes (`mapper.py | sort | reducer.py`) simulating YARN shuffle-sort with 100% fidelity.
- The web interface transparently indicates:
  `Environment Mode: Local High-Performance Lakehouse Engine (Docker Cluster Optional)`

