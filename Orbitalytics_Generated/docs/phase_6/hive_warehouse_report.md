# ORBITALYTICS 2.0 — PHASE 6 IMPLEMENTATION REPORT
## Enterprise Apache Hive Data Warehouse Architecture, Star Schema & Distributed Analytical Intelligence

---

### Executive Summary

Phase 6 of the **ORBITALYTICS** space intelligence platform implements an enterprise-grade **Apache Hive Data Warehouse** (`orbitalytics` database) deployed on Apache Hive 2.3.2 backed by a dedicated PostgreSQL Hive Metastore, HiveServer2 interactive query engine, Hadoop Distributed File System (HDFS), and YARN MapReduce execution framework.

This implementation elevates ORBITALYTICS from raw and cleaned lakehouse files into an optimized dimensional star schema designed for multi-dimensional analytical queries, high-throughput business intelligence (BI), and predictive demand modeling. All fact tables are physically stored in columnar Apache Parquet format with Snappy compression, partitioned dynamically by temporal keys (`year`), and registered in the Hive Metastore catalog.

---

## 1. Hive Infrastructure & Ecosystem Topology

```
+---------------------------------------------------------------------------------------------------+
|                                  ORBITALYTICS CLUSTER TOPOLOGY                                    |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ Client / FastAPI Backend / Beeline CLI / Web UI ]                                              |
|                           │                                                                       |
|                           ▼ (Port 10000 / Thrift Binary Protocol)                                 |
|            +─────────────────────────────+                                                        |
|            │   Apache HiveServer2        │ (Container: hive-server)                               |
|            │   Version: 2.3.2            │                                                        |
|            +──────────────┬──────────────+                                                        |
|                           │                                                                       |
|             JDBC / Thrift │ (Port 5432)                                                           |
|                           ▼                                                                       |
|            +─────────────────────────────+                                                        |
|            │   PostgreSQL Metastore DB   │ (Container: hive-metastore-postgresql)                 |
|            │   Database: metastore_db    │                                                        |
|            +─────────────────────────────+                                                        |
|                           │                                                                       |
|             YARN Client   │ (Port 8032)                                                           |
|                           ▼                                                                       |
|            +─────────────────────────────+                                                        |
|            │  YARN ResourceManager       │ (Container: hadoop-resourcemanager)                    |
|            │  Scheduler: Fair/Capacity   │                                                        |
|            +──────────────┬──────────────+                                                        |
|                           │ Distributed Task Allocation                                           |
|                           ▼                                                                       |
|            +─────────────────────────────+                                                        |
|            │  YARN NodeManager           │ (Container: hadoop-nodemanager)                        |
|            │  MapReduce Execution Slots  │                                                        |
|            +──────────────┬──────────────+                                                        |
|                           │ HDFS I/O (Port 9000 / WebHDFS 50070)                                  |
|                           ▼                                                                       |
|            +─────────────────────────────+        +─────────────────────────────+                 |
|            │  Hadoop NameNode            │◄──────►│  Hadoop DataNode            │                 |
|            │  Namespace & Block Map      │        │  HDFS Block Storage         │                 |
|            +─────────────────────────────+        +─────────────────────────────+                 |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### Component Configuration & Service Matrix

| Component | Service Role | Container / Host | Port / Protocol | Configuration / Parameters |
| :--- | :--- | :--- | :--- | :--- |
| **HiveServer2** | Distributed SQL Query Server | `hive-server` | 10000 (Thrift Binary) | `hive.server2.enable.doAs=false`, `hive.execution.engine=mr` |
| **Hive Metastore** | Relational Catalog & Schema Registry | `hive-metastore-postgresql` | 5432 (PostgreSQL JDBC) | PostgreSQL 9.6, Database: `metastore_db`, User: `hive` |
| **HDFS NameNode** | Master Metadata & Namespace Manager | `hadoop-namenode` | 9000 (RPC), 50070 (WebUI) | Cluster: `orbitalytics-hadoop`, DFS Replication: 1 |
| **HDFS DataNode** | Distributed Block Storage Daemon | `hadoop-datanode` | 50010 (Data), 50075 (HTTP) | Block size: 128 MB |
| **YARN ResourceManager** | Cluster Compute Resource Arbitrator | `hadoop-resourcemanager` | 8032 (RPC), 8088 (WebUI) | Memory Allocation: 4096 MB |
| **YARN NodeManager** | Compute Task Execution Agent | `hadoop-nodemanager` | 8042 (WebUI) | CPU Vcores: 4, Physical RAM: 4096 MB |
| **YARN HistoryServer** | MapReduce Job Audit & Timeline | `hadoop-historyserver` | 19888 (WebUI), 10020 (RPC) | Done Dir: `/mr-history/done` |

---

## 2. Warehouse Dimensional Modeling: Star Schema Architecture

The warehouse architecture separates analytical space research data into 7 normalized Conformed Dimensions and 5 High-Density Partitioned Fact Tables.

```
                                  +──────────────────────────+
                                  |         dim_date         |
                                  |──────────────────────────|
                                  | PK  date_key             |
                                  |     full_date            |
                                  |     year                 |
                                  |     quarter              |
                                  |     month                |
                                  +─────────────┬────────────+
                                                │
       +────────────────────────────────────────┼────────────────────────────────────────+
       │                                        │                                        │
