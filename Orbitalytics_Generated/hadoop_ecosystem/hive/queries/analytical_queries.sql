-- ====================================================================
-- ORBITALYTICS: Apache Hive Analytical SQL Queries
-- ====================================================================

-- 1. Agency Exploration Footprint & Mission Success Benchmarks
SELECT 
    m.agency,
    m.country,
    COUNT(DISTINCT m.mission_id) AS total_missions,
    ROUND(SUM(m.mission_budget_million_usd), 2) AS total_budget_m_usd,
    ROUND(AVG(m.payload_mass_kg), 1) AS avg_payload_kg,
    ROUND(SUM(CASE WHEN m.mission_status IN ('Successful', 'Operational', 'Completed') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS mission_success_rate_pct
FROM space_missions m
GROUP BY m.agency, m.country
ORDER BY total_missions DESC;

-- 2. Space Equipment Component Yearly Demand Trend & Lead Times
SELECT 
    d.year,
    d.equipment_type,
    d.equipment_category,
    SUM(d.units_demanded) AS total_units_demanded,
    ROUND(SUM(d.total_demand_value_million_usd), 2) AS total_demand_value_m_usd,
    ROUND(AVG(d.lead_time_days), 0) AS avg_lead_time_days,
    ROUND(AVG(d.avg_unit_cost_thousand_usd), 1) AS avg_unit_cost_k_usd
FROM equipment_component_demand d
GROUP BY d.year, d.equipment_type, d.equipment_category
ORDER BY d.year DESC, total_units_demanded DESC;

-- 3. Active Satellite Constellation Orbits & Power Generation Capacity
SELECT 
    s.orbit_type,
    COUNT(*) AS total_satellites,
    ROUND(AVG(s.orbital_altitude_km), 1) AS avg_altitude_km,
    ROUND(AVG(s.power_capacity_kw), 2) AS avg_power_kw,
    ROUND(AVG(s.expected_lifetime_years), 1) AS avg_expected_lifetime_yrs
FROM satellites_orbital s
WHERE s.operational_status = 'Active'
GROUP BY s.orbit_type
ORDER BY total_satellites DESC;

-- 4. Rocket Launch Vehicle Reliability & Commercial Reusability Shares
SELECT 
    l.vehicle,
    l.agency,
    COUNT(*) AS total_launches,
    ROUND(SUM(CASE WHEN l.launch_outcome = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS success_rate_pct,
    ROUND(AVG(l.launch_cost_million_usd), 2) AS avg_launch_cost_m_usd,
    ROUND(SUM(l.payload_to_orbit_kg) / 1000.0, 1) AS total_payload_delivered_metric_tons,
    ROUND(SUM(CASE WHEN l.commercial_flag = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS commercial_share_pct
FROM launch_activities l
GROUP BY l.vehicle, l.agency
ORDER BY total_launches DESC;

-- 5. Consumables & Propellant Annual Demand
SELECT 
    r.year,
    r.resource_type,
    MAX(r.unit) AS unit_of_measure,
    ROUND(SUM(r.quantity_consumed), 1) AS total_quantity_consumed,
    ROUND(SUM(r.consumption_cost_million_usd), 2) AS total_expenditure_million_usd
FROM resource_consumption r
GROUP BY r.year, r.resource_type
ORDER BY r.year DESC, total_quantity_consumed DESC;

-- 6. Future Multi-Year Exploration Investment Pipeline
SELECT 
    p.agency,
    p.country,
    COUNT(*) AS total_future_projects,
    ROUND(SUM(p.investment_million_usd) / 1000.0, 2) AS total_investment_billion_usd,
    ROUND(AVG(p.technology_readiness_level), 1) AS avg_trl_level
FROM research_investment_future_projects p
GROUP BY p.agency, p.country
ORDER BY total_investment_billion_usd DESC;

