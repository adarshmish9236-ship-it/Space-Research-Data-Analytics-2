# Dataset Profile: satellites_orbital
- **Total Rows:** 2400
- **Total Columns:** 15
- **Memory Usage:** 583.64 KB

## Column Summary
| Column | Type | Null Count (%) | Unique Values | Details |
| :--- | :--- | :--- | :--- | :--- |
| `satellite_id` | `str` | 0 (0.0%) | 2400 | SAT-2012-2000 (1), SAT-2013-2001 (1), SAT-2014-2002 (1) |
| `satellite_name` | `str` | 0 (0.0%) | 2400 | AstroSat-100 (1), AstroSat-101 (1), AstroSat-102 (1) |
| `operator_agency_id` | `str` | 0 (0.0%) | 7 | AGY-007 (365), AGY-003 (360), AGY-005 (357) |
| `operator_agency_name` | `str` | 0 (0.0%) | 7 | Commercial Space Operators (SpaceX / Blue Origin / Rocket Lab) (365), Indian Space Research Organisation (360), China National Space Administration (357) |
| `associated_mission_id` | `str` | 0 (0.0%) | 1198 | MSN-2014-2347 (7), MSN-2016-1873 (7), MSN-2013-1496 (7) |
| `orbit_type` | `str` | 0 (0.0%) | 6 | LEO (Low Earth Orbit) (408), SSO (Sun-Synchronous) (408), MEO (Medium Earth Orbit) (405) |
| `altitude_km` | `float64` | 0 (0.0%) | 1190 | Min: 425.5, Max: 119770.1, Mean: 39494.926 |
| `inclination_deg` | `float64` | 0 (0.0%) | 2121 | Min: 0.12, Max: 98.59, Mean: 49.437 |
| `launch_year` | `int64` | 0 (0.0%) | 17 | Min: 2010.0, Max: 2026.0, Mean: 2017.86 |
| `expected_lifetime_years` | `int64` | 0 (0.0%) | 16 | Min: 3.0, Max: 18.0, Mean: 10.539 |
| `dry_mass_kg` | `float64` | 0 (0.0%) | 2361 | Min: 54.1, Max: 6499.8, Mean: 3348.31 |
| `power_consumption_w` | `float64` | 0 (0.0%) | 2384 | Min: 200.8, Max: 14988.0, Mean: 7504.507 |
| `telemetry_band` | `str` | 0 (0.0%) | 5 | Ka-band (503), Ku-band (499), X-band (485) |
| `operational_status` | `str` | 0 (0.0%) | 4 | Active (1688), Decommissioned (380), Decayed (207) |
| `data_origin` | `str` | 0 (0.0%) | 1 | synthetic (2400) |
