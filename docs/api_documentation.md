# ORBITALYTICS 2.0 — REST API Specification & Endpoint Catalog

---

## 1. Overview

The ORBITALYTICS REST API is powered by **FastAPI** and provides high-performance asynchronous endpoints structured under the versioned route prefix `/api/v1/` (with dual mounting at `/api/` for backwards compatibility). The API enables programmatic access to all eight platform functional modules.

Interactive Swagger/OpenAPI documentation is available at `http://localhost:8000/docs`.

---

## 2. Complete Endpoint Catalog

### Module 1: Executive Overview
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/overview/kpis` | Platform-wide KPIs: total missions, satellites, budgets, quality scores | `OverviewKPIsResponse` |
| `GET` | `/api/v1/overview/insights` | Automated natural language intelligence insights | `List[InsightItem]` |
| `GET` | `/api/v1/overview/activity` | Recent pipeline execution activity logs | `List[ActivityItem]` |

### Module 2: Data Management & Ingestion
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/data/inventory` | Inventory of all 9 datasets across HDFS zones | `DatasetInventoryResponse` |
| `POST`| `/api/v1/data/upload` | Multipart file upload with schema validation & checksums | `FileUploadResponse` |
| `GET` | `/api/v1/data/governance/catalog` | Data governance catalog with provenance & MD5 signatures | `GovernanceCatalogResponse` |
| `GET` | `/api/v1/data/governance/quality` | Statistical data quality audits (IQR & Z-score anomalies) | `GovernanceQualityResponse` |
| `GET` | `/api/v1/data/pipeline/history` | Historical ETL pipeline run telemetry | `List[PipelineRunItem]` |

### Module 3: Hadoop Ecosystem Control
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/ecosystem/health` | Real-time TCP/RPC port probes for HDFS, YARN, Hive, Spark | `EcosystemHealthResponse` |
| `GET` | `/api/v1/ecosystem/hdfs/overview` | HDFS cluster storage, file count, and zone breakdown | `HDFSOverviewResponse` |
| `GET` | `/api/v1/ecosystem/yarn/status` | YARN resource manager allocation and active NodeManagers | `YARNStatusResponse` |
| `GET` | `/api/v1/ecosystem/mapreduce/jobs` | MapReduce job catalog and recent execution telemetry | `MapReduceCatalogResponse` |
| `POST`| `/api/v1/ecosystem/mapreduce/run/{job_name}` | Triggers distributed MapReduce job on YARN | `MRRunResponse` |
| `GET` | `/api/v1/ecosystem/spark/jobs` | PySpark cluster master status and distributed pipelines | `SparkCatalogResponse` |
| `GET` | `/api/v1/ecosystem/pig/jobs` | Apache Pig Latin script inventory and execution state | `PigCatalogResponse` |
| `POST`| `/api/v1/ecosystem/pig/run/{script_name}` | Executes Pig Latin data sanitation job | `PigRunResponse` |
| `GET` | `/api/v1/ecosystem/hive/tables` | Hive Data Warehouse dimension and fact table metadata | `HiveCatalogResponse` |
| `GET` | `/api/v1/ecosystem/hive/query/{query_id}` | Executes pre-compiled or ad-hoc Hive SQL query | `HiveQueryResponse` |

### Module 4: Space Research Analytics
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/analytics/missions` | Missions by agency, status breakdown, and payload trends | `MissionsAnalyticsResponse` |
| `GET` | `/api/v1/analytics/satellites` | Orbital satellite distribution, altitude, and longevity | `SatellitesAnalyticsResponse` |
| `GET` | `/api/v1/analytics/launches` | Launch vehicle cadence, costs, and success rates | `LaunchesAnalyticsResponse` |
| `GET` | `/api/v1/analytics/equipment` | Component demand totals and expenditure distribution | `EquipmentAnalyticsResponse` |
| `GET` | `/api/v1/analytics/resources` | Propellant, cryogenic, and telemetry burn rates | `ResourcesAnalyticsResponse` |
| `GET` | `/api/v1/analytics/manufacturing` | Aerospace cleanroom order backlog and throughput | `ManufacturingAnalyticsResponse` |
| `GET` | `/api/v1/analytics/investments` | Decadal research budget allocations by agency | `InvestmentsAnalyticsResponse` |
| `GET` | `/api/v1/analytics/geographic` | Global spaceports, launch locations, and coordinates | `GeographicAnalyticsResponse` |

### Module 5: Forecasting Studio
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/forecasting/models` | Catalog of 13 supported forecasting algorithms | `List[ModelDescriptor]` |
| `GET` | `/api/v1/forecasting/series` | Available time-series targets and historical coverage | `List[SeriesDescriptor]` |
| `GET` | `/api/v1/forecasting/comparison` | Backtested metric comparison matrix (RMSE, MAE, WAPE, R²)| `List[ModelEvaluationRecord]` |
| `GET` | `/api/v1/forecasting/projections` | 4-Quarter forward projections with 80% & 95% CIs | `ForecastProjectionsResponse` |
| `POST`| `/api/v1/forecasting/run` | Triggers dynamic multi-horizon forecast execution | `DynamicForecastResponse` |
| `GET` | `/api/v1/forecasting/registry` | Production Model Registry with Champion/Challenger status | `ModelRegistryResponse` |

### Module 6: Resource Planning & Optimization
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/optimization/shortages` | Identified hardware component and propellant deficits | `List[ShortageRecord]` |
| `GET` | `/api/v1/optimization/scenarios` | Pre-configured supply chain optimization scenarios | `List[ScenarioRecord]` |
| `POST`| `/api/v1/optimization/solve` | Solves SciPy HiGHS MILP constrained procurement model | `MILPSolutionResponse` |
| `GET` | `/api/v1/optimization/tornado` | Sensitivity tornado analysis on costs, lead-times, and capacity| `TornadoAnalysisResponse` |

### Module 7: Big Data Performance Benchmarking
| Method | Endpoint | Description | Return Schema |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/benchmarks/summary` | Executive summary of engine performance and speedups | `BenchmarkSummaryResponse` |
| `GET` | `/api/v1/benchmarks/matrix` | Full empirical benchmark matrix (75 trials) | `List[BenchmarkTrial]` |
| `GET` | `/api/v1/benchmarks/scaling` | Scaling curves across Small, Medium, and Large data sizes | `List[ScalingCurveRecord]` |

### Module 8: Report Generation & Exports
| Method | Endpoint | Description | Content-Type |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/reports/pdf` | Synthesizes formal publication-grade executive PDF whitepaper | `application/pdf` |
| `GET` | `/api/v1/reports/excel` | Multi-sheet Lakehouse Excel workbook with full data catalog | `application/vnd.openxmlformats` |
| `GET` | `/api/v1/reports/csv` | Exports raw or forecast dataset extracts | `text/csv` |