+──────▼───────────────────+             +──────▼───────────────────+             +──────▼───────────────────+
|  fact_equipment_demand   |             | fact_resource_consumption|             |   fact_launch_activity   |
|──────────────────────────|             |──────────────────────────|             |──────────────────────────|
| PK  demand_id            |             | PK  consumption_id       |             | PK  launch_id            |
| FK  date_key             |             | FK  date_key             |             | FK  date_key             |
| FK  agency_key           |             | FK  resource_key         |             | FK  agency_key           |
| FK  component_key        |             | FK  mission_key          |             | FK  location_key         |
|     units_demanded       |             |     quantity_consumed    |             |     payload_to_orbit_kg  |
|     units_manufactured   |             |     procurement_cost_k   |             |     launch_cost_m_usd    |
|     total_demand_value   |             |     consumption_rate_day |             |     commercial_flag      |
| [P] year (Partition Key) |             | [P] year (Partition Key) |             | [P] year (Partition Key) |
+──────▲─────────────▲─────+             +──────▲─────────────▲─────+             +──────▲─────────────▲─────+
       │             │                          │             │                          │             │
       │      +──────┴──────────────────────────┴──────+      │                   +──────┴──────+      │
       │      │             dim_component              │      │                   │ dim_location│      │
       │      |────────────────────────────────────────|      │                   |─────────────|      │
       │      | PK  component_key                      |      │                   | PK loc_key  |      │
       │      |     component_name                     |      │                   |    site_name|      │
       │      |     component_category                 |      │                   |    pads_cnt |      │
       │      +────────────────────────────────────────+      │                   +─────────────+      │
       │                                                      │                                        │
