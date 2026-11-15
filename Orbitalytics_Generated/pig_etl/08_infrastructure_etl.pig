-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 08
-- Domain: Space Infrastructure Requirements
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/infrastructure/space_infrastructure_requirements.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_infrastructure
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_infrastructure_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_infrastructure_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_infrastructure = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/infrastructure/space_infrastructure_requirements.csv'
    USING PigStorage(',')
    AS (
        infrastructure_record_id:chararray, date:chararray, year:int, month:int,
        facility_name:chararray, facility_type:chararray, agency_id:chararray,
        agency_name:chararray, location:chararray, utilization_rate_pct:double,
        queued_backlog_hours:double, maintenance_downtime_days:double,
        data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_infrastructure BY infrastructure_record_id != 'infrastructure_record_id';

-- ---- DISTINCT on record_id ------------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_infra = FILTER deduped BY
    infrastructure_record_id IS NOT NULL AND TRIM(infrastructure_record_id) != '' AND
    facility_name IS NOT NULL AND TRIM(facility_name) != '' AND
    facility_type IS NOT NULL AND TRIM(facility_type) != '' AND
    year IS NOT NULL AND year >= 1957 AND year <= 2035 AND
    utilization_rate_pct IS NOT NULL AND utilization_rate_pct >= 0.0 AND utilization_rate_pct <= 100.0;

invalid_infra = FILTER deduped BY
    infrastructure_record_id IS NULL OR TRIM(infrastructure_record_id) == '' OR
    facility_name IS NULL OR TRIM(facility_name) == '' OR
    facility_type IS NULL OR TRIM(facility_type) == '' OR
    year IS NULL OR year < 1957 OR year > 2035 OR
    utilization_rate_pct IS NULL OR utilization_rate_pct < 0.0 OR utilization_rate_pct > 100.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_infra = FOREACH valid_infra GENERATE
    infrastructure_record_id, date, year, month, facility_name,
    facility_type, agency_id, agency_name, location, utilization_rate_pct,
    queued_backlog_hours, maintenance_downtime_days, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_infra BY year ASC, month ASC, facility_type ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_infra = FOREACH invalid_infra GENERATE
    infrastructure_record_id, facility_name, facility_type, year, utilization_rate_pct,
    'INVALID_UTILIZATION_OR_BAD_YEAR_OR_NULL_NAME' AS rejection_reason;

-- ---- AGGREGATION: infrastructure by facility type ------------------------
by_facility_type = GROUP silver_infra BY facility_type;
agg_facility = FOREACH by_facility_type GENERATE
    group AS facility_type,
    COUNT(silver_infra) AS total_records,
    AVG(silver_infra.utilization_rate_pct) AS avg_utilization_pct,
    AVG(silver_infra.queued_backlog_hours) AS avg_backlog_hours,
    AVG(silver_infra.maintenance_downtime_days) AS avg_downtime_days;

-- ---- AGGREGATION: by agency ----------------------------------------------
by_agency = GROUP silver_infra BY agency_name;
agg_agency = FOREACH by_agency GENERATE
    group AS agency_name,
    COUNT(silver_infra) AS facility_count,
    AVG(silver_infra.utilization_rate_pct) AS avg_utilization_pct;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_infrastructure'
    USING PigStorage(',');

STORE quarantine_infra INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_infrastructure_rejected'
    USING PigStorage(',');

STORE agg_facility INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_infrastructure_analytics'
    USING PigStorage(',');

STORE agg_agency INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_infrastructure_by_agency'
    USING PigStorage(',');
