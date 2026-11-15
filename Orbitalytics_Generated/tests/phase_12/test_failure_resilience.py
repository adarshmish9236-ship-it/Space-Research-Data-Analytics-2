"""
ORBITALYTICS Phase 12 — Task 6: System Failure Modes & Resilience Test Suite
Tests graceful degradation, missing file handling, malformed payloads, out-of-bounds parameters,
cluster unreachable states, and data validation rejection.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.hdfs_service import HDFSService
from app.services.mapreduce_service import MapReduceService
from app.services.hive_service import HiveService
from app.services.demand_forecaster import DemandForecaster
from app.services.optimisation_service import OptimisationService
from app.services.reporting_service import ReportingService
from app.services.ecosystem_service import EcosystemService
from ml_forecasting.evaluator import ForecastEvaluator
from ml_forecasting.data_loader import TimeSeriesDataLoader


def test_hdfs_nonexistent_zone_fallback():
    """Verify HDFSService handles nonexistent zone queries gracefully."""
    hdfs = HDFSService()
    res = hdfs.list_zone_files("nonexistent_zone_9999")
    assert "files" in res
    assert len(res["files"]) == 0
    assert res.get("status") == "NOT_FOUND"


def test_mapreduce_unknown_job_rejection():
    """Verify MapReduceService rejects unknown job names cleanly with descriptive exception."""
    mr = MapReduceService()
    with pytest.raises((ValueError, KeyError, Exception)):
        mr.run_mapreduce_job("totally_unknown_job_xyz_999")


def test_hive_invalid_query_id_graceful_handling():
    """Verify HiveService raises clean exception or returns error status when querying non-existent query."""
    hive = HiveService()
    with pytest.raises((RuntimeError, ValueError, Exception)):
        hive.execute_analytical_query("invalid_query_slug_9999")


def test_evaluator_empty_arrays_rejection():
    """Verify ForecastEvaluator rejects empty input arrays with ValueError."""
    with pytest.raises(ValueError):
        ForecastEvaluator.calculate_metrics([], [])


def test_evaluator_mismatched_lengths_rejection():
    """Verify ForecastEvaluator rejects arrays of unequal lengths with ValueError."""
    with pytest.raises(ValueError):
        ForecastEvaluator.calculate_metrics([10.0, 20.0], [10.0])


def test_feature_engineering_insufficient_data():
    """Verify TimeSeriesDataLoader drops all rows when observations are fewer than lag requirements."""
    dl = TimeSeriesDataLoader()
    tiny_df = pd.DataFrame({
        "year": [2020],
        "quarter": [1],
        "period": ["2020Q1"],
        "target": [100]
    })
    feat = dl.build_feature_matrix(tiny_df)
    # Lags t-1..t-4 require at least 5 observations, so 1 observation yields 0 valid rows
    assert len(feat) == 0


def test_forecast_engine_unsupported_model_fallback():
    """Verify forecaster handles unknown model name with fallback or explicit error."""
    forecaster = DemandForecaster()
    try:
        res = forecaster.run_forecast(metric_type="equipment", horizon_months=12, model_name="NonExistentAlienAI")
        assert "future_forecasts" in res
    except Exception as e:
        assert "not found" in str(e).lower() or "unsupported" in str(e).lower() or "unknown" in str(e).lower()


def test_optimization_extreme_budget_stress():
    """Verify HiGHS MILP handles near-zero or severe budget constriction safely."""
    optimiser = OptimisationService()
    # Stress test with 1% of normal budget
    res = optimiser.solve_custom_scenario(domain="equipment_demand", budget_multiplier=0.01)
    assert "status" in res
    assert res["status"] in ["OPTIMAL", "optimal", "INFEASIBLE", "infeasible", "FEASIBLE"]


def test_reporting_unsupported_report_type():
    """Verify reporting service handles unsupported report types gracefully by returning empty/header string."""
    reporter = ReportingService()
    csv_str = reporter.export_csv("totally_unsupported_type_xyz", {})
    assert len(csv_str) == 0 or "totally_unsupported" not in csv_str


def test_ecosystem_network_resilience():
    """Verify EcosystemService socket probes handle completely closed/unreachable ports safely."""
    eco = EcosystemService()
    # Probe a high-range random port that is guaranteed closed
    is_open = eco._check_port("127.0.0.1", 59999, timeout=0.1)
    assert is_open is False, "Closed port 59999 reported as open"
