# Orbitalytics Phase 1: Problem Definition & Research Scope

## 1. Executive Summary
**Project Title:** Space Research Data Analytics: A Hadoop Ecosystem Approach to Demand Forecasting  
**Product Positioning:** An Intelligent Space Research Data Platform for Distributed Analytics, Predictive Demand Intelligence, and Strategic Resource Optimization.  
**Phase 1 Mandate:** Problem Definition, Data Identification, Dataset Collection, Standardisation, Quality Validation, and Foundational Modeling.

---

## 2. Problem Statement & Motivation
Modern space exploration is transitioning from infrequent national prestige missions to high-frequency commercial and international scientific operations. This industrial expansion involves multi-satellite mega-constellations, interplanetary sample return missions, lunar orbital stations (e.g., Lunar Gateway), and permanent surface outposts (Artemis Program).

Executing these complex missions demands vast quantities of specialized aerospace equipment, consumables, and infrastructure:
1. **Satellite Flight Hardware:** Radiation-hardened microprocessors (BAE Rad-750), high-efficiency multi-junction solar panels, Hall-effect ion propulsion thrusters, optical inter-satellite laser transceivers, star trackers, and reaction wheels.
2. **Space Resources & Consumables:** Cryogenic propellants (Liquid Oxygen, Liquid Hydrogen, RP-1), storable hypergolic fuels (Monomethyl Hydrazine), radiation shielding alloys (tantalum/tungsten), deep-space telemetry bandwidth (Ka-band / optical), and electrical generation capacity.
3. **Manufacturing & Cleanroom Throughput:** Vibration table testing, thermal vacuum chamber testing, cleanroom integration hours, and capacity allocation across CubeSats, SmallSats, and heavy geosynchronous buses.
4. **Launch Infrastructure & Ground Stations:** Deep Space Network (DSN) tracking hours, launch pad availability, and mission operations command centers.
5. **Research Expenditures & Programmatic Budgets:** Multi-billion dollar capital allocations distributed across national civil space agencies (NASA, ESA, ISRO, JAXA, CNSA) and private launch service operators.

### The Core Problem
Space research and procurement data are notoriously fragmented, siloed across heterogeneous institutions, and obfuscated by classification boundaries. Program managers lack a unified data lakehouse and predictive demand forecasting architecture. Inaccurate demand projections lead to:
- **Severe Flight Hardware Bottlenecks:** Unplanned lead times exceeding 12 to 18 months for radiation-hardened components.
- **Resource Stockouts:** Critical launch delays due to cryogenic propellant supply imbalances.
- **Capital Inefficiency:** Suboptimal inventory holding costs and misallocated R&D budgets.

---

## 3. The Five Formal Space Research Domains
To structure the data platform cleanly, Phase 1 establishes five formal data domains:

| Domain ID | Formal Domain Title | Core Entities & Scope | Primary Analytical / Modeling Use |
| :--- | :--- | :--- | :--- |
| **Domain 1** | **Satellite Component Demand** | Discrete flight hardware components, solar arrays, avionics, reaction wheels, laser links, lead times, costs. | **Primary Demand Forecasting Target** (Units Demanded, Value, Shortage Risk). |
| **Domain 2** | **Space Research Resource Consumption** | Consumables, cryogenic oxidizers, rocket fuels, radiation shielding alloys, telemetry bandwidth, power. | **Primary Resource Forecasting Target** (Metric Tons, Tbps, kW, Procurement Cost). |
| **Domain 3** | **Satellite Manufacturing Requirements** | Work orders, cleanroom integration hours, vibration testing results, satellite bus categories, contract values. | Manufacturing throughput, capacity planning, and lead-time analysis. |
| **Domain 4** | **Launch and Mission Requirements** | Orbital space missions, satellite telemetry, flight orbits (LEO, MEO, GEO, SSO), launch vehicles, launch sites, outcomes. | Explanatory covariate analysis for mission-driven component & fuel demand. |
| **Domain 5** | **Infrastructure & Research Investment** | Ground station network tracking time, cryogenic testing chambers, agency R&D expenditures, future project roadmaps. | Macro-economic budget planning and infrastructure capacity utilization. |

---

## 4. Forecasting Objectives & Prioritization
In strict adherence to engineering rigor, Phase 1 categorizes prospective forecasting targets:

### Primary Forecasting Targets (Rigorous Time-Series Diagnostics Applied):
1. **Equipment / Component Demand (`units_demanded`):** Monthly observations across 8 flight-critical component categories and 7 space agency operators. Evaluated for 12-month forward horizon.
2. **Resource Consumption (`quantity_consumed`):** Monthly observations across 7 vital resource consumables (LOX, RP-1, LH2, Hydrazine, Shielding Alloys, Telemetry, Power).

### Secondary & Supporting Analytical Targets:
- **Agency Research Expenditures:** Macro trend tracking across R&D, infrastructure, and flight operations.
- **Space Infrastructure Backlog:** Queue wait times on Deep Space Network antenna time and environmental test chambers.
- **Satellite Manufacturing Deliveries:** Annual delivery projections by spacecraft bus mass class.

---

## 5. Architectural Alignment with Future Big Data Phases
Phase 1 delivers the clean, validated, referentially sound relational foundation that feeds directly into subsequent big data phases:
```
[Phase 1 Data Foundation]
   ├── Reference Master Data (Agencies, Components, Resources, Units)
   ├── Raw Repositories (Public Authentic Data + Reproducible Synthetic Data)
   └── Validated Star-Schema Datasets (datasets/validated/)
               │
               ▼
[Future Big Data Ecosystem Processing]
   ├── Distributed Ingestion into Apache HDFS Lakehouse (128 MB blocks, 3x repl)
   ├── Apache Pig & Hadoop Streaming MapReduce (Batch processing & tokenization)
   ├── Apache Hive External Partitioned Warehouse (Analytical SQL)
   └── Apache Spark / PySpark In-Memory ETL & ML Pipelines (Demand Forecasting)
```

