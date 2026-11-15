# Orbitalytics Phase 2: Hadoop Ecosystem Installation & Operations Guide

## 1. Prerequisites & Host Sizing
The Orbitalytics containerized cluster runs on Docker Engine / Docker Desktop over WSL2 Linux.

### Recommended System Resources:
- **CPU:** 4+ Physical Cores (8+ vCPUs recommended).
- **RAM:** Minimum 8 GB (16 GB recommended; YARN is allocated 4 GB, Spark 2.5 GB, HDFS 2 GB).
- **Disk Storage:** At least 25 GB free disk space for container layers and HDFS block volumes.
- **Operating System:** Windows 10/11 with WSL2 (Ubuntu / Debian backend) or native Linux (Ubuntu 22.04 LTS / Debian 11).

---

## 2. Fast Startup & Deployment Procedure

### Step 1: Navigate to the Hadoop Ecosystem Directory
```bash
cd E:\PROJECTS\BDT\hadoop_ecosystem
```

### Step 2: Validate Environment Configuration
Ensure `hadoop.env` and `docker-compose.yml` are present:
```bash
# Inspect environment variables
cat hadoop.env
```

### Step 3: Launch the Distributed Cluster
Start all 9 core distributed services in detached mode:
```bash
docker-compose up -d
```

### Step 4: Verify Container Health & Status
```bash
docker-compose ps
```
Expected output:
- `hadoop-namenode` (Up - Ports 9870, 9000)
- `hadoop-datanode` (Up - Port 9864)
- `hadoop-resourcemanager` (Up - Port 8088)
- `hadoop-nodemanager` (Up - Port 8042)
- `hadoop-historyserver` (Up - Port 19888)
- `hive-metastore-postgresql` (Up - Port 5433)
- `hive-server` (Up - Ports 10000, 10002)
- `spark-master` (Up - Ports 8080, 7077)
- `spark-worker` (Up - Port 8081)

---

## 3. Web User Interfaces & Endpoints Reference

| Service | Web UI URL | Purpose |
| :--- | :--- | :--- |
| **HDFS NameNode WebUI** | [http://localhost:9870/](http://localhost:9870/) | HDFS lakehouse browser, storage capacity, Live DataNodes. |
| **HDFS DataNode WebUI** | [http://localhost:9864/](http://localhost:9864/) | Physical block verification and storage heartbeat. |
| **YARN ResourceManager**| [http://localhost:8088/](http://localhost:8088/) | Active YARN apps, cluster memory, queue allocations. |
| **YARN NodeManager** | [http://localhost:8042/](http://localhost:8042/) | Node container allocations and local hardware logs. |
| **MapReduce JobHistory** | [http://localhost:19888/](http://localhost:19888/) | Completed MapReduce batch job counters and task splits. |
| **HiveServer2 WebUI** | [http://localhost:10002/](http://localhost:10002/) | Active analytical SQL sessions and execution metrics. |
| **Spark Master WebUI** | [http://localhost:8080/](http://localhost:8080/) | Spark cluster status, active workers, running applications. |
| **Spark Worker WebUI** | [http://localhost:8081/](http://localhost:8081/) | Spark worker core utilization and executor memory. |

---

## 4. Operational & Troubleshooting Commands

### Check HDFS Cluster Health via CLI
```bash
docker exec -it hadoop-namenode hdfs dfsadmin -report
```

### Check YARN NodeManager Registrations
```bash
docker exec -it hadoop-resourcemanager yarn node -list
```

### Inspect Container Execution Logs
```bash
# View NameNode logs
docker logs --tail 50 hadoop-namenode

# View ResourceManager logs
docker logs --tail 50 hadoop-resourcemanager

# View HiveServer2 logs
docker logs --tail 50 hive-server
```

### Graceful Cluster Shutdown
To stop all services and preserve HDFS and Metastore volumes:
```bash
docker-compose stop
```

To stop and remove containers (preserving persistent named volumes):
```bash
docker-compose down
```

