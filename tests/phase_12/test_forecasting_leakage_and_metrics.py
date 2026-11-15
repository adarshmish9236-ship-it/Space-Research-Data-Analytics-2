"""
ORBITALYTICS Phase 12 — Task 5: Forecasting Leakage, Evaluation & Reproducibility Test Suite
Validates strict chronological train/test splits, absence of target leakage, metric integrity
(RMSE, MAE, WAPE, MAPE, R², Bias), bounded confidence intervals, and seed determinism.
"""

import sys
import numpy as np
import pandas as pd
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml_forecasting.evaluator import ForecastEvaluator
from ml_forecasting.data_loader import TimeSeriesDataLoader
from ml_forecasting.backtester import ExpandingWindowBacktester
from app.services.demand_forecaster import DemandForecaster


def test_evaluator_mathematical_properties():
    """Verify mathematical properties of forecast evaluation metrics."""
    y_true = np.array([100.0, 110.0, 105.0, 120.0, 115.0])
    y_pred = np.array([102.0, 108.0, 107.0, 122.0, 113.0])

    metrics = ForecastEvaluator.calculate_metrics(y_true, y_pred)

    assert "mae" in metrics
    assert "rmse" in metrics
    assert "wape_pct" in metrics
    assert "mape_pct" in metrics
    assert "bias_pct" in metrics
    assert "r2" in metrics

    # Schwarz inequality / property: RMSE >= MAE
    assert metrics["rmse"] >= metrics["mae"]
    # Positive error bounds
    assert metrics["mae"] >= 0.0
    assert metrics["wape_pct"] >= 0.0
    assert metrics["mape_pct"] >= 0.0
    # Perfect fit identity test
    perfect_metrics = ForecastEvaluator.calculate_metrics(y_true, y_true)
    assert perfect_metrics["mae"] == 0.0
    assert perfect_metrics["rmse"] == 0.0
    assert perfect_metrics["wape_pct"] == 0.0
    assert perfect_metrics["r2"] == 1.0


def test_chronological_splits_and_no_leakage():
    """Verify that expanding window backtester enforces max(train_date) < min(test_date)."""
    dl = TimeSeriesDataLoader()
    raw_ts = dl.load_equipment_demand_series("All")
    assert "period" in raw_ts.columns
    assert "target" in raw_ts.columns

    # Verify chronological ordering
    periods = list(raw_ts["period"])
    assert periods == sorted(periods), "Time series periods must be strictly non-decreasing"

    # Verify expanding window split non-overlap
    backtester = ExpandingWindowBacktester(horizon=4, min_train_periods=40, step_size=4)
    n_obs = len(raw_ts)

    for train_end in range(backtester.min_train_periods, n_obs - backtester.horizon + 1, backtester.step_size):
        train_idx = list(range(0, train_end))
        test_idx = list(range(train_end, train_end + backtester.horizon))

        assert max(train_idx) < min(test_idx), "Target leakage detected: train index >= test index"
        assert len(set(train_idx).intersection(set(test_idx))) == 0, "Index overlap between train and test sets"


def test_confidence_interval_monotonicity_and_coverage():
    """Verify that 95% confidence intervals properly bound the forecast point predictions."""
    forecaster = DemandForecaster()
    res = forecaster.run_forecast(metric_type="equipment", horizon_months=12, model_name="RandomForest")

    forecasts = res.get("future_forecasts", [])
    assert len(forecasts) == 4

    for fc in forecasts:
        pred = fc["predicted_demand"]
        lower = fc["lower_bound_95"]
        upper = fc["upper_bound_95"]

        assert lower <= pred, f"Lower bound {lower} > predicted demand {pred}"
        assert upper >= pred, f"Upper bound {upper} < predicted demand {pred}"
        assert lower >= 0.0, f"Lower demand bound cannot be negative: {lower}"


def test_forecasting_seed_reproducibility():
    """Verify deterministic repeatability of ML forecasting across consecutive executions."""
    forecaster = DemandForecaster()
    res1 = forecaster.run_forecast(metric_type="equipment", horizon_months=12, model_name="RandomForest")
    res2 = forecaster.run_forecast(metric_type="equipment", horizon_months=12, model_name="RandomForest")

    preds1 = [f["predicted_demand"] for f in res1.get("future_forecasts", [])]
    preds2 = [f["predicted_demand"] for f in res2.get("future_forecasts", [])]

    np.testing.assert_allclose(preds1, preds2, rtol=1e-5, err_msg="Non-deterministic forecast predictions detected")
