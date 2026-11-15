# ORBITALYTICS 2.0 — Big Data Performance Benchmarking Methodology

---

## 1. Experimental Objective & Controlled Design

Phase 10 conducted empirical, controlled performance benchmarking across four distributed and single-node processing frameworks:
1. **Local Python / In-Memory Pandas** (Baseline single-threaded memory execution).
2. **Apache PySpark Engine** (In-memory distributed resilient distributed datasets / DataFrames).
3. **Apache Hive Data Warehouse** (SQL-on-Hadoop running MapReduce/Tez execution plans).
4. **Hadoop Streaming MapReduce** (Two-phase batch shuffle-and-sort execution).
5. **Apache Pig Latin** (Declarative dataflow execution).

### Controlled Test Matrix:
- **Workload 1 (WL1):** Component Demand Aggregation (Group By component, Sum units, Avg cost).
- **Workload 2 (WL2):** Resource Consumption Aggregation (Group By year, resource, Sum tonnage).
- **Workload 3 (WL3):** Space Missions by Agency (Group By agency, Success rate %, Budget sum).
- **Workload 4 (WL4):** Manufacturing Requirements Summary (Order counts, cleanroom hours).
- **Workload 5 (WL5):** Multi-Dataset Relational Join (3-way join: Missions + Launches + Satellites).

### Controlled Dataset Scales:
- **Small:** 1,500 – 2,400 records (Standard canonical telemetry).
- **Medium:** 50,000 records (Synthetically generated via Phase 1 generator).
- **Large:** 250,000 records (Multi-partition stress scale).

---

## 2. Experimental Measurement Metrics

For each trial run, nine empirical metrics were captured:
1. **Wall-Clock Execution Time (s):** Total elapsed time from process invocation to final disk write.
2. **Input Data Size (MB):** Size of raw input files scanned.
3. **Output Data Size (MB):** Size of result artifacts written.
4. **Throughput (Records/sec):** $\frac{\text{Total Input Records}}{\text{Wall-Clock Time (s)}}$.
5. **Peak RAM Utilization (MB):** Peak resident set size (RSS) during execution.
6. **Peak CPU Utilization (%):** Aggregated CPU percentage across available cores.
7. **Shuffle Data Volume (MB):** Intermediate network/disk shuffle payload during partition re-distribution.
8. **GC / JVM Overhead (%):** Percentage of total execution time consumed by Java garbage collection.
9. **Failure / Retry Rate:** Number of task attempts and container failures.

---

## 3. Empirical Results & Findings

### Execution Time by Scale (Workload 1: Equipment Demand)

| Framework | Small (2.4K Rows) | Medium (50K Rows) | Large (250K Rows) | Scaling Factor ($T_{\text{large}} / T_{\text{small}}$) |
| :--- | :--- | :--- | :--- | :--- |
| **Local Pandas** | **0.012 s** | 0.285 s | 1.840 s | $153.3\times$ |
| **Apache PySpark** | 2.140 s | 3.420 s | **4.910 s** | **$2.29\times$** |
| **Hadoop MapReduce**| 12.850 s | 14.120 s | 19.850 s | $1.54\times$ |
| **Apache Hive** | 15.820 s | 16.140 s | 18.250 s | $1.15\times$ |
| **Apache Pig** | 16.450 s | 17.120 s | 20.400 s | $1.24\times$ |

### Scientific Insights:
1. **The Distributed Overhead Threshold:** For small datasets ($< 50,000$ rows), local Pandas outperforms distributed frameworks by up to $1,000\times$ because it incurs zero JVM bootstrap, container negotiation, or network shuffle latency.
2. **Spark's Sub-Linear Scaling Curve:** When scaling from 2.4K rows to 250K rows ($104\times$ data increase), PySpark's execution time only increases from 2.14s to 4.91s ($2.29\times$). Spark's Catalyst optimizer and Tungsten execution engine achieve superior amortized throughput once fixed overhead is amortized.
3. **Hive & MapReduce Fixed Cost Floor:** Hadoop MapReduce and Apache Hive exhibit a flat baseline cost floor of 12–16 seconds regardless of data size, driven by YARN ApplicationMaster container negotiation, DAG construction, and task heartbeat intervals. However, their scalability past millions of records is virtually unlimited.
