-- =============================================================================
-- Query 03: Quarterly Demand Trend Across Aerospace Categories
-- Advanced Features: Multi-dimensional Aggregation, CASE Pivot, Category Breakdown
-- =============================================================================
USE orbitalytics;

SELECT
    quarter,
    COUNT(demand_id) AS total_orders,
    ROUND(SUM(units_demanded), 1) AS total_units_demanded,
    ROUND(SUM(total_demand_value_m_usd), 2) AS total_demand_value_m_usd,
    ROUND(AVG(lead_time_days), 1) AS avg_lead_time_days,
    ROUND(SUM(CASE WHEN shortage_risk = 'High' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS high_shortage_risk_pct
FROM fact_equipment_demand
GROUP BY quarter
ORDER BY quarter ASC;

