# Orbitalytics Phase 1: Canonical Data Dictionary

## 1. Domain 1: Satellite Component Demand (`equipment_component_demand.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Domain Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `demand_id` | String | No | **PK** | Unique discrete demand observation identifier. Pattern: `DEM-YYYY-NNNNN`. | `DEM-2024-00142` |
| `date` | Date (ISO-8601) | No | - | First day of observation month (`YYYY-MM-DD`). | `2024-06-01` |
| `year` | Integer | No | - | Calendar year (2010 to 2026). | `2024` |
| `month` | Integer | No | - | Calendar month integer (1 to 12). | `6` |
| `quarter` | String | No | - | Programmatic quarter (`Q1`, `Q2`, `Q3`, `Q4`). | `Q2` |
| `component_id` | String | No | **FK** | Foreign key to `reference/components/components.csv`. | `CMP-002` |
| `component_name` | String | No | - | Canonical name of aerospace hardware component. | `Radiation-Hardened Rad-750 Single Board Computers` |
| `component_category`| String | No | - | Subsystem category (`Power Systems`, `Avionics`, `Propulsion`, etc.). | `Avionics` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-001` |
| `agency_name` | String | No | - | Canonical operating agency name. | `NASA` |
| `target_satellite_class`| String | No | - | Spacecraft bus class (`CubeSat`, `SmallSat`, `Medium Satellite`, `Heavy Geosynchronous Bus`). | `SmallSat (<500kg)` |
| `units_demanded` | Integer | No | - | **Primary Target:** Discrete unit count demanded in reporting period (>= 0). | `24` |
| `units_manufactured`| Integer | No | - | Units produced by industrial fabricators (>= 0). | `22` |
| `units_procured` | Integer | No | - | Units contracted and accepted by procurement office (>= 0). | `25` |
| `unit_of_measure` | String | No | - | Physical unit (`Units`). | `Units` |
| `avg_unit_cost_thousand_usd` | Float | No | - | Unit production/procurement cost in thousands of USD. | `450.5` |
| `total_demand_value_million_usd`| Float | No | - | Total financial footprint (`units_demanded * cost / 1000`). | `10.812` |
| `lead_time_days` | Integer | No | - | Hardware production lead time from order to delivery (days). | `320` |
| `shortage_risk` | String | No | - | Risk tier (`Low`, `Medium`, `High`, `Critical`). | `High` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 2. Domain 2: Space Research Resource Consumption (`resource_consumption.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Domain Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `consumption_id` | String | No | **PK** | Unique consumption record identifier. Pattern: `CNS-YYYY-NNNNN`. | `CNS-2023-00891` |
| `date` | Date (ISO-8601) | No | - | Monthly timestamp (`YYYY-MM-DD`). | `2023-11-01` |
| `year` | Integer | No | - | Calendar year (2010 to 2026). | `2023` |
| `month` | Integer | No | - | Calendar month (1 to 12). | `11` |
| `quarter` | String | No | - | Quarter (`Q1` to `Q4`). | `Q4` |
| `resource_id` | String | No | **FK** | Foreign key to `reference/resources/resources.csv`. | `RES-001` |
| `resource_name` | String | No | - | Name of consumable resource. | `Cryogenic Liquid Oxygen (LOX)` |
| `resource_category`| String | No | - | Resource classification (`Propellant & Oxidizer`, `Liquid Fuel`, etc.). | `Propellant & Oxidizer` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-003` |
| `agency_name` | String | No | - | Operating agency (`ISRO`). | `ISRO` |
| `mission_id` | String | No | **FK** | Foreign key to `space_missions.csv`. | `MSN-2023-1420` |
| `quantity_consumed`| Float | No | - | **Primary Target:** Quantity utilized in flight operations or ground tests. | `184.50` |
| `unit_of_measure` | String | No | - | Physical unit (`Metric Tons`, `Tbps`, `kW`). | `Metric Tons` |
| `procurement_cost_k_usd` | Float | No | - | Procurement cost in thousands of USD. | `147.60` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 3. Domain 4: Space Missions (`space_missions.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Domain Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `mission_id` | String | No | **PK** | Unique space flight mission identifier. Pattern: `MSN-YYYY-NNNN`. | `MSN-2022-1185` |
| `mission_name` | String | No | - | Programmatic flight designation. | `Earth Discovery 186` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-002` |
| `agency_name` | String | No | - | Space agency (`ESA`). | `ESA` |
| `mission_type` | String | No | - | Mission category (`Earth Observation`, `Planetary Exploration`, etc.). | `Earth Observation` |
| `launch_date` | Date (ISO-8601) | No | - | Exact launch calendar date (`YYYY-MM-DD`). | `2022-08-14` |
| `year` | Integer | No | - | Launch year (2010 to 2026). | `2022` |
| `quarter` | String | No | - | Launch quarter (`Q1` to `Q4`). | `Q3` |
| `budget_million_usd`| Float | No | - | Total mission development and operations budget (M$). | `480.50` |
| `payload_mass_kg` | Float | No | - | Total wet payload mass injected to orbit (kg). | `3450.0` |
| `status` | String | No | - | Mission outcome (`Successful`, `Operational`, `Completed`, etc.). | `Operational` |
| `crew_size` | Integer | No | - | Human flight crew count (0 for uncrewed robotic probes). | `0` |
| `duration_days` | Integer | No | - | Operational life duration in days. | `1825` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 4. Domain 4: Satellites and Orbital Mechanics (`satellites_orbital.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `satellite_id` | String | No | **PK** | Unique satellite identifier. Pattern: `SAT-YYYY-NNNN`. | `SAT-2021-2045` |
| `satellite_name` | String | No | - | Spacecraft name. | `AstroSat-145` |
| `operator_agency_id`| String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-001` |
| `operator_agency_name`| String | No | - | Operating agency name. | `NASA` |
| `associated_mission_id`| String | No | **FK** | Foreign key to `space_missions.csv`. | `MSN-2021-1090` |
| `orbit_type` | String | No | - | Orbital regime (`LEO`, `MEO`, `GEO`, `SSO`, `Deep Space / Lunar`, `Lagrange Point`). | `SSO (Sun-Synchronous)` |
| `altitude_km` | Float | No | - | Orbital apogee / operating altitude (km). | `680.0` |
| `inclination_deg`| Float | No | - | Orbital orbital inclination in degrees (0.0 to 98.6°). | `98.15` |
| `launch_year` | Integer | No | - | Year satellite placed into orbit. | `2021` |
| `expected_lifetime_years`| Integer | No | - | Design operational lifespan (years). | `8` |
| `dry_mass_kg` | Float | No | - | Spacecraft dry mass excluding propellant (kg). | `1250.0` |
| `power_consumption_w`| Float | No | - | Continuous electrical power consumption (Watts). | `2400.0` |
| `telemetry_band`| String | No | - | Communications link frequency (`Ka-band`, `X-band`, `Optical Laser`). | `Ka-band` |
| `operational_status`| String | No | - | Status (`Active`, `Decommissioned`, `Decayed`, `Standby`). | `Active` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 5. Domain 4: Launch Activities (`launch_activities.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `launch_id` | String | No | **PK** | Launch event identifier. Pattern: `LNCH-YYYY-NNN`. | `LNCH-2023-112` |
| `mission_id` | String | No | **FK** | Foreign key to `space_missions.csv`. | `MSN-2023-1045` |
| `launch_date` | Date (ISO-8601) | No | - | Rocket launch date (`YYYY-MM-DD`). | `2023-04-18` |
| `year` | Integer | No | - | Launch year (2010 to 2026). | `2023` |
| `month` | Integer | No | - | Launch month (1 to 12). | `4` |
| `vehicle` | String | No | - | Rocket booster class (`Falcon 9`, `Ariane 6`, `PSLV`, etc.). | `Falcon 9` |
| `launch_site` | String | No | - | Spaceport launch pad facility. | `Cape Canaveral SLC-40` |
| `country` | String | No | - | Launching state jurisdiction. | `United States` |
| `launch_outcome` | String | No | - | Outcome (`Success`, `Partial Failure`, `Launch Abort`, `Catastrophic Failure`). | `Success` |
| `commercial_flag`| Boolean | No | - | Boolean flag indicating commercial vs civil governmental launch. | `True` |
| `launch_cost_million_usd`| Float | No | - | Cost per launch event in millions of USD. | `67.50` |
| `payload_to_orbit_kg`| Float | No | - | Injected payload mass into target trajectory (kg). | `16200.0` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 6. Domain 5: Agency Research Expenditures (`agency_research_expenditures.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `expenditure_id` | String | No | **PK** | Expenditure record identifier. Pattern: `EXP-YYYY-NNNNN`. | `EXP-2024-00412` |
| `date` | Date (ISO-8601) | No | - | Monthly reporting period date (`YYYY-MM-DD`). | `2024-03-01` |
| `year` | Integer | No | - | Calendar year (2010 to 2026). | `2024` |
| `month` | Integer | No | - | Calendar month (1 to 12). | `3` |
| `quarter` | String | No | - | Fiscal quarter (`Q1` to `Q4`). | `Q1` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-001` |
| `agency_name` | String | No | - | Agency name (`NASA`). | `NASA` |
| `country` | String | No | - | Operating state. | `United States` |
| `rd_expenditure_million_usd`| Float | No | - | Advanced R&D expenditure (M$). | `345.20` |
| `infrastructure_expenditure_million_usd`| Float | No | - | Test stands and spaceport infrastructure expenditure (M$). | `210.80` |
| `mission_operations_million_usd`| Float | No | - | Active flight operations and tracking expenditure (M$). | `175.40` |
| `total_monthly_expenditure_million_usd`| Float | No | - | Sum of monthly outlays (M$). | `731.40` |
| `currency` | String | No | - | Currency code (`USD`). | `USD` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 7. Domain 3: Satellite Manufacturing Requirements (`satellite_manufacturing_requirements.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `order_id` | String | No | **PK** | Work order identifier. Pattern: `ORD-MFG-YYYY-NNNN`. | `ORD-MFG-2022-1084` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-003` |
| `agency_client` | String | No | - | Procurement client agency (`ISRO`). | `ISRO` |
| `satellite_class`| String | No | - | Bus category (`SmallSat (<500kg)`, `CubeSat`, `Heavy Bus`). | `SmallSat (<500kg)` |
| `units_ordered` | Integer | No | - | Number of flight units ordered under contract. | `8` |
| `delivery_year` | Integer | No | - | Contract delivery year (2021 to 2028). | `2024` |
| `cleanroom_hours_required`| Integer | No | - | Certified ISO-5 cleanroom assembly hours required. | `2400` |
| `vibration_testing_pass`| Boolean | No | - | Pass/Fail status on multi-axis acoustic vibration testing. | `True` |
| `contract_value_million_usd`| Float | No | - | Total manufacturing contract value (M$). | `42.50` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 8. Domain 5: Space Infrastructure Requirements (`space_infrastructure_requirements.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `infrastructure_record_id`| String | No | **PK** | Facility observation ID. Pattern: `INF-YYYY-NNNNN`. | `INF-2023-00120` |
| `date` | Date (ISO-8601) | No | - | Monthly timestamp (`YYYY-MM-DD`). | `2023-07-01` |
| `year` | Integer | No | - | Calendar year (2010 to 2026). | `2023` |
| `month` | Integer | No | - | Calendar month (1 to 12). | `7` |
| `facility_name` | String | No | - | Facility name (`Deep Space Network (DSN) Antenna Time`). | `Deep Space Network (DSN) Antenna Time` |
| `facility_type` | String | No | - | Facility classification (`Ground Station Network`, `Cryogenic Testing`, etc.). | `Ground Station Network` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-001` |
| `agency_name` | String | No | - | Operating agency name (`NASA`). | `NASA` |
| `location` | String | No | - | Geographic facility node (`Goldstone / Madrid / Canberra`). | `Goldstone / Madrid / Canberra` |
| `utilization_rate_pct`| Float | No | - | Facility duty cycle percentage (0.0 to 100.0%). | `89.4` |
| `queued_backlog_hours`| Integer | No | - | Backlog mission hours awaiting facility slot. | `245` |
| `maintenance_downtime_days`| Integer | No | - | Unplanned maintenance downtime (days). | `1` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

---

## 9. Domain 5: Research Investment Future Projects (`research_investment_future_projects.csv`)

| Field Name | Data Type | Nullable | Primary / Foreign Key | Description & Constraints | Sample Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `project_id` | String | No | **PK** | Project roadmap identifier. Pattern: `PRJ-YYYY-NNN`. | `PRJ-2028-215` |
| `project_title` | String | No | - | Strategic mission project title. | `NextGen Artemis Lunar Base Phase 2` |
| `agency_id` | String | No | **FK** | Foreign key to `reference/agencies/agencies.csv`. | `AGY-001` |
| `lead_agency` | String | No | - | Lead sponsoring agency. | `NASA` |
| `country` | String | No | - | Sponsoring nation. | `United States` |
| `research_theme` | String | No | - | Mission science theme (`Deep Space Exploration`, `Astrophysics`, etc.). | `Deep Space Exploration` |
| `target_commencement_year`| Integer | No | - | Planned start year (2025 to 2035). | `2028` |
| `estimated_investment_million_usd`| Float | No | - | Capital investment requirement (M$). | `4500.0` |
| `priority_tier` | String | No | - | Strategic prioritization tier (`Critical Strategic`, `High Priority`, etc.). | `Critical Strategic` |
| `technology_readiness_level`| Integer | No | - | NASA/DoD TRL maturity score (1 to 9). | `6` |
| `project_status`| String | No | - | Approval status (`Proposed`, `Funded - Phase A`, `Phase B Development`, `Approved`). | `Phase B Development` |
| `data_origin` | String | No | - | Provenance origin tag (`real`, `synthetic`). | `synthetic` |

