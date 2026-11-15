"""
Orbitalytics - MapReduce API Router
"""
from fastapi import APIRouter, HTTPException, Query, Body
from app.services.mapreduce_service import MapReduceService
from app.schemas.system import MapReduceRunRequest

router = APIRouter(prefix="/mapreduce", tags=["Hadoop MapReduce"])
service = MapReduceService()

@router.post("/run")
def run_mapreduce_job(job_name: str = Query("missions_aggregation", description="Options: missions_aggregation, demand_aggregation, launches_aggregation")):
    try:
        return service.run_job(job_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

