-- ====================================================================
-- Hive Analytical SQL Queries: Space Research & Demand Trends
-- ====================================================================

-- 1. Total Research Expenditure & Mission Count per Agency
SELECT 
    m.agency,
    COUNT(DISTINCT m.mission_id) AS total_missions,
    ROUND(SUM(m.budget_million_usd), 2) AS total_budget_m_usd,
    ROUND(AVG(m.payload_mass_kg), 1) AS avg_payload_kg,
    ROUND(SUM(CASE WHEN m.status IN ('Successful', 'Operational', 'Completed') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS mission_success_rate_pct
FROM space_missions m
GROUP BY m.agency
ORDER BY total_missions DESC;

-- 2. Equipment Component Yearly Demand Trend & Growth Rate
SELECT 
    d.year,
    d.equipment_type,
    SUM(d.units_demanded) AS total_units_demanded,
    ROUND(SUM(d.total_demand_value_million_usd), 2) AS total_demand_value_m_usd,
    ROUND(AVG(d.lead_time_days), 0) AS avg_lead_time_days
FROM equipment_component_demand d
GROUP BY d.year, d.equipment_type
ORDER BY d.year ASC, total_units_demanded DESC;

-- 3. Orbital Constellation Distribution and Power Requirements
SELECT 
    s.orbit_type,
    COUNT(*) AS total_satellites,
    ROUND(AVG(s.altitude_km), 1) AS avg_altitude_km,
    ROUND(AVG(s.power_consumption_w), 1) AS avg_power_watts,
    ROUND(AVG(s.expected_lifetime_years), 1) AS avg_design_lifetime_yrs
FROM satellites_orbital s
WHERE s.operational_status = 'Active'
GROUP BY s.orbit_type
ORDER BY total_satellites DESC;

-- 4. Propellant & Telemetry Critical Resource Consumption by Year
SELECT 
    r.year,
    r.resource_name,
    ROUND(SUM(r.quantity_consumed), 2) AS total_quantity,
    MAX(r.unit_of_measure) AS unit,
    ROUND(SUM(r.procurement_cost_k_usd) / 1000.0, 2) AS total_procurement_cost_m_usd
FROM resource_consumption r
GROUP BY r.year, r.resource_name
ORDER BY r.year ASC, total_quantity DESC;

-- 5. Launch Vehicle Reliability & Commercialization Trends
SELECT 
    l.vehicle,
    COUNT(*) AS total_launches,
    ROUND(SUM(CASE WHEN l.launch_outcome = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS success_rate_pct,
    ROUND(AVG(l.launch_cost_million_usd), 2) AS avg_launch_cost_m_usd,
    ROUND(SUM(l.payload_to_orbit_kg) / 1000.0, 2) AS total_payload_delivered_metric_tons,
    ROUND(SUM(CASE WHEN l.commercial_flag = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS commercial_share_pct
FROM launch_activities l
GROUP BY l.vehicle
ORDER BY total_launches DESC;

