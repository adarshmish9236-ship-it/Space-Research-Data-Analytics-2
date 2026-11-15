-- ORBITALYTICS Phase 10: Pig Benchmark WL3
A = LOAD '/orbitalytics/benchmark/$SCALE/space_missions/space_missions.csv' USING PigStorage(',') AS (
    mission_id:chararray,
    mission_name:chararray,
    agency:chararray,
    mission_type:chararray,
    launch_date:chararray,
    year_val:int,
    quarter:chararray,
    budget_million_usd:double,
    payload_mass_kg:double,
    status:chararray,
    crew_size:int,
    duration_days:double
);
B = FILTER A BY mission_id != 'mission_id';
C = GROUP B BY agency;
D = FOREACH C GENERATE group AS agency, COUNT(B) AS total_missions, SUM(B.budget_million_usd) AS total_budget, AVG(B.payload_mass_kg) AS avg_payload, AVG(B.duration_days) AS avg_duration;
rmf /orbitalytics/benchmark_out/pig_wl3_$SCALE;
STORE D INTO '/orbitalytics/benchmark_out/pig_wl3_$SCALE' USING PigStorage('\t');
