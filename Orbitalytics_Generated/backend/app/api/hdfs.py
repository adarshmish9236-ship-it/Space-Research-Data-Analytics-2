"""
Orbitalytics - HDFS API Router
"""
from fastapi import APIRouter, HTTPException, Query
from app.services.hdfs_service import HDFSService

router = APIRouter(prefix="/hdfs", tags=["Hadoop HDFS"])
service = HDFSService()

@router.get("/overview")
def get_hdfs_overview():
    try:
        return service.get_cluster_overview()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
def list_hdfs_files(zone: str = Query("curated", description="Zone: raw, processed, curated, analytics, forecasts, reports")):
    try:
        return service.list_zone_files(zone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

