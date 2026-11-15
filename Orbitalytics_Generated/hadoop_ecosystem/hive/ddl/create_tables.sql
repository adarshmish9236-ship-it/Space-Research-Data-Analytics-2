-- ====================================================================
-- ORBITALYTICS: Apache Hive Data Definition Language (DDL) Schema
-- Database: space_research_analytics
-- ====================================================================

CREATE DATABASE IF NOT EXISTS space_research_analytics
COMMENT 'Enterprise Big Data Lakehouse for Space Research and Predictive Demand Analytics'
LOCATION 'hdfs://namenode:9000/space_research/warehouse/';

USE space_research_analytics;

-- 1. Space Missions (Partitioned by launch_year)
CREATE EXTERNAL TABLE IF NOT EXISTS space_missions (
    mission_id STRING,
    mission_name STRING,
    agency STRING,
    country STRING,
    mission_type STRING,
    launch_date STRING,
    mission_status STRING,
    mission_budget_million_usd DOUBLE,
    payload_mass_kg DOUBLE,
    mission_duration_days INT,
    orbit_type STRING,
    destination STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (launch_year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/space_missions/';

-- 2. Satellites and Orbital Mechanics (Partitioned by launch_year)
CREATE EXTERNAL TABLE IF NOT EXISTS satellites_orbital (
    satellite_id STRING,
    satellite_name STRING,
    agency STRING,
    country STRING,
    launch_date STRING,
    orbit_type STRING,
    orbital_altitude_km DOUBLE,
    orbital_inclination_deg DOUBLE,
    operational_status STRING,
    expected_lifetime_years INT,
    power_capacity_kw DOUBLE,
    payload_type STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (launch_year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/satellites_orbital/';

-- 3. Launch Activities (Partitioned by year)
CREATE EXTERNAL TABLE IF NOT EXISTS launch_activities (
    launch_id STRING,
    launch_date STRING,
    agency STRING,
    country STRING,
    launch_site STRING,
    vehicle STRING,
    payload_to_orbit_kg DOUBLE,
    launch_cost_million_usd DOUBLE,
    launch_outcome STRING,
    commercial_flag BOOLEAN,
    mission_category STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/launch_activities/';

-- 4. Equipment Component Demand (Partitioned by year)
CREATE EXTERNAL TABLE IF NOT EXISTS equipment_component_demand (
    date STRING,
    month INT,
    equipment_type STRING,
    equipment_category STRING,
    units_demanded INT,
    avg_unit_cost_thousand_usd DOUBLE,
    total_demand_value_million_usd DOUBLE,
    lead_time_days INT,
    shortage_risk STRING,
    agency STRING,
    country STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/equipment_component_demand/';

-- 5. Agency Research Expenditures (Partitioned by year)
CREATE EXTERNAL TABLE IF NOT EXISTS agency_research_expenditures (
    date STRING,
    month INT,
    agency STRING,
    country STRING,
    rd_expenditure_million_usd DOUBLE,
    infrastructure_expenditure_million_usd DOUBLE,
    mission_operations_million_usd DOUBLE,
    total_monthly_expenditure_million_usd DOUBLE,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/agency_research_expenditures/';

-- 6. Resource Consumption (Partitioned by year)
CREATE EXTERNAL TABLE IF NOT EXISTS resource_consumption (
    date STRING,
    month INT,
    resource_type STRING,
    quantity_consumed DOUBLE,
    unit STRING,
    agency STRING,
    mission_category STRING,
    country STRING,
    consumption_cost_million_usd DOUBLE,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/resource_consumption/';

-- 7. Satellite Manufacturing Requirements
CREATE EXTERNAL TABLE IF NOT EXISTS satellite_manufacturing_requirements (
    date STRING,
    month INT,
    satellite_category STRING,
    manufacturing_quantity INT,
    component_requirement STRING,
    production_cost_million_usd DOUBLE,
    manufacturing_capacity INT,
    projected_shortage INT,
    agency STRING,
    country STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
PARTITIONED BY (year INT)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/satellite_manufacturing_requirements/';

-- 8. Space Infrastructure Requirements
CREATE EXTERNAL TABLE IF NOT EXISTS space_infrastructure_requirements (
    project_id STRING,
    project_name STRING,
    country STRING,
    agency STRING,
    infrastructure_type STRING,
    estimated_cost_million_usd DOUBLE,
    construction_year INT,
    required_capacity STRING,
    project_status STRING,
    priority STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/space_infrastructure_requirements/';

-- 9. Future Research Investment Projects
CREATE EXTERNAL TABLE IF NOT EXISTS research_investment_future_projects (
    project_id STRING,
    project_name STRING,
    agency STRING,
    country STRING,
    research_category STRING,
    proposed_year INT,
    investment_million_usd DOUBLE,
    priority STRING,
    technology_readiness_level INT,
    expected_resource_requirement STRING,
    project_status STRING,
    data_source STRING,
    is_synthetic BOOLEAN
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/space_research/curated/research_investment_future_projects/';

