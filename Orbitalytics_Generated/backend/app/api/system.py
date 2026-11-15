"""
Orbitalytics - System API Router
"""
from fastapi import APIRouter, HTTPException
from app.services.monitoring_service import MonitoringService
from app.core.config import settings

router = APIRouter(prefix="/system", tags=["System"])
service = MonitoringService()

@router.get("/status")
def get_status():
    return service.get_system_status()

@router.get("/configuration")
def get_configuration():
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "api_v1_str": settings.API_V1_STR,
        "hadoop_namenode": settings.HADOOP_NAMENODE_URL,
        "hive_database": settings.HIVE_DATABASE,
        "spark_master": settings.SPARK_MASTER,
        "block_size_mb": settings.HDFS_BLOCK_SIZE_MB,
        "replication_factor": settings.HDFS_REPLICATION_FACTOR
    }