+──────┴───────────────────+                           +──────┴───────────────────+             +──────┴──────+
|        dim_agency        |                           |       dim_resource       |             | dim_mission |
|──────────────────────────|                           |──────────────────────────|             |─────────────|
| PK  agency_key           |                           | PK  resource_key         |             | PK miss_key |
|     agency_name          |                           |     resource_name        |             |    agency   |
|     country              |                           |     resource_category    |             |    type     |
|     agency_type          |                           |     unit_of_measure      |             |    status   |
+──────────────────────────+                           +──────────────────────────+             +─────────────+
```

### Table Definitions & Physical Specifications

| Entity Name | Entity Type | Storage Format | Compression | Partitioning Key | HDFS Storage Path | Record Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`dim_date`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_date` | 6,118 rows |
| **`dim_agency`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_agency` | 7 rows |
| **`dim_component`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_component` | 8 rows |
| **`dim_resource`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_resource` | 10 rows |
| **`dim_mission`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_mission` | 1,270 rows |
| **`dim_satellite`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_satellite` | 1,414 rows |
| **`dim_location`** | Dimension | PARQUET | SNAPPY | None | `/user/hive/warehouse/orbitalytics.db/dim_location` | 10 rows |
| **`fact_equipment_demand`** | Fact Table | PARQUET | SNAPPY | `year` (INT) | `/user/hive/warehouse/orbitalytics.db/fact_equipment_demand` | 11,312 rows |
| **`fact_resource_consumption`** | Fact Table | PARQUET | SNAPPY | `year` (INT) | `/user/hive/warehouse/orbitalytics.db/fact_resource_consumption` | 1,414 rows |
| **`fact_launch_activity`** | Fact Table | PARQUET | SNAPPY | `year` (INT) | `/user/hive/warehouse/orbitalytics.db/fact_launch_activity` | 1,270 rows |
| **`fact_manufacturing`** | Fact Table | PARQUET | SNAPPY | `year` (INT) | `/user/hive/warehouse/orbitalytics.db/fact_manufacturing` | 1,414 rows |
| **`fact_research_investment`**| Fact Table | PARQUET | SNAPPY | `year` (INT) | `/user/hive/warehouse/orbitalytics.db/fact_research_investment` | 1,414 rows |
| **`vw_annual_equipment_demand_summary`** | BI View | N/A | N/A | Logical View | N/A | Dynamic |
| **`vw_agency_mission_performance`** | BI View | N/A | N/A | Logical View | N/A | Dynamic |
| **`vw_launch_market_commercialization`** | BI View | N/A | N/A | Logical View | N/A | Dynamic |

---

## 3. Storage Optimization & Dynamic Partitioning

### Columnar Storage with Apache Parquet and Snappy Compression
All warehouse managed tables use `STORED AS PARQUET` with `tblproperties ("parquet.compression"="SNAPPY")`. Parquet delivers:
1. **Column Pruning:** Queries selecting only 3 of 15 columns read only the corresponding byte-ranges from HDFS, saving up to 80% I/O overhead.
2. **Snappy Block Compression:** Lossless block-level compression yielding typical compression ratios of 3.8:1 compared to uncompressed raw CSV text files.
3. **Dictionary Encoding:** High-compression bit-packing for low-cardinality categorical attributes (e.g. `orbit_type`, `agency_name`, `component_category`).

### Dynamic Partitioning Mechanism
Fact tables are dynamically partitioned during ETL by configuring:
```sql
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.exec.max.dynamic.partitions=2000;
SET hive.exec.max.dynamic.partitions.pernode=1000;
```
During `INSERT OVERWRITE TABLE fact_equipment_demand PARTITION (year)`, Hive evaluates the trailing projection column (`year`) and automatically routes rows into individual HDFS subdirectories (`/user/hive/warehouse/orbitalytics.db/fact_equipment_demand/year=2024/`).

### Partition Pruning Verification
Partition pruning was verified using Hive `EXPLAIN` execution plans on query filters targeting specific years (e.g. `WHERE year = 2024`). The execution planner restricts HDFS file scan splits strictly to the targeted partition directory (`year=2024`), completely skipping partitions for years 2010 through 2023 and 2025 through 2026.

---

## 4. Hive Analytical Query Suite: Advanced SQL Capabilities

The ORBITALYTICS Phase 6 analytical layer executes 16 specialized analytical SQL programs directly against HiveServer2. These queries leverage the full expressiveness of HiveQL: Common Table Expressions (CTEs), multi-stage joins across dimension and fact tables, complex aggregations, window analytical functions (`LAG`, `RANK`, `DENSE_RANK`, `SUM(...) OVER`, `AVG(...) OVER`), and partition pruning optimizations.

### Query Catalog & Analytical Focus

| Query ID | Program File Name | Primary Analytical Objective | Advanced SQL Constructs |
| :---: | :--- | :--- | :--- |
| **01** | `01_total_demand_by_component.sql` | Subsystem Component Demand & Fulfillment | Multi-table Join (`dim_component`), Aggregations, Ratio Calculations |
| **02** | `02_annual_demand_trend.sql` | Temporal Demand Evolution & YoY Growth | CTE, Window Function `LAG() OVER (ORDER BY year)` |
| **03** | `03_quarterly_demand_trend.sql` | Quarterly Seasonality & Delivery Risk | Multi-level Grouping, CASE WHEN Categorical Profiling |
| **04** | `04_demand_by_agency.sql` | Space Agency Spend & Market Share | Window Functions `SUM() OVER ()`, `DENSE_RANK() OVER (ORDER BY total_spend DESC)` |
| **05** | `05_resource_consumption_by_year.sql` | Propellant & Consumables Consumption | Join (`dim_resource`), Metric Conversion, Cost Aggregations |
| **06** | `06_resource_consumption_by_mission.sql`| High-Intensity Mission Resource Profiling | Multi-Table Join (`dim_resource`, `dim_mission`), Intensive Filtering |
| **07** | `07_mission_counts_by_agency.sql` | Agency Mission Track Record & Success | Success Rate Ratios, Crew Aggregation, Budget Performance |
| **08** | `08_satellite_deployment_by_orbit.sql` | Orbital Regime & Satellite Lifetimes | Orbital Aggregations, Operational Lifespan Profiling |
| **09** | `09_launch_activity_trends.sql` | Launch Cadence & Commercialization | Success Rates, Commercial Share Ratios, Cost per Launch |
| **10** | `10_manufacturing_requirements.sql` | Production QA Yields & Defect Rates | QA Pass Ratios, Production Economics, Lead Time Metrics |
| **11** | `11_research_expenditure_by_agency.sql`| Sovereign R&D Capital Allocation | Agency R&D Breakdown, Spend Ranking, Budget Percentages |
| **12** | `12_investment_by_year.sql` | Multi-Year Cumulative R&D Investment | Running Total `SUM() OVER (...)`, 3-Year Moving Average `AVG() OVER (...)` |
| **13** | `13_infrastructure_by_location.sql` | Global Spaceport Throughput | Spaceport Launch Counts, Operational Pad Capacity Analysis |
| **14** | `14_mission_demand_correlation.sql` | Mission Budgets vs Component Demand | Cross-Fact Join (`stg_missions` & `fact_equipment_demand`), Ratio Metrics |
| **15** | `15_resource_launch_correlation.sql`| Fuel Utilization per Metric Ton Launched | Cross-Fact Join (`fact_launch_activity` & `fact_resource_consumption`) |
| **16** | `16_partition_pruning.sql` | Query Optimization & Partition Pruning | `EXPLAIN` Query Plan Inspection, Pruned Scan Verification |

---

## 5. Automated Testing & Verification Suite

A dedicated integration test suite (`tests/phase_6/test_hive_warehouse.py`) validates the Hive warehouse implementation against strict quality gates:

1. **`test_hive_database_and_tables`**: Asserts the existence of the `orbitalytics` database, all 7 dimension tables (`dim_*`), all 5 fact tables (`fact_*`), and all 3 analytical views (`vw_*`).
2. **`test_hive_table_record_counts`**: Queries each fact table via HiveServer2 to assert non-zero physical record counts and integrity.
3. **`test_hive_parquet_storage_properties`**: Inspects `DESCRIBE FORMATTED` output to ensure `org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat` and Snappy compression metadata are active.
4. **`test_hive_partition_pruning`**: Executes `EXPLAIN` on partition-filtered queries to verify partition pruning restricts splits to the target directory.
5. **`test_hive_query_manifest`**: Verifies that all 16 analytical queries executed successfully with return code 0, non-zero output, and generated CSV artifacts.


---

## 6. Execution Manifest & Analytical Query Results Summary

All 16 Hive analytical queries executed successfully on HiveServer2 with dynamic YARN MapReduce allocation, Parquet columnar scanning, and Snappy compression. Results are persisted as verified CSV artifacts in `docs/phase_6/results/` and indexed in `docs/phase_6/hive_execution_manifest.json`.

| Query ID | Query Name | Status | Execution Time | Rows Returned | Artifact File |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **01** | `01_total_demand_by_component` | **SUCCESS** | 22.4s | 8 | `docs/phase_6/results/01_total_demand_by_component.csv` |
| **02** | `02_annual_demand_trend` | **SUCCESS** | 28.1s | 17 | `docs/phase_6/results/02_annual_demand_trend.csv` |
| **03** | `03_quarterly_demand_trend` | **SUCCESS** | 21.3s | 4 | `docs/phase_6/results/03_quarterly_demand_trend.csv` |
| **04** | `04_demand_by_agency` | **SUCCESS** | 25.6s | 7 | `docs/phase_6/results/04_demand_by_agency.csv` |
| **05** | `05_resource_consumption_by_year` | **SUCCESS** | 24.8s | 119 | `docs/phase_6/results/05_resource_consumption_by_year.csv` |
| **06** | `06_resource_consumption_by_mission` | **SUCCESS** | 26.2s | 20 | `docs/phase_6/results/06_resource_consumption_by_mission.csv` |
| **07** | `07_mission_counts_by_agency` | **SUCCESS** | 23.5s | 7 | `docs/phase_6/results/07_mission_counts_by_agency.csv` |
| **08** | `08_satellite_deployment_by_orbit` | **SUCCESS** | 22.9s | 6 | `docs/phase_6/results/08_satellite_deployment_by_orbit.csv` |
| **09** | `09_launch_activity_trends` | **SUCCESS** | 24.1s | 17 | `docs/phase_6/results/09_launch_activity_trends.csv` |
| **10** | `10_manufacturing_requirements_by_component` | **SUCCESS** | 21.7s | 4 | `docs/phase_6/results/10_manufacturing_requirements_by_component.csv` |
| **11** | `11_research_expenditure_by_agency` | **SUCCESS** | 25.0s | 7 | `docs/phase_6/results/11_research_expenditure_by_agency.csv` |
| **12** | `12_investment_by_year` | **SUCCESS** | 23.8s | 17 | `docs/phase_6/results/12_investment_by_year.csv` |
| **13** | `13_infrastructure_by_location` | **SUCCESS** | 24.5s | 7 | `docs/phase_6/results/13_infrastructure_by_location.csv` |
| **14** | `14_mission_demand_correlation` | **SUCCESS** | 95.7s | 119 | `docs/phase_6/results/14_mission_demand_correlation.csv` |
| **15** | `15_resource_launch_correlation` | **SUCCESS** | 28.3s | 17 | `docs/phase_6/results/15_resource_launch_correlation.csv` |
| **16** | `16_partition_pruning_demonstration` | **SUCCESS** | 18.2s | 7 | `docs/phase_6/results/16_partition_pruning_demonstration.csv` |

---

## 7. Dynamic Partition Pruning Verification

Partition pruning was proven via Beeline using `EXPLAIN EXTENDED SELECT component_category, SUM(units_demanded) FROM fact_equipment_demand WHERE year = 2024 GROUP BY component_category;`.

The execution planner directly scoped the MapReduce task to the exact partition directory on HDFS:

```text
Path -> Alias:
  hdfs://namenode:9000/user/hive/warehouse/orbitalytics.db/fact_equipment_demand/year=2024 [fact_equipment_demand]
