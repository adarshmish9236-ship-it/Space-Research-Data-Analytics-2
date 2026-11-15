"""
Orbitalytics 2.0 - Data Governance, Lineage, and Quality Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class LineageNode(BaseModel):
    id: str
    label: str
    layer: str  # SOURCE, BRONZE, SILVER, GOLD, ANALYTICS, CONSUMPTION
    description: str
    record_count: Optional[int] = None
    engine: str  # PYTHON_INGEST, PYSPARK_CLEANER, HIVE_DDL, MAPREDUCE_AGG, ML_STUDIO

class LineageEdge(BaseModel):
    source: str
    target: str
    operation: str
    transformation_type: str

class DataLineageResponse(BaseModel):
    nodes: List[LineageNode]
    edges: List[LineageEdge]
    pipeline_version: str
    last_curated_at: str

class CatalogDatasetItem(BaseModel):
    dataset_id: str
    title: str
    zone: str  # Bronze, Silver, Gold
    category: str
    format: str
    record_count: int
    column_count: int
    size_kb: float
    md5_checksum: str
    quality_score: float
    provenance: str
    last_updated: str
    schema_fields: List[Dict[str, str]]

class DataCatalogResponse(BaseModel):
    total_datasets: int
    total_records: int
    average_quality_score: float
    catalog: List[CatalogDatasetItem]

class AnomalyDetail(BaseModel):
    column: str
    method: str  # Z_SCORE, IQR, RANGE_CHECK
    outlier_count: int
    outlier_percentage: float
    threshold_applied: str
    sample_values: List[Any]
    recommendation: str

class DatasetQualityAudit(BaseModel):
    dataset_id: str
    overall_quality_score: float  # 0 to 100
    total_records: int
    passed_records: int
    quarantined_records: int
    completeness_score: float
    validity_score: float
    uniqueness_score: float
    consistency_score: float
    detected_anomalies: List[AnomalyDetail]
    audit_verdict: str  # PRODUCTION_READY, CAUTION_REVIEW, REJECTED

