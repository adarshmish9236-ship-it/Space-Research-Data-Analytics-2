-- ORBITALYTICS Phase 10: Pig Benchmark WL1
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
C = GROUP B BY equipment_type;
D = FOREACH C GENERATE group AS equipment_type, SUM(B.units_demanded) AS total_units, AVG(B.avg_unit_cost_thousand_usd) AS avg_cost, SUM(B.total_demand_value_million_usd) AS total_val, COUNT(B) AS rec_cnt;
rmf /orbitalytics/benchmark_out/pig_wl1_$SCALE;
STORE D INTO '/orbitalytics/benchmark_out/pig_wl1_$SCALE' USING PigStorage('\t');
