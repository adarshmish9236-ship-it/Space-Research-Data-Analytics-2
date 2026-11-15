-- ====================================================================
-- Hive Data Definition Language (DDL) Schema: Space Research Big Data
-- Database: space_research_analytics
-- ====================================================================

CREATE DATABASE IF NOT EXISTS space_research_analytics
COMMENT 'Enterprise Big Data Warehouse for Space Research and Demand Forecasting'
LOCATION '/space_research/warehouse/';

USE space_research_analytics;

-- 1. Space Missions Table (Partitioned by Year)
CREATE EXTERNAL TABLE IF NOT EXISTS space_missions (
    mission_id STRING,
    mission_name STRING,
    agency STRING,
    mission_type STRING,
    launch_date STRING,
    quarter STRING,
    budget_million_usd DOUBLE,
    payload_mass_kg DOUBLE,
    status STRING,
    crew_size INT,
    duration_days INT
)
PARTITIONED BY (year INT)
STORED AS PARQUET
LOCATION '/space_research/curated/space_missions/';

-- 2. Satellites and Orbital Information
CREATE EXTERNAL TABLE IF NOT EXISTS satellites_orbital (
    satellite_id STRING,
    satellite_name STRING,
    operator_agency STRING,
    orbit_type STRING,
    altitude_km INT,
    inclination_deg DOUBLE,
    expected_lifetime_years INT,
    dry_mass_kg DOUBLE,
    power_consumption_w DOUBLE,
    telemetry_band STRING,
    operational_status STRING
)
PARTITIONED BY (launch_year INT)
STORED AS PARQUET
LOCATION '/space_research/curated/satellites_orbital/';

-- 3. Launch Activities Table
CREATE EXTERNAL TABLE IF NOT EXISTS launch_activities (
    launch_id STRING,
    launch_date STRING,
    vehicle STRING,
    launch_site STRING,
    launch_outcome STRING,
    commercial_flag BOOLEAN,
    launch_cost_million_usd DOUBLE,
    payload_to_orbit_kg DOUBLE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/space_research/curated/launch_activities/';

-- 4. Space Agency Research Expenditures Table
CREATE EXTERNAL TABLE IF NOT EXISTS agency_research_expenditures (
    date STRING,
    agency STRING,
    rd_expenditure_million_usd DOUBLE,
    infrastructure_expenditure_million_usd DOUBLE,
    mission_operations_million_usd DOUBLE,
    total_monthly_expenditure_million_usd DOUBLE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/space_research/curated/agency_research_expenditures/';

-- 5. Space Equipment and Component Demand Table
CREATE EXTERNAL TABLE IF NOT EXISTS equipment_component_demand (
    date STRING,
    equipment_type STRING,
    units_demanded INT,
    avg_unit_cost_thousand_usd DOUBLE,
    total_demand_value_million_usd DOUBLE,
    lead_time_days INT,
    shortage_risk STRING
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/space_research/curated/equipment_component_demand/';

-- 6. Historical Resource Consumption Table
CREATE EXTERNAL TABLE IF NOT EXISTS resource_consumption (
    date STRING,
    resource_name STRING,
    quantity_consumed DOUBLE,
    unit_of_measure STRING,
    procurement_cost_k_usd DOUBLE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/space_research/curated/resource_consumption/';

-- 7. Satellite Manufacturing Requirements
CREATE EXTERNAL TABLE IF NOT EXISTS satellite_manufacturing_requirements (
    order_id STRING,
    agency_client STRING,
    satellite_class STRING,
    units_ordered INT,
    delivery_year INT,
    cleanroom_hours_required INT,
    vibration_testing_pass BOOLEAN,
    contract_value_million_usd DOUBLE
)
STORED AS PARQUET
LOCATION '/space_research/curated/satellite_manufacturing_requirements/';

-- 8. Space Infrastructure Requirements Table
CREATE EXTERNAL TABLE IF NOT EXISTS space_infrastructure_requirements (
    date STRING,
    facility_name STRING,
    utilization_rate_pct DOUBLE,
    queued_backlog_hours INT,
    maintenance_downtime_days INT
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET
LOCATION '/space_research/curated/space_infrastructure_requirements/';

-- 9. Future Project Targets Table
CREATE EXTERNAL TABLE IF NOT EXISTS research_investment_future_projects (
    project_code STRING,
    project_title STRING,
    lead_agency STRING,
    target_commencement_year INT,
    estimated_investment_billion_usd DOUBLE,
    priority_tier STRING,
    readiness_level_TRL INT
)
STORED AS PARQUET
LOCATION '/space_research/curated/research_investment_future_projects/';

