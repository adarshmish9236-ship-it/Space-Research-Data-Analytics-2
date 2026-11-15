-- ORBITALYTICS Phase 10: Pig Benchmark WL4
A = LOAD '/orbitalytics/benchmark/$SCALE/equipment_demand/equipment_component_demand.csv' USING PigStorage(',') AS (
    date_val:chararray,
    year_val:int,
    month_val:int,
    equipment_type:chararray,
    units_demanded:int,
    avg_unit_cost_thousand_usd:double,
    total_demand_value_million_usd:double,
    lead_time_days:int,
    shortage_risk:chararray
);
B = FILTER A BY equipment_type != 'equipment_type';
C = GROUP B BY (equipment_type, year_val);
D = FOREACH C GENERATE group.equipment_type AS equipment_type, group.year_val AS year_val, SUM(B.units_demanded) AS total_units, SUM(B.total_demand_value_million_usd) AS total_val, AVG(B.lead_time_days) AS avg_lt;
rmf /orbitalytics/benchmark_out/pig_wl4_$SCALE;
STORE D INTO '/orbitalytics/benchmark_out/pig_wl4_$SCALE' USING PigStorage('\t');
