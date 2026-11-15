-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 05
-- Domain: Agency Research Expenditure
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/agency_expenditure/agency_research_expenditures.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_agency_expenditure
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_agency_expenditure_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_agency_expenditure_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_expenditure = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/agency_expenditure/agency_research_expenditures.csv'
    USING PigStorage(',')
    AS (
        expenditure_id:chararray, date:chararray, year:int, month:int,
        quarter:chararray, agency_id:chararray, agency_name:chararray,
        country:chararray, rd_expenditure_million_usd:double,
        infrastructure_expenditure_million_usd:double,
        mission_operations_million_usd:double,
        total_monthly_expenditure_million_usd:double,
        currency:chararray, data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_expenditure BY expenditure_id != 'expenditure_id';

-- ---- DISTINCT on expenditure_id -------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_expenditure = FILTER deduped BY
    expenditure_id IS NOT NULL AND TRIM(expenditure_id) != '' AND
    agency_name IS NOT NULL AND TRIM(agency_name) != '' AND
    country IS NOT NULL AND TRIM(country) != '' AND
    year IS NOT NULL AND year >= 1957 AND year <= 2035 AND
    total_monthly_expenditure_million_usd IS NOT NULL AND
    total_monthly_expenditure_million_usd > 0.0;

invalid_expenditure = FILTER deduped BY
    expenditure_id IS NULL OR TRIM(expenditure_id) == '' OR
    agency_name IS NULL OR TRIM(agency_name) == '' OR
    country IS NULL OR TRIM(country) == '' OR
    year IS NULL OR year < 1957 OR year > 2035 OR
    total_monthly_expenditure_million_usd IS NULL OR
    total_monthly_expenditure_million_usd <= 0.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_expenditure = FOREACH valid_expenditure GENERATE
    expenditure_id, date, year, month, quarter, agency_id, agency_name,
    country, rd_expenditure_million_usd, infrastructure_expenditure_million_usd,
    mission_operations_million_usd, total_monthly_expenditure_million_usd,
    currency, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_expenditure BY year ASC, month ASC, agency_name ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_expenditure = FOREACH invalid_expenditure GENERATE
    expenditure_id, agency_name, year, total_monthly_expenditure_million_usd,
    'INVALID_EXPENDITURE_OR_NULL_AGENCY_OR_BAD_YEAR' AS rejection_reason;

-- ---- AGGREGATION: annual expenditure by agency ---------------------------
by_agency_year = GROUP silver_expenditure BY (agency_name, year);
agg_annual = FOREACH by_agency_year GENERATE
    FLATTEN(group) AS (agency_name, year),
    SUM(silver_expenditure.rd_expenditure_million_usd) AS annual_rd_m_usd,
    SUM(silver_expenditure.infrastructure_expenditure_million_usd) AS annual_infra_m_usd,
    SUM(silver_expenditure.mission_operations_million_usd) AS annual_ops_m_usd,
    SUM(silver_expenditure.total_monthly_expenditure_million_usd) AS annual_total_m_usd;

-- ---- AGGREGATION: by country ---------------------------------------------
by_country = GROUP silver_expenditure BY country;
agg_country = FOREACH by_country GENERATE
    group AS country,
    COUNT(silver_expenditure) AS record_count,
    SUM(silver_expenditure.total_monthly_expenditure_million_usd) AS cumulative_expenditure_m_usd,
    AVG(silver_expenditure.total_monthly_expenditure_million_usd) AS avg_monthly_expenditure_m_usd;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_agency_expenditure'
    USING PigStorage(',');

STORE quarantine_expenditure INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_agency_expenditure_rejected'
    USING PigStorage(',');

STORE agg_annual INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_agency_expenditure_analytics'
    USING PigStorage(',');

STORE agg_country INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_expenditure_by_country'
    USING PigStorage(',');

