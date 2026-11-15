-- =============================================================================
-- Query 13: Spaceport Infrastructure Throughput by Geographic Location
-- Advanced Features: Dimension-Fact Aggregations, Geographic Performance
-- =============================================================================
USE orbitalytics;

SELECT
    l.launch_site,
    l.country,
    l.operator_type,
    COUNT(f.launch_id) AS total_launches_hosted,
    SUM(CASE WHEN f.launch_outcome = 'Success' THEN 1 ELSE 0 END) AS successful_launches,
    ROUND((SUM(CASE WHEN f.launch_outcome = 'Success' THEN 1 ELSE 0 END) / COUNT(f.launch_id)) * 100.0, 2) AS site_success_rate_pct,
    ROUND(SUM(f.payload_to_orbit_kg) / 1000.0, 2) AS total_payload_shipped_metric_tons,
    ROUND(SUM(f.launch_cost_m_usd), 2) AS total_site_economic_activity_m_usd
FROM fact_launch_activity f
JOIN dim_location l ON f.launch_site = l.launch_site
GROUP BY l.launch_site, l.country, l.operator_type
ORDER BY total_launches_hosted DESC;

