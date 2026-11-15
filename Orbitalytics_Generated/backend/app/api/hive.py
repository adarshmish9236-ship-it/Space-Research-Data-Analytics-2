"""
Orbitalytics - Apache Hive API Router
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional
from app.services.hive_service import HiveService
from app.schemas.system import HiveQueryRequest

router = APIRouter(prefix="/hive", tags=["Apache Hive"])
service = HiveService()

@router.get("/tables")
def get_hive_tables():
    try:
        return service.get_metastore_tables()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
def execute_query_post(req: HiveQueryRequest):
    try:
        return service.execute_analytical_query(req.query_id, req.custom_sql)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/query")
def execute_query_get(query_id: str = Query("agency_missions", description="Options: agency_missions, equipment_demand_trend, orbit_distribution, launch_vehicles, future_investments")):
    try:
        return service.execute_analytical_query(query_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

