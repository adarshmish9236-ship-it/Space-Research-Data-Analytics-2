# ORBITALYTICS — PHASE 6: APACHE HIVE DATA WAREHOUSE ARCHITECTURE & DESIGN SPECIFICATION

## 1. Executive Summary

This architecture specification details the enterprise data warehouse design and implementation for **ORBITALYTICS: Space Research Data Analytics: A Hadoop Ecosystem Approach to Demand Forecasting**.

The warehouse is built on **Apache Hive 2.3.2** powered by **Hive Metastore (PostgreSQL)**, **HiveServer2**, and **HDFS distributed storage** (`/user/hive/warehouse/orbitalytics.db`). It transforms validated HDFS Silver lakehouse datasets into an analytical Star Schema with Parquet storage, Snappy compression, dynamic year-based partitioning, and analytical business views.

---

## 2. Dimensional Data Warehouse Architecture

```
+----------------------------------------------------------------------------------------------------+
|                                    HDFS SILVER LAKEHOUSE STORAGE                                   |
|   (/orbitalytics/silver/pig_equipment_demand, pig_missions, pig_satellites, pig_launches, etc.)   |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                      EXTERNAL STAGING LAYER                                        |
|   stg_equipment_demand, stg_resource_consumption, stg_launches, stg_missions, stg_satellites, etc. |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                 ORBITALYTICS DATA WAREHOUSE                                        |
|                                                                                                    |
|   +-----------------------+   +----------------------+   +-----------------------+                 |
|   |       DIMENSIONS      |   |   PARTITIONED FACTS  |   |    ANALYTICAL VIEWS   |                 |
|   +-----------------------+   +----------------------+   +-----------------------+                 |
|   | * dim_date            |   | * fact_equipment_    |   | * vw_annual_equipment_|                 |
|   | * dim_agency          |   |   demand (by year)   |   |   demand_summary      |                 |
|   | * dim_component       |   | * fact_resource_     |   | * vw_agency_mission_  |                 |
|   | * dim_resource        |   |   consumption (year) |   |   performance         |                 |
|   | * dim_mission         |   | * fact_launch_       |   | * vw_launch_market_   |                 |
|   | * dim_satellite       |   |   activity (year)    |   |   commercialization   |                 |
|   | * dim_location        |   | * fact_manufacturing |   +-----------------------+                 |
|   +-----------------------+   |   (delivery_year)    |                                             |
|                               | * fact_research_     |                                             |
|                               |   investment (year)  |                                             |
|                               +----------------------+                                             |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                  ANALYTICAL SQL SERVING TIER                                       |
|  - 16 Optimized Analytical Queries (CTEs, Window Functions, Partition Pruning, Joins)             |
|  - HiveServer2 Thrift Service (Port 10000)                                                         |
|  - FastAPI Backend Service Integration (backend/app/services/hive_service.py)                     |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Warehouse Schema Design

### 3.1 Dimension Tables (Stored as Parquet + Snappy)

1. **`dim_date`**: Calendar date attributes, quarters (Q1-Q4), months, day names, weekend flags for chronological trending and seasonal demand profiling.
2. **`dim_agency`**: Space agency registry, headquarters country, operator tier (National Space Agency, Commercial Operator, Intergovernmental Consortium).
3. **`dim_component`**: Catalog of aerospace components (SAR Antennas, Rad-750 Single Board Computers, Ion Thrusters, Solar Panels), subsystem categories, and standard lead times.
4. **`dim_resource`**: Consumable resources (LOX, RP-1 Kerosene, Liquid Hydrogen, Xenon Propellant, Alloys), categories, and handling hazard tiers.
5. **`dim_mission`**: Mission metadata, mission objectives (Science, Communications, Exploration), operational status, crew size, and mission duration.
6. **`dim_satellite`**: Satellite catalog, orbital regimes (LEO, GEO, MEO, SSO, Lagrange Points, Deep Space/Lunar), altitude, inclination, dry mass, and power consumption.
7. **`dim_location`**: Geographic spaceport facilities, host countries, coordinates, and civil/military launch range classification.

### 3.2 Partitioned Fact Tables (Parquet + Snappy, Partitioned by Year)

1. **`fact_equipment_demand`**:
   - Granularity: One row per equipment component procurement order / demand allocation.
   - Partition Key: `year INT` (2010 through 2026).
   - Metrics: `units_demanded`, `units_manufactured`, `units_procured`, `avg_unit_cost_k_usd`, `total_demand_value_m_usd`, `lead_time_days`.
2. **`fact_resource_consumption`**:
   - Granularity: One row per consumable propellant or raw material consumption event.
   - Partition Key: `year INT`.
   - Metrics: `quantity_consumed`, `procurement_cost_k_usd`.
3. **`fact_launch_activity`**:
   - Granularity: One row per orbital launch attempt.
   - Partition Key: `year INT`.
   - Metrics: `launch_cost_m_usd`, `payload_to_orbit_kg`, commercial indicator, outcome success indicator.
4. **`fact_manufacturing`**:
   - Granularity: One row per spacecraft manufacturing order.
   - Partition Key: `delivery_year INT`.
   - Metrics: `units_ordered`, `cleanroom_hours_required`, `contract_value_m_usd`, QA testing pass flag.
5. **`fact_research_investment`**:
   - Granularity: One row per monthly agency expenditure report.
   - Partition Key: `year INT`.
   - Metrics: `rd_expenditure_m_usd`, `infrastructure_expenditure_m_usd`, `mission_operations_m_usd`, `total_monthly_expenditure_m_usd`.

---

## 4. Partitioning Strategy & Pruning Optimization

### 4.1 Anti-Over-Partitioning Principle
Over-partitioning causes the **HDFS Small File Problem**, degrading NameNode heap efficiency and causing high Map task scheduling overhead.
- High-cardinality columns (e.g. `date`, `mission_id`, `component_id`) are **never** used as partition keys.
- `year INT` provides an optimal granularity: 17 uniform partitions spanning 2010 to 2026, with tens of thousands of records cleanly partitioned without fragmentation.

### 4.2 Partition Pruning Mechanics
When an analytical query specifies a partition predicate such as `WHERE year = 2024`:
1. The Hive Metastore evaluates the predicate during query compilation.
2. The Query Planner prunes all partition directories other than `year=2024`.
3. InputFormat only constructs splits for `/user/hive/warehouse/orbitalytics.db/fact_equipment_demand/year=2024/*.parquet`.
4. Up to **94.1% of HDFS data blocks are completely skipped**, cutting query execution time and cluster I/O dramatically.

---

## 5. Storage & Format Efficiency: Parquet vs Text

| Dimension | Raw Text / CSV | Hive Parquet + Snappy | Improvement |
| :--- | :--- | :--- | :--- |
| **Storage Layout** | Row-oriented | Columnar with dictionary encoding | Selective column scanning |
| **Compression** | Uncompressed text | Snappy block compression | **~75% disk space reduction** |
| **Projection Pushdown** | Reads all columns from disk | Only reads requested columns | **Up to 85% I/O reduction** |
| **Type Safety** | Implicit string parsing | Native binary typed encodings | Zero parsing failures |
| **Statistics** | None | Column min/max in metadata | Automatic block skipping |

