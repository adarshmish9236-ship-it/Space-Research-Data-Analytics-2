"""
ORBITALYTICS Phase 11 — Comprehensive Dashboard & System Integration Test Suite
Tests all 8 core platform modules and 30+ versioned REST endpoints:
- Module 1: Executive Overview
- Module 2: Data Management & Ingestion
- Module 3: Hadoop Ecosystem Control
- Module 4: Space Research Analytics
- Module 5: Forecasting Studio
- Module 6: Resource Planning & Optimization
- Module 7: Big Data Performance Benchmarking
- Module 8: Report Generation & Exports
"""

import pytest
import io
import sys
from pathlib import Path

# Add backend directory to sys.path so 'app' imports resolve cleanly
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ==============================================================================
# 1. Module 1: Executive Overview Tests
# ==============================================================================
def test_01_executive_kpis():
    """Verify executive KPIs derived from actual backend datasets."""
    response = client.get("/api/v1/overview/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_processed_records" in data
    assert "total_missions" in data
    assert "total_satellites_cataloged" in data
    assert "active_satellites_in_orbit" in data
    assert "launch_success_rate_pct" in data
    assert "cumulative_mission_investment_billion_usd" in data
    assert data["total_processed_records"] > 0
    assert data["data_pipeline_health"] == "100% OPERATIONAL"


def test_02_executive_insights():
    """Verify automated natural language intelligence generation."""
    response = client.get("/api/v1/overview/insights")
    assert response.status_code == 200
    insights = response.json()
    assert isinstance(insights, list)
    assert len(insights) >= 4
    for item in insights:
        assert "headline" in item
        assert "detail" in item
        assert "category" in item
        assert "importance" in item


# ==============================================================================
# 2. Module 2: Data Management Tests
# ==============================================================================
def test_03_data_inventory():
    """Verify Lakehouse dataset inventory across Bronze, Silver, Gold."""
    response = client.get("/api/v1/data/inventory")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["total_datasets"] == 9
    assert data["total_records"] > 10000


def test_04_data_upload_multipart():
    """Verify multipart file upload, schema validation, and checksum calculation."""
    csv_content = b"sample_id,component_name,quantity\n1,Solar Panel Array,50\n2,Reaction Wheel,25\n"
    files = {"file": ("test_upload.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/api/v1/data/upload", files=files, data={"zone": "raw"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["filename"] == "test_upload.csv"
    assert data["record_count"] == 2
    assert "sample_id" in data["columns_detected"]
    assert "md5_checksum" in data


def test_05_governance_catalog():
    """Verify governance data catalog metadata and MD5 signatures."""
    response = client.get("/api/v1/governance/catalog")
    assert response.status_code == 200
    data = response.json()
    assert "catalog" in data
    assert len(data["catalog"]) == 9
    first_item = data["catalog"][0]
    assert "title" in first_item
    assert "gold_fact_table" in first_item
    assert "md5_checksum" in first_item
    assert "quality_score" in first_item


def test_06_governance_quality():
    """Verify IQR and Z-score outlier anomaly detection reports."""
    response = client.get("/api/v1/governance/quality")
    assert response.status_code == 200
    data = response.json()
    assert data["platform_average_quality_score"] >= 95.0
    assert "reports" in data
    assert len(data["reports"]) >= 3


def test_07_pipeline_history_and_run():
    """Verify 14-stage pipeline execution and history tracking."""
    # Check history
    res_hist = client.get("/api/v1/pipeline/history")
    assert res_hist.status_code == 200
    history = res_hist.json()
    assert len(history) > 0
    assert len(history[0]["stages"]) == 14

    # Trigger run
    res_run = client.post("/api/v1/pipeline/run")
    assert res_run.status_code == 200
    run_data = res_run.json()
    assert run_data["status"] == "COMPLETED"
    assert run_data["stages_completed"] == 14


# ==============================================================================
# 3. Module 3: Hadoop Ecosystem Control Tests
# ==============================================================================
def test_08_ecosystem_health_probe():
    """Verify real cluster node probing adherence: Never show active unless verified."""
    response = client.get("/api/v1/ecosystem/health")
    assert response.status_code == 200
    data = response.json()
    assert "cluster_status" in data
    assert "services" in data
    assert len(data["services"]) == 9
    for s in data["services"]:
        assert s["status"] in ["HEALTHY", "UNREACHABLE"]
        assert "service_name" in s
        assert "container_name" in s


def test_09_hdfs_overview_and_zones():
    """Verify HDFS Lakehouse storage metrics, simulated blocks, and replication."""
    response = client.get("/api/v1/hdfs/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_size_formatted" in data
    assert "simulated_hdfs_blocks" in data
    assert "zones" in data
    assert len(data["zones"]) >= 5


def test_10_yarn_status():
    """Verify YARN ResourceManager memory, vcores, and active application list."""
    response = client.get("/api/v1/yarn/status")
    assert response.status_code == 200
    data = response.json()
    assert "allocated_memory_mb" in data
    assert "recent_applications" in data
    assert len(data["recent_applications"]) > 0


def test_11_mapreduce_streaming_job():
    """Verify MapReduce streaming job execution with mapper/reducer counters."""
    response = client.post("/api/v1/mapreduce/run", json={"job_name": "missions_aggregation"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCEEDED"
    assert "counters" in data
    assert data["counters"]["MAP_INPUT_RECORDS"] > 0
    assert len(data["results"]) > 0


def test_12_spark_and_pig_jobs():
    """Verify Spark and Pig script submission endpoints."""
    res_spark = client.post("/api/v1/spark/run", json={"job_name": "01_data_access_verification"})
    assert res_spark.status_code == 200
    assert res_spark.json()["number_of_stages"] > 0

    res_pig = client.post("/api/v1/pig/run", json={"script_name": "01_missions_etl.pig"})
    assert res_pig.status_code == 200
    assert res_pig.json()["status"] == "SUCCEEDED"


def test_13_hive_query_execution():
    """Verify Apache Hive query execution via HiveService."""
    response = client.get("/api/v1/hive/query?query_id=01_total_demand_by_component")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "records" in data
    assert len(data["records"]) > 0


# ==============================================================================
# 4. Module 4: Space Research Analytics Tests
# ==============================================================================
def test_14_missions_and_satellites_analytics():
    """Verify mission agency rankings and satellite orbit distribution."""
    res_m = client.get("/api/v1/missions/analytics")
    assert res_m.status_code == 200
    data_m = res_m.json()
    assert data_m["total_missions"] == 1500
    assert len(data_m["agencies"]) >= 5

    res_s = client.get("/api/v1/satellites/analytics")
    assert res_s.status_code == 200
    data_s = res_s.json()
    assert data_s["total_satellites"] == 2400
    assert len(data_s["orbit_distribution"]) >= 4


def test_15_launches_and_geographic_analytics():
    """Verify launch cadence trends and spaceport geographic distribution."""
    res_l = client.get("/api/v1/launches/analytics")
    assert res_l.status_code == 200
    data_l = res_l.json()
    assert data_l["total_launches"] == 1200
    assert len(data_l["vehicles"]) >= 5

    res_g = client.get("/api/v1/geographic/analytics")
    assert res_g.status_code == 200
    data_g = res_g.json()
    assert "territories" in data_g
    assert "spaceports" in data_g


def test_16_equipment_resources_manufacturing_investments():
    """Verify equipment demand, resource consumption, manufacturing, and R&D spend."""
    res_eq = client.get("/api/v1/equipment/analytics")
    assert res_eq.status_code == 200
    assert res_eq.json()["total_units_demanded"] > 0

    res_res = client.get("/api/v1/resources/analytics")
    assert res_res.status_code == 200
    assert len(res_res.json()["resources"]) > 0

    res_mfg = client.get("/api/v1/manufacturing/analytics")
    assert res_mfg.status_code == 200
    assert res_mfg.json()["total_manufacturing_orders"] > 0

    res_inv = client.get("/api/v1/investments/analytics")
    assert res_inv.status_code == 200
    assert len(res_inv.json()["agency_expenditures"]) > 0


# ==============================================================================
# 5. Module 5: Forecasting Studio Tests
# ==============================================================================
def test_17_forecasting_prediction():
    """Verify predictive forecasting engine with 95% confidence bands and model leaderboard."""
    req_body = {
        "target": "equipment",
        "algorithm": "RandomForest",
        "horizon_months": 12,
        "scenario": "baseline"
    }
    response = client.post("/api/v1/forecasting/predict", json=req_body)
    assert response.status_code == 200
    data = response.json()
    assert "target_name" in data
    assert "evaluation_metrics" in data
    assert data["evaluation_metrics"]["rmse"] > 0
    assert len(data["historical_data"]) > 0
    assert len(data["forecasts"]) == 4  # 12 months = 4 quarters
    for f in data["forecasts"]:
        assert f["ci_95_upper"] >= f["predicted_value"]
        assert f["ci_95_lower"] <= f["predicted_value"]
    assert len(data["leaderboard"]) >= 5
    assert len(data["feature_importance"]) > 0


def test_18_forecasting_catalogs():
    """Verify model catalog, series list, and comparison matrix."""
    res_models = client.get("/api/v1/forecasting/models")
    assert res_models.status_code == 200
    assert len(res_models.json()) >= 10

    res_series = client.get("/api/v1/forecasting/series")
    assert res_series.status_code == 200
    assert len(res_series.json()) >= 10


# ==============================================================================
# 6. Module 6: Resource Planning & Optimization Tests
# ==============================================================================
def test_19_procurement_optimization():
    """Verify SciPy HiGHS MILP procurement solver allocations."""
    req_body = {"budget_ceiling_usd": 60000000.0, "criticality_penalty_weight": 2.5}
    response = client.post("/api/v1/optimization/procurement", json=req_body)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPTIMAL_SOLVED"
    assert data["total_allocated_spend_usd"] <= 60000000.0
    assert len(data["allocations"]) > 0
    for a in data["allocations"]:
        assert "component_name" in a
        assert "allocated_units" in a
        assert "fulfillment_pct" in a


def test_20_demand_gap_and_inventory():
    """Verify supply-demand gap audit and safety-stock inventory planning."""
    res_gap = client.post("/api/v1/optimization/demand-gap", json={"category": "Equipment", "horizon_months": 12})
    assert res_gap.status_code == 200
    data_gap = res_gap.json()
    assert "total_forecast_demand" in data_gap
    assert len(data_gap["items"]) > 0

    res_inv = client.post("/api/v1/optimization/inventory", json={"item_name": "Solar Panel Array High Efficiency", "lead_time_days": 90, "service_level": 0.95})
    assert res_inv.status_code == 200
    data_inv = res_inv.json()
    assert data_inv["safety_stock_units"] > 0
    assert data_inv["reorder_point_units"] > data_inv["safety_stock_units"]


def test_21_scenarios_and_monte_carlo():
    """Verify digital twin scenario simulation and Monte Carlo stochastic draw distributions."""
    res_sc = client.post("/api/v1/scenarios/run", json={"budget_growth_pct": 10.0, "launch_cadence_change_pct": 15.0, "equipment_price_inflation_pct": 5.0})
    assert res_sc.status_code == 200
    data_sc = res_sc.json()
    assert "baseline" in data_sc
    assert "optimistic" in data_sc
    assert "conservative" in data_sc
    assert "custom" in data_sc

    res_mc = client.post("/api/v1/scenarios/monte-carlo", json={"iterations": 300, "volatility_pct": 15.0})
    assert res_mc.status_code == 200
    data_mc = res_mc.json()
    assert data_mc["iterations"] == 300
    assert len(data_mc["distribution_histogram"]) > 0


# ==============================================================================
# 7. Module 7: Big Data Benchmarking Tests
# ==============================================================================
def test_22_benchmarking_endpoints():
    """Verify benchmark run, summary, matrix, scaling, and manifest endpoints."""
    # Run
    res_run = client.post("/api/v1/benchmarks/run", json={"workload": "agency_mission_aggregation", "dataset_name": "space_missions"})
    assert res_run.status_code == 200
    data_run = res_run.json()
    assert len(data_run["results"]) == 5  # 5 engines
    assert "scalability_verdict" in data_run

    # Summary
    res_sum = client.get("/api/v1/benchmarks/summary")
    assert res_sum.status_code == 200

    # Matrix
    res_mat = client.get("/api/v1/benchmarks/matrix")
    assert res_mat.status_code == 200
    assert len(res_mat.json()) == 75

    # Scaling
    res_scale = client.get("/api/v1/benchmarks/scaling")
    assert res_scale.status_code == 200
    assert len(res_scale.json()) == 25


# ==============================================================================
# 8. Module 8: Report Generation & Download Tests
# ==============================================================================
def test_23_pdf_and_csv_reports():
    """Verify downloadable PDF whitepapers and CSV dataset extractions."""
    # Executive PDF
    res_pdf = client.get("/api/v1/reports/executive/pdf")
    assert res_pdf.status_code == 200
    assert res_pdf.headers["content-type"] == "application/pdf"
    assert len(res_pdf.content) > 1000

    # Lakehouse Excel/CSV
    res_excel = client.get("/api/v1/reports/lakehouse/excel")
    assert res_excel.status_code == 200
    assert "text/csv" in res_excel.headers["content-type"]
    assert b"Space Missions Master Registry" in res_excel.content

    # Raw CSV Export
    res_raw = client.get("/api/v1/reports/raw/csv?dataset_name=space_missions")
    assert res_raw.status_code == 200
    assert b"mission_id" in res_raw.content
