# ORBITALYTICS 2.0 — Troubleshooting & Operational Runbook

---

## 1. Common Issues & Quick Resolutions

### 1.1 Port Conflicts (Ports 8000, 9000, 9870, 8088, 10000)
- **Symptom:** Docker container fails to start with `bind: address already in use` or Uvicorn server exits immediately.
- **Cause:** Another process or previous instance is holding the port.
- **Resolution:**
  ```powershell
  # Find PID using port (e.g. 8000)
  Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
  # Terminate offending PID
  Stop-Process -Id <PID> -Force
  ```

### 1.2 Docker Container Named Pipe Access Denied
- **Symptom:** `permission denied while trying to connect to the docker API at npipe:////./pipe/docker_engine`.
- **Cause:** Docker Desktop is stopped, restarting, or the current user is not in the `docker-users` group.
- **Resolution:**
  1. Open Docker Desktop application from the Windows Start menu.
  2. Verify the engine icon in the lower-left displays green (Engine running).
  3. Run `docker ps` from PowerShell to verify connectivity.

### 1.3 HDFS SafeMode Is ON
- **Symptom:** `org.apache.hadoop.hdfs.server.namenode.SafeModeException: Cannot create directory /space_research. Name node is in safe mode.`
- **Cause:** NameNode enters SafeMode upon boot while waiting for DataNodes to report block status.
- **Resolution:**
  ```bash
  docker exec -it hadoop-namenode hdfs dfsadmin -safemode leave
  ```

### 1.4 HiveServer2 Thrift Connection Refused
- **Symptom:** Beeline fails with `Could not open client transport with JDBC Uri: Connection refused`.
- **Cause:** HiveServer2 is still compiling its initial schema or waiting for Metastore PostgreSQL to become healthy.
- **Resolution:**
  Wait 20–30 seconds after `docker compose up -d` before initiating JDBC queries, or check logs:
  ```bash
  docker logs --tail 50 hive-server
  ```

### 1.5 PyArrow Categorical Comparison TypeError
- **Symptom:** `TypeError: Unordered Categoricals can only compare equality or not`.
- **Cause:** Partitioned Parquet columns (e.g., `year`) loaded via `pd.read_parquet` are typed as unordered Categorical on newer pandas/pyarrow engines.
- **Resolution:**
  Cast the categorical series explicitly before range comparisons:
  ```python
  df["year"] = df["year"].astype(int)
  mask = df["year"] >= 2022
  ```

---

## 2. Cluster Health Diagnostic Script

Execute the built-in diagnostic probe to verify all cluster subsystems:
```powershell
python -c "from app.services.ecosystem_service import EcosystemService; print(EcosystemService().probe_cluster_health())"
```
