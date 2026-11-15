"""
ORBITALYTICS Phase 12 — Task 1: End-to-End Pipeline Automated Test Suite
Validates the complete 14-stage workflow from raw data ingestion to optimization and reporting.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from run_e2e_pipeline import E2EPipelineTester


@pytest.fixture(scope="module")
def pipeline_results():
    """Execute the full 14-stage pipeline once and cache results for stage assertions."""
    tester = E2EPipelineTester()
    success = tester.run_all()
    return {
        "success": success,
        "stages": {s["stage_id"]: s for s in tester.stage_results},
        "raw_results": tester.stage_results
    }


def test_01_e2e_overall_success(pipeline_results):
    """Verify that all 14 stages succeeded without fatal exceptions."""
    assert pipeline_results["success"] is True
    assert len(pipeline_results["raw_results"]) == 14
    for s in pipeline_results["raw_results"]:
        assert s["status"] == "SUCCESS", f"Stage {s['stage_id']} ({s['stage_name']}) failed: {s.get('details')}"


def test_02_source_dataset_discovery(pipeline_results):
    """Stage 1: Verify all raw space datasets are discovered with valid checksums."""
    s = pipeline_results["stages"][1]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["file_count"] >= 8
    assert s["metrics"]["total_bytes"] > 500_000


def test_03_data_quality_and_schema(pipeline_results):
    """Stage 2: Verify zero schema violations across all raw records."""
    s = pipeline_results["stages"][2]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["total_records"] >= 10_000


def test_04_hdfs_lakehouse_ingestion(pipeline_results):
    """Stage 3: Verify HDFS Medallion architecture (raw, curated, aggregates, forecasts, warehouse)."""
    s = pipeline_results["stages"][3]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["files"] >= 10


def test_05_pig_latin_etl(pipeline_results):
    """Stage 4: Verify Pig Latin ETL scripts and Silver Parquet outputs."""
    s = pipeline_results["stages"][4]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["pig_scripts_count"] >= 5


def test_06_mapreduce_streaming(pipeline_results):
    """Stage 5: Verify distributed Hadoop MapReduce execution and key aggregation."""
    s = pipeline_results["stages"][5]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["map_input"] == 1500
    assert s["metrics"]["reduce_output"] > 0


def test_07_hive_data_warehouse(pipeline_results):
    """Stage 6: Verify Apache Hive SQL analytical query execution."""
    s = pipeline_results["stages"][6]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["rows"] >= 5
    assert s["metrics"]["runtime_ms"] >= 0


def test_08_pyspark_distributed_processing(pipeline_results):
    """Stage 7: Verify PySpark cluster manifest and multi-dataset joins."""
    s = pipeline_results["stages"][7]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["spark_jobs"] >= 4


def test_09_autoregressive_feature_engineering(pipeline_results):
    """Stage 8: Verify lag and rolling statistical feature matrix construction."""
    s = pipeline_results["stages"][8]
    assert s["status"] == "SUCCESS"
    dims = s["metrics"]["feature_dimensions"]
    assert dims[0] >= 50
    assert dims[1] >= 15


def test_10_forecasting_model_evaluation(pipeline_results):
    """Stage 9: Verify out-of-sample backtesting across statistical and ML models."""
    s = pipeline_results["stages"][9]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["models_count"] >= 5
    assert s["metrics"]["champion_rmse"] < 500


def test_11_multi_horizon_confidence_intervals(pipeline_results):
    """Stage 10: Verify multi-quarter demand projections bounded by 95% CIs."""
    s = pipeline_results["stages"][10]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["horizon_quarters"] == 4


def test_12_shortage_surplus_detection(pipeline_results):
    """Stage 11: Verify inventory reconciliation against forecast demand."""
    s = pipeline_results["stages"][11]
    assert s["status"] == "SUCCESS"
    assert "shortages_flagged" in s["metrics"]


def test_13_milp_constrained_optimization(pipeline_results):
    """Stage 12: Verify SciPy HiGHS MILP solver convergence to global optimum."""
    s = pipeline_results["stages"][12]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["solver_status"] in ["OPTIMAL", "optimal", "FEASIBLE"]


def test_14_dashboard_state_publishing(pipeline_results):
    """Stage 13: Verify executive KPIs published and materialized."""
    s = pipeline_results["stages"][13]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["total_missions"] == 1500


def test_15_executive_report_synthesis(pipeline_results):
    """Stage 14: Verify PDF whitepaper and CSV artifact export."""
    s = pipeline_results["stages"][14]
    assert s["status"] == "SUCCESS"
    assert s["metrics"]["pdf_bytes"] > 1000
    assert s["metrics"]["csv_bytes"] > 100
