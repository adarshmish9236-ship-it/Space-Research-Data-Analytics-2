-- =============================================================================
-- Query 15: Resource Consumption and Launch Activity Correlation Matrix
-- Advanced Features: Fact-to-Fact Join across Partitioned Domains, Efficiency Ratios
-- =============================================================================
USE orbitalytics;

WITH annual_launches AS (
    SELECT
        year,
        COUNT(launch_id) AS total_launches,
        ROUND(SUM(payload_to_orbit_kg), 1) AS total_payload_launched_kg,
        ROUND(SUM(launch_cost_m_usd), 2) AS total_launch_cost_m_usd
    FROM fact_launch_activity
    GROUP BY year
),
annual_propellants AS (
    SELECT
        year,
        ROUND(SUM(quantity_consumed), 1) AS total_propellant_consumed_kg,
        ROUND(SUM(procurement_cost_k_usd) / 1000.0, 2) AS total_propellant_cost_m_usd
    FROM fact_resource_consumption
    GROUP BY year
)
SELECT
    l.year,
    l.total_launches,
    l.total_payload_launched_kg,
    l.total_launch_cost_m_usd,
    p.total_propellant_consumed_kg,
    p.total_propellant_cost_m_usd,
    ROUND(p.total_propellant_consumed_kg / NULLIF(l.total_launches, 0), 1) AS avg_propellant_per_launch_kg,
    ROUND(p.total_propellant_consumed_kg / NULLIF(l.total_payload_launched_kg, 0), 2) AS propellant_to_payload_ratio,
    ROUND(l.total_launch_cost_m_usd / NULLIF(l.total_payload_launched_kg / 1000.0, 0), 2) AS launch_cost_per_metric_ton_m_usd
FROM annual_launches l
JOIN annual_propellants p ON l.year = p.year
ORDER BY l.year ASC;

