# ORBITALYTICS 2.0 — Dataset Documentation & Provenance Catalog

---

## 1. Catalog Summary

The ORBITALYTICS platform operates over nine canonical space exploration and research datasets, representing historical and decadal mission activities from 2010 through 2026. All datasets have undergone rigorous validation, checksum indexing, and relational integrity auditing.

| Dataset Identifier | Domain | Records | Size (KB) | Format | Primary Key | Partition Key | Quality Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `space_missions.csv` | Mission Operations | 1,500 | 188.7 | CSV / Parquet | `mission_id` | `year` (2010-2026) | 99.8% |
| `satellites_orbital.csv` | Orbital Dynamics | 2,400 | 279.0 | CSV / Parquet | `satellite_id` | `launch_year` | 98.9% |
| `launch_activities.csv` | Spaceport Launches | 1,200 | 108.4 | CSV / Parquet | `launch_id` | `year` (2010-2026) | 99.5% |
| `equipment_component_demand.csv` | Hardware Supply Chain | 1,616 | 106.6 | CSV / Parquet | Compound | `year` (2010-2026) | 99.2% |
| `resource_consumption.csv` | Propellant & Consumables | 1,414 | 92.8 | CSV / Parquet | Compound | `year` (2010-2026) | 99.1% |
| `agency_research_expenditures.csv`| Economic Appropriations | 1,414 | 85.2 | CSV / Parquet | Compound | `year` (2010-2026) | 99.7% |
| `satellite_manufacturing_requirements.csv` | Aerospace Cleanrooms | 600 | 50.2 | CSV / Parquet | `order_id` | Non-partitioned | 99.4% |
| `space_infrastructure_requirements.csv` | DSN & Ground Stations | 1,010 | 65.3 | CSV / Parquet | `station_id` | `year` (2010-2026) | 98.7% |
| `research_investment_future_projects.csv` | Decadal Strategic Surveys | 150 | 13.9 | CSV / Parquet | `project_id` | Non-partitioned | 100.0% |

**Total Platform Records:** 11,304 rows across 9 schemas with zero critical schema errors.

---

## 2. Schema Specifications & Field Dictionaries

### 2.1 `space_missions.csv`
- `mission_id` (String): Unique mission code (e.g., `MSN-2010-1000`). Primary Key.
- `mission_name` (String): Nominal mission name (e.g., `Earth Discovery 1`).
- `agency` (String): Sponsoring entity (`NASA (USA)`, `ESA (Europe)`, `ISRO (India)`, `CNSA (China)`, `Roscosmos (Russia)`, `JAXA (Japan)`).
- `mission_type` (String): `Earth Observation`, `Deep Space`, `Human Spaceflight`, `Planetary Science`, `Astrophysics`.
- `launch_date` (Date, `YYYY-MM-DD`): Scheduled or actual launch timestamp.
- `year` (Integer, 2010-2026): Calendar launch year (Partition Key).
- `quarter` (String, `Q1`-`Q4`): Calendar launch quarter.
- `budget_million_usd` (Float): Total mission expenditure allocation ($M USD).
- `payload_mass_kg` (Float): Net mass injected into orbit (kg).
- `status` (String): `Successful`, `In-Flight`, `Operational`, `Retired`, `Failure`.
- `crew_size` (Integer, 0-7): Number of astronauts onboard.
- `duration_days` (Integer): Total mission mission duration in days.

### 2.2 `satellites_orbital.csv`
- `satellite_id` (String): International Satellite Catalog ID (e.g., `SAT-2012-2000`). Primary Key.
- `satellite_name` (String): Spacecraft designation.
- `operator_agency` (String): Governing agency or commercial operator.
- `orbit_type` (String): `LEO (Low Earth Orbit)`, `MEO (Medium Earth Orbit)`, `GEO (Geostationary)`, `SSO (Sun-Synchronous)`, `Lagrange Points (L1/L2)`, `Deep Space / Lunar`.
- `altitude_km` (Float): Semi-major axis or orbital apogee above Earth's geoid (km).
- `inclination_deg` (Float): Orbital inclination relative to equatorial plane ($0.0^\circ - 98.0^\circ$).
- `launch_year` (Integer, 2010-2026): Launch year (Partition Key).
- `expected_lifetime_years` (Integer, 3-20): Design operational lifespan.
- `dry_mass_kg` (Float): Mass of bus and instrumentation excluding consumables.
- `power_consumption_w` (Float): Peak electrical draw in watts from solar/RTG arrays.
- `telemetry_band` (String): Communications link (`S-band`, `X-band`, `Ka-band`, `Optical Laser`).
- `operational_status` (String): `Active`, `Standby`, `Decayed`, `Decommissioned`.

### 2.3 `equipment_component_demand.csv`
- `date` (Date, `YYYY-MM-DD`): Telemetry recording date.
- `year` (Integer, 2010-2026): Year of demand log (Partition Key).
- `month` (Integer, 1-12): Month index.
- `quarter` (String, `Q1`-`Q4`): Fiscal quarter.
- `equipment_type` (String): Component class name (`Radiation-Hardened Rad-750 CPUs`, `Optical Inter-Satellite Links`, `SAR Radar Antennas`, `Ion Propulsion Engines`, `High-Efficiency Solar Arrays`, `Reaction Wheels`, `Star Trackers`, `Cryogenic Tanks`).
- `units_demanded` (Integer): Aggregate count of component units required for assembly.
- `avg_unit_cost_thousand_usd` (Float): Unit procurement cost ($K USD).
- `total_demand_value_million_usd` (Float): Gross component procurement valuation ($M USD).
- `lead_time_days` (Integer, 90-450): Supplier production and qualification cycle duration.
- `shortage_risk` (String): Qualitative assessment (`Low`, `Medium`, `High`, `Critical`).

### 2.4 `resource_consumption.csv`
- `date` (Date, `YYYY-MM-DD`): Telemetry recording date.
- `year` (Integer, 2010-2026): Consumption year (Partition Key).
- `month` (Integer, 1-12): Month index.
- `quarter` (String, `Q1`-`Q4`): Fiscal quarter.
- `resource_name` (String): Consumable identifier (`Cryogenic Liquid Oxygen (LOX)`, `RP-1 Rocket Fuel`, `Liquid Hydrogen (LH2)`, `Hypergolic Hydrazine`, `Deep Space Telemetry (Tbps)`, `Radiation Shielding Alloys`).
- `total_consumed` (Float): Consumed quantity in standard unit (Tons, Cubic Meters, or Tbps).
- `avg_unit_cost_usd` (Float): Acquisition price per unit ($ USD).
- `total_cost_k_usd` (Float): Net resource expense ($K USD).
- `criticality_rating` (String): Operational priority (`Tier-1 Strategic`, `Tier-2 Tactical`).

---

## 3. Data Quality & Anomaly Detection Rules

Automated quality auditing is performed across three statistical methods:
1. **IQR Outlier Scan:** Interquartile range detection flagging observations with $x > Q_3 + 1.5 \cdot \text{IQR}$ or $x < Q_1 - 1.5 \cdot \text{IQR}$.
2. **Z-Score Scan:** Standard normal deviation flagging $|Z| > 3.0$.
3. **Domain Constraint Bounds:** Enforcing strict boundaries (e.g., payload mass $\ge 0$, success rate between 0% and 100%, budget $> 0$).
