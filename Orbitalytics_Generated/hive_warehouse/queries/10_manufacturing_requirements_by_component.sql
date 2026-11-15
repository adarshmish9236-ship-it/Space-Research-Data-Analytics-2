-- =============================================================================
-- Query 10: Manufacturing Requirements by Satellite Class and Component
-- Advanced Features: Fact-to-Fact Correlation, Cleanroom Workload Analysis
-- =============================================================================
USE orbitalytics;

SELECT
    satellite_class,
    COUNT(order_id) AS total_orders,
    SUM(units_ordered) AS total_units_ordered,
    ROUND(AVG(cleanroom_hours_required), 1) AS mean_cleanroom_hours,
    ROUND(SUM(cleanroom_hours_required), 1) AS total_cleanroom_workload_hours,
    ROUND(SUM(contract_value_m_usd), 2) AS total_contract_value_m_usd,
    ROUND(AVG(contract_value_m_usd), 2) AS avg_order_contract_m_usd,
    ROUND((SUM(CASE WHEN vibration_testing_pass = 'True' THEN 1 ELSE 0 END) / COUNT(*)) * 100.0, 2) AS qa_test_pass_rate_pct
FROM fact_manufacturing
GROUP BY satellite_class
ORDER BY total_contract_value_m_usd DESC;

