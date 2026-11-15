# ORBITALYTICS 2.0 — Apache Pig Latin ETL Architecture

---

## 1. Overview & Role in Lakehouse Pipeline

**Apache Pig** provides the declarative, high-level dataflow programming language (**Pig Latin**) responsible for translating messy, unformatted, and potentially corrupt raw Bronze CSV telemetry into clean, schema-typed, null-imputed Silver records stored in Apache Parquet.

In ORBITALYTICS 2.0, Pig acts as the primary data sanitation boundary before records enter Hive or Spark.

---

## 2. Pig Latin Script Inventory

The platform maintains nine production Pig scripts located in `/pig_etl/`:

| Script File | Target Domain | Input Path | Output Path | Key Transformations |
| :--- | :--- | :--- | :--- | :--- |
| `01_clean_missions.pig` | Space Missions | `/space_research/raw/space_missions.csv` | `/space_research/silver/space_missions/` | Filters negative budgets, maps missing status to 'Unknown', casts types |
| `02_clean_satellites.pig` | Satellites | `/space_research/raw/satellites_orbital.csv` | `/space_research/silver/satellites_orbital/` | Enforces orbital altitude bounds ($> 100$ km), parses TLE band codes |
| `03_clean_launches.pig` | Launch Activities | `/space_research/raw/launch_activities.csv` | `/space_research/silver/launch_activities/` | Standardizes launch vehicle names, normalizes boolean commercial flags |
| `04_clean_equipment.pig` | Equipment Demand | `/space_research/raw/equipment_component_demand.csv` | `/space_research/silver/equipment_component_demand/` | Validates positive units demanded, computes total demand value |
| `05_clean_resources.pig` | Resource Consumables | `/space_research/raw/resource_consumption.csv` | `/space_research/silver/resource_consumption/` | Converts units to metric tons, filters zero-cost anomalies |
| `06_clean_manufacturing.pig`| Cleanroom Work Orders | `/space_research/raw/satellite_manufacturing_requirements.csv` | `/space_research/silver/manufacturing/` | Computes cleanroom labor hours, checks vibration test status |
| `07_clean_expenditures.pig`| Agency Appropriations | `/space_research/raw/agency_research_expenditures.csv` | `/space_research/silver/agency_research_expenditures/` | Verifies R&D vs Ops breakdown splits, validates currency values |
| `08_clean_infrastructure.pig`| DSN Ground Stations | `/space_research/raw/space_infrastructure_requirements.csv` | `/space_research/silver/space_infrastructure_requirements/` | Verifies tracking availability percentages ($0\% - 100\%$) |
| `09_clean_future_projects.pig`| Decadal Roadmaps | `/space_research/raw/research_investment_future_projects.csv` | `/space_research/silver/future_projects/` | Standardizes priority tiers, flags uncommitted budget plans |

---

## 3. Representative Pig Latin Implementation (`04_clean_equipment.pig`)

```pig
-- Load raw equipment demand telemetry from HDFS Bronze zone
RAW_DEMAND = LOAD 'hdfs://hadoop-namenode:9000/space_research/raw/equipment_component_demand.csv' 
    USING PigStorage(',') 
    AS (
        date:chararray,
        year:int,
        month:int,
        quarter:chararray,
        equipment_type:chararray,
        units_demanded:int,
        avg_unit_cost_thousand_usd:float,
        total_demand_value_million_usd:float,
        lead_time_days:int,
        shortage_risk:chararray
    );

-- Filter header and eliminate malformed or corrupt rows
CLEAN_DATA = FILTER RAW_DEMAND BY 
    (year >= 2010 AND year <= 2026) AND 
    (units_demanded > 0) AND 
    (equipment_type IS NOT NULL);

-- Apply data type transformations and compute validated demand values
VALIDATED = FOREACH CLEAN_DATA GENERATE
    date,
    year,
    month,
    quarter,
    TRIM(equipment_type) AS equipment_type,
    units_demanded,
    avg_unit_cost_thousand_usd,
    ROUND((units_demanded * avg_unit_cost_thousand_usd) / 1000.0) AS total_demand_value_million_usd,
    (lead_time_days > 0 ? lead_time_days : 180) AS lead_time_days,
    (shortage_risk IS NOT NULL ? shortage_risk : 'Medium') AS shortage_risk;

-- Group by Year and Component for summary statistics
GROUPED = GROUP VALIDATED BY (year, equipment_type);
AGGREGATED = FOREACH GROUPED GENERATE
    FLATTEN(group) AS (year, equipment_type),
    SUM(VALIDATED.units_demanded) AS annual_units,
    SUM(VALIDATED.total_demand_value_million_usd) AS annual_spend_m_usd;

-- Store sanitized output into HDFS Silver zone
STORE VALIDATED INTO 'hdfs://hadoop-namenode:9000/space_research/silver/equipment_component_demand'
    USING org.apache.pig.piggybank.storage.avro.AvroStorage();
```

---

## 4. Execution & Validation

Pig scripts can be launched directly via the platform backend API or through the Pig CLI on the cluster:
```bash
# Execute Pig script in local/MapReduce mode
docker exec -it hadoop-namenode pig -x local -f /pig_etl/04_clean_equipment.pig
```
All Pig jobs log input record counts, filtered records, map-reduce task counts, and execution runtimes to `logs/pig_etl/`.
