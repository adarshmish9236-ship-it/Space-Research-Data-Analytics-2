-- =============================================================================
-- ORBITALYTICS Phase 4 — Pig ETL Script 09
-- Domain: Research Investment and Future Projects
-- Input:  hdfs://namenode:9000/orbitalytics/bronze/research_projects/research_investment_future_projects.csv
-- Output: hdfs://namenode:9000/orbitalytics/silver/pig_research_projects
--         hdfs://namenode:9000/orbitalytics/quarantine/pig_research_projects_rejected
--         hdfs://namenode:9000/orbitalytics/gold/pig_research_projects_analytics
-- =============================================================================

SET pig.noSplitCombination true;
SET mapreduce.job.reduces 1;

-- ---- LOAD -----------------------------------------------------------------
raw_research = LOAD 'hdfs://namenode:9000/orbitalytics/bronze/research_projects/research_investment_future_projects.csv'
    USING PigStorage(',')
    AS (
        project_id:chararray, project_title:chararray, agency_id:chararray,
        lead_agency:chararray, country:chararray, research_theme:chararray,
        target_commencement_year:int, estimated_investment_million_usd:double,
        priority_tier:chararray, technology_readiness_level:int,
        project_status:chararray, data_origin:chararray
    );

-- ---- FILTER header --------------------------------------------------------
no_header = FILTER raw_research BY project_id != 'project_id';

-- ---- DISTINCT on project_id -----------------------------------------------
deduped = DISTINCT no_header;

-- ---- VALIDATE -------------------------------------------------------------
valid_research = FILTER deduped BY
    project_id IS NOT NULL AND TRIM(project_id) != '' AND
    project_title IS NOT NULL AND TRIM(project_title) != '' AND
    research_theme IS NOT NULL AND TRIM(research_theme) != '' AND
    target_commencement_year IS NOT NULL AND target_commencement_year >= 1957 AND target_commencement_year <= 2045 AND
    estimated_investment_million_usd IS NOT NULL AND estimated_investment_million_usd > 0.0 AND
    technology_readiness_level IS NOT NULL AND technology_readiness_level >= 1 AND technology_readiness_level <= 9;

invalid_research = FILTER deduped BY
    project_id IS NULL OR TRIM(project_id) == '' OR
    project_title IS NULL OR TRIM(project_title) == '' OR
    research_theme IS NULL OR TRIM(research_theme) == '' OR
    target_commencement_year IS NULL OR target_commencement_year < 1957 OR target_commencement_year > 2045 OR
    estimated_investment_million_usd IS NULL OR estimated_investment_million_usd <= 0.0 OR
    technology_readiness_level IS NULL OR technology_readiness_level < 1 OR technology_readiness_level > 9;

-- ---- TRANSFORM silver -----------------------------------------------------
silver_research = FOREACH valid_research GENERATE
    project_id, project_title, agency_id, lead_agency, country,
    research_theme, target_commencement_year, estimated_investment_million_usd,
    priority_tier, technology_readiness_level, project_status, data_origin;

-- ---- ORDER ----------------------------------------------------------------
silver_ordered = ORDER silver_research BY target_commencement_year ASC, research_theme ASC;

-- ---- QUARANTINE -----------------------------------------------------------
quarantine_research = FOREACH invalid_research GENERATE
    project_id, project_title, research_theme, estimated_investment_million_usd,
    'INVALID_TRL_OR_BAD_YEAR_OR_NEGATIVE_INVESTMENT' AS rejection_reason;

-- ---- AGGREGATION: investment by research theme ---------------------------
by_theme = GROUP silver_research BY research_theme;
agg_theme = FOREACH by_theme GENERATE
    group AS research_theme,
    COUNT(silver_research) AS project_count,
    SUM(silver_research.estimated_investment_million_usd) AS total_investment_m_usd,
    AVG(silver_research.estimated_investment_million_usd) AS avg_investment_m_usd,
    AVG(silver_research.technology_readiness_level) AS avg_trl;

-- ---- AGGREGATION: by priority tier ---------------------------------------
by_tier = GROUP silver_research BY priority_tier;
agg_tier = FOREACH by_tier GENERATE
    group AS priority_tier,
    COUNT(silver_research) AS project_count,
    SUM(silver_research.estimated_investment_million_usd) AS total_investment_m_usd;

-- ---- STORE ----------------------------------------------------------------
STORE silver_ordered INTO 'hdfs://namenode:9000/orbitalytics/silver/pig_research_projects'
    USING PigStorage(',');

STORE quarantine_research INTO 'hdfs://namenode:9000/orbitalytics/quarantine/pig_research_projects_rejected'
    USING PigStorage(',');

STORE agg_theme INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_research_projects_analytics'
    USING PigStorage(',');

STORE agg_tier INTO 'hdfs://namenode:9000/orbitalytics/gold/pig_research_by_tier'
    USING PigStorage(',');

