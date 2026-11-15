-- =============================================================================
-- Query 09: Launch Activity Trends and Commercialization Rate
-- Advanced Features: Partitioned Fact Filtering, Multi-metric Trending
-- =============================================================================
USE orbitalytics;

SELECT
    year,
    COUNT(launch_id) AS total_launches,
    SUM(CASE WHEN launch_outcome = 'Success' THEN 1 ELSE 0 END) AS successful_launches,
    ROUND((SUM(CASE WHEN launch_outcome = 'Success' THEN 1 ELSE 0 END) / COUNT(launch_id)) * 100.0, 2) AS success_rate_pct,
    SUM(CASE WHEN commercial_flag IN ('1', 'True', 'Commercial', 'true') THEN 1 ELSE 0 END) AS commercial_launches,
    ROUND((SUM(CASE WHEN commercial_flag IN ('1', 'True', 'Commercial', 'true') THEN 1 ELSE 0 END) / COUNT(launch_id)) * 100.0, 2) AS commercial_share_pct,
    ROUND(SUM(launch_cost_m_usd), 2) AS total_launch_spend_m_usd,
    ROUND(AVG(launch_cost_m_usd), 2) AS avg_cost_per_launch_m_usd,
    ROUND(SUM(payload_to_orbit_kg), 1) AS total_payload_to_orbit_kg
FROM fact_launch_activity
GROUP BY year
ORDER BY year ASC;

