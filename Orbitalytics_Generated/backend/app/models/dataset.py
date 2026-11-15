"""
Orbitalytics - In-Memory and Persistent Metadata Models
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
class DatasetRegistryEntry:
    dataset_name: str
    display_name: str
    category: str
    file_name: str
    row_count: int
    column_count: int
    is_synthetic: bool
    provenance: str
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ForecastExecutionLog:
    id: str
    target: str
    horizon_months: int
    model_name: str
    mae: float
    rmse: float
    accuracy_pct: float
    executed_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class PipelineJobLog:
    job_id: str
    stage_name: str
    status: str
    records_in: int
    records_out: int
    duration_sec: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

