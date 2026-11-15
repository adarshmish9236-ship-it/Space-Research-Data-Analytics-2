-- =============================================================================
-- Query 04: Component Demand and Expenditure by Space Agency
-- Advanced Features: Window Functions (RANK, SUM OVER), Market Share Calculation
-- =============================================================================
USE orbitalytics;

WITH agency_totals AS (
    SELECT
        a.agency_key,
        a.agency_name,
        a.country,
        COUNT(f.demand_id) AS total_procurement_events,
        ROUND(SUM(f.units_demanded), 1) AS total_units_demanded,
        ROUND(SUM(f.total_demand_value_m_usd), 2) AS total_spend_m_usd
    FROM fact_equipment_demand f
    JOIN dim_agency a ON f.agency_key = a.agency_key
    GROUP BY a.agency_key, a.agency_name, a.country
)
SELECT
    agency_key,
    agency_name,
    country,
    total_procurement_events,
    total_units_demanded,
    total_spend_m_usd,
    ROUND((total_spend_m_usd / SUM(total_spend_m_usd) OVER ()) * 100.0, 2) AS global_market_share_pct,
    RANK() OVER (ORDER BY total_spend_m_usd DESC) AS agency_rank
FROM agency_totals
ORDER BY agency_rank ASC;
