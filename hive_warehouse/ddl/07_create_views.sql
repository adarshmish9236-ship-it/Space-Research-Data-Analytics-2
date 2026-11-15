-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 07_create_views.sql
-- Analytical Business Intelligence Views
-- =============================================================================

USE orbitalytics;

SET hive.strict.checks.cartesian.product=false;
SET hive.mapred.mode=nonstrict;

-- 1. View: Annual Equipment Subsystem Demand & Fulfillment
DROP VIEW IF EXISTS vw_annual_equipment_demand_summary;
CREATE VIEW vw_annual_equipment_demand_summary AS
SELECT
    f.year,
    f.component_category,
    COUNT(f.demand_id) AS total_orders,
    ROUND(SUM(f.units_demanded), 1) AS total_units_demanded,
    ROUND(SUM(f.units_manufactured + f.units_procured), 1) AS total_units_supplied,
    ROUND((SUM(f.units_manufactured + f.units_procured) / SUM(f.units_demanded)) * 100.0, 2) AS fulfillment_rate_pct,
    ROUND(SUM(f.total_demand_value_m_usd), 2) AS total_value_million_usd,
    ROUND(AVG(f.lead_time_days), 1) AS avg_lead_time_days
FROM fact_equipment_demand f
GROUP BY f.year, f.component_category;

-- 2. View: Space Agency Launch & Mission Performance
DROP VIEW IF EXISTS vw_agency_mission_performance;
CREATE VIEW vw_agency_mission_performance AS
SELECT
    a.agency_key,
    a.agency_name,
    a.country,
    a.agency_type,
    COUNT(m.mission_id) AS total_missions,
    SUM(CASE WHEN m.status IN ('Completed', 'Successful', 'Operational') THEN 1 ELSE 0 END) AS successful_missions,
    ROUND((SUM(CASE WHEN m.status IN ('Completed', 'Successful', 'Operational') THEN 1 ELSE 0 END) / COUNT(m.mission_id)) * 100.0, 2) AS success_rate_pct,
    ROUND(SUM(m.budget_m_usd), 2) AS total_budget_m_usd,
    ROUND(AVG(m.duration_days), 1) AS avg_mission_duration_days,
    SUM(m.crew_size) AS total_crew_deployed
FROM stg_missions m
JOIN dim_agency a ON m.agency_id = a.agency_key
GROUP BY a.agency_key, a.agency_name, a.country, a.agency_type;

-- 3. View: Annual Launch Market Commercialization & Payload Throughput
DROP VIEW IF EXISTS vw_launch_market_commercialization;
CREATE VIEW vw_launch_market_commercialization AS
SELECT
    year,
    COUNT(launch_id) AS total_launches,
    SUM(CASE WHEN launch_outcome = 'Success' THEN 1 ELSE 0 END) AS successful_launches,
    ROUND((SUM(CASE WHEN launch_outcome = 'Success' THEN 1 ELSE 0 END) / COUNT(launch_id)) * 100.0, 2) AS launch_success_rate_pct,
    SUM(CASE WHEN commercial_flag IN ('1', 'True', 'Commercial', 'true') THEN 1 ELSE 0 END) AS commercial_launches,
    ROUND((SUM(CASE WHEN commercial_flag IN ('1', 'True', 'Commercial', 'true') THEN 1 ELSE 0 END) / COUNT(launch_id)) * 100.0, 2) AS commercial_share_pct,
    ROUND(SUM(launch_cost_m_usd), 2) AS total_launch_cost_m_usd,
    ROUND(AVG(launch_cost_m_usd), 2) AS avg_launch_cost_m_usd,
    ROUND(SUM(payload_to_orbit_kg), 1) AS total_payload_to_orbit_kg
FROM fact_launch_activity
GROUP BY year;
