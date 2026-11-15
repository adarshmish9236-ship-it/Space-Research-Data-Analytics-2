# Orbitalytics Phase 2: Distributed Service Configuration & Tuning Guide

## 1. Overview
Hadoop ecosystem components are configured through declarative XML descriptor files and container environment variables. This document explains the exact technical rationale behind each parameter configured for Phase 2.

---

## 2. Distributed Filesystem Configuration (`hdfs-site.xml` & `core-site.xml`)

### 1. `dfs.replication = 1` vs `dfs.replication = 3`
- **Development Configuration (`dfs.replication = 1`):**
  In a single-DataNode development cluster, setting the replication factor to 3 causes the NameNode block replication monitor to continuously report `UNDER-REPLICATED BLOCKS: 100%`, because physical blocks cannot be placed on 3 distinct machines. To maintain clean health metrics and eliminate false-positive error logs, `dfs.replication` is configured to `1`.
- **Enterprise Multi-Node Production (`dfs.replication = 3`):**
  In multi-rack enterprise clusters (AWS/GCP), `dfs.replication` is set to `3`. The NameNode block placement policy writes Replica 1 on the local node, Replica 2 on a different node in the same rack, and Replica 3 on a node in an entirely separate rack to survive rack-level power failures.

### 2. Block Size: `dfs.blocksize = 134217728` (128 MB)
Standard Hadoop default of 128 MB per block split. This is optimal for columnar Apache Parquet files, minimizing metadata pressure on the NameNode RAM while providing large sequential read throughput for MapReduce mappers and Spark partitions.

### 3. Buffer Size: `io.file.buffer.size = 131072` (128 KB)
Increased from the 4 KB default to 128 KB to optimize network streaming between Python/PySpark clients and HDFS DataNodes over WebHDFS.

---

## 3. YARN Resource Management Configuration (`yarn-site.xml`)

### 1. NodeManager Memory Pool: `yarn.nodemanager.resource.memory-mb = 4096`
Allocates a 4,096 MB physical container pool to the NodeManager. This ensures sufficient capacity to concurrently host:
- 1 ApplicationMaster container (512 MB)
- Up to 4 MapReduce Mapper tasks (512 MB each)
- Up to 2 MapReduce Reducer tasks (512 MB each)

### 2. Auxiliary Services: `yarn.nodemanager.aux-services = mapreduce_shuffle`
Enforces the MapReduce Shuffle auxiliary handler on the NodeManager, allowing Reducers to pull partitioned map output over HTTP without external socket proxies.

---

## 4. MapReduce Workload Configuration (`mapred-site.xml`)

### 1. Framework Delegation: `mapreduce.framework.name = yarn`
Directs the Hadoop MapReduce job client to submit all job jars to YARN rather than running in local JVM mode.

### 2. Container Memory Bounds:
- `yarn.app.mapreduce.am.resource.mb = 512`
- `mapreduce.map.memory.mb = 512`
- `mapreduce.reduce.memory.mb = 512`

---

## 5. Apache Hive & Metastore Configuration (`hive-site.xml`)

### 1. Warehouse HDFS Root: `hive.metastore.warehouse.dir = hdfs://namenode:9000/user/hive/warehouse`
Enforces that all Hive managed tables and external Parquet tables are physically stored within the HDFS distributed filesystem, rather than local container storage.

### 2. External Relational Catalog:
- `javax.jdo.option.ConnectionURL = jdbc:postgresql://hive-metastore-postgresql:5432/metastore`
- `javax.jdo.option.ConnectionDriverName = org.postgresql.Driver`
- `javax.jdo.option.ConnectionUserName = hive`
- `javax.jdo.option.ConnectionPassword = hive`

Eliminates embedded Derby concurrency locks, allowing HiveServer2, Beeline, and PySpark to concurrently query the catalog schema.