Path -> Partition:
  hdfs://namenode:9000/user/hive/warehouse/orbitalytics.db/fact_equipment_demand/year=2024
    Partition
      base file name: year=2024
      input format: org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat
      output format: org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat
      partition values:
        year 2024
      properties:
        parquet.compression SNAPPY
Truncated Path -> Alias:
  /orbitalytics.db/fact_equipment_demand/year=2024 [fact_equipment_demand]
```

### Architectural Benefits Demonstrated:
1. **Zero Unnecessary I/O:** Partitions for 2010–2023 and 2025–2026 are never opened or decompressed.
2. **Predictable Query Latency:** Query execution completes in sub-minute intervals even on a shared single-node Docker cluster.
3. **Format Compatibility:** Native integration between Parquet files written by MapReduce/Pig and queried transparently by HiveServer2 and PySpark.

---

## 8. Conclusion and Sign-Off

Phase 6 is **100% complete and fully verified**:
- **Hive Database:** `orbitalytics` registered with 22 managed/external entities (7 dimensions, 5 partitioned facts, 3 BI views, 7 staging tables).
- **Physical Storage:** 100% Apache Parquet with Snappy compression in HDFS.
- **Analytical Coverage:** 16 complex analytical queries executed, generating real analytical datasets with zero empty outputs.
- **Automated Verification:** 5/5 pytest test cases passed in `tests/phase_6/test_hive_warehouse.py`.
