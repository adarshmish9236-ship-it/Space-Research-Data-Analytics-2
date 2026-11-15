"""
Orbitalytics - Reports & System Schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ReportGenerationRequest(BaseModel):
    report_type: str = "executive_pdf" # executive_pdf, forecast_csv, excel_workbook
    target: Optional[str] = "equipment"
    horizon_months: Optional[int] = 12
    model: Optional[str] = "RandomForest"

class SystemStatusResponse(BaseModel):
    system_name: str
    version: str
    status: str
    python_version: str
    environment_mode: str # "Cluster Connected" or "Local Demonstration Engine"
    hdfs_connectivity: str
    hive_connectivity: str
    yarn_status: str
    spark_engine: str
    datasets_ready: bool
    total_lakehouse_files: int
    uptime_seconds: float

