-- =============================================================================
-- ORBITALYTICS Phase 7 — Task 5: Spark SQL Query Library
-- Reusable SQL analytics executed against Spark temp views from Silver Parquet
-- =============================================================================

-- ===== Q1: Annual Equipment Demand Trend with YoY Growth (Window Function) =====
SELECT
    year,
    COUNT(demand_id)                                      AS order_count,
    ROUND(SUM(units_demanded), 1)                         AS total_units_demanded,
    ROUND(SUM(total_demand_value_m_usd), 2)               AS total_value_m_usd,
    ROUND(SUM(units_demanded) - LAG(SUM(units_demanded), 1) OVER (ORDER BY year), 1)
                                                           AS yoy_unit_delta,
    ROUND(
        (SUM(units_demanded) - LAG(SUM(units_demanded), 1) OVER (ORDER BY year))
        / LAG(SUM(units_demanded), 1) OVER (ORDER BY year) * 100.0, 2
    )                                                      AS yoy_growth_pct
FROM equipment_demand
GROUP BY year
ORDER BY year;

-- ===== Q2: Agency-Level Demand Ranking with Market Share =====
SELECT
    agency_id,
    ROUND(SUM(units_demanded), 1)                         AS total_units,
    ROUND(SUM(total_demand_value_m_usd), 2)               AS total_spend_m_usd,
    ROUND(SUM(total_demand_value_m_usd) / SUM(SUM(total_demand_value_m_usd)) OVER () * 100.0, 2)
                                                           AS market_share_pct,
    RANK() OVER (ORDER BY SUM(total_demand_value_m_usd) DESC)
                                                           AS spend_rank
FROM equipment_demand
GROUP BY agency_id;

-- ===== Q3: Resource Consumption Efficiency by Resource Category =====
SELECT
    resource_category,
    year,
    ROUND(SUM(quantity_consumed), 2)                       AS total_consumed,
    ROUND(SUM(procurement_cost_k_usd), 2)                 AS total_cost_k_usd,
    ROUND(SUM(procurement_cost_k_usd) / SUM(quantity_consumed), 4)
                                                           AS cost_per_unit_k_usd,
    ROUND(AVG(consumption_rate_per_day), 3)               AS avg_daily_rate,
    ROUND(
        SUM(quantity_consumed) - LAG(SUM(quantity_consumed), 1)
            OVER (PARTITION BY resource_category ORDER BY year), 2
    )                                                      AS yoy_consumption_delta
FROM resource_consumption
GROUP BY resource_category, year
ORDER BY resource_category, year;

-- ===== Q4: Launch Activity Trend with 3-Year Rolling Average =====
SELECT
    year,
    COUNT(launch_id)                                       AS total_launches,
    ROUND(SUM(launch_cost_m_usd), 2)                      AS total_cost_m_usd,
    ROUND(SUM(payload_to_orbit_kg), 1)                    AS total_payload_kg,
    ROUND(AVG(COUNT(launch_id)) OVER (ORDER BY year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1)
                                                           AS rolling_3yr_avg_launches,
    ROUND(SUM(CASE WHEN launch_outcome = 'Success' THEN 1 ELSE 0 END) / COUNT(*) * 100.0, 2)
                                                           AS success_rate_pct
FROM launches
GROUP BY year
ORDER BY year;

-- ===== Q5: Mission-Resource Intensity Analysis =====
SELECT
    m.agency_id,
    m.mission_type,
    COUNT(DISTINCT m.mission_id)                           AS mission_count,
    ROUND(AVG(m.budget_m_usd), 2)                         AS avg_mission_budget_m_usd,
    ROUND(SUM(m.payload_mass_kg), 1)                      AS total_payload_kg,
    ROUND(SUM(rc.quantity_consumed), 2)                   AS total_resource_consumed,
    ROUND(SUM(rc.quantity_consumed) / COUNT(DISTINCT m.mission_id), 2)
                                                           AS avg_resources_per_mission
FROM missions m
LEFT JOIN resource_consumption rc ON m.mission_id = rc.associated_mission_id
GROUP BY m.agency_id, m.mission_type
ORDER BY mission_count DESC;

-- ===== Q6: Equipment Demand Forecast Feature View (pre-aggregated per entity) =====
SELECT
    year,
    agency_id,
    component_id,
    component_category,
    ROUND(SUM(units_demanded), 1)                          AS annual_units,
    ROUND(SUM(units_demanded) - LAG(SUM(units_demanded), 1)
        OVER (PARTITION BY agency_id, component_id ORDER BY year), 1)
                                                            AS yoy_unit_delta,
    ROUND(SUM(total_demand_value_m_usd), 2)                AS annual_value_m_usd,
    ROUND(AVG(lead_time_days), 1)                          AS avg_lead_time_days
FROM equipment_demand
GROUP BY year, agency_id, component_id, component_category
ORDER BY year, agency_id, component_id;

-- ===== Q7: Satellite Deployment vs Component Demand Correlation =====
WITH sat_deploy AS (
    SELECT
        launch_year AS year,
        orbit_type,
        COUNT(satellite_id) AS satellites_deployed
    FROM satellites
    GROUP BY launch_year, orbit_type
),
demand_by_category AS (
    SELECT
        year,
        component_category,
        ROUND(SUM(units_demanded), 1) AS total_demand
    FROM equipment_demand
    GROUP BY year, component_category
)
SELECT
    s.year,
    s.orbit_type,
    s.satellites_deployed,
    d.component_category,
    d.total_demand,
    ROUND(d.total_demand / s.satellites_deployed, 2) AS demand_per_satellite
FROM sat_deploy s
JOIN demand_by_category d ON s.year = d.year
WHERE s.satellites_deployed > 0
ORDER BY s.year, s.orbit_type, d.component_category;

-- ===== Q8: Research Investment Efficiency (R&D per Mission) =====
SELECT
    ri.year,
    ri.agency_id,
    ROUND(SUM(ri.rd_expenditure_m_usd), 2)                AS annual_rd_m_usd,
    COUNT(m.mission_id)                                    AS missions_launched,
    ROUND(SUM(ri.rd_expenditure_m_usd) / NULLIF(COUNT(m.mission_id), 0), 2)
                                                           AS rd_per_mission_m_usd,
    ROUND(SUM(ri.total_monthly_expenditure_m_usd), 2)     AS total_budget_m_usd
FROM research_investment ri
LEFT JOIN missions m ON ri.agency_id = m.agency_id AND ri.year = m.year
GROUP BY ri.year, ri.agency_id
ORDER BY ri.year, annual_rd_m_usd DESC;
