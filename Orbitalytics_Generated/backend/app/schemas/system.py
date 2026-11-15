"""
Orbitalytics - System & Hadoop Monitoring Schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class HDFSOverview(BaseModel):
    cluster_status: str
    active_namenodes: int
    active_datanodes: int
    block_size_mb: int
    replication_factor: int
    total_files: int
    total_size_mb: float
    simulated_blocks: int
    zones: List[Dict[str, Any]]

class HiveQueryRequest(BaseModel):
    query_id: str
    custom_sql: Optional[str] = None

class HiveQueryResponse(BaseModel):
    query_id: str
    sql: str
    execution_time_ms: float
    rows_returned: int
    columns: List[str]
    records: List[Dict[str, Any]]

class MapReduceRunRequest(BaseModel):
    job_name: str # missions_aggregation, demand_aggregation, launches_aggregation

class MapReduceRunResponse(BaseModel):
    job_name: str
    yarn_application_id: str
    status: str
    execution_duration_sec: float
    map_input_records: int
    reduce_output_records: int
    output_path: str
    streaming_command: str
    headers: List[str]
    records: List[Dict[str, Any]]

class PipelineStageInfo(BaseModel):
    id: str
    name: str
    component: str
    status: str
    throughput: str
    latency_ms: int
    error_rate: str
    detail: str

class PipelineStatusResponse(BaseModel):
    cluster_health: str
    pipeline_state: str
    stages: List[PipelineStageInfo]
    cluster_nodes: List[Dict[str, Any]]

