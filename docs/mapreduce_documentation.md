# ORBITALYTICS 2.0 — Hadoop Streaming MapReduce Specification

---

## 1. MapReduce Architecture & Pipeline

**Hadoop MapReduce** is used for distributed batch aggregation of high-volume Silver telemetry stored across HDFS data blocks. To maximize reliability, modularity, and language independence, ORBITALYTICS utilizes **Hadoop Streaming**, streaming data records line-by-line via standard input (`sys.stdin`) and emitting tab-delimited key-value pairs to standard output (`sys.stdout`).

```
                Hadoop Streaming MapReduce Execution Flow
                -----------------------------------------

  [ Input HDFS File ] (Silver Parquet / CSV via LineRecordReader)
          |
          v
  [ Mapper Phase ] (Python mapper_*.py)
      * Parse line, validate schema, extract group keys (Agency, Component, Year)
      * Emit key-value pair:  "<key>\t<metric_1>,<metric_2>,..."
          |
          v
  [ Distributed Shuffle & Sort ] (Hadoop YARN Infrastructure)
      * Partition keys across reducers via HashPartitioner
      * Secondary merge-sort guarantees all identical keys arrive consecutively
          |
          v
  [ Reducer Phase ] (Python reducer_*.py)
      * State machine groups identical consecutive keys
      * Compute aggregate sums, counts, averages, and rates
      * Handle missing data and numeric precision
      * Emit formatted final result: "<key>\t<aggregate_results>"
          |
          v
  [ Output HDFS File ] (/space_research/aggregates/job_output)
```

---

## 2. Implemented MapReduce Jobs

The platform provides seven dedicated mapper and reducer script pairs in `/mapreduce/`:

| Job Name | Mapper Script | Reducer Script | Map Key | Aggregations Computed |
| :--- | :--- | :--- | :--- | :--- |
| `equipment_demand_by_component` | `mapper_demand.py` | `reducer_demand.py` | `component_name` | Total Units, Mean Unit Cost ($K), Total Valuation ($M), Max Lead Time |
| `resource_consumption_by_year` | `mapper_resources.py`| `reducer_resources.py`| `year\tresource` | Total Consumed Quantity, Total Cost ($K), Average Monthly Draw |
| `missions_by_agency` | `mapper_missions.py` | `reducer_missions.py` | `agency` | Total Missions, Total Budget ($M), Avg Payload (kg), Success Rate (%) |
| `satellites_by_orbit_type` | `mapper_satellites.py`| `reducer_satellites.py`| `orbit_type` | Satellite Count, Mean Altitude (km), Mean Lifespan, Active Rate (%) |
| `launch_activities_by_year` | `mapper_launches.py` | `reducer_launches.py` | `year` | Total Launches, Commercial Count, Total Cost ($M), Mean Payload (kg) |
| `manufacturing_by_component` | `mapper_mfg.py` | `reducer_mfg.py` | `component_type` | Order Count, Total Units Built, Mean Cleanroom Hours, Pass Rate (%) |
| `research_investment_by_agency`| `mapper_invest.py` | `reducer_invest.py` | `agency\tyear` | Total R&D ($M), Infrastructure ($M), Operations ($M), Grand Total |

---

## 3. Representative Implementation (`missions_by_agency`)

### 3.1 Mapper (`mapper_missions.py`)
```python
#!/usr/bin/env python3
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("mission_id"):
            continue  # Skip empty lines and header
        
        parts = line.split(",")
        if len(parts) < 10:
            continue  # Malformed row safety check
        
        agency = parts[2].strip()
        try:
            budget = float(parts[7].strip()) if parts[7].strip() else 0.0
            payload = float(parts[8].strip()) if parts[8].strip() else 0.0
            status = parts[9].strip().lower()
            is_success = 1 if status in ["successful", "in-flight", "operational"] else 0
            
            # Emit: agency \t count,budget,payload,is_success
            print(f"{agency}\t1,{budget:.2f},{payload:.2f},{is_success}")
        except ValueError:
            continue

if __name__ == "__main__":
    main()
```

### 3.2 Reducer (`reducer_missions.py`)
```python
#!/usr/bin/env python3
import sys

def main():
    current_agency = None
    total_missions = 0
    total_budget = 0.0
    total_payload = 0.0
    successful_missions = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            agency, values = line.split("\t", 1)
            count, budget, payload, is_success = values.split(",")
            count = int(count)
            budget = float(budget)
            payload = float(payload)
            is_success = int(is_success)
        except ValueError:
            continue

        if current_agency == agency:
            total_missions += count
            total_budget += budget
            total_payload += payload
            successful_missions += is_success
        else:
            if current_agency is not None:
                avg_payload = total_payload / total_missions if total_missions > 0 else 0.0
                success_rate = (successful_missions / total_missions * 100.0) if total_missions > 0 else 0.0
                print(f"{current_agency}\t{total_missions}\t{total_budget:.2f}\t{avg_payload:.2f}\t{success_rate:.2f}")

            current_agency = agency
            total_missions = count
            total_budget = budget
            total_payload = payload
            successful_missions = is_success

    # Flush final key
    if current_agency is not None:
        avg_payload = total_payload / total_missions if total_missions > 0 else 0.0
        success_rate = (successful_missions / total_missions * 100.0) if total_missions > 0 else 0.0
        print(f"{current_agency}\t{total_missions}\t{total_budget:.2f}\t{avg_payload:.2f}\t{success_rate:.2f}")

if __name__ == "__main__":
    main()
```

---

## 4. Execution Command on Hadoop YARN

```bash
docker exec -it hadoop-resourcemanager hadoop jar \
    /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -D mapreduce.job.name="Orbitalytics Missions Aggregation" \
    -D mapreduce.job.reduces=2 \
    -input /space_research/raw/space_missions.csv \
    -output /space_research/aggregates/missions_by_agency \
    -mapper "python3 /mapreduce/mapper_missions.py" \
    -reducer "python3 /mapreduce/reducer_missions.py"
```
The execution plan creates genuine YARN applications with status reports, task container allocations, and aggregate output written directly back to HDFS.
