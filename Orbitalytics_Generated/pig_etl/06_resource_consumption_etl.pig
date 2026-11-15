-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 06
-- Domain: Resource Consumption
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/resource_consumption/resource_consumption.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_resource_consumption
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_resource_consumption_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_resource_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_resource = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/resource_consumption/resource_consumption.csv'
    USING PigStorage(',')
    AS (
        consumption_id:chararray, date:chararray, year:int, month:int,
        quarter:chararray, resource_id:chararray, resource_name:chararray,
        resource_category:chararray, agency_id:chararray, agency_name:chararray,
        mission_id:chararray, quantity_consumed:double, unit_of_measure:chararray,
        procurement_cost_k_usd:double, data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_resource BY consumption_id != 'consumption_id';

-- ---- DISTINCT on consumption_id ------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_resource = FILTER deduped BY
    consumption_id IS NOT NULL AND TRIM(consumption_id) != '' AND
    resource_name IS NOT NULL AND TRIM(resource_name) != '' AND
    resource_category IS NOT NULL AND TRIM(resource_category) != '' AND
    year IS NOT NULL AND year >= 1957 AND year <= 2035 AND
    quantity_consumed IS NOT NULL AND quantity_consumed > 0.0 AND
    procurement_cost_k_usd IS NOT NULL AND procurement_cost_k_usd > 0.0;

invalid_resource = FILTER deduped BY
    consumption_id IS NULL OR TRIM(consumption_id) == '' OR
    resource_name IS NULL OR TRIM(resource_name) == '' OR
    resource_category IS NULL OR TRIM(resource_category) == '' OR
    year IS NULL OR year < 1957 OR year > 2035 OR
    quantity_consumed IS NULL OR quantity_consumed <= 0.0 OR
    procurement_cost_k_usd IS NULL OR procurement_cost_k_usd <= 0.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_resource = FOREACH valid_resource GENERATE
    consumption_id, date, year, month, quarter, resource_id, resource_name,
    resource_category, agency_id, agency_name, mission_id, quantity_consumed,
    unit_of_measure, procurement_cost_k_usd, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_resource BY year ASC, month ASC, resource_category ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_resource = FOREACH invalid_resource GENERATE
    consumption_id, resource_name, resource_category, year, quantity_consumed,
    'INVALID_QUANTITY_OR_NULL_RESOURCE_OR_BAD_YEAR' AS rejection_reason;

-- ---- AGGREGATION: consumption by resource category -----------------------
by_cat_year = GROUP silver_resource BY (resource_category, year);
agg_cat_year = FOREACH by_cat_year GENERATE
    FLATTEN(group) AS (resource_category, year),
    SUM(silver_resource.quantity_consumed) AS total_quantity,
    SUM(silver_resource.procurement_cost_k_usd) AS total_cost_k_usd,
    COUNT(silver_resource) AS record_count;

-- ---- AGGREGATION: by agency ----------------------------------------------
by_agency = GROUP silver_resource BY agency_name;
agg_agency = FOREACH by_agency GENERATE
    group AS agency_name,
    SUM(silver_resource.quantity_consumed) AS total_consumed,
    SUM(silver_resource.procurement_cost_k_usd) AS total_cost_k_usd,
    COUNT(silver_resource) AS record_count;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_resource_consumption'
    USING PigStorage(',');

STORE quarantine_resource INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_resource_consumption_rejected'
    USING PigStorage(',');

STORE agg_cat_year INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_resource_analytics'
    USING PigStorage(',');

STORE agg_agency INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_resource_by_agency'
    USING PigStorage(',');

