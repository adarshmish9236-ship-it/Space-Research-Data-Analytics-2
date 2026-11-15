-- ======================================================================
-- ORBITALYTICS - Apache Pig Latin Data Processing Script
-- Analyzes discrete satellite component demand from HDFS
-- Calculates total aggregated units demanded and average value by component
-- ======================================================================

-- 1. Load component demand records from HDFS
raw_demand = LOAD 'hdfs://namenode:9000/space_research/raw/equipment_component_demand.csv' USING PigStorage(',') AS (
    demand_id:chararray,
    date:chararray,
    year:int,
    month:int,
    quarter:chararray,
    component_id:chararray,
    component_name:chararray,
    component_category:chararray,
    agency_id:chararray,
    agency_name:chararray,
    target_satellite_class:chararray,
    units_demanded:int,
    units_manufactured:int,
    units_procured:int,
    unit_of_measure:chararray,
    avg_unit_cost_thousand_usd:float,
    total_demand_value_million_usd:float,
    lead_time_days:int,
    shortage_risk:chararray,
    data_origin:chararray
);

-- 2. Filter header row and invalid units
filtered_demand = FILTER raw_demand BY (demand_id != 'demand_id') AND (units_demanded > 0);

-- 3. Group by component category and component name
grouped_components = GROUP filtered_demand BY (component_category, component_name);

-- 4. Aggregate sum of units and average financial footprint
component_aggregations = FOREACH grouped_components GENERATE
    FLATTEN(group) AS (category, component),
    COUNT(filtered_demand) AS observation_count,
    SUM(filtered_demand.units_demanded) AS total_units_demanded,
    ROUND(AVG(filtered_demand.total_demand_value_million_usd) * 100.0) / 100.0 AS avg_demand_value_m_usd;

-- 5. Order by total units demanded descending
ordered_summary = ORDER component_aggregations BY total_units_demanded DESC;

-- 6. Store result back into HDFS analytics directory
STORE ordered_summary INTO 'hdfs://namenode:9000/space_research/analytics/pig_demand_summary' USING PigStorage('\t');

