-- =============================================================================
-- Query 02: Annual Equipment Demand Trend with YoY Growth
-- Advanced Features: Window Functions (LAG), CTE, Year-over-Year Growth Calculation
-- =============================================================================
USE orbitalytics;

WITH annual_stats AS (
    SELECT
        year,
        COUNT(demand_id) AS order_count,
        ROUND(SUM(units_demanded), 1) AS total_units_demanded,
        ROUND(SUM(total_demand_value_m_usd), 2) AS total_demand_value_m_usd,
        ROUND(AVG(avg_unit_cost_k_usd), 2) AS avg_unit_cost_k_usd
    FROM fact_equipment_demand
    GROUP BY year
)
SELECT
    year,
    order_count,
    total_units_demanded,
    LAG(total_units_demanded, 1) OVER (ORDER BY year) AS prev_year_units_demanded,
    ROUND(((total_units_demanded - LAG(total_units_demanded, 1) OVER (ORDER BY year)) / 
           LAG(total_units_demanded, 1) OVER (ORDER BY year)) * 100.0, 2) AS yoy_demand_growth_pct,
    total_demand_value_m_usd,
    avg_unit_cost_k_usd
FROM annual_stats
ORDER BY year ASC;

