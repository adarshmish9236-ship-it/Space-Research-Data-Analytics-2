"""
Orbitalytics - Reports & Export API Router
"""
from fastapi import APIRouter, HTTPException, Query, Response
from app.services.reporting_service import ReportingService
from app.services.demand_forecaster import DemandForecaster
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/reports", tags=["Reports"])
reporting_service = ReportingService()
forecaster = DemandForecaster()
analytics_service = AnalyticsService()

@router.get("/download/pdf")
def download_pdf(
    target: str = Query("equipment"),
    horizon_months: int = Query(12),
    model: str = Query("RandomForest")
):
    try:
        fc = forecaster.predict(target=target, horizon_months=horizon_months, model_name=model)
        kpis = analytics_service.get_overview_kpis()
        pdf_bytes = reporting_service.generate_pdf_whitepaper(fc, kpis)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=Orbitalytics_Research_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/excel")
def download_excel(
    target: str = Query("equipment"),
    horizon_months: int = Query(12),
    model: str = Query("RandomForest")
):
    try:
        fc = forecaster.predict(target=target, horizon_months=horizon_months, model_name=model)
        excel_bytes = reporting_service.generate_excel_workbook(fc)
        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=Orbitalytics_Workbook.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/csv")
def download_csv(
    target: str = Query("equipment"),
    horizon_months: int = Query(12),
    model: str = Query("RandomForest")
):
    try:
        fc = forecaster.predict(target=target, horizon_months=horizon_months, model_name=model)
        csv_str = reporting_service.export_csv(fc)
        return Response(
            content=csv_str,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=Orbitalytics_Forecast.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

