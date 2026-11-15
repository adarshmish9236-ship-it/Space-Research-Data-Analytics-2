# ORBITALYTICS — PHASE 4: APACHE PIG ETL IMPLEMENTATION & LAKEHOUSE ARCHITECTURE

## 1. Executive Summary & Architecture Overview

Phase 4 of **ORBITALYTICS: Space Research Data Analytics** implements enterprise-grade, distributed Extract-Transform-Load (ETL) pipelines using **Apache Pig Latin (v0.17.0)** running natively on Hadoop MapReduce and Apache YARN.

The Pig ETL layer transforms raw, immutable data lake assets in the **Bronze Lakehouse (`/orbitalytics/bronze/`)** into cleansed, strongly validated, and standardized records in the **Silver Lakehouse (`/orbitalytics/silver/pig_{domain}/`)**, while simultaneously generating pre-aggregated analytics marts in the **Gold Lakehouse (`/orbitalytics/gold/pig_{analytics}/`)**. Any records that fail schema, domain, or integrity checks are routed to **Quarantine (`/orbitalytics/quarantine/pig_{domain}_rejected/`)** with explanatory diagnostic rejection codes.

```
       +-------------------------------------------------------+
       |             ORBITALYTICS BRONZE LAKEHOUSE             |
       |     Raw CSV Ingestion Files (/orbitalytics/bronze/)   |
       +-------------------------------------------------------+
                                  |
                                  |  (Apache Pig LOAD via PigStorage)
                                  v
+-------------------------------------------------------------------------+
|                  APACHE PIG LATIN ETL PROCESSING ENGINE                 |
|                                                                         |
|  1. Ingestion & Header Pruning    : LOAD, FILTER != 'header'            |
|  2. Deduplication                 : DISTINCT key                        |
|  3. Data Validation & Splitting   : FILTER (valid vs invalid criteria)  |
|  4. Silver Projection & Casting   : FOREACH ... GENERATE (typed fields) |
|  5. Deterministic Ordering        : ORDER BY (temporal / agency / class)|
|  6. Business Aggregations         : GROUP BY, SUM, COUNT, AVG, FLATTEN  |
|  7. Distributed Multi-Store       : STORE silver, quarantine, gold marts|
+-------------------------------------------------------------------------+
       |                                |                            |
       | (Clean Silver Records)         | (Rejection Reasons)        | (Pre-computed Aggregations)
       v                                v                            v
+-----------------------------+ +----------------------------+ +-----------------------------+
|   SILVER LAKEHOUSE          | |   QUARANTINE VAULT         | |    GOLD ANALYTICS MARTS     |
| /orbitalytics/silver/pig_*  | | /orbitalytics/quarantine/  | | /orbitalytics/gold/pig_*    |
+-----------------------------+ +----------------------------+ +-----------------------------+
```

---

## 2. Environment & Engine Configuration

| Configuration Parameter | Value | Description |
| :--- | :--- | :--- |
| **Apache Pig Version** | `0.17.0 (r1797386)` | Installed in `/opt/pig-0.17.0` |
| **Hadoop Version** | `Apache Hadoop 3.2.1` | Native cluster orchestrating NameNode & DataNode |
| **Execution Engine** | `MapReduce (YARN)` | Pig executes with `ExecType: MAPREDUCE` |
| **YARN ResourceManager** | `resourcemanager:8032` | Distributed cluster resource scheduling |
| **JobHistory Server** | `historyserver:10020` | MapReduce job history and counters delegate |
| **Input Protocol** | `hdfs://namenode:9000/orbitalytics/bronze/` | Distributed raw data storage |
| **Output Protocol** | `hdfs://namenode:9000/orbitalytics/{silver,quarantine,gold}/` | Distributed data lake layers |

---

## 3. Pig Latin Pipeline Specification Matrix (9 Domains)

All nine core operational and research domains have dedicated, independently reproducible Pig scripts:

