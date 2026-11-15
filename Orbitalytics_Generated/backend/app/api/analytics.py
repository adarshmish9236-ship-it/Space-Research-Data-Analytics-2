"""
Orbitalytics - Advanced Analytics API Router
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
service = AnalyticsService()

@router.get("/missions")
def get_missions(agency: Optional[str] = None, country: Optional[str] = None):
    try:
        return service.get_mission_analytics(agency, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/satellites")
def get_satellites():
    try:
        return service.get_satellite_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/launches")
def get_launches():
    try:
        return service.get_launch_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/equipment-demand")
def get_equipment_demand():
    try:
        return service.get_equipment_demand_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resources")
def get_resources():
    try:
        return service.get_resource_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/investments")
def get_investments():
    try:
        return service.get_investment_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/infrastructure")
def get_infrastructure():
    try:
        return service.get_infrastructure_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geographic-distribution")
def get_geographic_distribution():
    try:
        return service.get_geographic_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agency-comparison")
def get_agency_comparison():
    try:
        return service.get_mission_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights")
def get_insights():
    try:
        return service.get_automated_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

