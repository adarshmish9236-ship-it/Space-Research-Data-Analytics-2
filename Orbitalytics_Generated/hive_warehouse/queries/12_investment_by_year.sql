-- =============================================================================
-- Query 12: Annual Research Investment with Cumulative Running Total
-- Advanced Features: Window Functions (SUM OVER ORDER BY), Multi-Year Progression
-- =============================================================================
USE orbitalytics;

WITH annual_investment AS (
    SELECT
        year,
        COUNT(expenditure_id) AS records_count,
        ROUND(SUM(rd_expenditure_m_usd), 2) AS annual_rd_m_usd,
        ROUND(SUM(infrastructure_expenditure_m_usd), 2) AS annual_infra_m_usd,
        ROUND(SUM(total_monthly_expenditure_m_usd), 2) AS annual_total_m_usd
    FROM fact_research_investment
    GROUP BY year
)
SELECT
    year,
    records_count,
    annual_rd_m_usd,
    annual_infra_m_usd,
    annual_total_m_usd,
    ROUND(SUM(annual_total_m_usd) OVER (ORDER BY year ASC), 2) AS cumulative_investment_m_usd,
    ROUND(AVG(annual_total_m_usd) OVER (ORDER BY year ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS three_year_moving_avg_m_usd
FROM annual_investment
ORDER BY year ASC;

