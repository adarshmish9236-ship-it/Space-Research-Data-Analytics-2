-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 07
-- Domain: Satellite Manufacturing Requirements
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/manufacturing/satellite_manufacturing_requirements.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_manufacturing
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_manufacturing_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_manufacturing_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_manufacturing = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/manufacturing/satellite_manufacturing_requirements.csv'
    USING PigStorage(',')
    AS (
        order_id:chararray, agency_id:chararray, agency_client:chararray,
        satellite_class:chararray, units_ordered:int, delivery_year:int,
        cleanroom_hours_required:double, vibration_testing_pass:chararray,
        contract_value_million_usd:double, data_origin:chararray,
        country:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_manufacturing BY order_id != 'order_id';

-- ---- DISTINCT on order_id -------------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_mfg = FILTER deduped BY
    order_id IS NOT NULL AND TRIM(order_id) != '' AND
    satellite_class IS NOT NULL AND TRIM(satellite_class) != '' AND
    units_ordered IS NOT NULL AND units_ordered > 0 AND
    delivery_year IS NOT NULL AND delivery_year >= 1957 AND delivery_year <= 2035 AND
    contract_value_million_usd IS NOT NULL AND contract_value_million_usd > 0.0;

invalid_mfg = FILTER deduped BY
    order_id IS NULL OR TRIM(order_id) == '' OR
    satellite_class IS NULL OR TRIM(satellite_class) == '' OR
    units_ordered IS NULL OR units_ordered <= 0 OR
    delivery_year IS NULL OR delivery_year < 1957 OR delivery_year > 2035 OR
    contract_value_million_usd IS NULL OR contract_value_million_usd <= 0.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_mfg = FOREACH valid_mfg GENERATE
    order_id, agency_id, agency_client, satellite_class, units_ordered,
    delivery_year, cleanroom_hours_required, vibration_testing_pass,
    contract_value_million_usd, data_origin, country;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_mfg BY delivery_year ASC, satellite_class ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_mfg = FOREACH invalid_mfg GENERATE
    order_id, satellite_class, delivery_year, contract_value_million_usd,
    'INVALID_UNITS_OR_CONTRACT_VALUE_OR_DELIVERY_YEAR' AS rejection_reason;

-- ---- AGGREGATION: manufacturing by satellite class -----------------------
by_class = GROUP silver_mfg BY satellite_class;
agg_class = FOREACH by_class GENERATE
    group AS satellite_class,
    SUM(silver_mfg.units_ordered) AS total_units_ordered,
    SUM(silver_mfg.contract_value_million_usd) AS total_contract_value_m_usd,
    AVG(silver_mfg.cleanroom_hours_required) AS avg_cleanroom_hours;

-- ---- AGGREGATION: manufacturing by delivery year -------------------------
by_year = GROUP silver_mfg BY delivery_year;
agg_year = FOREACH by_year GENERATE
    group AS delivery_year,
    SUM(silver_mfg.units_ordered) AS total_units,
    SUM(silver_mfg.contract_value_million_usd) AS total_value_m_usd;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_manufacturing'
    USING PigStorage(',');

STORE quarantine_mfg INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_manufacturing_rejected'
    USING PigStorage(',');

STORE agg_class INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_manufacturing_analytics'
    USING PigStorage(',');

STORE agg_year INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_manufacturing_by_year'
    USING PigStorage(',');

