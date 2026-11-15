# Orbitalytics: Interactive User & Evaluation Guide

Step-by-step walkthrough of the Orbitalytics platform features and demonstration workflows.

---

## 1. Navigating the Two Presentation Layers

The top navigation header features the **Layer Switcher**:
- Click **Research Intelligence** to evaluate high-level mission findings, territory breakdowns, and demand forecasts.
- Click **Big Data Engineering** to inspect HDFS storage tiers, run Hive SQL queries, trigger MapReduce jobs, and monitor PySpark pipeline stages.

---

## 2. Research Intelligence Walkthrough

### 2.1 Executive Overview
- Review high-level KPI cards (Total Missions, Active Satellites, Launch Success Rate, Curated Records).
- Read dynamically computed automated insights.
- Inspect annual launch cadences and cumulative agency budget allocations.

### 2.2 Geographic & Territory Analytics (ESPI-Inspired)
- Review private vs. public launch ownership splits.
- Examine launches by territory (USA, Europe, India, China, Japan, Russia).
- View global spaceport coordinates and performance benchmarks.

### 2.3 Demand Forecasting & Policy Scenario Simulator
1. Select a **Target Dimension** (e.g., *Space Equipment & Components*).
2. Choose a **Prediction Horizon** (3, 6, 12, or 36 Months).
3. Select an **ML Algorithm** (*Random Forest*, *Gradient Boosting*, *Exponential Smoothing*, etc.).
4. Click **Run Forecast**.
5. Observe the dual-axis chart comparing historical actuals against the predicted trajectory with the 95% Confidence Interval band.
6. Use the **Policy Scenario Simulator** sliders (R&D Investment, Launch Cadence, Cost Variation) and click **Simulate Policy Impact** to generate optimistic and conservative trajectories.

### 2.4 Data Explorer
- Select any of the 9 space research datasets.
- Search by keyword and navigate server-side pages.
- Click **Download CSV** to export raw records.

### 2.5 Reports & Document Export
- Click **Download PDF** to generate an executive ReportLab whitepaper.
- Click **Download Excel** to export an OpenPyXL formatted multi-sheet workbook.
- Click **Export CSV** to download the active forecast matrix.

---

## 3. Big Data Engineering Walkthrough

### 3.1 Pipeline Monitor
- Inspect the 6-stage distributed execution graph:
  * Ingestion $\to$ HDFS Replication $\to$ Spark Cleanroom $\to$ Hive Catalog $\to$ MapReduce $\to$ ML Inference.
- Check daemon CPU, RAM, disk, and uptime for `NameNode`, `DataNodes`, `ResourceManager`, and `HiveServer2`.

### 3.2 HDFS Lakehouse Tiers
- Inspect physical file counts, storage bytes, and 128 MB block allocations across `raw`, `processed`, `curated`, `analytics`, `forecasts`, and `reports`.

### 3.3 Apache Hive Query Console
- Select any pre-configured analytical SQL query (or run custom queries).
- Observe actual execution duration in milliseconds, schema column definitions, and returned row counts.

### 3.4 Hadoop Streaming MapReduce Runner
- Choose a job (*missions_aggregation*, *demand_aggregation*, or *launches_aggregation*).
- Click **Run MR Job**.
- Inspect YARN Application ID, mapper input records, and reducer grouped outputs saved to `/space_research/analytics/`.

