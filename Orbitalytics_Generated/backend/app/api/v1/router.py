"""
Orbitalytics 2.0 - API v1 Master Router
Consolidates all modular endpoints across Research Intelligence,
Big Data Engineering Workbench, ML Forecasting, Prescriptive Optimization, and Data Governance.
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from app.services.analytics_service import AnalyticsService
from app.services.demand_forecaster import demand_forecaster
from app.services.optimization_service import optimization_service
from app.services.scenario_service import scenario_service
from app.services.governance_service import governance_service
from app.services.data_validation_service import DataValidationService
from app.services.hdfs_service import hdfs_service
from app.services.hive_service import hive_service
from app.services.mapreduce_service import mapreduce_service
from app.services.spark_service import spark_service
from app.services.yarn_service import yarn_service
from app.services.benchmark_service import benchmark_service
from app.services.pipeline_service import pipeline_service
from app.services.reporting_service import ReportingService
from app.services.monitoring_service import MonitoringService
from app.services.ingestion_service import IngestionService
from app.db.metadata_db import metadata_repo

router = APIRouter()
analytics = AnalyticsService()
validator = DataValidationService()
reporting = ReportingService()
monitoring = MonitoringService()
ingestion = IngestionService()

# -------------------------------------------------------------
# 1. OVERVIEW & AUTOMATED INSIGHTS
# -------------------------------------------------------------
@router.get("/overview/kpis", tags=["Overview"])
def get_kpis():
    return analytics.get_overview_kpis()

@router.get("/overview/insights", tags=["Overview"])
def get_insights():
    return analytics.get_automated_insights()

# -------------------------------------------------------------
# 2. DOMAIN RESEARCH INTELLIGENCE
# -------------------------------------------------------------
@router.get("/missions/analytics", tags=["Domain Intelligence"])
def get_mission_analytics(agency: Optional[str] = None, country: Optional[str] = None):
    return analytics.get_mission_analytics(agency=agency, country=country)

@router.get("/satellites/analytics", tags=["Domain Intelligence"])
def get_satellite_analytics():
    return analytics.get_satellite_analytics()

@router.get("/launches/analytics", tags=["Domain Intelligence"])
def get_launch_analytics():
    return analytics.get_launch_analytics()

@router.get("/equipment/analytics", tags=["Domain Intelligence"])
def get_equipment_analytics():
    return analytics.get_equipment_demand_analytics()

@router.get("/resources/analytics", tags=["Domain Intelligence"])
def get_resource_analytics():
    return analytics.get_resource_analytics()

@router.get("/investments/analytics", tags=["Domain Intelligence"])
def get_investment_analytics():
    return analytics.get_investment_analytics()

@router.get("/infrastructure/analytics", tags=["Domain Intelligence"])
def get_infrastructure_analytics():
    return analytics.get_infrastructure_analytics()

@router.get("/geographic/analytics", tags=["Domain Intelligence"])
def get_geographic_analytics():
    return analytics.get_geographic_distribution()

# -------------------------------------------------------------
# 3. DATA GOVERNANCE, CATALOG & LINEAGE
# -------------------------------------------------------------
@router.get("/governance/catalog", tags=["Data Governance"])
def get_data_catalog():
    return governance_service.get_data_catalog()

@router.get("/governance/lineage", tags=["Data Governance"])
def get_data_lineage():
    return governance_service.get_data_lineage()

@router.get("/governance/quality", tags=["Data Governance"])
def get_all_dataset_quality():
    return validator.validate_all_datasets()

@router.get("/datasets/{dataset_name}/quality", tags=["Data Governance"])
def get_single_dataset_quality(dataset_name: str):
    return validator.validate_dataset(dataset_name)

# -------------------------------------------------------------
# 4. BIG DATA: HDFS, HIVE, MAPREDUCE, SPARK, YARN, BENCHMARKS
# -------------------------------------------------------------
@router.get("/hdfs/overview", tags=["Hadoop Ecosystem"])
def get_hdfs_overview():
    return hdfs_service.get_cluster_overview()

@router.get("/hdfs/files", tags=["Hadoop Ecosystem"])
def list_hdfs_files(zone: str = Query("curated")):
    return hdfs_service.list_zone_files(zone)

@router.get("/hive/tables", tags=["Apache Hive"])
def get_hive_tables():
    return hive_service.get_metastore_tables()

@router.get("/hive/query", tags=["Apache Hive"])
def execute_hive_query(query_id: str = Query("agency_missions")):
    return hive_service.execute_analytical_query(query_id)

@router.post("/hive/query", tags=["Apache Hive"])
def execute_hive_query_post(body: Dict[str, Any] = Body(...)):
    query_id = body.get("query_id", "agency_missions")
    custom_sql = body.get("custom_sql")
    return hive_service.execute_analytical_query(query_id, custom_sql)

@router.get("/mapreduce/jobs", tags=["Hadoop MapReduce"])
def list_mapreduce_jobs():
    return mapreduce_service.list_jobs()

@router.post("/mapreduce/run", tags=["Hadoop MapReduce"])
def run_mapreduce_job(body: Dict[str, Any] = Body(...)):
    job_name = body.get("job_name", "missions_aggregation")
    return mapreduce_service.run_job(job_name)

@router.get("/spark/jobs", tags=["Apache Spark"])
def list_spark_jobs():
    return spark_service.list_spark_jobs()

@router.post("/spark/run", tags=["Apache Spark"])
def run_spark_job(body: Dict[str, Any] = Body(...)):
    job_name = body.get("job_name", "spark_large_scale_aggregation")
    return spark_service.run_spark_job(job_name)

@router.get("/yarn/status", tags=["YARN Cluster"])
def get_yarn_status():
    return yarn_service.get_cluster_status()

@router.post("/benchmarks/run", tags=["Benchmark Lab"])
def run_distributed_benchmark(body: Dict[str, Any] = Body(...)):
    workload = body.get("workload", "agency_mission_aggregation")
    dataset_name = body.get("dataset_name", "space_missions")
    return benchmark_service.run_benchmark(workload=workload, dataset_name=dataset_name)

@router.get("/benchmarks/history", tags=["Benchmark Lab"])
def get_benchmark_history():
    return metadata_repo.get_benchmark_runs(limit=30)

# -------------------------------------------------------------
# 5. PREDICTIVE DEMAND FORECASTING STUDIO
# -------------------------------------------------------------
@router.get("/forecasting/targets", tags=["Demand Forecasting"])
def get_forecasting_targets():
    return demand_forecaster.get_supported_targets()

@router.post("/forecasting/predict", tags=["Demand Forecasting"])
def generate_forecast(body: Dict[str, Any] = Body(...)):
    target = body.get("target") or body.get("component_name") or "equipment"
    if "Solar" in target:
        target = "equipment"
    algo = body.get("algorithm") or body.get("model_type") or "champion"
    horizon = int(body.get("horizon_months", 12))
    scenario = body.get("scenario", "baseline")
    return demand_forecaster.train_and_forecast(target=target, algorithm=algo, horizon_months=horizon, scenario=scenario)

@router.get("/forecasting/registry", tags=["Demand Forecasting"])
def get_model_registry(target: Optional[str] = None):
    return metadata_repo.get_registered_models(target=target)

# -------------------------------------------------------------
# 6. DEMAND-TO-CAPACITY OPTIMIZATION STUDIO
# -------------------------------------------------------------
@router.post("/optimization/demand-gap", tags=["Optimization Studio"])
def compute_demand_gap(body: Dict[str, Any] = Body(...)):
    cat = body.get("category", "Equipment")
    horizon = int(body.get("horizon_months", 12))
    cap_mult = float(body.get("capacity_multiplier", 0.88))
    return optimization_service.analyze_demand_gap(category=cat, horizon_months=horizon, capacity_multiplier=cap_mult)

@router.post("/optimization/inventory", tags=["Optimization Studio"])
def compute_inventory_plan(body: Dict[str, Any] = Body(...)):
    item = body.get("item_name", "Solar Panel Array High Efficiency")
    lead_time = int(body.get("lead_time_days", 90))
    service_level = float(body.get("service_level", 0.95))
    return optimization_service.plan_inventory(item_name=item, lead_time_days=lead_time, service_level=service_level)

@router.post("/optimization/procurement", tags=["Optimization Studio"])
def run_procurement_optimization(body: Dict[str, Any] = Body(...)):
    budget = float(body.get("budget_ceiling_usd", 60000000.0))
    penalty = float(body.get("criticality_penalty_weight", 2.5))
    return optimization_service.optimize_procurement(budget_ceiling_usd=budget, criticality_penalty_weight=penalty)

@router.post("/optimization/budget", tags=["Optimization Studio"])
def run_budget_allocation(body: Dict[str, Any] = Body(...)):
    budget = float(body.get("total_budget_usd", 25000000000.0))
    focus = body.get("focus_domain", "Balanced")
    return optimization_service.allocate_budget(total_budget_usd=budget, focus_domain=focus)

@router.get("/optimization/runs", tags=["Optimization Studio"])
def get_optimization_history():
    return metadata_repo.get_optimization_runs(limit=20)

# -------------------------------------------------------------
# 7. SCENARIO SIMULATION & DIGITAL TWIN
# -------------------------------------------------------------
@router.post("/scenarios/run", tags=["Scenario Studio"])
def run_scenario_comparison(body: Dict[str, Any] = Body(...)):
    return scenario_service.run_scenario_comparison(
        budget_growth_pct=float(body.get("budget_growth_pct", 0.0)),
        launch_cadence_change_pct=float(body.get("launch_cadence_change_pct", 0.0)),
        satellite_deployment_change_pct=float(body.get("satellite_deployment_change_pct", 0.0)),
        equipment_price_inflation_pct=float(body.get("equipment_price_inflation_pct", 3.0)),
        supplier_capacity_change_pct=float(body.get("supplier_capacity_change_pct", 0.0))
    )

@router.post("/scenarios/monte-carlo", tags=["Scenario Studio"])
def run_monte_carlo(body: Dict[str, Any] = Body(...)):
    target = body.get("target", "equipment_demand")
    iterations = int(body.get("iterations", 500))
    volatility = float(body.get("volatility_pct", 15.0))
    seed = int(body.get("seed", 42))
    return scenario_service.run_monte_carlo(target=target, iterations=iterations, volatility_pct=volatility, seed=seed)

@router.get("/scenarios/sensitivity", tags=["Scenario Studio"])
def get_sensitivity_analysis():
    return scenario_service.run_sensitivity_analysis()

# -------------------------------------------------------------
# 8. PIPELINE ORCHESTRATION & INGESTION
# -------------------------------------------------------------
@router.post("/pipeline/run", tags=["Pipeline Orchestrator"])
def run_pipeline(body: Optional[Dict[str, Any]] = None):
    profile = body.get("profile", "medium") if body else "medium"
    return pipeline_service.trigger_full_pipeline(profile=profile)

@router.get("/pipeline/history", tags=["Pipeline Orchestrator"])
def get_pipeline_history():
    return pipeline_service.get_pipeline_history()

@router.post("/ingestion/run", tags=["Ingestion"])
def run_ingestion():
    return ingestion.run_full_ingestion_and_curation()

# -------------------------------------------------------------
# 9. REPORTING & EXPORTS
# -------------------------------------------------------------
@router.get("/reports/executive/pdf", tags=["Reports"])
def export_executive_pdf():
    return reporting.generate_executive_pdf_report()

@router.get("/reports/lakehouse/excel", tags=["Reports"])
def export_lakehouse_excel():
    return reporting.generate_lakehouse_excel_report()

@router.get("/reports/raw/csv", tags=["Reports"])
def export_raw_csv(dataset_name: str = Query("space_missions")):
    return reporting.export_dataset_csv(dataset_name)

# -------------------------------------------------------------
# 10. SYSTEM OBSERVABILITY & HEALTH
# -------------------------------------------------------------
@router.get("/monitoring/health", tags=["Monitoring"])
def get_health():
    return monitoring.get_system_health()

