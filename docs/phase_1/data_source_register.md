# Orbitalytics Phase 1: Data Source Register & Provenance

## 1. Overview & Data Source Taxonomy
Phase 1 catalogs both authentic public space research repositories and controlled, reproducible synthetic simulation models. 

Every record in the platform carries a mandatory `data_origin` metadata attribute:
- `data_origin = 'real'`: Authentic historical data sourced directly from verified public government and scientific archives.
- `data_origin = 'synthetic'`: Scientifically grounded, physics-informed synthetic data generated to bridge empirical secrecy gaps without confusing evaluators.

---

## 2. Public Data Sources Register

### 1. NASA Open Data Portal & NSSDC Master Catalog
- **Source Identifier:** `SRC-001`
- **Publisher:** National Aeronautics and Space Administration (NASA)
- **Portal URL:** [https://data.nasa.gov/](https://data.nasa.gov/)
- **API Endpoint:** [https://api.nasa.gov/](https://api.nasa.gov/)
- **Licence:** NASA Open Data Policy / Public Domain (CC0 Equivalent)
- **Coverage Period:** 1958 – Present
- **Formats Available:** JSON, CSV, RESTful APIs
- **Domains Covered:** Orbital Missions, Satellite Telemetry, Solar System Trajectories
- **Transformations Applied:** Filtered to prominent deep-space and astrophysics observatories (Hubble, JWST, Curiosity, Cassini); ISO-8601 date normalization.

### 2. European Space Agency (ESA) Science Portal
- **Source Identifier:** `SRC-002`
- **Publisher:** European Space Agency (ESA)
- **Portal URL:** [https://www.esa.int/Science_Exploration](https://www.esa.int/Science_Exploration)
- **API Endpoint:** [https://scihub.copernicus.eu/](https://scihub.copernicus.eu/)
- **Licence:** CC BY-SA 3.0 IGO / Open Access
- **Coverage Period:** 1975 – Present
- **Formats Available:** XML, JSON, GeoTIFF, Tabular Mission Profiles
- **Domains Covered:** Planetary Science, Earth Observation (Copernicus), Heliophysics
- **Transformations Applied:** Standardized agency metadata and international designations.

### 3. Indian Space Research Organisation (ISRO) Archives
- **Source Identifier:** `SRC-003`
- **Publisher:** Indian Space Research Organisation (ISRO)
- **Portal URL:** [https://www.isro.gov.in/](https://www.isro.gov.in/)
- **API Endpoint:** [https://www.isro.gov.in/Missions.html](https://www.isro.gov.in/Missions.html)
- **Licence:** Government of India Open Access Public Information
- **Coverage Period:** 1969 – Present
- **Formats Available:** HTML Releases, Annual Reports, Technical Bulletins
- **Domains Covered:** Lunar Missions (Chandrayaan-1, 2, 3), Mars Orbiter Mission (Mangalyaan), Launch Vehicles (PSLV, GSLV, LVM3)
- **Transformations Applied:** Tabulation of mission budgets and payload specifications.

### 4. United Nations Office for Outer Space Affairs (UNOOSA)
- **Source Identifier:** `SRC-004`
- **Publisher:** United Nations OOSA
- **Portal URL:** [https://www.unoosa.org/oosa/en/spaceobjectregister/index.html](https://www.unoosa.org/oosa/en/spaceobjectregister/index.html)
- **Licence:** UN Treaty on Principles Governing the Activities of States in Outer Space (Public Registry)
- **Coverage Period:** 1962 – Present
- **Formats Available:** CSV, Online Searchable Index
- **Domains Covered:** Registration of Objects Launched into Outer Space, International Orbital Parameters

---

## 3. The Empirical Secrecy Gap Disclosure
A primary finding of the Phase 1 Data Audit is the existence of an intractable secrecy gap in public space data:

> **Formal Limitation Statement:**  
> While civil agencies publish high-level programmatic announcements, flight trajectories, and total mission appropriations, granular month-by-month bills of materials (BOM), exact discrete component demand quantities (e.g., number of Rad-750 processors, reaction wheels, or optical transceivers procured monthly), and precise consumable propellant burn logs are classified under **International Traffic in Arms Regulations (ITAR)**, national defense security protocols, and commercial confidentiality (SpaceX, Blue Origin proprietary supply contracts).

### Methodological Resolution:
To enable rigorous Big Data engineering, distributed analytics (Hadoop/HDFS/Hive/Spark), and demand forecasting, Orbitalytics implements a controlled, reproducible, physics-informed synthetic data generation module (`SyntheticDataGenerator`). All synthetic records are explicitly tagged with `data_origin='synthetic'` and `is_synthetic=True`, ensuring complete transparency, provenance traceability, and zero confounding with authentic historical observations.

---

## 4. Synthetic Simulation Model Register
- **Model Name:** Orbitalytics Physics-Informed Space Research Simulator
- **Source Identifier:** `SRC-005`
- **Implementation File:** `modules/phase_1/synthetic_data_generator.py`
- **Licence:** Apache-2.0 / Academic Engineering Use
- **Deterministic Seed:** `SEED = 42`
- **Profiles Supported:**
  1. `small` (1.0x multiplier, ~29,500 records)
  2. `medium` (10.0x multiplier, ~100,000+ records)
  3. `large` (100.0x multiplier, ~1,000,000+ records)
- **Relational Integrity:** Foreign keys guaranteed against canonical master tables.

