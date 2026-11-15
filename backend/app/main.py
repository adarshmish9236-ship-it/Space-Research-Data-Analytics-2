"""
Space Research Big Data Analytics Platform - FastAPI Main Server
Provides production REST API endpoints for:
- System Overview & KPIs
- Data Ingestion & Pipeline Orchestration
- HDFS Cluster Storage Monitoring
- Apache Hive Catalog & Analytical Queries
- MapReduce Jobs Execution
- PySpark Distributed ETL Jobs
- Demand Forecasting Engine (Random Forest / Gradient Boosting with multi-horizon projections)
- Dynamic Insight Generation
- CSV and PDF Report Generation
"""

from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List, Dict, Any
import io
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

from app.services.hdfs_service import HDFSService
from app.services.hive_service import HiveService
from app.services.mapreduce_service import MapReduceService
from app.services.analytics_service import AnalyticsService
from app.services.demand_forecaster import DemandForecaster
from app.services.reporting_service import ReportingService
from app.services.spark_service import SparkService
from app.services.optimisation_service import OptimisationService
from app.services.benchmarking_service import BenchmarkingService
from app.api.v1 import api_v1_router

app = FastAPI(
    title="Space Research Data Analytics Platform",
    description="A Hadoop Ecosystem Approach to Demand Forecasting for Space Resources and Activities",
    version="2.0.0"
)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file mounts for high-resolution textures and frontend assets
assets_path = FRONTEND_DIR / "assets"
if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

# Mount versioned API routers for Module 1-8
app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(api_v1_router, prefix="/api")

# Instantiate services
hdfs_service = HDFSService()
hive_service = HiveService()
mr_service = MapReduceService()
analytics_service = AnalyticsService()
forecaster = DemandForecaster()
reporting_service = ReportingService()
spark_service = SparkService()
optimisation_service = OptimisationService()
benchmarking_service = BenchmarkingService()

@app.get("/")
def serve_index():
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return {"message": "Frontend index.html not found"}

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "Space Research Big Data Platform API",
        "hadoop_ecosystem": "ACTIVE"
    }

# 1. Overview and Analytics Endpoints
@app.get("/api/overview/kpis")
def get_kpis():
    try:
        return analytics_service.get_overview_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/agency-missions")
def get_agency_missions():
    try:
        return analytics_service.get_mission_agency_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/launch-trends")
def get_launch_trends():
    try:
        return analytics_service.get_yearly_launch_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/resource-consumption")
def get_resource_consumption():
    try:
        return analytics_service.get_resource_consumption_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/geographic-distribution")
def get_geographic_distribution():
    try:
        return analytics_service.get_geographic_distribution()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pipeline/status")
def get_pipeline_status():
    try:
        return analytics_service.get_big_data_pipeline_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/insights")
def get_insights():
    try:
        return analytics_service.get_automated_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. HDFS Endpoints
@app.get("/api/hdfs/overview")
def get_hdfs_overview():
    try:
        return hdfs_service.get_storage_overview()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hdfs/zone-files")
