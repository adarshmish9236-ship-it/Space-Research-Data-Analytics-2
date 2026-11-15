"""
Orbitalytics 2.0 - Big Data Schemas
Contracts for HDFS, Hive, MapReduce, PySpark, YARN, and Distributed Benchmark Laboratory.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class BenchmarkRequest(BaseModel):
    workload: str = Field(default="agency_mission_aggregation", description="Workload ID to benchmark")
    dataset_name: str = Field(default="space_missions", description="Dataset identifier")
    scale_multiplier: int = Field(default=1, ge=1, le=10, description="Multiplier for stress testing")

class EngineBenchmarkResult(BaseModel):
    engine: str  # Local Pandas, PySpark, Apache Hive, Hadoop MapReduce
    execution_time_ms: float
    input_records: int
    output_records: int
    throughput_rec_sec: float
    estimated_memory_mb: float
    status: str
    execution_mode: str  # IN_PROCESS_VECTORIZED, CLUSTER_STANDALONE, STREAMING_SUBPROCESS, SQL_METASTORE
    notes: str

class BenchmarkResponse(BaseModel):
    workload: str
    dataset_name: str
    total_input_records: int
    timestamp: str
    results: List[EngineBenchmarkResult]
    fastest_engine: str
    scalability_verdict: str

class YarnApplication(BaseModel):
    app_id: str
    name: str
    application_type: str  # SPARK, MAPREDUCE
    user: str
    queue: str
    state: str  # RUNNING, FINISHED, FAILED
    final_status: str
    allocated_memory_mb: int
    allocated_vcores: int
    elapsed_time_sec: float

class YarnClusterStatus(BaseModel):
    cluster_state: str
    resource_manager_url: str
    total_memory_mb: int
    available_memory_mb: int
    total_vcores: int
    available_vcores: int
    active_nodes: int
    running_apps_count: int
    completed_apps_count: int
    recent_applications: List[YarnApplication]

class HdfsZoneSummary(BaseModel):
    zone_name: str
    hdfs_path: str
    file_count: int
    total_size_mb: float
    block_count: int
    replication_factor: int

class HdfsOverviewResponse(BaseModel):
    namenode_url: str
    storage_mode: str  # LOCAL_EMULATED_LAKEHOUSE or DISTRIBUTED_HDFS
    total_capacity_gb: float
    used_capacity_gb: float
    free_capacity_gb: float
    block_size_mb: int
    default_replication: int
    zones: List[HdfsZoneSummary]
    total_blocks_simulated: int

