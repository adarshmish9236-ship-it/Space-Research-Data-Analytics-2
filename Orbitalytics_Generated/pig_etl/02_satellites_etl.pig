-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 02
-- Domain: Satellites / Orbital Data
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/satellites/satellites_orbital.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_satellites
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_satellites_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_satellite_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_satellites = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/satellites/satellites_orbital.csv'
    USING PigStorage(',')
    AS (
        satellite_id:chararray, satellite_name:chararray,
        operator_agency_id:chararray, operator_agency_name:chararray,
        associated_mission_id:chararray, orbit_type:chararray,
        altitude_km:double, inclination_deg:double, launch_year:int,
        expected_lifetime_years:double, dry_mass_kg:double,
        power_consumption_w:double, telemetry_band:chararray,
        operational_status:chararray, data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_satellites BY satellite_id != 'satellite_id';

-- ---- DISTINCT on satellite_id ---------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_satellites = FILTER deduped BY
    satellite_id IS NOT NULL AND TRIM(satellite_id) != '' AND
    orbit_type IS NOT NULL AND TRIM(orbit_type) != '' AND
    altitude_km IS NOT NULL AND altitude_km > 0.0 AND
    launch_year IS NOT NULL AND launch_year >= 1957 AND launch_year <= 2035 AND
    dry_mass_kg IS NOT NULL AND dry_mass_kg > 0.0;

invalid_satellites = FILTER deduped BY
    satellite_id IS NULL OR TRIM(satellite_id) == '' OR
    orbit_type IS NULL OR TRIM(orbit_type) == '' OR
    altitude_km IS NULL OR altitude_km <= 0.0 OR
    launch_year IS NULL OR launch_year < 1957 OR launch_year > 2035 OR
    dry_mass_kg IS NULL OR dry_mass_kg <= 0.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_satellites = FOREACH valid_satellites GENERATE
    satellite_id, satellite_name, operator_agency_id, operator_agency_name,
    associated_mission_id, orbit_type, altitude_km, inclination_deg,
    launch_year, expected_lifetime_years, dry_mass_kg, power_consumption_w,
    telemetry_band, operational_status, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_satellites BY launch_year ASC, orbit_type ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_satellites = FOREACH invalid_satellites GENERATE
    satellite_id, satellite_name, orbit_type, altitude_km,
    'INVALID_ALTITUDE_OR_NULL_ORBIT_OR_BAD_YEAR' AS rejection_reason;

-- ---- AGGREGATION: satellites by orbit type --------------------------------
by_orbit = GROUP silver_satellites BY orbit_type;
agg_orbit = FOREACH by_orbit GENERATE
    group AS orbit_type,
    COUNT(silver_satellites) AS total_satellites,
    AVG(silver_satellites.altitude_km) AS avg_altitude_km,
    AVG(silver_satellites.dry_mass_kg) AS avg_dry_mass_kg,
    AVG(silver_satellites.expected_lifetime_years) AS avg_lifetime_years,
    SUM(silver_satellites.power_consumption_w) AS total_power_w;

-- ---- AGGREGATION: satellites by agency & year ----------------------------
by_agency_year = GROUP silver_satellites BY (operator_agency_name, launch_year);
agg_agency_year = FOREACH by_agency_year GENERATE
    FLATTEN(group) AS (agency_name, launch_year),
    COUNT(silver_satellites) AS satellite_count,
    AVG(silver_satellites.altitude_km) AS avg_altitude_km;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_satellites'
    USING PigStorage(',');

STORE quarantine_satellites INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_satellites_rejected'
    USING PigStorage(',');

STORE agg_orbit INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_satellite_analytics'
    USING PigStorage(',');

STORE agg_agency_year INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_satellite_by_agency_year'
    USING PigStorage(',');

