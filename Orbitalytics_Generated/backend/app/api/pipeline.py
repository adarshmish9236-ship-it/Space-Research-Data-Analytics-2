"""
Orbitalytics - Pipeline API Router
"""
from fastapi import APIRouter, HTTPException, Query
from app.services.pipeline_service import PipelineService
from app.services.monitoring_service import MonitoringService

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])
pipeline_service = PipelineService()
monitoring_service = MonitoringService()

@router.post("/run")
def trigger_pipeline(profile: str = Query("medium", description="Generation profile: small, medium, large")):
    try:
        return pipeline_service.trigger_full_pipeline(profile=profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def get_pipeline_status():
    try:
        return monitoring_service.get_pipeline_stages_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_pipeline_history():
    return pipeline_service.get_execution_history()

