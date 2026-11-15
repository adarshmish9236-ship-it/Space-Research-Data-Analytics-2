# Orbitalytics Phase 2: Big Data Ecosystem Compatibility Matrix

## 1. Overview & Theoretical Coherence
A frequent pitfall in big data deployments is combining incompatible versions of distributed engines, storage protocols, and runtime virtual machines. For example:
- Running Hadoop 3.x with Java 17 directly triggers byte-code reflection errors in the Java security manager.
- Hive 2.x requires specific Hadoop 2.7 / 3.2 binary shims to resolve class loading.
- PySpark 3.1.x requires specific `hadoop-aws` / `hadoop-client` 3.2.x dependencies.

Orbitalytics selects an industry-tested, mathematically coherent technology stack pinned to **Hadoop 3.2.1 and Java 8 (OpenJDK 1.8.0)**.

---

## 2. Technology Stack Compatibility Matrix

| Component | Selected Version | Runtime / Host Platform | Compatible Version Range | Technical Compatibility Justification |
| :--- | :--- | :--- | :--- | :--- |
| **Apache Hadoop** | **3.2.1** | Linux (Debian 9/10 / Alpine) | Hadoop 3.2.0 – 3.3.1 | Core distributed storage (HDFS) and resource negotiation (YARN). Pinned to 3.2.1 for maximum Hive/Spark compatibility. |
| **Java Runtime (JVM)** | **OpenJDK 8u212** | Container Internal | OpenJDK 8 (1.8.0) | Standard JVM for Hadoop 3.2.x and Hive 2.3.x. Avoids Java 9+ module isolation issues (`--illegal-access=permit`). |
| **Host OS / Engine** | **Docker Desktop 29.4** | Windows 11 / WSL2 Linux 6.6 | Docker Engine >= 20.10 | Native Linux execution inside WSL2 avoids Windows POSIX emulation issues with `winutils.exe` and `hadoop.dll`. |
| **Apache Hive** | **2.3.2** | JVM 8 / PostgreSQL Metastore | Hive 2.3.x – 3.1.2 | Provides structured SQL table warehousing over HDFS-backed Parquet storage. Uses PostgreSQL JDBC driver. |
| **Hive Metastore DB** | **PostgreSQL 13 / 9.6** | Container Internal | Postgres 9.6 – 13.x | Persistent relational storage for Hive schemas, avoiding ephemeral Derby file locking limitations. |
| **Apache Pig** | **0.17.0** | JVM 8 / Hadoop 3.2.x | Pig 0.16 – 0.17 | Scripting dataflow language for batch extract-transform-load (ETL) running over MapReduce. |
| **Apache Spark** | **3.1.2** | JVM 8 / Scala 2.12 | Spark 3.0.x – 3.2.x | High-throughput distributed in-memory data processing, Spark SQL, and machine learning engine (MLlib). |
| **PySpark** | **3.1.2 / 3.3.x** | Python 3.8 – 3.11 | Python >= 3.7 | Python API for Apache Spark supporting distributed DataFrame operations and pipeline stages. |
| **Host Python** | **Python 3.14.0** | Windows 11 Host | Python >= 3.9 | Hosts FastAPI backend, REST endpoints, and orchestration clients communicating via WebHDFS & JDBC. |

---

## 3. Storage & Serialization Compatibility

| Format / Protocol | Version / Standard | Integration Target | Compatibility Notes |
| :--- | :--- | :--- | :--- |
| **Apache Parquet** | Format 2.4+ / Snappy | HDFS, Hive, PySpark | Columnar storage format with embedded dictionary encoding and statistics. |
| **WebHDFS** | v1 HTTP REST API | Python `requests`, FastAPI | Allows host machine and external APIs to stream files in/out of HDFS without local Hadoop binaries. |
| **Thrift Protocol** | Thrift v0.9.3 | HiveServer2, Beeline, Spark SQL | Remote procedure call protocol for executing analytical SQL queries. |
| **YARN REST API** | Hadoop 3.2 Cluster API | FastAPI Cluster Monitor | Provides real-time metrics on allocated memory, vcores, active NodeManagers, and queue statuses. |

