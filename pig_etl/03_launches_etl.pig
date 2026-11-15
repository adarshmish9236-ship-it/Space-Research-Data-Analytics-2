-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 03
-- Domain: Launch Activities
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/launches/launch_activities.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_launches
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_launches_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_launch_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_launches = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/launches/launch_activities.csv'
    USING PigStorage(',')
    AS (
        launch_id:chararray, mission_id:chararray, launch_date:chararray,
        year:int, month:int, vehicle:chararray, launch_site:chararray,
        country:chararray, launch_outcome:chararray, commercial_flag:chararray,
        launch_cost_million_usd:double, payload_to_orbit_kg:double,
        data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_launches BY launch_id != 'launch_id';

-- ---- DISTINCT on launch_id ------------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_launches = FILTER deduped BY
    launch_id IS NOT NULL AND TRIM(launch_id) != '' AND
    mission_id IS NOT NULL AND TRIM(mission_id) != '' AND
    year IS NOT NULL AND year >= 1957 AND year <= 2035 AND
    launch_outcome IS NOT NULL AND TRIM(launch_outcome) != '' AND
    launch_cost_million_usd IS NOT NULL AND launch_cost_million_usd > 0.0;

invalid_launches = FILTER deduped BY
    launch_id IS NULL OR TRIM(launch_id) == '' OR
    mission_id IS NULL OR TRIM(mission_id) == '' OR
    year IS NULL OR year < 1957 OR year > 2035 OR
    launch_outcome IS NULL OR TRIM(launch_outcome) == '' OR
    launch_cost_million_usd IS NULL OR launch_cost_million_usd <= 0.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_launches = FOREACH valid_launches GENERATE
    launch_id, mission_id, launch_date, year, month, vehicle,
    launch_site, country, launch_outcome, commercial_flag,
    launch_cost_million_usd, payload_to_orbit_kg, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_launches BY year ASC, month ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_launches = FOREACH invalid_launches GENERATE
    launch_id, mission_id, year, launch_outcome, launch_cost_million_usd,
    'INVALID_COST_OR_NULL_ID_OR_BAD_YEAR' AS rejection_reason;

-- ---- AGGREGATION: launches by country & year -----------------------------
by_country_year = GROUP silver_launches BY (country, year);
agg_country = FOREACH by_country_year GENERATE
    FLATTEN(group) AS (country, year),
    COUNT(silver_launches) AS total_launches,
    SUM(silver_launches.launch_cost_million_usd) AS total_cost_m_usd,
    SUM(silver_launches.payload_to_orbit_kg) AS total_payload_kg;

-- ---- AGGREGATION: outcome rates ------------------------------------------
by_outcome = GROUP silver_launches BY launch_outcome;
agg_outcome = FOREACH by_outcome GENERATE
    group AS launch_outcome,
    COUNT(silver_launches) AS launch_count,
    SUM(silver_launches.launch_cost_million_usd) AS total_cost_m_usd;

-- ---- AGGREGATION: by vehicle ---------------------------------------------
by_vehicle = GROUP silver_launches BY vehicle;
agg_vehicle = FOREACH by_vehicle GENERATE
    group AS vehicle,
    COUNT(silver_launches) AS launch_count,
    AVG(silver_launches.payload_to_orbit_kg) AS avg_payload_kg,
    AVG(silver_launches.launch_cost_million_usd) AS avg_cost_m_usd;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_launches'
    USING PigStorage(',');

STORE quarantine_launches INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_launches_rejected'
    USING PigStorage(',');

STORE agg_country INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_launch_analytics'
    USING PigStorage(',');

STORE agg_outcome INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_launch_outcome_rates'
    USING PigStorage(',');

STORE agg_vehicle INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_launch_by_vehicle'
    USING PigStorage(',');

