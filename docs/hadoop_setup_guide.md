# ORBITALYTICS 2.0 — Hadoop Ecosystem Setup & Operational Guide

---

## 1. Overview

ORBITALYTICS 2.0 integrates a multi-service Apache Hadoop cluster running via container orchestration. The services work in harmony to support distributed data lake storage (HDFS), distributed resource scheduling (YARN), streaming batch processing (MapReduce), declarative data transformation (Pig), SQL data warehousing (Hive), and in-memory analytics (Spark).

---

## 2. Service Architecture & Configuration

### 2.1 HDFS NameNode & DataNode
- **Base Image:** `bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8` / `hadoop-datanode`
- **Cluster ID:** `CID-orbitalytics-cluster-v2`
- **Block Size:** 134,217,728 bytes (128 MB)
- **Replication Factor:** 1 (single-node development container) / configurable to 3 in multi-node production.
- **FSImage & EditLog Directory:** `/hadoop/dfs/name` and `/hadoop/dfs/data`

```xml
<!-- core-site.xml -->
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop-namenode:9000</value>
    </property>
</configuration>
```

```xml
<!-- hdfs-site.xml -->
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.blocksize</name>
        <value>134217728</value>
    </property>
</configuration>
```

### 2.2 YARN ResourceManager & NodeManager
- **ResourceManager Web UI:** `http://localhost:8088`
- **Scheduler:** CapacityScheduler with queues `default` (100% capacity) and strict preemption limits.
- **NodeManager Memory:** 8,192 MB allocated memory; 4 virtual cores (vCores).
- **NodeManager vmem ratio:** 2.1

```xml
<!-- yarn-site.xml -->
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop-resourcemanager</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
    </property>
</configuration>
```

### 2.3 Apache Hive & Hive Metastore
- **Hive Version:** 2.3.2 / 3.1.2
- **Metastore Database:** PostgreSQL 13 (`hive-metastore-postgresql`)
- **Connection JDBC:** `jdbc:postgresql://hive-metastore-postgresql:5432/metastore`
- **HiveServer2 Thrift Port:** 10000
- **Beeline CLI invocation:**
```bash
docker exec -it hive-server beeline -u "jdbc:hive2://localhost:10000/orbitalytics_dw" -n root
```

### 2.4 Apache Spark Master & Worker
- **Spark Version:** 3.1.2 / 3.2.1
- **Master URL:** `spark://spark-master:7077`
- **Web UI:** `http://localhost:8080`
- **Worker Web UI:** `http://localhost:8081`
- **Worker Cores:** 2 cores
- **Worker Memory:** 2 GB heap

---

## 3. Storage Directory Layout

The HDFS file system maintains the canonical directory tree:
```
hdfs://hadoop-namenode:9000/space_research/
├── raw/                         <- Immutable Bronze CSV dumps
├── bronze/                      <- Validated, schema-checked CSVs
├── silver/                      <- Partitioned Parquet (year=YYYY)
│   ├── equipment_component_demand/
│   ├── space_missions/
│   ├── launch_activities/
│   ├── resource_consumption/
│   └── satellites_orbital/
├── gold/                        <- Star-schema Hive dimension and fact tables
├── curated/                     <- PySpark joined and aggregated tables
├── forecasts/                   <- Model backtesting results and multi-horizon predictions
└── warehouse/                   <- Hive managed warehouse directory
```

---

## 4. Maintenance Commands & Health Diagnostics

### 4.1 Checking HDFS Health & Block Reports
```bash
docker exec -it hadoop-namenode hdfs dfsadmin -report
```

### 4.2 Inspecting HDFS Directory Contents
```bash
docker exec -it hadoop-namenode hdfs dfs -ls -R /space_research
```

### 4.3 Monitoring YARN Applications
```bash
docker exec -it hadoop-resourcemanager yarn application -list
```

### 4.4 Checking Docker Container Logs
```bash
docker logs --tail 100 hadoop-namenode
docker logs --tail 100 hive-server
docker logs --tail 100 spark-master
```
