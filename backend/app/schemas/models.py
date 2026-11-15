"""
ORBITALYTICS Phase 11 — Enterprise Pydantic Schemas & Data Transfer Objects (DTOs)
Provides validation, serialization, and OpenAPI documentation across all 8 modules.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


# ==============================================================================
# Common & Pagination Schemas
# ==============================================================================
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=50, ge=1, le=500, description="Items per page")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_desc: bool = Field(default=False, description="Sort descending")


class StandardResponse(BaseModel):
    status: str = Field(default="SUCCESS")
    timestamp: datetime = Field(default_factory=datetime.now)
    message: Optional[str] = None
    data: Optional[Any] = None


# ==============================================================================
# Module 1: Executive Overview
# ==============================================================================
class ExecutiveKPIs(BaseModel):
    total_processed_records: int
    total_missions: int
    total_satellites_cataloged: int
    active_satellites_in_orbit: int
    total_historical_launches: int
    launch_success_rate_pct: float
    cumulative_mission_investment_billion_usd: float
    total_equipment_units_demanded: int = 161600
    predicted_future_demand_units: int = 34500
    identified_resource_shortages: int = 4
    hdfs_lakehouse_storage_mb: float = 52.8
    data_quality_score_pct: float = 99.4
    data_pipeline_health: str = "100% OPERATIONAL"


class InsightItem(BaseModel):
    title: str
    badge: str
    badgeColor: str
    description: str
    timestamp: str


# ==============================================================================
# Module 2: Data Management & Ingestion
# ==============================================================================
class DatasetCatalogItem(BaseModel):
    title: str
    gold_fact_table: str
    record_count: int
    size_kb: float
    md5_checksum: str
    quality_score: float
    provenance: str
    last_updated: str


class DataUploadResponse(BaseModel):
    status: str
    filename: str
    file_format: str
    file_size_bytes: int
    record_count: int
    columns_detected: List[str]
    hdfs_landing_path: str
    schema_validation: str
    upload_timestamp: datetime = Field(default_factory=datetime.now)


# ==============================================================================
# Module 3: Hadoop Ecosystem Control
# ==============================================================================
class ServiceHealthItem(BaseModel):
    service_name: str
    container_name: str
    role: str
    status: str
    port: int
    uptime: str
    memory_usage_mb: float
    cpu_percent: float


class ClusterHealthSummary(BaseModel):
    cluster_status: str
    total_services: int
    healthy_services: int
    services: List[ServiceHealthItem]
    hdfs_namenode_status: str
    yarn_resourcemanager_status: str
    hive_server_status: str
    spark_master_status: str


class MapReduceJobRequest(BaseModel):
    job_name: str = Field(..., description="MapReduce job identifier (e.g. 01_equipment_demand)")
    num_reducers: int = Field(default=2, ge=1, le=8)


class SparkJobRequest(BaseModel):
    job_name: str = Field(..., description="Spark job identifier (e.g. 01_data_access_verification)")
    driver_memory: str = Field(default="1024m")
    executor_memory: str = Field(default="1536m")


class PigJobRequest(BaseModel):
    script_name: str = Field(..., description="Pig script identifier (e.g. 01_missions_etl.pig)")
    exec_type: str = Field(default="mapreduce")


# ==============================================================================
# Module 5: Forecasting Studio
# ==============================================================================
class ForecastRequest(BaseModel):
    target: str = Field(default="equipment_units_demanded")
    algorithm: str = Field(default="RandomForest")
    horizon_months: int = Field(default=12, ge=1, le=36)
    scenario: str = Field(default="baseline")
    agency: Optional[str] = None


class EvaluationMetrics(BaseModel):
    rmse: float
    mae: float
    mape: float
    r2: float


class TimeSeriesPoint(BaseModel):
    date: str
    value: float
    lower_ci: Optional[float] = None
    upper_ci: Optional[float] = None


class ForecastResponse(BaseModel):
    target_name: str
    unit: str
    champion_algorithm: str
    explanation: str
    evaluation_metrics: EvaluationMetrics
    historical_data: List[TimeSeriesPoint]
    forecast_data: List[TimeSeriesPoint]
    feature_importance: List[Dict[str, Any]]


# ==============================================================================
# Module 6: Resource Planning & Optimization
# ==============================================================================
class ProcurementOptRequest(BaseModel):
    budget_ceiling_usd: float = Field(default=60000000.0, ge=1000000.0)
    criticality_penalty_weight: float = Field(default=2.5, ge=1.0, le=10.0)
    safety_stock_z: float = Field(default=1.645)


class AllocationItem(BaseModel):
    component_name: str
    forecast_demand: int
    allocated_units: int
    total_cost_usd: float
    fulfillment_pct: float
    shortage_units: int
    surplus_units: int
    procurement_priority: str
    supplier_lead_time_days: int


class ProcurementOptResponse(BaseModel):
    status: str
    total_budget_usd: float
    total_allocated_spend_usd: float
    overall_fulfillment_pct: float
    solver_runtime_ms: float
    allocations: List[AllocationItem]


class ScenarioRunRequest(BaseModel):
    scenario_name: str = Field(default="baseline")
    demand_multiplier: float = Field(default=1.0, ge=0.5, le=3.0)
    budget_limit_usd: Optional[float] = None
    lead_time_penalty: float = Field(default=1.0, ge=0.5, le=3.0)


# ==============================================================================
# Module 7: Big Data Benchmarking
# ==============================================================================
class BenchmarkRunRequest(BaseModel):
    workload: str = Field(default="WL1_EQUIPMENT_DEMAND")
    scale_tier: str = Field(default="small")
    dataset_name: str = Field(default="equipment_component_demand")


class EngineBenchmarkResult(BaseModel):
    engine: str
    execution_time_ms: float
    throughput_records_per_sec: int
    peak_memory_mb: float
    status: str