### Domain 1: Space Missions (`01_missions_etl.pig`)
- **Input:** `/orbitalytics/bronze/missions/space_missions.csv` (1,500 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `mission_id` is NOT NULL and non-empty
  - `agency_name` is NOT NULL and non-empty
  - `budget_million_usd > 0.0`
  - `1957 <= year <= 2035`
- **Quarantine Tag:** `INVALID_BUDGET_OR_NULL_AGENCY_OR_BAD_YEAR`
- **Business Transformations:**
  - Aggregation 1: Cumulative & average budget, mission counts, and duration by agency.
  - Aggregation 2: Temporal mission count and investment volume by year and mission type.

### Domain 2: Satellites & Orbital Catalog (`02_satellites_etl.pig`)
- **Input:** `/orbitalytics/bronze/satellites/satellites_orbital.csv` (2,400 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `satellite_id` is NOT NULL and non-empty
  - `orbit_type` is valid string
  - `altitude_km > 0.0`
  - `dry_mass_kg > 0.0`
  - `1957 <= launch_year <= 2035`
- **Quarantine Tag:** `INVALID_ALTITUDE_OR_NULL_ORBIT_OR_BAD_YEAR`
- **Business Transformations:**
  - Aggregation 1: Mean altitude, mass, expected lifespan, and total power by `orbit_type` (LEO, GEO, MEO, SSO, HEO).
  - Aggregation 2: Deployment volume and trajectory by operating agency and launch year.

### Domain 3: Launch Activities (`03_launches_etl.pig`)
- **Input:** `/orbitalytics/bronze/launches/launch_activities.csv` (1,200 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `launch_id`, `mission_id` non-null
  - `launch_outcome` non-null
  - `launch_cost_million_usd > 0.0`
  - `1957 <= year <= 2035`
- **Quarantine Tag:** `INVALID_COST_OR_NULL_ID_OR_BAD_YEAR`
- **Business Transformations:**
  - Aggregation 1: Total launches, aggregate launch expenditure, and payload capacity by country and year.
  - Aggregation 2: Launch outcome distribution (Success, Failure, Partial Failure).
  - Aggregation 3: Vehicle fleet metrics (average cost per launch, mean payload to orbit).

### Domain 4: Equipment & Component Demand (`04_equipment_demand_etl.pig`)
- **Input:** `/orbitalytics/bronze/equipment_demand/equipment_component_demand.csv` (11,312 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `demand_id`, `component_name`, `component_category` non-null
  - `units_demanded >= 0.0`
  - `avg_unit_cost_thousand_usd > 0.0`
  - `1957 <= year <= 2035`
- **Quarantine Tag:** `INVALID_UNITS_OR_NULL_COMPONENT_OR_ZERO_COST`
- **Business Transformations:**
  - Aggregation 1: Component category demand, manufacturing production, and procurement valuation by year.
  - Aggregation 2: Critical component demand ranking, lead time distribution, and unit cost baselines.
  - Aggregation 3: Supply chain shortage risk distribution (Low, Medium, High, Critical).

### Domain 5: Agency Research Expenditures (`05_agency_expenditure_etl.pig`)
- **Input:** `/orbitalytics/bronze/agency_expenditure/agency_research_expenditures.csv` (1,414 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `expenditure_id`, `agency_name`, `country` non-null
  - `total_monthly_expenditure_million_usd > 0.0`
  - `1957 <= year <= 2035`
- **Quarantine Tag:** `INVALID_EXPENDITURE_OR_NULL_AGENCY_OR_BAD_YEAR`
- **Business Transformations:**
  - Aggregation 1: Annual R&D, infrastructure, mission operations, and gross budget breakdown per agency.
  - Aggregation 2: Macro space investment volume and mean monthly expenditures grouped by sovereign state.

### Domain 6: Resource Consumption (`06_resource_consumption_etl.pig`)
- **Input:** `/orbitalytics/bronze/resource_consumption/resource_consumption.csv` (9,898 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `consumption_id`, `resource_name`, `resource_category` non-null
  - `quantity_consumed > 0.0`
  - `procurement_cost_k_usd > 0.0`
  - `1957 <= year <= 2035`
- **Quarantine Tag:** `INVALID_QUANTITY_OR_NULL_RESOURCE_OR_BAD_YEAR`
- **Business Transformations:**
  - Aggregation 1: Consumable materials volume (propellants, rare gases, metals) and financial expenditure by category and year.
  - Aggregation 2: Institutional material usage metrics across major space agencies.

### Domain 7: Satellite Manufacturing Requirements (`07_manufacturing_etl.pig`)
- **Input:** `/orbitalytics/bronze/manufacturing/satellite_manufacturing_requirements.csv` (600 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `order_id`, `satellite_class` non-null
  - `units_ordered > 0`
  - `contract_value_million_usd > 0.0`
  - `1957 <= delivery_year <= 2035`
- **Quarantine Tag:** `INVALID_UNITS_OR_CONTRACT_VALUE_OR_DELIVERY_YEAR`
- **Business Transformations:**
  - Aggregation 1: Total units ordered, cumulative contract valuation, and cleanroom qualification hours by satellite class.
  - Aggregation 2: Production pipeline load forecast by target delivery year.

### Domain 8: Space Infrastructure Requirements (`08_infrastructure_etl.pig`)
- **Input:** `/orbitalytics/bronze/infrastructure/space_infrastructure_requirements.csv` (1,010 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `infrastructure_record_id`, `facility_name`, `facility_type` non-null
  - `0.0 <= utilization_rate_pct <= 100.0`
  - `1957 <= year <= 2035`
- **Quarantine Tag:** `INVALID_UTILIZATION_OR_BAD_YEAR_OR_NULL_NAME`
- **Business Transformations:**
  - Aggregation 1: Facility capacity analytics (average utilization percentage, queued backlog hours, maintenance downtime) by facility type.
  - Aggregation 2: Operating efficiency and facility portfolio by sponsoring space agency.

### Domain 9: Research Investment & Future Projects (`09_research_projects_etl.pig`)
- **Input:** `/orbitalytics/bronze/research_projects/research_investment_future_projects.csv` (160 rows)
- **Pig Operators:** `LOAD`, `FILTER`, `DISTINCT`, `FOREACH`, `GENERATE`, `ORDER`, `GROUP`, `STORE`
- **Validation Rules:**
  - `project_id`, `project_title`, `research_theme` non-null
  - `estimated_investment_million_usd > 0.0`
  - `1 <= technology_readiness_level (TRL) <= 9`
  - `1957 <= target_commencement_year <= 2045`
- **Quarantine Tag:** `INVALID_TRL_OR_BAD_YEAR_OR_NEGATIVE_INVESTMENT`
- **Business Transformations:**
  - Aggregation 1: Research capital allocation, project density, and average TRL by research theme (e.g. Deep Space Propulsion, Quantum Satellite Communications).
  - Aggregation 2: Strategic investment distribution categorized by priority tier (Critical, High, Medium).

---

## 4. Record Accountability & Quarantine Architecture

To guarantee audit compliance and scientific validity, the Pig ETL implementation enforces a **Strict Zero Silent Deletion Policy**:

$$\text{Bronze Input Records} = \text{Silver Clean Records} + \text{Quarantine Rejected Records}$$

Every single record read from the Bronze HDFS ingestion directory is accounted for:
1. Valid rows are cleansed, projected, and committed to `/orbitalytics/silver/pig_{domain}`.
2. Invalid rows are explicitly tagged with a standardized rejection reason code and stored in `/orbitalytics/quarantine/pig_{domain}_rejected`.
3. Ingestion headers are discarded deterministically by value comparison rather than truncation.

This enables end-to-end data provenance tracking across all phases of the ORBITALYTICS big data lifecycle.

