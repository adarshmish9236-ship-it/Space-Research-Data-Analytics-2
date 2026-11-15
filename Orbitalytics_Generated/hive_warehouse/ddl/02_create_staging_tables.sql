-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 02_create_staging_tables.sql
-- External Staging Tables mapped to HDFS Silver Lakehouse Datasets
-- =============================================================================

USE orbitalytics;

-- 1. Staging Equipment Demand
DROP TABLE IF EXISTS stg_equipment_demand;
CREATE EXTERNAL TABLE stg_equipment_demand (
    demand_id STRING,
    date_val STRING,
    year INT,
    month INT,
    quarter STRING,
    component_id STRING,
    component_name STRING,
    component_category STRING,
    agency_id STRING,
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
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_equipment_demand';

-- 2. Staging Resource Consumption
DROP TABLE IF EXISTS stg_resource_consumption;
CREATE EXTERNAL TABLE stg_resource_consumption (
    consumption_id STRING,
    date_val STRING,
    year INT,
    month INT,
    quarter STRING,
    resource_id STRING,
    resource_name STRING,
    resource_category STRING,
    agency_id STRING,
    agency_name STRING,
    mission_id STRING,
    quantity_consumed DOUBLE,
    unit_of_measure STRING,
    procurement_cost_k_usd DOUBLE,
    data_origin STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_resource_consumption';

-- 3. Staging Launches
DROP TABLE IF EXISTS stg_launches;
CREATE EXTERNAL TABLE stg_launches (
    launch_id STRING,
    mission_id STRING,
    launch_date STRING,
    year INT,
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
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_launches';

-- 4. Staging Missions
DROP TABLE IF EXISTS stg_missions;
CREATE EXTERNAL TABLE stg_missions (
    mission_id STRING,
    mission_name STRING,
    agency_id STRING,
    agency_name STRING,
    mission_type STRING,
    launch_date STRING,
    year INT,
    quarter STRING,
    budget_m_usd DOUBLE,
    payload_mass_kg DOUBLE,
    status STRING,
    crew_size INT,
    duration_days DOUBLE,
    data_origin STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_missions';

-- 5. Staging Satellites
DROP TABLE IF EXISTS stg_satellites;
CREATE EXTERNAL TABLE stg_satellites (
    satellite_id STRING,
    satellite_name STRING,
    operator_agency_id STRING,
    operator_agency_name STRING,
    associated_mission_id STRING,
    orbit_type STRING,
    altitude_km DOUBLE,
    inclination_deg DOUBLE,
    launch_year INT,
    expected_lifetime_years DOUBLE,
    dry_mass_kg DOUBLE,
    power_consumption_w DOUBLE,
    telemetry_band STRING,
    operational_status STRING,
    data_origin STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_satellites';

-- 6. Staging Manufacturing
DROP TABLE IF EXISTS stg_manufacturing;
CREATE EXTERNAL TABLE stg_manufacturing (
    order_id STRING,
    agency_id STRING,
    agency_name STRING,
    satellite_class STRING,
    units_ordered INT,
    delivery_year INT,
    cleanroom_hours_required DOUBLE,
    vibration_testing_pass STRING,
    contract_value_m_usd DOUBLE,
    data_origin STRING,
    country STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_manufacturing';

-- 7. Staging Agency Research Expenditure
DROP TABLE IF EXISTS stg_agency_expenditure;
CREATE EXTERNAL TABLE stg_agency_expenditure (
    expenditure_id STRING,
    date_val STRING,
    year INT,
    month INT,
    quarter STRING,
    agency_id STRING,
    agency_name STRING,
    country STRING,
    rd_expenditure_m_usd DOUBLE,
    infrastructure_expenditure_m_usd DOUBLE,
    mission_operations_m_usd DOUBLE,
    total_monthly_expenditure_m_usd DOUBLE,
    currency STRING,
    data_origin STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/orbitalytics/silver/pig_agency_expenditure';

