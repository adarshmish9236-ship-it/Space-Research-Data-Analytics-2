# ORBITALYTICS — PHASE 5: HADOOP MAPREDUCE ARCHITECTURE & DESIGN SPECIFICATION

## 1. Executive Overview

This specification details the design and distributed implementation of **Phase 5: Hadoop MapReduce Implementation** for **ORBITALYTICS: Space Research Data Analytics: A Hadoop Ecosystem Approach to Demand Forecasting**.

The MapReduce processing tier performs high-throughput distributed batch aggregation over cleansed HDFS Silver datasets (`/orbitalytics/silver/pig_*`), outputting business intelligence marts into the HDFS Gold tier (`/orbitalytics/gold/mr_*`).

Jobs are executed through **Hadoop Streaming (`hadoop-streaming-3.2.1.jar`)** running against the live multi-node Apache Hadoop YARN cluster.

---

## 2. Distributed Architecture: Map, Combiner, Shuffle & Sort, Reducer

```
+---------------------------------------------------------------------------------------------------+
|                                      HDFS SILVER DATA LAKE                                        |
|  (/orbitalytics/silver/pig_equipment_demand, pig_missions, pig_satellites, pig_launches, etc.)   |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                          MAP PHASE                                                |
|  - InputFormat: TextInputFormat splits HDFS block files                                          |
|  - Streamed line-by-line into Python Mapper via sys.stdin                                         |
|  - Safe parsing (csv.reader, type coercion, null checks, header stripping)                       |
|  - Emits tab-delimited key-value tuples: <Key>\t<val1,val2,...,valN,count>                        |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                COMBINER PHASE (Local Pre-Aggregation)                             |
|  - Runs locally in-memory/spill on each NodeManager map task                                      |
|  - Evaluates associative & commutative operations (Sum, Count)                                    |
|  - Drastically compresses network payloads before network serialization                           |
|  - Demonstrated in Job 01 (Equipment Demand) and Job 05 (Launch Activities)                       |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                     SHUFFLE & SORT PHASE                                          |
|  - Distributed Partitioning: HashPartitioner routes keys across N reducers                        |
|  - HTTP Network Fetch: Reducer nodes pull mapped partitions across the cluster                    |
|  - External Merge Sort: Combines spilled map outputs into contiguous sorted streams               |
|  - Key Grouping: Groups identical keys for sequential reducer consumption                         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                        REDUCE PHASE                                               |
|  - Multi-Reducer Execution (numReduceTasks = 2)                                                   |
|  - Reads grouped key records sequentially from sys.stdin                                          |
|  - Computes exact metrics (totals, averages, rates, fulfillment %, payload ratios)                |
|  - Emits formatted tab-delimited records to sys.stdout                                             |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                       HDFS GOLD MARTS                                             |
|  (/orbitalytics/gold/mr_equipment_demand_by_component/part-00000, part-00001)                      |
|  (/orbitalytics/gold/mr_resource_consumption_by_year/part-00000, part-00001)                       |
|  (/orbitalytics/gold/mr_missions_by_agency/part-00000, part-00001)                                 |
|  (/orbitalytics/gold/mr_satellites_by_orbit_type/part-00000, part-00001)                           |
|  (/orbitalytics/gold/mr_launches_by_year/part-00000, part-00001)                                   |
|  (/orbitalytics/gold/mr_manufacturing_by_component/part-00000, part-00001)                         |
|  (/orbitalytics/gold/mr_research_investment_by_agency_year/part-00000, part-00001)                 |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Detailed Component Roles

### 3.1 The Mapper Phase
- **Input Mechanism**: Reads line by line from `sys.stdin`.
- **Validation**: Strips whitespace, skips header records (`demand_id`, `mission_id`, etc.), ignores corrupted lines with insufficient column counts, and strictly enforces domain ranges (e.g. `year >= 1957`, `cost > 0`).
- **Data Emission**: Projects relevant numerical attributes and outputs `<Key>\t<Values,Count>` to `sys.stdout`.

### 3.2 The Combiner Phase
- **Theoretical Foundation**: An associative function satisfies $f(a, f(b, c)) = f(f(a, b), c)$ and a commutative function satisfies $f(a, b) = f(b, a)$. For additions such as:
  $$\text{Total Demanded} = \sum_{i} u_i, \quad \text{Total Cost} = \sum_{i} c_i, \quad \text{Count} = \sum_{i} 1$$
- **Bandwidth Optimization**: In Job 01, 11,312 map output records are compressed to just 16 records before traversing the cluster network, yielding a **99.85% network I/O reduction**.

### 3.3 The Shuffle & Sort Phase
- Genuine YARN MapReduce engine manages the shuffle. No local sorting or artificial in-memory dictionary shuffles are used.
- The framework guarantees that every reducer receives keys in strictly non-decreasing sorted order, with all values for a given key delivered to a single reducer partition.

### 3.4 The Reducer Phase
- **Multi-Reducer Scalability**: Two parallel reducers (`-numReduceTasks 2`) run simultaneously on YARN, balancing key partitions across cluster nodes.
- **Metric Formulation**: Computes derived indicators including fulfillment percentages, average lead times, launch success percentages, and compound budget averages.

---

## 4. MapReduce Jobs Specification Matrix

| Job ID | Script Base Name | Input HDFS Path | Output HDFS Path | Grouping Key | Output Metrics Computed |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | `01_equipment_demand` | `/orbitalytics/silver/pig_equipment_demand` | `/orbitalytics/gold/mr_equipment_demand_by_component` | `component_name` | Total demanded, manufactured, procured, avg demanded, avg lead time, total value ($M), fulfillment %, order count. |
| **02** | `02_resource_consumption` | `/orbitalytics/silver/pig_resource_consumption` | `/orbitalytics/gold/mr_resource_consumption_by_year` | `year::resource_name` | Total quantity, total procurement cost ($K, $M), avg event quantity, event count. |
| **03** | `03_missions` | `/orbitalytics/silver/pig_missions` | `/orbitalytics/gold/mr_missions_by_agency` | `agency_name` | Total missions, successful missions, success rate %, total budget ($M), avg budget ($M), total payload (kg), avg payload (kg), total crew, avg duration (days). |
| **04** | `04_satellites` | `/orbitalytics/silver/pig_satellites` | `/orbitalytics/gold/mr_satellites_by_orbit_type` | `orbit_type` | Satellite count, avg altitude (km), avg inclination (deg), avg lifetime (years), total mass (kg), avg mass (kg), avg power (W), total power (kW). |
| **05** | `05_launches` | `/orbitalytics/silver/pig_launches` | `/orbitalytics/gold/mr_launches_by_year` | `year` | Total launches, successful launches, success rate %, commercial launches, commercial rate %, total cost ($M), avg cost ($M), total payload (kg), avg payload (kg). |
| **06** | `06_manufacturing` | `/orbitalytics/silver/pig_equipment_demand` | `/orbitalytics/gold/mr_manufacturing_by_component` | `component_name` | Total manufactured units, avg units per order, total manufacturing cost ($K, $M), total order count. |
| **07** | `07_research_investment` | `/orbitalytics/silver/pig_agency_expenditure` | `/orbitalytics/gold/mr_research_investment_by_agency_year` | `agency_name::year` | Total R&D investment ($M), total infra ($M), total operations ($M), grand total ($M), R&D share %, reporting months count. |

---

## 5. Execution Environment & Parameters

- **Hadoop Version**: 3.2.1
- **Python Execution Runtime**: Python 3.5.3 (Debian Stretch cluster container runtime)
- **Streaming Jar**: `/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar`
- **Memory Allocation**:
  - `mapreduce.map.memory.mb`: 1024 MB
  - `mapreduce.reduce.memory.mb`: 1024 MB
- **Parallel Reducers**: 2 tasks per job

