-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 05_populate_dimensions.sql
-- Population of Star Schema Dimension Tables from Cleansed Staging Tables
-- =============================================================================

USE orbitalytics;

-- 1. Populate dim_agency
INSERT OVERWRITE TABLE dim_agency
SELECT DISTINCT
    COALESCE(agency_id, 'AGY-UNKNOWN') AS agency_key,
    TRIM(agency_name) AS agency_name,
    CASE 
        WHEN agency_name LIKE '%NASA%' OR agency_name LIKE '%Commercial%' THEN 'United States'
        WHEN agency_name LIKE '%ESA%' OR agency_name LIKE '%European%' THEN 'Europe'
        WHEN agency_name LIKE '%Roscosmos%' THEN 'Russia'
        WHEN agency_name LIKE '%ISRO%' THEN 'India'
        WHEN agency_name LIKE '%JAXA%' OR agency_name LIKE '%Japan%' THEN 'Japan'
        WHEN agency_name LIKE '%China%' THEN 'China'
        ELSE 'International'
    END AS country,
    CASE 
        WHEN agency_name LIKE '%Commercial%' THEN 'Commercial Operator'
        WHEN agency_name LIKE '%European%' THEN 'Intergovernmental'
        ELSE 'National Space Agency'
    END AS agency_type
FROM stg_missions
WHERE agency_name IS NOT NULL AND TRIM(agency_name) != '';

-- 2. Populate dim_component
INSERT OVERWRITE TABLE dim_component
SELECT
    component_id AS component_key,
    component_name,
    component_category,
    MAX(unit_of_measure) AS unit_of_measure,
    CAST(ROUND(AVG(lead_time_days)) AS INT) AS standard_lead_time_days
FROM stg_equipment_demand
WHERE component_name IS NOT NULL AND TRIM(component_name) != ''
GROUP BY component_id, component_name, component_category;

-- 3. Populate dim_resource
INSERT OVERWRITE TABLE dim_resource
SELECT
    resource_id AS resource_key,
    resource_name,
    resource_category,
    MAX(unit_of_measure) AS unit_of_measure,
    CASE 
        WHEN resource_category LIKE '%Cryogenic%' THEN 'Cryogenic Hazardous'
        WHEN resource_category LIKE '%Storable%' OR resource_category LIKE '%Liquid%' THEN 'Toxic Volatile'
        ELSE 'Standard Industrial'
    END AS hazard_tier
FROM stg_resource_consumption
WHERE resource_name IS NOT NULL AND TRIM(resource_name) != ''
GROUP BY resource_id, resource_name, resource_category;

-- 4. Populate dim_mission
INSERT OVERWRITE TABLE dim_mission
SELECT DISTINCT
    mission_id AS mission_key,
    mission_name,
    mission_type,
    status,
    crew_size,
    duration_days
FROM stg_missions
WHERE mission_id IS NOT NULL AND TRIM(mission_id) != '';

-- 5. Populate dim_satellite
INSERT OVERWRITE TABLE dim_satellite
SELECT DISTINCT
    satellite_id AS satellite_key,
    satellite_name,
    orbit_type,
    altitude_km,
    inclination_deg,
    telemetry_band,
    operational_status
FROM stg_satellites
WHERE satellite_id IS NOT NULL AND TRIM(satellite_id) != '';

-- 6. Populate dim_location
INSERT OVERWRITE TABLE dim_location
SELECT
    CONCAT('LOC-', SUBSTR(MD5(CONCAT(launch_site, country)), 1, 8)) AS location_key,
    launch_site,
    country,
    CASE 
        WHEN launch_site LIKE '%SpaceX%' OR launch_site LIKE '%Cape Canaveral%' OR launch_site LIKE '%Kodiak%' THEN 'Commercial / Civil Spaceport'
        WHEN launch_site LIKE '%Baikonur%' OR launch_site LIKE '%Plesetsk%' OR launch_site LIKE '%Jiuquan%' THEN 'Government Launch Range'
        ELSE 'International Launch Center'
    END AS operator_type
FROM (
    SELECT DISTINCT launch_site, country
    FROM stg_launches
    WHERE launch_site IS NOT NULL AND TRIM(launch_site) != ''
) loc_raw;

-- 7. Populate dim_date
INSERT OVERWRITE TABLE dim_date
SELECT DISTINCT
    date_val AS date_key,
    date_val AS full_date,
    year,
    quarter,
    month,
    CASE month
        WHEN 1 THEN 'Jan' WHEN 2 THEN 'Feb' WHEN 3 THEN 'Mar'
        WHEN 4 THEN 'Apr' WHEN 5 THEN 'May' WHEN 6 THEN 'Jun'
        WHEN 7 THEN 'Jul' WHEN 8 THEN 'Aug' WHEN 9 THEN 'Sep'
        WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dec'
        ELSE 'Unk'
    END AS month_name,
    CAST(SUBSTR(date_val, 9, 2) AS INT) AS day_of_month,
    0 AS is_weekend
FROM stg_equipment_demand
WHERE date_val IS NOT NULL AND TRIM(date_val) != '';

