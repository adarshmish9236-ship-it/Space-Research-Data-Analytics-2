-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 01
-- Domain: Space Missions
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/missions/space_missions.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_missions
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_missions_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_mission_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_missions = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/missions/space_missions.csv'
    USING PigStorage(',')
    AS (
        mission_id:chararray, mission_name:chararray, agency_id:chararray,
        agency_name:chararray, mission_type:chararray, launch_date:chararray,
        year:int, quarter:chararray, budget_million_usd:double,
        payload_mass_kg:double, status:chararray, crew_size:int,
        duration_days:double, data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_missions BY mission_id != 'mission_id';

-- ---- DISTINCT on mission_id -----------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_missions = FILTER deduped BY
    mission_id IS NOT NULL AND
    TRIM(mission_id) != '' AND
    agency_name IS NOT NULL AND
    TRIM(agency_name) != '' AND
    budget_million_usd IS NOT NULL AND
    budget_million_usd > 0.0 AND
    year IS NOT NULL AND
    year >= 1957 AND year <= 2035;

invalid_missions = FILTER deduped BY
    mission_id IS NULL OR
    TRIM(mission_id) == '' OR
    agency_name IS NULL OR
    TRIM(agency_name) == '' OR
    budget_million_usd IS NULL OR
    budget_million_usd <= 0.0 OR
    year IS NULL OR
    year < 1957 OR year > 2035;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_missions = FOREACH valid_missions GENERATE
    mission_id,
    mission_name,
    agency_id,
    agency_name,
    mission_type,
    launch_date,
    year,
    quarter,
    budget_million_usd,
    payload_mass_kg,
    status,
    crew_size,
    duration_days,
    data_origin;

-- ---- ORDER silver ---------------------------------------------------------
silver_ordered = ORDER silver_missions BY year ASC, agency_name ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_missions = FOREACH invalid_missions GENERATE
    mission_id AS mission_id,
    mission_name AS mission_name,
    year AS year,
    budget_million_usd AS budget_million_usd,
    'INVALID_BUDGET_OR_NULL_AGENCY_OR_BAD_YEAR' AS rejection_reason;

-- ---- BUSINESS AGGREGATION: missions & budget by agency -------------------
by_agency = GROUP silver_missions BY agency_name;
agg_agency = FOREACH by_agency GENERATE
    group AS agency_name,
    COUNT(silver_missions) AS total_missions,
    SUM(silver_missions.budget_million_usd) AS total_budget_m_usd,
    AVG(silver_missions.budget_million_usd) AS avg_budget_m_usd,
    AVG(silver_missions.duration_days) AS avg_duration_days;

-- ---- AGGREGATION: missions by year & type ---------------------------------
by_year_type = GROUP silver_missions BY (year, mission_type);
agg_year_type = FOREACH by_year_type GENERATE
    FLATTEN(group) AS (year, mission_type),
    COUNT(silver_missions) AS mission_count,
    SUM(silver_missions.budget_million_usd) AS total_budget_m_usd;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_missions'
    USING PigStorage(',');

STORE quarantine_missions INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_missions_rejected'
    USING PigStorage(',');

STORE agg_agency INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_mission_analytics'
    USING PigStorage(',');

STORE agg_year_type INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_mission_by_year_type'
    USING PigStorage(',');

