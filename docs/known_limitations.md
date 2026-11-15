# ORBITALYTICS 2.0 — Known System Limitations & Constraints

---

## 1. Architectural & Execution Limitations

In strict adherence to academic integrity and transparency, the following technical boundaries and operational constraints are documented:

### 1.1 Single-Node Docker Containerization
- **Constraint:** The development cluster runs on a single host machine inside nine orchestrated Docker containers. While each container simulates a discrete cluster node (NameNode, DataNode, ResourceManager, NodeManager, HiveServer, Spark Master, Spark Worker), all containers share the host's underlying physical CPU, RAM, and NVMe disk bus.
- **Consequence:** Network I/O latency between cluster components is near-zero (loopback/virtual bridge), whereas a physical multi-rack data center would incur inter-rack network switch delays.

### 1.2 Python Version Constraints in Big Data Containers
- **Constraint:** Off-the-shelf Apache Hadoop and Apache Spark Docker base images (`bde2020`) ship with older system runtimes (Debian/CentOS with Python 3.5 or Python 2.7 for Hadoop Streaming).
- **Consequence:** MapReduce mapper and reducer scripts are engineered to use pure standard library constructs compatible across Python 3.5 through Python 3.14 without modern third-party C-extensions inside the streaming container.

### 1.3 Asynchronous Multipart File Upload in Python 3.14
- **Constraint:** In Python 3.14 on Windows, Starlette's `TestClient` utilizing `httpx` encounters an internal threadpool deadlock when streaming multipart/form-data files over in-process memory channels without a live TCP socket.
- **Consequence:** The live HTTP API running on Uvicorn handles file uploads normally over standard TCP, but in-process Pytest suites must test multipart handler logic directly rather than through ASGI TestClient file streaming.

---

## 2. Data & Modeling Limitations

### 2.1 Synthetic Telemetry Generator Boundaries
- **Constraint:** The 9 canonical datasets were synthesized using the Phase 1 generation engine, calibrated against published historical space mission parameters (NASA decadal surveys, ESA budgets, UCS satellite database).
- **Consequence:** While the data accurately reflects secular growth trends, seasonal quarterly cycles, and known spaceport locations, it cannot account for unanticipated geopolitical supply shocks (e.g., sudden export embargoes on specific rare-earth elements) not encoded in the synthetic distribution.

### 2.2 Quarterly Aggregate Frequency
- **Constraint:** The historical baseline spans 67 quarterly observations (2010 Q1 through 2026 Q3).
- **Consequence:** While 67 quarters is sufficient for seasonal ARIMA and rolling-window Random Forest models with lag orders $p \le 4$, it provides limited degrees of freedom for deep learning architectures (e.g., LSTM, Transformer) which typically require tens of thousands of continuous time-steps to avoid severe overfitting.

### 2.3 Optimization Solver Relaxations
- **Constraint:** The Mixed-Integer Linear Programming (MILP) model assumes constant unit procurement costs and deterministic delivery lead-times within each scenario horizon.
- **Consequence:** Non-linear volume discounts (economies of scale) or stochastic supplier disruptions are evaluated via scenario sensitivity sweeps rather than continuous stochastic dynamic programming.
