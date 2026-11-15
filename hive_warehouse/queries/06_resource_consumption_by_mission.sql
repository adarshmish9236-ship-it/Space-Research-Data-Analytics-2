-- =============================================================================
-- Query 06: Resource Consumption by Space Mission
-- Advanced Features: Fact-Dimension Join, Multi-Level Rollup, Mission Profiling
-- =============================================================================
USE orbitalytics;

SELECT
    m.mission_key,
    m.mission_name,
    m.mission_type,
    m.status AS mission_status,
    COUNT(f.consumption_id) AS consumable_lines,
    ROUND(SUM(f.quantity_consumed), 1) AS total_consumables_mass,
    ROUND(SUM(f.procurement_cost_k_usd) / 1000.0, 2) AS total_consumable_cost_m_usd,
    m.duration_days
FROM fact_resource_consumption f
JOIN dim_mission m ON f.mission_key = m.mission_key
GROUP BY m.mission_key, m.mission_name, m.mission_type, m.status, m.duration_days
ORDER BY total_consumable_cost_m_usd DESC
LIMIT 20;

