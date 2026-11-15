# Orbitalytics Phase 1: Comprehensive Dataset Inventory

## 1. Overview
The Orbitalytics Phase 1 repository manages physical datasets across six functional tiers:
1. `datasets/reference/` — Canonical master lookup tables (agencies, components, resources, units).
2. `datasets/raw/public/` — Authentic historical aerospace records from verified public archives.
3. `datasets/raw/synthetic/` — Reproducible, seed-controlled synthetic records bridging the ITAR/defense secrecy gap.
4. `datasets/raw/existing/` — Preserved legacy baseline files from the original repository audit.
5. `datasets/validated/` — Schema-enforced, standardized, quality-certified datasets.
6. `datasets/rejected/` — Isolated defective records with structured rejection codes and audit reasons.

---

## 2. Nine Core Datasets Inventory

| # | Dataset File | Domain | Primary Key | Total Records | Size (KB) | Data Origin | Description |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | `space_missions.csv` | Domain 4: Mission Requirements | `mission_id` | 1,500 | 357.0 | Synthetic | Historical orbital space missions, payloads, programmatic budgets, status, and flight durations (2010–2026). |
| **2** | `satellites_orbital.csv` | Domain 4: Orbital Parameters | `satellite_id` | 2,400 | 583.6 | Synthetic | Spacecraft orbital parameters (LEO, MEO, GEO, SSO), dry mass, power requirements, and telemetry bands. |
| **3** | `launch_activities.csv` | Domain 4: Launch Activities | `launch_id` | 1,200 | 219.0 | Synthetic | Rocket launch events, launch vehicles (Falcon 9, Ariane 6, PSLV, etc.), spaceports, launch costs, and outcomes. |
| **4** | `equipment_component_demand.csv` | **Domain 1: Component Demand** | `demand_id` | 11,312 | 3,725.7 | Synthetic | **Primary Target:** Monthly discrete demand for flight hardware (solar arrays, Rad-750 CPUs, thrusters, star trackers). |
| **5** | `agency_research_expenditures.csv` | Domain 5: Agency Expenditures | `expenditure_id` | 1,414 | 279.5 | Synthetic | Monthly expenditures across R&D, infrastructure, and operations for NASA, ESA, ISRO, JAXA, CNSA, Roscosmos, and Commercial. |
| **6** | `resource_consumption.csv` | **Domain 2: Resource Consumption** | `consumption_id` | 9,898 | 2,754.9 | Synthetic | **Primary Target:** Monthly consumption of cryogenic propellants, materials, telemetry bandwidth, and solar power. |
| **7** | `satellite_manufacturing_requirements.csv` | Domain 3: Manufacturing | `order_id` | 600 | 107.1 | Synthetic | Cleanroom integration hours, vibration test results, spacecraft mass classes, and contract order volumes. |
| **8** | `space_infrastructure_requirements.csv` | Domain 5: Infrastructure | `infrastructure_record_id` | 1,010 | 266.0 | Synthetic | Deep Space Network (DSN) antenna time, cryogenic vacuum testing chambers, utilization rates, and queue backlog hours. |
| **9** | `research_investment_future_projects.csv` | Domain 5: Strategic Roadmaps | `project_id` | 160 | 40.8 | Synthetic | Future strategic projects (Artemis, Lunar Gateway, Mars Sample Return), Technology Readiness Levels (TRL), and proposed investments. |

---

## 3. Reference & Master Data Tables

| Reference File | Key Field | Records | Purpose & Schema Scope |
| :--- | :--- | :---: | :--- |
| `reference/agencies/agencies.csv` | `agency_id` | 7 | Master registry of civil space agencies (NASA, ESA, ISRO, JAXA, CNSA, Roscosmos) and commercial launch consortiums. |
| `reference/components/components.csv` | `component_id` | 8 | Master catalog of aerospace components, sub-systems (ADCS, EPS, COMMS, C&DH), criticality tiers, and baseline lead times. |
| `reference/resources/resources.csv` | `resource_id` | 7 | Master catalog of physical and non-physical space resources, hazard classifications, unit costs, and storage requirements. |
| `reference/units/units.csv` | `unit_code` | 12 | Canonical physical and financial units of measurement with SI base equivalents and conversion ratios. |

---

## 4. Authentic Public Baseline Datasets

| Public File | Primary Key | Records | Source Publisher | Licence | Verified Real Observations |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `raw/public/nasa_public_space_missions.csv` | `mission_id` | 8 | NASA Open Data / Master Catalog | NASA CC0 Public Domain | Apollo, Hubble, Cassini, Curiosity, JWST, Chandrayaan-1, Chandrayaan-3, BepiColombo, Tianwen-1. |
| `raw/public/public_satellite_registry.csv` | `satellite_id` | 4 | NASA NSSDC / Space-Track / ESA | Public Domain / Open Access | Hubble (HST), International Space Station (ISS), SARAL AltiKa, Sentinel-1A. |

---

## 5. Storage Metrics & Volume Summary

- **Total Cataloged Files:** 32 physical CSV/JSON files across all workspace layers.
- **Total Validated Records:** 29,494 records in `datasets/validated/`.
- **Quality Score Average:** 100.0% across all 9 validated core datasets.
- **Defective Rejection Ratio:** 0.0% in validated baseline; complete rejection tracking enabled in `datasets/rejected/`.

