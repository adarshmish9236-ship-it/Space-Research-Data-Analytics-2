# ORBITALYTICS — PHASE 5: HADOOP MAPREDUCE EXECUTION & RESULTS REPORT

## 1. Executive Summary

This report documents the genuine distributed execution, cluster metrics, and analytical results of **Phase 5: Hadoop MapReduce Implementation** for **ORBITALYTICS: Space Research Data Analytics: A Hadoop Ecosystem Approach to Demand Forecasting**.

All seven MapReduce jobs were executed on the live Apache Hadoop 3.2.1 YARN cluster using **Hadoop Streaming (`hadoop-streaming-3.2.1.jar`)** with Python 3 mapper, reducer, and combiner programs. 

Every job ran under full distributed coordination:
- Real YARN application tokens and job IDs were assigned by the ResourceManager (`application_1794633145439_0061` through `application_1794633145439_0067`).
- MapReduce shuffle and sort was performed entirely by the distributed Hadoop framework across 2 parallel reducer containers per job.
- Associative combiners in Job 01 and Job 05 achieved **up to 99.86% local data reduction** before network transmission.
- Zero synthetic mockups or local sort emulations were utilized.

---

## 2. Distributed Job Execution Matrix

| Job ID | Job Name & Domain | YARN Application ID | MapReduce Job ID | Duration | Map In / Out | Combiner In / Out | Reduce Groups / Out | Reducers | HDFS Output Path |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **01** | `01_equipment_demand` | `application_1794633145439_0061` | `job_1794633145439_0061` | 21.12s | 11,312 / 11,312 | **11,312 / 16** | 8 / 8 | 2 | `/orbitalytics/gold/mr_equipment_demand_by_component` |
| **02** | `02_resource_consumption` | `application_1794633145439_0062` | `job_1794633145439_0062` | 21.15s | 9,898 / 9,898 | N/A | 119 / 119 | 2 | `/orbitalytics/gold/mr_resource_consumption_by_year` |
| **03** | `03_missions` | `application_1794633145439_0063` | `job_1794633145439_0063` | 22.37s | 1,500 / 1,500 | N/A | 7 / 7 | 2 | `/orbitalytics/gold/mr_missions_by_agency` |
| **04** | `04_satellites` | `application_1794633145439_0064` | `job_1794633145439_0064` | 20.87s | 2,400 / 2,400 | N/A | 6 / 6 | 2 | `/orbitalytics/gold/mr_satellites_by_orbit_type` |
| **05** | `05_launches` | `application_1794633145439_0065` | `job_1794633145439_0065` | 20.43s | 1,200 / 1,200 | **1,200 / 18** | 17 / 17 | 2 | `/orbitalytics/gold/mr_launches_by_year` |
| **06** | `06_manufacturing` | `application_1794633145439_0066` | `job_1794633145439_0066` | 20.80s | 11,312 / 11,312 | N/A | 8 / 8 | 2 | `/orbitalytics/gold/mr_manufacturing_by_component` |
| **07** | `07_research_investment` | `application_1794633145439_0067` | `job_1794633145439_0067` | 21.04s | 1,414 / 1,414 | N/A | 119 / 119 | 2 | `/orbitalytics/gold/mr_research_investment_by_agency_year` |
| **TOTAL** | **All 7 MapReduce Jobs** | — | — | **147.78s** | **39,036 / 39,036** | **12,512 / 34** | **284 / 284** | **14 Tasks** | **7 Verified Gold Marts** |

---

## 3. Detailed Analytical Findings by Domain

### 3.1 Job 01: Equipment Demand by Component
- **Input Records**: 11,312 orders across 8 mission-critical satellite subsystems.
- **Combiner Effect**: Compressed 11,312 map output records to 16 intermediate records, eliminating **99.86%** of map output network spill.
- **Key Findings**:
  - Highest demanded component: **High-Efficiency Multi-Junction Solar Panels** (77,601 units demanded, $38,554.44M total value, 196.34% combined fulfillment).
  - Longest lead-time component: **C-Band / X-Band Synthetic Aperture Radar (SAR) Antennas** (average 410.9 days lead time, 77,548 units demanded).
  - Shortest lead-time component: **Ultra-Low Jitter Momentum & Reaction Wheels** (157.4 days lead time, 67,510 units demanded).

### 3.2 Job 02: Resource Consumption by Year and Resource
- **Input Records**: 9,898 propellant and raw material consumption transactions.
- **Output Cohorts**: 119 annual resource profiles spanning 2010 through 2026.
- **Key Findings**:
  - Highest volume bulk propellants: **Liquid Oxygen (LOX)** and **RP-1 Kerosene** exceeding 10,000 metric tons consumed annually.
  - Highest value strategic materials: **Radiation Shielding Tantalum & Tungsten Alloys** ($158.7M annually) and **Spacecraft Grade Carbon Composite Prepreg**.

