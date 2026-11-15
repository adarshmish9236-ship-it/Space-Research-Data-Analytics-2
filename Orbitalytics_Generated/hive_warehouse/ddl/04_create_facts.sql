-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 04_create_facts.sql
-- Star Schema Partitioned Fact Tables (Parquet + Snappy, Partitioned by Year)
-- =============================================================================

USE orbitalytics;

-- 1. Fact Equipment Component Demand
DROP TABLE IF EXISTS fact_equipment_demand;
CREATE TABLE fact_equipment_demand (
    demand_id STRING,
    date_val STRING,
    month INT,
    quarter STRING,
    component_key STRING,
    component_name STRING,
    component_category STRING,
    agency_key STRING,
    agency_name STRING,
    target_satellite_class STRING,
    units_demanded DOUBLE,
    units_manufactured DOUBLE,
    units_procured DOUBLE,
    unit_of_measure STRING,
    avg_unit_cost_k_usd DOUBLE,
    total_demand_value_m_usd DOUBLE,
    lead_time_days INT,
    shortage_risk STRING,
    data_origin STRING
)
PARTITIONED BY (year INT)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 2. Fact Resource & Propellant Consumption
DROP TABLE IF EXISTS fact_resource_consumption;
CREATE TABLE fact_resource_consumption (
    consumption_id STRING,
    date_val STRING,
    month INT,
    quarter STRING,
    resource_key STRING,
    resource_name STRING,
    resource_category STRING,
    agency_key STRING,
    agency_name STRING,
    mission_key STRING,
    quantity_consumed DOUBLE,
    unit_of_measure STRING,
    procurement_cost_k_usd DOUBLE,
    data_origin STRING
)
PARTITIONED BY (year INT)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 3. Fact Launch Activities
DROP TABLE IF EXISTS fact_launch_activity;
CREATE TABLE fact_launch_activity (
    launch_id STRING,
    mission_key STRING,
    launch_date STRING,
    month INT,
    vehicle STRING,
    launch_site STRING,
    country STRING,
    launch_outcome STRING,
    commercial_flag STRING,
    launch_cost_m_usd DOUBLE,
    payload_to_orbit_kg DOUBLE,
    data_origin STRING
)
PARTITIONED BY (year INT)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 4. Fact Satellite Manufacturing
DROP TABLE IF EXISTS fact_manufacturing;
CREATE TABLE fact_manufacturing (
    order_id STRING,
    agency_key STRING,
    agency_name STRING,
    satellite_class STRING,
    units_ordered INT,
    cleanroom_hours_required DOUBLE,
    vibration_testing_pass STRING,
    contract_value_m_usd DOUBLE,
    country STRING,
    data_origin STRING
)
PARTITIONED BY (delivery_year INT)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 5. Fact Research & Infrastructure Investment
DROP TABLE IF EXISTS fact_research_investment;
CREATE TABLE fact_research_investment (
    expenditure_id STRING,
    date_val STRING,
    month INT,
    quarter STRING,
    agency_key STRING,
    agency_name STRING,
    country STRING,
    rd_expenditure_m_usd DOUBLE,
    infrastructure_expenditure_m_usd DOUBLE,
    mission_operations_m_usd DOUBLE,
    total_monthly_expenditure_m_usd DOUBLE,
    currency STRING,
    data_origin STRING
)
PARTITIONED BY (year INT)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

