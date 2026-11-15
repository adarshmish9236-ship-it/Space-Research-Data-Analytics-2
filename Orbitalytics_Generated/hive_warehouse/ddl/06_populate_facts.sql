-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 06_populate_facts.sql
-- Dynamic Partition Population of Star Schema Fact Tables (Parquet + Snappy)
-- =============================================================================

USE orbitalytics;

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
SET hive.exec.max.dynamic.partitions=1000;
SET hive.exec.max.dynamic.partitions.pernode=1000;
SET mapreduce.map.memory.mb=1024;
SET mapreduce.reduce.memory.mb=1024;

-- 1. Populate fact_equipment_demand (Partitioned by year)
INSERT OVERWRITE TABLE fact_equipment_demand PARTITION (year)
SELECT
    demand_id,
    date_val,
    month,
    quarter,
    component_id AS component_key,
    component_name,
    component_category,
    agency_id AS agency_key,
    agency_name,
    target_satellite_class,
    units_demanded,
    units_manufactured,
    units_procured,
    unit_of_measure,
    avg_unit_cost_k_usd,
    total_demand_value_m_usd,
    lead_time_days,
    shortage_risk,
    data_origin,
    year
FROM stg_equipment_demand
WHERE year IS NOT NULL AND year >= 1957 AND year <= 2035;

-- 2. Populate fact_resource_consumption (Partitioned by year)
INSERT OVERWRITE TABLE fact_resource_consumption PARTITION (year)
SELECT
    consumption_id,
    date_val,
    month,
    quarter,
    resource_id AS resource_key,
    resource_name,
    resource_category,
    agency_id AS agency_key,
    agency_name,
    mission_id AS mission_key,
    quantity_consumed,
    unit_of_measure,
    procurement_cost_k_usd,
    data_origin,
    year
FROM stg_resource_consumption
WHERE year IS NOT NULL AND year >= 1957 AND year <= 2035;

-- 3. Populate fact_launch_activity (Partitioned by year)
INSERT OVERWRITE TABLE fact_launch_activity PARTITION (year)
SELECT
    launch_id,
    mission_id AS mission_key,
    launch_date,
    month,
    vehicle,
    launch_site,
    country,
    launch_outcome,
    commercial_flag,
    launch_cost_m_usd,
    payload_to_orbit_kg,
    data_origin,
    year
FROM stg_launches
WHERE year IS NOT NULL AND year >= 1957 AND year <= 2035;

-- 4. Populate fact_manufacturing (Partitioned by delivery_year)
INSERT OVERWRITE TABLE fact_manufacturing PARTITION (delivery_year)
SELECT
    order_id,
    agency_id AS agency_key,
    agency_name,
    satellite_class,
    units_ordered,
    cleanroom_hours_required,
    vibration_testing_pass,
    contract_value_m_usd,
    country,
    data_origin,
    delivery_year
FROM stg_manufacturing
WHERE delivery_year IS NOT NULL AND delivery_year >= 1957 AND delivery_year <= 2035;

-- 5. Populate fact_research_investment (Partitioned by year)
INSERT OVERWRITE TABLE fact_research_investment PARTITION (year)
SELECT
    expenditure_id,
    date_val,
    month,
    quarter,
    agency_id AS agency_key,
    agency_name,
    country,
    rd_expenditure_m_usd,
    infrastructure_expenditure_m_usd,
    mission_operations_m_usd,
    total_monthly_expenditure_m_usd,
    currency,
    data_origin,
    year
FROM stg_agency_expenditure
WHERE year IS NOT NULL AND year >= 1957 AND year <= 2035;

