"""
Orbitalytics - Datasets Schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DatasetMeta(BaseModel):
    name: str
    display_name: str
    description: str
    file_name: str
    record_count: int
    size_formatted: str
    columns_count: int
    data_source: str
    is_synthetic: bool
    last_updated: str
    curated_format: str

class DatasetQualityReport(BaseModel):
    dataset_name: str
    total_records: int
    total_columns: int
    null_counts: Dict[str, int]
    duplicate_records: int
    completeness_score_pct: float
    data_provenance: str
    quality_status: str

