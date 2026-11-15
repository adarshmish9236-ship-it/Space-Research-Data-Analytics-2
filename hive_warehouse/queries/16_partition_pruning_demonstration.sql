-- =============================================================================
-- Query 16: Partition Pruning Demonstration and EXPLAIN Plan Validation
-- Advanced Features: EXPLAIN Plan Inspection, Dynamic Partition Pruner Verification
-- =============================================================================
USE orbitalytics;

-- 1. EXPLAIN Plan showing Partition Pruning on fact_equipment_demand for year = 2024
EXPLAIN
SELECT
    component_category,
    COUNT(demand_id) AS orders_count,
    ROUND(SUM(units_demanded), 1) AS total_units_demanded,
    ROUND(SUM(total_demand_value_m_usd), 2) AS total_spend_m_usd
FROM fact_equipment_demand
WHERE year = 2024
GROUP BY component_category;

-- 2. Execution of Partition Pruned Query
SELECT
    component_category,
    COUNT(demand_id) AS orders_count,
    ROUND(SUM(units_demanded), 1) AS total_units_demanded,
    ROUND(SUM(total_demand_value_m_usd), 2) AS total_spend_m_usd
FROM fact_equipment_demand
WHERE year = 2024
GROUP BY component_category
ORDER BY total_spend_m_usd DESC;

