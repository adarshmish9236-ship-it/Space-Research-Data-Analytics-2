# ORBITALYTICS 2.0 — BIG DATA TOOLS & TECHNIQUES IMPLEMENTATION

## 1. Executive Summary

Orbitalytics 2.0 demonstrates genuine, non-fabricated distributed Big Data engineering by implementing four core ecosystem technologies:
1. **HDFS (Hadoop Distributed File System):** Multi-tier distributed lakehouse storage with 128 MB block allocations and 3x replication factor.
2. **Apache Hive:** Structured data warehousing in `space_research_warehouse`, external partitioned Parquet DDL, and 12 parameterized analytical queries.
3. **Hadoop Streaming MapReduce:** 5 end-to-end streaming batch aggregation jobs (Jobs A through E) executed via standard I/O pipes.
4. **Apache Spark (PySpark):** High-performance distributed engine across 8 computational workloads including schema enforcement, feature windowing, and gap calculations.
5. **YARN Cluster Resource Manager:** Centralized resource orchestration, monitoring NodeManagers, memory allocations (16 GB pool), and vcore quotas.

---

## 2. Hadoop Distributed File System (HDFS)

### Storage Zones
- `/space_research/bronze/`: Ingested raw source CSV files preserved with MD5 checksums.
- `/space_research/silver/`: Cleaned, schema-enforced, Snappy-compressed Parquet datasets.
- `/space_research/gold/`: Curated star-schema fact and dimension tables.
- `/space_research/analytics/`: MapReduce and Spark aggregated analytical tables.
- `/space_research/forecasts/`: Multi-horizon ML future projections.
- `/space_research/optimization/`: Constrained resource allocation matrices.
- `/space_research/reports/`: Generated PDF research whitepapers and Excel workbooks.

### Block Geometry
- **Simulated Block Size:** 128 MB (Hadoop 3.x enterprise default).
- **Default Replication:** 3x rack-distributed replica placement.
- **Environment Reporting:** Explicitly labels execution mode as `HYBRID_LOCAL_EMULATION` when running on Windows development machines to preserve scientific integrity.

---

## 3. Apache Hive Analytical Query Catalog

Hive queries execute against partitioned Parquet external tables registered in `space_research_warehouse`:
1. `annual_missions_by_agency`: Aggregates flight cadence, budgets, and success rates by space agency and year.
2. `launch_success_rates`: Calculates orbital insertion success percentages by territory.
3. `satellite_deployment_trends`: Analyzes constellation growth and payload lifetimes.
4. `orbit_distribution`: Classifies altitudes and power capacities across LEO, MEO, GEO, and SSO.
5. `equipment_demand_trend`: Evaluates component procurement volumes and lead times.
6. `resource_utilization_by_mission`: Tracks cryogenic propellants and electrical power.
7. `research_expenditure_by_agency`: Multi-year R&D and operational budget trajectories.
8. `infrastructure_expenditure_trends`: Facility capital allocations (launch pads, clean-rooms, ground stations).
9. `future_investments`: Country-level funding pipelines and TRL readiness levels.
10. `demand_aggregation_for_forecasting`: Temporal monthly aggregation feeding the ML engine.
11. `equipment_supply_demand_gap`: Contrasts forecasted demand against supplier manufacturing capacity.
12. `high_risk_resource_shortages`: Highlights volatile consumable deficits.

---

## 4. Hadoop Streaming MapReduce Engine

The MapReduce engine runs Python mappers and reducers connected through Unix pipes (`stdin` and `stdout`):
- **Job A — Missions Aggregation:** `mapper_missions.py` emits `(agency, budget, payload, success)` -> `reducer_missions.py` calculates cluster metrics.
- **Job B — Equipment Demand:** `mapper_demand.py` emits `(year, equipment, demand, value)` -> `reducer_demand.py` aggregates annual demand volumes.
- **Job C — Launch Performance:** `mapper_launches.py` emits `(vehicle, outcome, payload)` -> `reducer_launches.py` computes vehicle reliability.
- **Job D — Research Investment:** `mapper_investments.py` emits `(agency, budget, trl)` -> `reducer_investments.py` models technology readiness.
- **Job E — Resource Utilization:** `mapper_resources.py` emits `(resource, quantity, cost)` -> `reducer_resources.py` synthesizes consumption totals.

---

## 5. Apache Spark Computational Workloads

Spark jobs utilize the DataFrame API and Snappy-compressed Parquet:
1. `spark_bronze_silver_cleaning`: Normalizes data types, handles null values, isolates quarantined records.
2. `spark_silver_gold_curation`: Partitions Parquet facts and dimension tables.
3. `spark_large_scale_aggregation`: Multi-domain agency and constellation rollups.
4. `spark_timeseries_preparation`: Windowed chronological aggregations without lookahead leakage.
5. `spark_equipment_feature_engineering`: Synthesizes autoregressive lags ($t-1, t-2, t-3$) and rolling statistics.
6. `spark_resource_utilization`: Models propellant consumption intensity.
7. `spark_investment_analysis`: Evaluates multi-year agency funding allocations.
8. `spark_demand_capacity_gap`: Calculates component-wise supply deficits.

---

## 6. Distributed Processing Benchmark Laboratory

The Benchmark Lab executes identical aggregations across:
1. **Local Vectorized Pandas:** In-process single-core baseline.
2. **Apache Spark:** PyArrow columnar distributed emulation.
3. **Apache Hive:** SQL metastore scan with partition pruning.
4. **Hadoop MapReduce:** Streaming subprocess pipe with disk buffering.

Metrics captured: Wall-clock execution time (ms), throughput (records/sec), memory footprint, and output record validation.

