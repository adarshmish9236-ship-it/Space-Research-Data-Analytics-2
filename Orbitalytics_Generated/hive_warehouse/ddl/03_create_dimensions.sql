-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 03_create_dimensions.sql
-- Star Schema Dimension Tables (Parquet + Snappy)
-- =============================================================================

USE orbitalytics;

-- 1. Date Dimension
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
    date_key STRING COMMENT 'Date identifier in YYYY-MM-DD',
    full_date STRING COMMENT 'ISO Date string',
    year INT COMMENT 'Calendar year',
    quarter STRING COMMENT 'Quarter Q1-Q4',
    month INT COMMENT 'Month 1-12',
    month_name STRING COMMENT 'Month name abbreviation',
    day_of_month INT COMMENT 'Day 1-31',
    is_weekend INT COMMENT '1 if Saturday or Sunday, else 0'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 2. Space Agency Dimension
DROP TABLE IF EXISTS dim_agency;
CREATE TABLE dim_agency (
    agency_key STRING COMMENT 'Surrogate / Business key e.g. AGY-001',
    agency_name STRING COMMENT 'Full legal name of the space agency / operator',
    country STRING COMMENT 'Headquarters nation',
    agency_type STRING COMMENT 'Government, Commercial, or International'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 3. Spacecraft Component Dimension
DROP TABLE IF EXISTS dim_component;
CREATE TABLE dim_component (
    component_key STRING COMMENT 'Component identifier e.g. CMP-001',
    component_name STRING COMMENT 'Full technical designation of subsystem',
    component_category STRING COMMENT 'Subsystem functional domain',
    unit_of_measure STRING COMMENT 'Physical unit (Units, Assemblies, Sets)',
    standard_lead_time_days INT COMMENT 'Nominal manufacturing lead time in days'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 4. Consumable Resource Dimension
DROP TABLE IF EXISTS dim_resource;
CREATE TABLE dim_resource (
    resource_key STRING COMMENT 'Resource identifier e.g. RES-001',
    resource_name STRING COMMENT 'Propellant, gas, alloy, or energy consumable',
    resource_category STRING COMMENT 'Cryogenic, storable, structural, or electronic',
    unit_of_measure STRING COMMENT 'Physical metric unit (kg, Liters, kWh)',
    hazard_tier STRING COMMENT 'Hazard handling tier (Cryogenic, Toxic, Inert)'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 5. Space Mission Dimension
DROP TABLE IF EXISTS dim_mission;
CREATE TABLE dim_mission (
    mission_key STRING COMMENT 'Mission ID e.g. MSN-2020-001',
    mission_name STRING COMMENT 'Operational designation of mission',
    mission_type STRING COMMENT 'Scientific, Communications, Exploration, etc.',
    status STRING COMMENT 'Completed, Successful, Operational, Failed',
    crew_size INT COMMENT 'Astronaut complement',
    duration_days DOUBLE COMMENT 'Total mission duration in days'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 6. Satellite Catalog Dimension
DROP TABLE IF EXISTS dim_satellite;
CREATE TABLE dim_satellite (
    satellite_key STRING COMMENT 'Satellite catalog key e.g. SAT-001',
    satellite_name STRING COMMENT 'Spacecraft designation',
    orbit_type STRING COMMENT 'Orbital regime (LEO, GEO, MEO, SSO, Lagrange, Deep Space)',
    altitude_km DOUBLE COMMENT 'Semi-major orbital altitude in km',
    inclination_deg DOUBLE COMMENT 'Orbital inclination angle in degrees',
    telemetry_band STRING COMMENT 'RF Communication band (S-band, X-band, Ka-band)',
    operational_status STRING COMMENT 'Active, Decommissioned, Standby'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- 7. Geographic Launch & Facility Location Dimension
DROP TABLE IF EXISTS dim_location;
CREATE TABLE dim_location (
    location_key STRING COMMENT 'Location identifier',
    launch_site STRING COMMENT 'Cosmodrome / Spaceport / Facility Name',
    country STRING COMMENT 'Host nation',
    operator_type STRING COMMENT 'Government Military, Civil, or Commercial'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