def get_hdfs_zone_files(zone: str = Query("curated", description="Zone: raw, processed, curated, analytics, forecasting, reports")):
    try:
        return hdfs_service.list_files_in_zone(zone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. Apache Hive Endpoints
@app.get("/api/hive/tables")
def get_hive_tables():
    try:
        return hive_service.get_tables_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hive/dimensions")
def get_hive_dimensions():
    try:
        return hive_service.get_dimensions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hive/facts")
def get_hive_facts():
    try:
        return hive_service.get_facts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hive/views")
def get_hive_views():
    try:
        return hive_service.get_views()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hive/manifest")
def get_hive_manifest():
    try:
        return hive_service.get_execution_manifest()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hive/query")
def run_hive_query(query_id: str = Query("01_total_demand_by_component", description="Query ID or alias (01 to 16, agency_missions, equipment_demand_trend, etc.)")):
    try:
        return hive_service.execute_analytical_query(query_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3b. Apache Spark & PySpark Analytics Endpoints
@app.get("/api/spark/manifest")
def get_spark_manifest():
    try:
        return spark_service.get_manifest()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/spark/gold/catalog")
def get_spark_gold_catalog():
    try:
        return spark_service.get_gold_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/spark/gold/{dataset_name}")
def get_spark_gold_dataset(dataset_name: str):
    try:
        return spark_service.get_gold_dataset_info(dataset_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/spark/features")
def get_spark_features():
    try:
        return spark_service.get_feature_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. MapReduce Endpoints
@app.post("/api/mapreduce/run")
def run_mapreduce(job_name: str = Query("missions_aggregation", description="Options: missions_aggregation, demand_aggregation")):
    try:
        return mr_service.run_mapreduce_job(job_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 5. Demand Forecasting Endpoints (Phase 8 Advanced Architecture)
@app.get("/api/forecasting/models")
def get_forecasting_models():
    """Returns catalog of all 13 supported forecasting models across 4 families."""
    try:
        return forecaster.get_available_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecasting/series")
def get_forecasting_series():
    """Returns list of all 17 modeled space time-series with champions and coverage."""
    try:
        return forecaster.get_series_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecasting/comparison")
def get_forecasting_comparison(
    domain: Optional[str] = Query(None, description="Filter by domain: equipment_demand or resource_consumption"),
    series: Optional[str] = Query(None, description="Filter by series name substring")
):
    """Returns out-of-sample backtested metrics (MAE, RMSE, WAPE %, MAPE %, Bias %, R²) for all models."""
    try:
        return forecaster.get_comparison_matrix(domain=domain, series_name=series)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecasting/projections")
def get_forecasting_projections(
    domain: Optional[str] = Query(None, description="Filter by domain: equipment_demand or resource_consumption"),
    series_id: Optional[str] = Query(None, description="Filter by specific series ID (e.g. eq_aggregate_all_components)")
):
    """Returns 4-quarter forward projections with 80% and 95% confidence intervals and feature importances."""
    try:
        return forecaster.get_projections(domain=domain, series_id=series_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecasting/registry")
def get_model_registry():
    """Returns the production Model Registry with champion models, hyperparams, and drift specs."""
    try:
        return forecaster.get_model_registry()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecasting/spark-mllib")
def get_spark_mllib_metrics():
    """Returns distributed PySpark MLlib cluster training metrics on HDFS Gold datasets."""
    try:
        return forecaster.get_spark_mllib_results()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/forecasting/predict")
def run_demand_forecast(
    metric_type: str = Query("equipment", description="Options: equipment, launches, satellites, expenditures"),
    horizon: int = Query(12, description="Horizon in months: 3, 6, 12, 36"),
    model: str = Query("RandomForest", description="Options: RandomForest, GradientBoosting")
):
    try:
        return forecaster.run_forecast(metric_type=metric_type, horizon_months=horizon, model_name=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Resource Optimisation & Shortage Detection Endpoints (Phase 9)
@app.get("/api/optimisation/scenarios")
def get_optimisation_scenarios(domain: Optional[str] = Query(None, description="equipment_demand or resource_consumption")):
    """Returns side-by-side comparison matrix across 5 operational scenarios."""
    try:
        return optimisation_service.get_scenario_comparison(domain=domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimisation/shortages")
def get_optimisation_shortages(
    domain: Optional[str] = Query(None, description="equipment_demand or resource_consumption"),
    item_name: Optional[str] = Query(None, description="Filter by component/resource name")
):
    """Returns quarterly shortage, surplus, safety stock, and fill rate reports."""
    try:
        return optimisation_service.get_shortage_report(domain=domain, item_name=item_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimisation/procurement")
def get_optimisation_procurement(
    domain: Optional[str] = Query(None, description="equipment_demand or resource_consumption"),
    item_name: Optional[str] = Query(None, description="Filter by component/resource name")
):
    """Returns suggested procurement schedules, lead-time offsets, and capital expenditures."""
    try:
        return optimisation_service.get_procurement_recommendations(domain=domain, item_name=item_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimisation/allocation")
def get_optimisation_allocation(
    domain: Optional[str] = Query(None, description="equipment_demand or resource_consumption"),
    tier: Optional[str] = Query(None, description="Filter by priority tier")
):
    """Returns priority-weighted mission resource allocation breakdown."""
    try:
        return optimisation_service.get_priority_allocations(domain=domain, tier=tier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/optimisation/summary")
def get_optimisation_summary(domain: str = Query("equipment_demand", description="equipment_demand or resource_consumption")):
    """Returns aggregate fleet procurement metrics, baseline performance, and documented assumptions."""
    try:
        return optimisation_service.get_fleet_summary(domain=domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimisation/solve")
def solve_custom_scenario_endpoint(
    domain: str = Query("equipment_demand", description="equipment_demand or resource_consumption"),
    budget_multiplier: float = Query(1.0, description="Multiplier on quarterly budget (e.g. 0.65 for austerity, 1.2 for surplus)"),
    capacity_multiplier: float = Query(1.0, description="Multiplier on internal cleanroom capacity (e.g. 1.35)"),
    demand_multiplier: float = Query(1.0, description="Multiplier on forecast demand (e.g. 1.15 for surge)")
):
    """Dynamically solves custom scenario using the HiGHS MILP solver."""
    try:
        return optimisation_service.solve_custom_scenario(
            domain=domain,
            budget_multiplier=budget_multiplier,
            capacity_multiplier=capacity_multiplier,
            demand_multiplier=demand_multiplier
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. Benchmarking Endpoints (Phase 10)
@app.get("/api/benchmarks/summary")
def get_benchmarks_summary():
    try:
        return benchmarking_service.get_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/benchmarks/matrix")
def get_benchmarks_matrix():
    try:
        return benchmarking_service.get_results_matrix()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/benchmarks/scaling")
def get_benchmarks_scaling():
    try:
        return benchmarking_service.get_scaling_analysis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/benchmarks/manifest")
def get_benchmarks_manifest():
    try:
        return benchmarking_service.get_manifest()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. Report Generation Endpoints
@app.get("/api/reports/download/pdf")
def download_pdf_report(
    metric_type: str = "equipment",
    horizon: int = 12,
    model: str = "RandomForest"
):
    try:
        fc = forecaster.run_forecast(metric_type=metric_type, horizon_months=horizon, model_name=model)
        kpis = analytics_service.get_overview_kpis()
        pdf_bytes = reporting_service.export_pdf(fc, kpis)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Space_Research_Forecast_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/download/csv")
def download_csv_report(
    metric_type: str = "equipment",
    horizon: int = 12,
    model: str = "RandomForest"
):
    try:
        fc = forecaster.run_forecast(metric_type=metric_type, horizon_months=horizon, model_name=model)
        csv_str = reporting_service.export_csv("forecast_summary", fc)
        return Response(
            content=csv_str,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=Space_Research_Forecast.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static frontend directory for any additional assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

