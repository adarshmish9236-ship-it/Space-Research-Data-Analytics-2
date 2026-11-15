-- =============================================================================
-- Query 01: Total Equipment Demand by Component
-- Advanced Features: Fact-Dimension Join, Aggregation, Sorting, Currency Formatting
-- =============================================================================
USE orbitalytics;

SELECT
    c.component_key,
    c.component_name,
    c.component_category,
    c.standard_lead_time_days,
    COUNT(f.demand_id) AS total_orders,
    ROUND(SUM(f.units_demanded), 1) AS total_units_demanded,
    ROUND(SUM(f.units_manufactured), 1) AS total_units_manufactured,
    ROUND(SUM(f.units_procured), 1) AS total_units_procured,
    ROUND((SUM(f.units_manufactured + f.units_procured) / SUM(f.units_demanded)) * 100.0, 2) AS fulfillment_rate_pct,
    ROUND(SUM(f.total_demand_value_m_usd), 2) AS total_demand_value_m_usd,
    ROUND(AVG(f.lead_time_days), 1) AS actual_avg_lead_time_days
FROM fact_equipment_demand f
JOIN dim_component c ON f.component_key = c.component_key
GROUP BY c.component_key, c.component_name, c.component_category, c.standard_lead_time_days
ORDER BY total_demand_value_m_usd DESC;

