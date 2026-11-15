# Orbitalytics: Data Dictionary & Provenance Registry

A complete guide to the 9 space research datasets curated in the Orbitalytics platform.

---

## 1. Dataset Provenance & Overview

| Dataset Identifier | Physical File | Curated Format | Domain Category | Records (Medium Profile) |
| :--- | :--- | :--- | :--- | :---: |
| `space_missions` | `space_missions.csv` | Partitioned Parquet | Missions & Science | 1,500 |
| `satellites_orbital` | `satellites_orbital.csv` | Partitioned Parquet | Orbital Mechanics | 2,400 |
| `launch_activities` | `launch_activities.csv` | Partitioned Parquet | Launch Vehicles | 1,200 |
| `equipment_component_demand` | `equipment_component_demand.csv` | Partitioned Parquet | Supply Chain | 1,624 |
| `agency_research_expenditures`| `agency_research_expenditures.csv`| Partitioned Parquet | Fiscal & Budgets | 1,421 |
| `resource_consumption` | `resource_consumption.csv` | Partitioned Parquet | Consumables & Power | 1,624 |
| `satellite_manufacturing_requirements` | `satellite_manufacturing_requirements.csv` | Partitioned Parquet | Manufacturing | 600 |
| `space_infrastructure_requirements` | `space_infrastructure_requirements.csv` | Single Parquet | Infrastructure | 180 |
| `research_investment_future_projects` | `research_investment_future_projects.csv` | Single Parquet | Strategic Roadmaps | 160 |

---

## 2. Field Specifications

### 2.1 Space Missions (`space_missions.csv`)
- `mission_id` (STRING, Primary Key): Unique alphanumeric mission identifier (e.g. `MSN-2022-1045`).
- `mission_name` (STRING): Formal program or expedition title.
- `agency` (STRING): Operating agency (`NASA`, `ESA`, `ISRO`, `JAXA`, `CNSA`, `Roscosmos`, `Commercial`).
- `country` (STRING): Sovereign territory or geographical jurisdiction.
- `mission_type` (STRING): Scientific objective (`Earth Observation`, `Planetary Exploration`, `Human Spaceflight`, etc.).
- `launch_date` (DATE, ISO-8601): Exact launch date (`YYYY-MM-DD`).
- `launch_year` (INT, Partition Key): Calendar year of launch.
- `mission_status` (STRING): Status (`Successful`, `Operational`, `In-Flight`, `Completed`, `Partial Failure`, `Retired`).
- `mission_budget_million_usd` (DOUBLE): Programmatic budget allocation in Millions USD.
- `payload_mass_kg` (DOUBLE): Total launch vehicle payload mass in kilograms.
- `mission_duration_days` (INT): Total operational lifespan in days.
- `orbit_type` (STRING): Target operational orbit.
- `destination` (STRING): Target celestial destination.
- `data_source` (STRING): Data provenance metadata.
- `is_synthetic` (BOOLEAN): Transparency flag confirming synthetic data simulation.

### 2.2 Satellites Orbital Data (`satellites_orbital.csv`)
- `satellite_id` (STRING, Primary Key): Standard satellite catalog designation.
- `satellite_name` (STRING): Operational spacecraft designation.
- `agency` (STRING): Operating space agency or private operator.
- `country` (STRING): Flag state of registration.
- `launch_date` (DATE): Deployment date.
- `launch_year` (INT, Partition Key): Calendar year of deployment.
- `orbit_type` (STRING): Orbital regime (`LEO`, `MEO`, `GEO`, `SSO`, `Deep Space`, `Lagrange`).
- `orbital_altitude_km` (DOUBLE): Perigee/apogee mean altitude in kilometers.
- `orbital_inclination_deg` (DOUBLE): Orbital plane inclination relative to the equator.
- `operational_status` (STRING): (`Active`, `Decommissioned`, `Decayed`, `Standby`).
- `expected_lifetime_years` (INT): Operational design lifespan.
- `power_capacity_kw` (DOUBLE): Onboard electrical solar power capacity in kilowatts.
- `payload_type` (STRING): Primary sensor package.

### 2.3 Launch Activities (`launch_activities.csv`)
- `launch_id` (STRING): Launch sequence code (`LNCH-YYYY-NNN`).
- `launch_date` (DATE): Liftoff timestamp.
- `year` (INT, Partition Key): Calendar year.
- `vehicle` (STRING): Rocket launcher (`Falcon 9`, `Starship`, `Ariane 6`, `PSLV`, etc.).
- `launch_site` (STRING): Launch complex (`Cape Canaveral SLC-40`, `Kourou ELA-4`, `Satish Dhawan SHAR`, etc.).
- `payload_to_orbit_kg` (DOUBLE): Net mass inserted into orbit.
- `launch_cost_million_usd` (DOUBLE): Total commercial or government mission launch cost.
- `launch_outcome` (STRING): Outcome (`Success`, `Partial Failure`, `Launch Abort`, `Catastrophic Failure`).
- `commercial_flag` (BOOLEAN): `True` for private commercial flights, `False` for institutional state missions.

