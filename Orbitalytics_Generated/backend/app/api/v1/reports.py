"""
ORBITALYTICS Phase 11 — API v1: Module 8 Report Generation & Download Endpoints
Provides automated export endpoints for:
- Executive Summary Whitepapers (PDF)
- Lakehouse Catalog Summaries (Excel / CSV)
- Raw and Curated Dataset Extracts (CSV)
- Demand Forecasting Schedules (PDF & CSV)
"""

from fastapi import APIRouter, HTTPException, Query, Response
from pathlib import Path
import io
import pandas as pd

from app.services.reporting_service import ReportingService
from app.services.analytics_service import AnalyticsService
from app.services.demand_forecaster import DemandForecaster

router = APIRouter(tags=["Module 8: Reports"])

reporting_service = ReportingService()
analytics_service = AnalyticsService()
forecaster = DemandForecaster()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CURATED_DIR = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "curated"
RAW_DIR = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "raw"


@router.get("/reports/executive/pdf")
def download_executive_pdf():
    """Generates and downloads the comprehensive executive PDF whitepaper."""
    try:
        kpis = analytics_service.get_overview_kpis()
        fc = forecaster.run_forecast(metric_type="equipment", horizon_months=12, model_name="RandomForest")
        pdf_bytes = reporting_service.export_pdf(fc, kpis)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=Orbitalytics_Executive_Intelligence_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF report generation failed: {str(e)}")


@router.get("/reports/lakehouse/excel")
def download_lakehouse_excel():
    """Generates and downloads the Lakehouse inventory summary as a CSV / spreadsheet."""
    try:
        from app.api.v1.data_management import DATASET_CATALOG
        df = pd.DataFrame(DATASET_CATALOG)
        output = io.StringIO()
        df.to_csv(output, index=False)
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=Orbitalytics_Lakehouse_Catalog_Inventory.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lakehouse catalog export failed: {str(e)}")


@router.get("/reports/raw/csv")
def download_raw_dataset_csv(dataset_name: str = Query("space_missions", description="Dataset identifier")):
    """Extracts and streams any space research dataset as standard CSV."""
    try:
        # Check raw CSV first
        raw_file = RAW_DIR / f"{dataset_name}.csv"
        if raw_file.exists():
            return Response(
                content=raw_file.read_text(encoding="utf-8"),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={dataset_name}_export.csv"}
            )

        # Check curated Parquet
        curated_path = CURATED_DIR / dataset_name
        if not curated_path.exists():
            curated_path = CURATED_DIR / f"{dataset_name}.parquet"

        if curated_path.exists():
            df = pd.read_parquet(curated_path)
            output = io.StringIO()
            df.head(2000).to_csv(output, index=False)
            return Response(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={dataset_name}_export.csv"}
            )

        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found in Lakehouse.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dataset export error: {str(e)}")


@router.get("/reports/download/pdf")
def download_pdf_report(
    metric_type: str = Query("equipment"),
    horizon: int = Query(12),
    model: str = Query("RandomForest")
):
    """Downloads forecast PDF report for specific metric, horizon, and algorithm."""
    try:
        fc = forecaster.run_forecast(metric_type=metric_type, horizon_months=horizon, model_name=model)
        kpis = analytics_service.get_overview_kpis()
        pdf_bytes = reporting_service.export_pdf(fc, kpis)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Space_Research_Forecast_{metric_type}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/download/csv")
def download_csv_report(
    metric_type: str = Query("equipment"),
    horizon: int = Query(12),
    model: str = Query("RandomForest")
):
    """Downloads forecast CSV report for specific metric, horizon, and algorithm."""
    try:
        fc = forecaster.run_forecast(metric_type=metric_type, horizon_months=horizon, model_name=model)
        csv_str = reporting_service.export_csv("forecast_summary", fc)
        return Response(
            content=csv_str,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=Space_Research_Forecast_{metric_type}.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
