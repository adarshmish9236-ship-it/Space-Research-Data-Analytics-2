-- =============================================================================
-- Query 07: Space Mission Counts and Success Rates by Space Agency
-- Advanced Features: Staging / Dim Aggregations, Success Ratio, Budget Performance
-- =============================================================================
USE orbitalytics;

SELECT
    a.agency_key,
    a.agency_name,
    a.country,
    COUNT(m.mission_id) AS total_missions,
    SUM(CASE WHEN m.status IN ('Completed', 'Successful', 'Operational') THEN 1 ELSE 0 END) AS successful_missions,
    ROUND((SUM(CASE WHEN m.status IN ('Completed', 'Successful', 'Operational') THEN 1 ELSE 0 END) / COUNT(m.mission_id)) * 100.0, 2) AS success_rate_pct,
    ROUND(SUM(m.budget_m_usd), 2) AS total_budget_m_usd,
    ROUND(AVG(m.budget_m_usd), 2) AS avg_mission_budget_m_usd,
    ROUND(SUM(m.payload_mass_kg), 1) AS total_payload_mass_kg,
    SUM(m.crew_size) AS total_crew_members
FROM stg_missions m
JOIN dim_agency a ON m.agency_id = a.agency_key
GROUP BY a.agency_key, a.agency_name, a.country
ORDER BY total_missions DESC;
