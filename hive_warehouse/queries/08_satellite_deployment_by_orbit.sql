-- =============================================================================
-- Query 08: Satellite Deployment Analytics by Orbit Type
-- Advanced Features: Dimension Aggregations, Orbital Mechanics Profiling
-- =============================================================================
USE orbitalytics;

SELECT
    orbit_type,
    COUNT(satellite_id) AS total_satellites_deployed,
    ROUND(AVG(altitude_km), 1) AS mean_altitude_km,
    ROUND(AVG(inclination_deg), 2) AS mean_inclination_deg,
    ROUND(AVG(dry_mass_kg), 1) AS mean_dry_mass_kg,
    ROUND(SUM(dry_mass_kg) / 1000.0, 2) AS total_mass_deployed_metric_tons,
    SUM(CASE WHEN operational_status = 'Active' THEN 1 ELSE 0 END) AS active_satellites_count,
    ROUND((SUM(CASE WHEN operational_status = 'Active' THEN 1 ELSE 0 END) / COUNT(*)) * 100.0, 2) AS active_fleet_ratio_pct
FROM stg_satellites
GROUP BY orbit_type
ORDER BY total_satellites_deployed DESC;

