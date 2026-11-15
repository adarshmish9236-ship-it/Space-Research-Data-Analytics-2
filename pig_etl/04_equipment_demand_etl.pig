
-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 04
-- Domain: Equipment Component Demand
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/equipment_demand/equipment_component_demand.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_equipment_demand
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_equipment_demand_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_equipment_demand_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_demand = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/equipment_demand/equipment_component_demand.csv'
    USING PigStorage(',')
    AS (
        demand_id:chararray, date:chararray, year:int, month:int, quarter:chararray,
        component_id:chararray, component_name:chararray, component_category:chararray,
        agency_id:chararray, agency_name:chararray, target_satellite_class:chararray,
        units_demanded:double, units_manufactured:double, units_procured:double,
        unit_of_measure:chararray, avg_unit_cost_thousand_usd:double,
        total_demand_value_million_usd:double, lead_time_days:int,
        shortage_risk:chararray, data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_demand BY demand_id != 'demand_id';

-- ---- DISTINCT on demand_id ------------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_demand = FILTER deduped BY
    demand_id IS NOT NULL AND TRIM(demand_id) != '' AND
    component_name IS NOT NULL AND TRIM(component_name) != '' AND
    component_category IS NOT NULL AND TRIM(component_category) != '' AND
    units_demanded IS NOT NULL AND units_demanded >= 0.0 AND
    year IS NOT NULL AND year >= 1957 AND year <= 2035 AND
    avg_unit_cost_thousand_usd IS NOT NULL AND avg_unit_cost_thousand_usd > 0.0;

invalid_demand = FILTER deduped BY
    demand_id IS NULL OR TRIM(demand_id) == '' OR
    component_name IS NULL OR TRIM(component_name) == '' OR
    component_category IS NULL OR TRIM(component_category) == '' OR
    units_demanded IS NULL OR units_demanded < 0.0 OR
    year IS NULL OR year < 1957 OR year > 2035 OR
    avg_unit_cost_thousand_usd IS NULL OR avg_unit_cost_thousand_usd <= 0.0;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_demand = FOREACH valid_demand GENERATE
    demand_id, date, year, month, quarter, component_id, component_name,
    component_category, agency_id, agency_name, target_satellite_class,
    units_demanded, units_manufactured, units_procured, unit_of_measure,
    avg_unit_cost_thousand_usd, total_demand_value_million_usd,
    lead_time_days, shortage_risk, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_demand BY year ASC, month ASC, component_category ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_demand = FOREACH invalid_demand GENERATE
    demand_id, component_name, component_category, year, units_demanded,
    'INVALID_UNITS_OR_NULL_COMPONENT_OR_ZERO_COST' AS rejection_reason;

-- ---- AGGREGATION: demand by component category & year -------------------
by_cat_year = GROUP silver_demand BY (component_category, year);
agg_cat_year = FOREACH by_cat_year GENERATE
    FLATTEN(group) AS (component_category, year),
    SUM(silver_demand.units_demanded) AS total_units_demanded,
    SUM(silver_demand.units_manufactured) AS total_units_manufactured,
    SUM(silver_demand.total_demand_value_million_usd) AS total_demand_value_m_usd,
    AVG(silver_demand.lead_time_days) AS avg_lead_time_days;

-- ---- AGGREGATION: top components by demand volume -----------------------
by_component = GROUP silver_demand BY component_name;
agg_component = FOREACH by_component GENERATE
    group AS component_name,
    SUM(silver_demand.units_demanded) AS total_demanded,
    SUM(silver_demand.total_demand_value_million_usd) AS total_value_m_usd,
    AVG(silver_demand.avg_unit_cost_thousand_usd) AS avg_cost_k_usd,
    AVG(silver_demand.lead_time_days) AS avg_lead_time_days;

-- ---- AGGREGATION: shortage risk summary ---------------------------------
by_shortage = GROUP silver_demand BY shortage_risk;
agg_shortage = FOREACH by_shortage GENERATE
    group AS shortage_risk,
    COUNT(silver_demand) AS record_count,
    SUM(silver_demand.units_demanded) AS total_units_at_risk;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_equipment_demand'
    USING PigStorage(',');

STORE quarantine_demand INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_equipment_demand_rejected'
    USING PigStorage(',');

STORE agg_cat_year INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_equipment_demand_analytics'
    USING PigStorage(',');

STORE agg_component INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_component_demand_summary'
    USING PigStorage(',');

STORE agg_shortage INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_shortage_risk_summary'
    USING PigStorage(',');
