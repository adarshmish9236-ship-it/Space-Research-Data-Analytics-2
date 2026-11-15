# ORBITALYTICS 2.0 — Installation & Deployment Guide

---

## 1. System Requirements

### 1.1 Hardware Specifications
- **Processor:** x86_64 Quad-Core CPU (Intel i5/i7/Xeon or AMD Ryzen 5/7/Threadripper) or equivalent.
- **Memory (RAM):** 16 GB minimum recommended (8 GB allocated to Docker containers, 8 GB for Host OS & Python analytics).
- **Disk Space:** 25 GB free disk space (NVMe SSD strongly recommended for fast Parquet I/O).

### 1.2 Software Prerequisites
- **Operating System:** Windows 10/11 (with WSL2 enabled), Ubuntu 22.04 LTS, or macOS 13+.
- **Container Runtime:** Docker Desktop (v4.20+) or Docker Engine with Docker Compose v2.
- **Python Environment:** Python 3.10 to Python 3.14 with `pip` and virtual environment support.
- **Java Runtime:** OpenJDK 8 or 11 (required for local Hadoop/Spark utilities if running outside Docker).

---

## 2. Quick-Start Setup Sequence

### Step 1: Clone Repository & Navigate to Workspace
```bash
git clone https://github.com/space-analytics/orbitalytics.git
cd orbitalytics
```

### Step 2: Establish Python Virtual Environment & Install Dependencies
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Step 3: Launch Dockerized Hadoop Ecosystem
```bash
# Navigate to Docker environment directory
cd docker

# Spin up complete 9-container Big Data cluster
docker compose up -d

# Verify all containers are healthy
docker compose ps
```

Expected healthy containers:
- `hadoop-namenode` (Port 9000, 9870)
- `hadoop-datanode` (Port 9864)
- `hadoop-resourcemanager` (Port 8032, 8088)
- `hadoop-nodemanager` (Port 8042)
- `hadoop-historyserver` (Port 8188)
- `hive-metastore-postgresql` (Port 5432)
- `hive-server` (Port 10000, 10002)
- `spark-master` (Port 7077, 8080)
- `spark-worker` (Port 8081)

### Step 4: Run End-to-End Ingestion & Verification
```powershell
# From project root
python scripts/run_e2e_pipeline.py
```

### Step 5: Start FastAPI Backend & Access Dashboard
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open your web browser and navigate to:
- **Application Dashboard:** `http://localhost:8000/`
- **Interactive OpenAPI Documentation:** `http://localhost:8000/docs`
- **HDFS NameNode UI:** `http://localhost:9870/`
- **YARN Resource Manager UI:** `http://localhost:8088/`
- **Spark Cluster UI:** `http://localhost:8080/`

---

## 3. Verification & Acceptance Testing

Run the automated test suite to ensure that all 80 system tests pass:
```powershell
python -m pytest tests/phase_12 -v
```
All 80 tests should complete with `100% PASSED` in under 10 seconds.
