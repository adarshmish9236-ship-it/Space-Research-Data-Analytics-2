"""
ORBITALYTICS Phase 12 — Task 2: Comprehensive Functional API Endpoint Test Suite
Verifies all 30+ endpoints across all 8 functional modules of the versioned REST API.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Module 1: Executive Overview
from app.api.v1.overview import (
    get_executive_kpis,
    get_executive_insights
)

# Module 2: Data Management
from app.api.v1.data_management import (
    get_dataset_inventory,
    get_governance_catalog,
    get_governance_quality,
    get_pipeline_history
)

# Module 3: Hadoop Ecosystem Control
from app.api.v1.ecosystem import (
    get_ecosystem_health,
    get_hdfs_overview,
    get_yarn_status,
    get_mapreduce_jobs,
    get_spark_jobs,
    get_pig_jobs,
    get_hive_tables,
    run_hive_query
)

# Module 4: Space Research Analytics
from app.api.v1.analytics import (
    get_missions_analytics,
    get_satellites_analytics,
    get_launches_analytics,
    get_equipment_analytics,
    get_resources_analytics,
    get_manufacturing_analytics,
    get_investments_analytics,
    get_geographic_analytics
)

# Module 5: Forecasting Studio
from app.api.v1.forecasting import (
    get_forecasting_models,
    get_forecasting_series,
    get_forecasting_comparison,
    get_forecasting_projections,
    get_model_registry,
    get_spark_mllib_metrics
)

# Module 6: Resource Planning & Optimization
from app.api.v1.optimization import (
    get_optimisation_shortages,
    get_optimisation_scenarios,
    get_optimisation_summary,
    get_sensitivity_tornado
)

# Module 7: Big Data Performance Benchmarking
from app.api.v1.benchmarks import (
    get_benchmarks_summary,
    get_benchmarks_matrix,
    get_benchmarks_scaling,
    get_benchmarks_manifest
)

# Module 8: Report Generation & Exports
from app.api.v1.reports import (
    download_executive_pdf,
    download_lakehouse_excel,
    download_raw_dataset_csv
)


# ------------------------------------------------------------------------------
# 1. Module 1: Executive Overview Tests
# ------------------------------------------------------------------------------
def test_functional_overview_kpis():
    kpis = get_executive_kpis()
    assert kpis["total_missions"] == 1500
    assert kpis["data_pipeline_health"] == "100% OPERATIONAL"
    assert kpis["total_processed_records"] > 5000


def test_functional_overview_insights():
    insights = get_executive_insights()
    assert isinstance(insights, list)
    assert len(insights) >= 4
    for item in insights:
        assert "headline" in item
        assert "detail" in item


# ------------------------------------------------------------------------------
# 2. Module 2: Data Management Tests
# ------------------------------------------------------------------------------
def test_functional_data_inventory():
    inv = get_dataset_inventory()
    assert "datasets" in inv
    assert len(inv["datasets"]) >= 9


def test_functional_governance_catalog():
    cat = get_governance_catalog()
    assert "catalog" in cat
    assert len(cat["catalog"]) >= 9


def test_functional_governance_quality():
    qual = get_governance_quality()
    assert "platform_average_quality_score" in qual
    assert qual["platform_average_quality_score"] >= 95.0


def test_functional_pipeline_history():
    hist = get_pipeline_history()
    assert isinstance(hist, list)
    assert len(hist) >= 1


# ------------------------------------------------------------------------------
# 3. Module 3: Hadoop Ecosystem Control Tests
# ------------------------------------------------------------------------------
def test_functional_ecosystem_health():
    health = get_ecosystem_health()
    assert "services" in health
    assert "cluster_status" in health
    assert len(health["services"]) >= 6


def test_functional_ecosystem_hdfs():
    hdfs = get_hdfs_overview()
    assert "zones" in hdfs
    assert "total_bytes" in hdfs or "total_size_bytes" in hdfs


def test_functional_ecosystem_yarn():
    yarn = get_yarn_status()
    assert "total_memory_mb" in yarn
    assert yarn["total_memory_mb"] > 0


def test_functional_ecosystem_mapreduce():
    mr = get_mapreduce_jobs()
    assert "available_jobs" in mr
    assert len(mr["available_jobs"]) >= 2


def test_functional_ecosystem_spark():
    spark = get_spark_jobs()
    assert "total_jobs" in spark
    assert spark["total_jobs"] >= 4


def test_functional_ecosystem_pig():
    pig = get_pig_jobs()
    assert "scripts" in pig
    assert len(pig["scripts"]) >= 5


def test_functional_ecosystem_hive():
    hive_tables = get_hive_tables()
    assert "tables" in hive_tables

    q_res = run_hive_query("01_total_demand_by_component")
    assert "records" in q_res or "data" in q_res


# ------------------------------------------------------------------------------
# 4. Module 4: Space Research Analytics Tests
# ------------------------------------------------------------------------------
def test_functional_analytics_missions():
    missions = get_missions_analytics()
    assert "total_missions" in missions
    assert missions["total_missions"] == 1500


def test_functional_analytics_satellites():
    satellites = get_satellites_analytics()
    assert "total_satellites" in satellites
    assert satellites["total_satellites"] == 2400


def test_functional_analytics_launches():
    launches = get_launches_analytics()
    assert "total_launches" in launches


def test_functional_analytics_equipment():
    equipment = get_equipment_analytics()
    assert "components" in equipment
    assert len(equipment["components"]) >= 5


def test_functional_analytics_resources():
    resources = get_resources_analytics()
    assert "resources" in resources
    assert len(resources["resources"]) >= 5


def test_functional_analytics_manufacturing():
    mfg = get_manufacturing_analytics()
    assert "classes" in mfg
    assert len(mfg["classes"]) >= 3


def test_functional_analytics_investments():
    inv = get_investments_analytics()
    assert "agency_expenditures" in inv
    assert len(inv["agency_expenditures"]) >= 5


def test_functional_analytics_geographic():
    geo = get_geographic_analytics()
    assert "territories" in geo
    assert len(geo["territories"]) >= 4


# ------------------------------------------------------------------------------
# 5. Module 5: Forecasting Studio Tests
# ------------------------------------------------------------------------------
def test_functional_forecasting_models():
    models = get_forecasting_models()
    assert isinstance(models, list)
    assert len(models) >= 5


def test_functional_forecasting_series():
    series = get_forecasting_series()
    assert isinstance(series, list)
    assert len(series) >= 3


def test_functional_forecasting_comparison():
    comp = get_forecasting_comparison(domain=None, series=None)
    assert isinstance(comp, list)
    assert len(comp) >= 5


def test_functional_forecasting_projections():
    proj = get_forecasting_projections(domain=None, series_id=None)
    assert "pipeline" in proj or "series" in proj


def test_functional_model_registry():
    reg = get_model_registry()
    assert "models" in reg or "registered_models" in reg or "registry" in reg


def test_functional_spark_mllib_metrics():
    mllib = get_spark_mllib_metrics()
    assert "phase" in mllib
    assert mllib["phase"] == 8


# ------------------------------------------------------------------------------
# 6. Module 6: Resource Planning & Optimization Tests
# ------------------------------------------------------------------------------
def test_functional_optimization_shortages():
    shortages = get_optimisation_shortages(domain=None, item_name=None)
    assert isinstance(shortages, list)
    assert len(shortages) > 0


def test_functional_optimization_scenarios():
    scenarios = get_optimisation_scenarios(domain=None)
    assert isinstance(scenarios, list)
    assert len(scenarios) > 0


def test_functional_optimization_summary():
    summary = get_optimisation_summary(domain="equipment_demand")
    assert "domain" in summary
    assert "baseline_metrics" in summary


def test_functional_sensitivity_tornado():
    tornado = get_sensitivity_tornado()
    assert "factors" in tornado
    assert len(tornado["factors"]) >= 3


# ------------------------------------------------------------------------------
# 7. Module 7: Big Data Performance Benchmarking Tests
# ------------------------------------------------------------------------------
def test_functional_benchmarks_summary():
    summary = get_benchmarks_summary()
    assert "total_trials_evaluated" in summary


def test_functional_benchmarks_matrix():
    matrix = get_benchmarks_matrix()
    assert isinstance(matrix, list)
    assert len(matrix) > 0


def test_functional_benchmarks_scaling():
    scaling = get_benchmarks_scaling()
    assert isinstance(scaling, list)
    assert len(scaling) > 0


def test_functional_benchmarks_manifest():
    manifest = get_benchmarks_manifest()
    assert "project" in manifest
    assert manifest["phase"] == "Phase 10"


# ------------------------------------------------------------------------------
# 8. Module 8: Report Generation & Exports Tests
# ------------------------------------------------------------------------------
def test_functional_reports_pdf():
    response = download_executive_pdf()
    assert response.status_code == 200
    assert response.media_type == "application/pdf"
    assert len(response.body) > 1000


def test_functional_reports_excel():
    response = download_lakehouse_excel()
    assert response.status_code == 200
    assert len(response.body) > 1000


def test_functional_reports_csv():
    response = download_raw_dataset_csv(dataset_name="space_missions")
    assert response.status_code == 200
    assert len(response.body) > 100
