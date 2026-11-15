-- =============================================================================
-- Query 14: Mission Activity and Component Demand Correlation Matrix
-- Advanced Features: Multi-Fact Joins, Cross-Domain Analytical Aggregation
-- =============================================================================
USE orbitalytics;

WITH agency_annual_missions AS (
    SELECT
        year,
        agency_name,
        COUNT(mission_id) AS active_missions_count,
        ROUND(SUM(budget_m_usd), 2) AS total_mission_budget_m_usd,
        ROUND(SUM(payload_mass_kg), 1) AS total_mission_payload_kg
    FROM stg_missions
    GROUP BY year, agency_name
),
agency_annual_demand AS (
    SELECT
        year,
        agency_name,
        COUNT(demand_id) AS total_component_orders,
        ROUND(SUM(units_demanded), 1) AS total_units_demanded,
        ROUND(SUM(total_demand_value_m_usd), 2) AS total_component_procurement_m_usd
    FROM fact_equipment_demand
    GROUP BY year, agency_name
)
SELECT
    m.year,
    m.agency_name,
    m.active_missions_count,
    m.total_mission_budget_m_usd,
    m.total_mission_payload_kg,
    COALESCE(d.total_component_orders, 0) AS total_component_orders,
    COALESCE(d.total_units_demanded, 0.0) AS total_units_demanded,
    COALESCE(d.total_component_procurement_m_usd, 0.0) AS total_component_procurement_m_usd,
    ROUND(d.total_component_procurement_m_usd / NULLIF(m.total_mission_budget_m_usd, 0) * 100.0, 2) AS component_share_of_budget_pct
FROM agency_annual_missions m
JOIN agency_annual_demand d ON m.year = d.year AND m.agency_name = d.agency_name
ORDER BY m.year DESC, m.total_mission_budget_m_usd DESC;

