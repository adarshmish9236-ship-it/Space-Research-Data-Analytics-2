-- =============================================================================
-- Query 05: Consumable Resource Consumption by Year
-- Advanced Features: Partitioned Fact Aggregation, Metric Conversion, Top Resources
-- =============================================================================
USE orbitalytics;

SELECT
    f.year,
    r.resource_category,
    COUNT(f.consumption_id) AS consumption_events,
    ROUND(SUM(f.quantity_consumed), 1) AS total_quantity_consumed,
    MAX(f.unit_of_measure) AS unit_of_measure,
    ROUND(SUM(f.procurement_cost_k_usd) / 1000.0, 2) AS total_cost_million_usd,
    ROUND(AVG(f.procurement_cost_k_usd), 2) AS avg_cost_per_event_k_usd
FROM fact_resource_consumption f
JOIN dim_resource r ON f.resource_key = r.resource_key
GROUP BY f.year, r.resource_category
ORDER BY f.year DESC, total_cost_million_usd DESC;

