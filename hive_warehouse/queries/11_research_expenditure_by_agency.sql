-- =============================================================================
-- Query 11: Research Expenditure Breakdown by Space Agency
-- Advanced Features: Partitioned Expenditure Rollup, Budget Portfolio Ratios
-- =============================================================================
USE orbitalytics;

SELECT
    a.agency_key,
    a.agency_name,
    a.country,
    COUNT(f.expenditure_id) AS reporting_months,
    ROUND(SUM(f.rd_expenditure_m_usd), 2) AS total_rd_spend_m_usd,
    ROUND(SUM(f.infrastructure_expenditure_m_usd), 2) AS total_infrastructure_spend_m_usd,
    ROUND(SUM(f.mission_operations_m_usd), 2) AS total_operations_spend_m_usd,
    ROUND(SUM(f.total_monthly_expenditure_m_usd), 2) AS grand_total_budget_m_usd,
    ROUND((SUM(f.rd_expenditure_m_usd) / SUM(f.total_monthly_expenditure_m_usd)) * 100.0, 2) AS rd_allocation_pct,
    ROUND((SUM(f.infrastructure_expenditure_m_usd) / SUM(f.total_monthly_expenditure_m_usd)) * 100.0, 2) AS infra_allocation_pct
FROM fact_research_investment f
JOIN dim_agency a ON f.agency_key = a.agency_key
GROUP BY a.agency_key, a.agency_name, a.country
ORDER BY grand_total_budget_m_usd DESC;
