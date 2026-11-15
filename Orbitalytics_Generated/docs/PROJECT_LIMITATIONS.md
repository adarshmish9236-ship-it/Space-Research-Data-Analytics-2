# ORBITALYTICS 2.0 — PROJECT LIMITATIONS & FUTURE EXTENSIONS

## 1. Scientific Integrity & Known Limitations

To maintain academic credibility and research transparency, Orbitalytics 2.0 explicitly documents all operational boundaries and development assumptions:

### 1.1 Synthetic vs Real Space Telemetry
- The 9 space research datasets are synthetically generated based on published aerospace industry statistics (NASA, ESA, ISRO, Space-Track).
- All records carry explicit metadata flags (`data_source: SYNTHETIC_SIMULATION_V2`, `is_synthetic: TRUE`) to prevent misrepresentation as genuine space agency telemetry.

### 1.2 Storage Mode (Local Emulation vs Distributed Cluster)
- When executed in local development mode without a running multi-node Hadoop cluster, the system operates in `HYBRID_LOCAL_EMULATION` mode.
- Block sizes (128 MB) and 3x replication factors are calculated mathematically to reflect true distributed HDFS block topology without requiring multi-terabyte disk allocations on developer laptops.
- For Docker-based distributed execution, the provided `docker-compose.yml` deploys genuine Apache Hadoop NameNodes, DataNodes, and HiveServer2 daemons.

### 1.3 MapReduce Subprocess Execution
- In Windows local mode, Hadoop Streaming jobs execute mappers and reducers using native Python subprocess pipes (`stdin`/`stdout`).
- While identical in logic and data contracts to production Hadoop Streaming, cluster-level YARN container isolation requires a Linux/Docker host environment.

---

## 2. Recommended Future Research Extensions

1. **Live NASA Open API Integration:** Connecting real-time ingestion adapters to NASA Small-Body Database, Horizons API, and ESA Telemetry portals.
2. **Deep Learning Sequence Models:** Extending the forecasting library to include Temporal Fusion Transformers (TFT) and N-BEATS when multi-decade historical hourly datasets become available.
3. **Graph Neural Networks for Constellation Routing:** Modeling inter-satellite optical link latency across mega-constellations in Low Earth Orbit (LEO).
4. **Quantum Annealing for Procurement:** Reformulating the multi-constraint aerospace procurement optimization problem as a Quadratic Unconstrained Binary Optimization (QUBO) problem for D-Wave quantum annealers.