### 3.3 Job 03: Space Missions by Space Agency
- **Input Records**: 1,500 orbital and interplanetary space missions.
- **Output Groups**: 7 global space agencies / commercial consortiums.
- **Key Findings**:
  - Highest total budget: **NASA** ($350,676.86M total mission expenditures, 211 missions).
  - Highest mission success rate: **Japan Aerospace Exploration Agency (JAXA)** at **83.17%**, followed closely by Commercial Space Operators at **82.30%**.
  - Total payload mass deployed: Over 13.8 million kg across all agencies.

### 3.4 Job 04: Satellite Deployment by Orbit Type
- **Input Records**: 2,400 active and historical satellites.
- **Output Groups**: 6 distinct orbital regimes.
- **Key Findings**:
  - Most populated orbit: **LEO (Low Earth Orbit)** with 408 satellites (mean altitude 550.0 km, average dry mass 3,320.9 kg).
  - High-energy orbit: **GEO (Geostationary)** with 399 satellites (mean altitude 35,786.0 km, 10.4 years mean lifetime).
  - Deep Space / Lunar missions: 392 probes (mean altitude 62,607.3 km, power consumption 7,462.1 W).

### 3.5 Job 05: Launch Activities by Year
- **Input Records**: 1,200 orbital launch operations.
- **Combiner Effect**: 1,200 records compressed to 18 combiner records (**98.5% network reduction**).
- **Key Findings**:
  - Annual launch rate grew from 64 launches in 2010 to over 85 launches in recent operational years.
  - Commercialization percentage climbed from **70.31%** in 2010 to peak at **78.4%** in recent years.
  - Overall mission launch success rate remained consistently high between **88.7% and 93.8%**.

### 3.6 Job 06: Manufacturing Quantity by Component
- **Input Records**: 11,312 equipment manufacturing records.
- **Output Groups**: 8 discrete subsystem manufacturing pipelines.
- **Key Findings**:
  - Total units manufactured: 74,307 Multi-Junction Solar Panels, 73,388 SAR Antennas, 73,250 Rad-750 Single Board Computers, and 64,139 Cryogenic Tanks.
  - Average batch size across all component lines: 45.3 to 51.9 units per manufacturing lot.

### 3.7 Job 07: Research Investment by Agency and Year
- **Input Records**: 1,414 monthly agency expenditure reports.
- **Output Cohorts**: 119 agency-year combinations.
- **Key Findings**:
  - R&D investment allocation maintained a steady **48.0% share** of total monthly agency expenditures across major global programs, with infrastructure capturing 28% and operations capturing 24%.

---

## 4. Architectural Analysis: Map, Combiner, Shuffle & Sort, Reducer

1. **Mapper (`sys.stdin` $\to$ `<Key>\t<Values>`):**
   - Pure streaming pipeline parsing incoming text splits without materializing entire files into memory.
   - Enforces schema validity, numerical constraints, and header avoidance.
2. **Combiner (`<Key>\t<Values>` $\to$ `<Key>\t<Pre-aggregated Values>`):**
   - Intercepts map task output locally before serialization to disk/network.
   - Performs partial reductions for associative additions ($\sum$).
   - Dramatically cuts network I/O and reduce-side sorting overhead.
3. **Shuffle & Sort (YARN Distributed Hash Partitioning):**
   - Automatically distributes keys uniformly across 2 reducers.
   - Merges and sorts spilled partitions into ordered key streams.
4. **Reducer (`sys.stdin` $\to$ HDFS Gold Mart):**
   - Iterates through sorted keys, calculating multi-variate statistical rollups, success percentages, and compound aggregates.
   - Generates dual partition files (`part-00000`, `part-00001`) in HDFS Gold.

---

## 5. Automated Test Suite Verification

The Phase 5 test suite [tests/phase_5/test_mapreduce.py](file:///e:/PROJECTS/BDT/tests/phase_5/test_mapreduce.py) was executed with `pytest`:

```
tests/phase_5/test_mapreduce.py::test_mapreduce_scripts_exist PASSED     [ 20%]
tests/phase_5/test_mapreduce.py::test_mapreduce_execution_manifest PASSED [ 40%]
tests/phase_5/test_mapreduce.py::test_mapreduce_gold_hdfs_outputs PASSED [ 60%]
tests/phase_5/test_mapreduce.py::test_mapreduce_combiner_optimization PASSED [ 80%]
tests/phase_5/test_mapreduce.py::test_multi_reducer_partitioning PASSED  [100%]

============================= 5 passed in 33.54s ==============================
```

- **`test_mapreduce_scripts_exist`**: Confirmed presence and non-zero size for all 7 mappers, 7 reducers, 2 combiners, runner, and orchestrator.
- **`test_mapreduce_execution_manifest`**: Confirmed all 7 jobs achieved `status: SUCCESS` with valid `application_*` and `job_*` tokens.
- **`test_mapreduce_gold_hdfs_outputs`**: Confirmed `_SUCCESS` flag and non-empty data files for all 7 HDFS Gold directories.
- **`test_mapreduce_combiner_optimization`**: Confirmed that combiners reduced record volume by >98% before shuffle.
- **`test_multi_reducer_partitioning`**: Confirmed that every job generated exactly 2 partitions (`part-00000`, `part-00001`) reflecting parallel reducer execution.

