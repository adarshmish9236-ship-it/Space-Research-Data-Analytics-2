-- ORBITALYTICS Phase 10: Pig Benchmark WL5
MSN = LOAD '/orbitalytics/benchmark/$SCALE/space_missions/space_missions.csv' USING PigStorage(',') AS (
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
MSN_F = FILTER MSN BY mission_id != 'mission_id';
MSN_GRP = GROUP MSN_F BY (agency, year_val);
MSN_AGG = FOREACH MSN_GRP GENERATE group.agency AS agency, group.year_val AS year_val, COUNT(MSN_F) AS m_cnt, SUM(MSN_F.budget_million_usd) AS m_bgt;

EXP = LOAD '/orbitalytics/benchmark/$SCALE/agency_expenditure/agency_research_expenditures.csv' USING PigStorage(',') AS (
    date_val:chararray,
    year_val:int,
    month_val:int,
    agency:chararray,
    rd_expenditure_million_usd:double,
    infrastructure_expenditure_million_usd:double,
    mission_operations_million_usd:double,
    total_monthly_expenditure_million_usd:double
);
EXP_F = FILTER EXP BY date_val != 'date';
EXP_GRP = GROUP EXP_F BY (agency, year_val);
EXP_AGG = FOREACH EXP_GRP GENERATE group.agency AS agency, group.year_val AS year_val, SUM(EXP_F.total_monthly_expenditure_million_usd) AS e_tot;

JOINED = JOIN MSN_AGG BY (agency, year_val), EXP_AGG BY (agency, year_val);
RESULT = FOREACH JOINED GENERATE MSN_AGG::agency, MSN_AGG::year_val, MSN_AGG::m_cnt, MSN_AGG::m_bgt, EXP_AGG::e_tot, (MSN_AGG::m_bgt / EXP_AGG::e_tot) * 100.0;
rmf /orbitalytics/benchmark_out/pig_wl5_$SCALE;
STORE RESULT INTO '/orbitalytics/benchmark_out/pig_wl5_$SCALE' USING PigStorage('\t');
