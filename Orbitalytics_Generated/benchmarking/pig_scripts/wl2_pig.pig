-- ORBITALYTICS Phase 10: Pig Benchmark WL2
A = LOAD '/orbitalytics/benchmark/$SCALE/resource_consumption/resource_consumption.csv' USING PigStorage(',') AS (
    date_val:chararray,
    year_val:int,
    month_val:int,
    resource_name:chararray,
    quantity_consumed:double,
    unit_of_measure:chararray,
    procurement_cost_k_usd:double
);
B = FILTER A BY date_val != 'date' AND date_val != 'consumption_id';
C = GROUP B BY year_val;
D = FOREACH C GENERATE group AS year_val, SUM(B.quantity_consumed) AS total_qty, SUM(B.procurement_cost_k_usd) AS total_cost, AVG(B.quantity_consumed) AS avg_qty, COUNT(B) AS rec_cnt;
rmf /orbitalytics/benchmark_out/pig_wl2_$SCALE;
STORE D INTO '/orbitalytics/benchmark_out/pig_wl2_$SCALE' USING PigStorage('\t');
