# ORBITALYTICS 2.0 — HDFS Architecture & Lakehouse Storage Specification

---

## 1. Storage Architecture Overview

ORBITALYTICS 2.0 employs **Hadoop Distributed File System (HDFS)** as the scalable, fault-tolerant persistence backbone for space research big data. In compliance with the enterprise Lakehouse paradigm, data progresses through tiered storage zones representing increasing levels of data purity, schema validation, and optimization for distributed queries.

```
HDFS Root: /space_research/
│
├── raw/                  [Bronze Unstructured / CSV Landing]
│   └── *.csv             (9 raw datasets, immutable, original source dumps)
│
├── bronze/               [Bronze Governed]
│   └── *.csv             (Verified header schemas, standardized nulls, UTF-8 clean)
│
├── silver/               [Silver Columnar Parquet / Partitioned]
│   ├── equipment_component_demand/year=2010..2026/*.parquet
│   ├── space_missions/year=2010..2026/*.parquet
│   ├── launch_activities/year=2010..2026/*.parquet
│   ├── resource_consumption/year=2010..2026/*.parquet
│   ├── satellites_orbital/launch_year=2010..2026/*.parquet
│   ├── agency_research_expenditures/year=2010..2026/*.parquet
│   └── space_infrastructure_requirements/year=2010..2026/*.parquet
│
├── gold/                 [Gold Star-Schema Data Warehouse]
│   ├── dim_agency/*.parquet
│   ├── dim_component/*.parquet
│   ├── dim_resource/*.parquet
│   ├── dim_date/*.parquet
│   ├── dim_mission/*.parquet
│   ├── dim_satellite/*.parquet
│   ├── fact_equipment_demand/*.parquet
│   ├── fact_resource_consumption/*.parquet
│   ├── fact_launch_activity/*.parquet
│   ├── fact_manufacturing/*.parquet
│   └── fact_research_investment/*.parquet
│
├── curated/              [Pre-Aggregated PySpark Analytics & Joins]
│   └── *.parquet         (Consolidated multi-dataset join views)
│
├── forecasts/            [Predictive Projections]
│   └── *.json, *.parquet (13-model backtesting logs & multi-horizon forecast envelopes)
│
└── warehouse/            [Hive Managed Tables]
    └── *.db / *.table    (Internal ACID Hive warehouse storage)
```

---

## 2. Block Storage & Replication Policies

- **Default Block Size:** `134,217,728 bytes` (128 MB). Space telemetry files smaller than 128 MB occupy a single block. In the multi-terabyte synthetic benchmarking scale, records span dozens to hundreds of discrete 128 MB blocks.
- **Replication Factor:** Set to `1` in the containerized development environment to conserve host memory; dynamically configured to `3` in production cluster profiles via `hdfs-site.xml`.
- **Rack Awareness:** Supported via `net.topology.script.file.name` to isolate primary and secondary replicas across different availability zones or compute racks.

---

## 3. Partitioning Strategy

Fact datasets are partitioned primarily by Calendar Year:
```
/space_research/silver/equipment_component_demand/year=2024/baf6c5a070ca4d678274678469ee2396-0.parquet
```
**Benefits:**
- **Zero-Scan Overhead:** Queries filtering on `year = 2024` prune all non-relevant year directories entirely at the NameNode metadata level, avoiding reading 94% of the raw data lake.
- **Parallel Ingestion:** Distributed Pig and Spark workers write directly into independent partition paths without lock contention.
- **Hive Metastore Compatibility:** Partitions conform to Hive's automatic partition discovery standard (`MSCK REPAIR TABLE`).

---

## 4. Checksums & Verification Commands

All files uploaded to HDFS are indexed with both MD5 and SHA-256 signatures:
```bash
# Verify HDFS directory structure and block allocations
docker exec -it hadoop-namenode hdfs fsck /space_research -files -blocks -locations

# Calculate HDFS storage footprint
docker exec -it hadoop-namenode hdfs dfs -du -h /space_research
```
