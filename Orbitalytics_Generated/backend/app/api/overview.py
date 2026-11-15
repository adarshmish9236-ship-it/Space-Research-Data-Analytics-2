"""
Orbitalytics - Overview API Router
"""
from fastapi import APIRouter, HTTPException
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/overview", tags=["Overview"])
analytics_service = AnalyticsService()

@router.get("/kpis")
def get_kpis():
    try:
        return analytics_service.get_overview_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
def get_summary():
    try:
        kpis = analytics_service.get_overview_kpis()
        insights = analytics_service.get_automated_insights()
        return {
            "kpis": kpis,
            "automated_insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends")
def get_overview_trends():
    try:
        launches = analytics_service.get_launch_analytics()
        missions = analytics_service.get_mission_analytics()
        return {
            "launch_cadence": launches["yearly_trends"],
            "agency_allocations": missions["agencies"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

