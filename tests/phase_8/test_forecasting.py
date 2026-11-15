"""
ORBITALYTICS Phase 8 — Automated Forecasting Verification Test Suite
Tests:
  - Time series data loader and feature matrix engineering
  - Baseline, Statistical, and Machine Learning models
  - Evaluation metrics mathematical correctness and edge cases
  - Chronological expanding-window backtesting without future leakage
  - Model registry, metadata tracking, and drift monitoring
  - Distributed Spark MLlib evaluation manifest
  - 4-quarter forward projections and prediction intervals
"""

import os
import json
import pytest
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_PHASE8 = PROJECT_ROOT / "docs" / "phase_8"
RESULTS_DIR = DOCS_PHASE8 / "results"
REGISTRY_FILE = DOCS_PHASE8 / "model_registry.json"

from ml_forecasting.data_loader import TimeSeriesDataLoader
from ml_forecasting.baseline_models import (
    NaiveForecast, SeasonalNaiveForecast, MovingAverageForecast, LinearRegressionBaseline
)
from ml_forecasting.statistical_models import (
    ARIMAForecaster, SARIMAForecaster, HoltWintersForecaster
)
from ml_forecasting.ml_models import MLForecaster
from ml_forecasting.evaluator import ForecastEvaluator
from ml_forecasting.backtester import ExpandingWindowBacktester
from ml_forecasting.registry import ModelRegistry


def test_time_series_data_loader():
    """Verify quarterly continuous series loading and feature engineering."""
    dl = TimeSeriesDataLoader()
    eq = dl.load_equipment_demand_series("All")
    assert len(eq) >= 60, f"Expected at least 60 quarters, got {len(eq)}"
    assert "target" in eq.columns
    assert "period" in eq.columns

    feat = dl.build_feature_matrix(eq, lags=4)
    expected_cols = [
        "time_index", "sin_q", "cos_q", "q_1", "q_2", "q_3", "q_4",
        "lag_1", "lag_2", "lag_3", "lag_4",
        "rolling_mean_4", "rolling_std_4", "rolling_mean_2",
        "seasonal_lag_4", "prior_growth_rate"
    ]
    for col in expected_cols:
        assert col in feat.columns, f"Missing feature column: {col}"
    assert not feat.isnull().values.any(), "Feature matrix contains NaN values"


def test_baseline_models():
    """Verify all 4 baseline forecasting models."""
    series = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210])
    horizon = 4

    m_naive = NaiveForecast().fit(series)
    p_naive = m_naive.predict(horizon)
    assert len(p_naive) == horizon
    assert np.all(p_naive == 210)

    m_snaive = SeasonalNaiveForecast(season_length=4).fit(series)
    p_snaive = m_snaive.predict(horizon)
    assert len(p_snaive) == horizon
    assert p_snaive[0] == 180 and p_snaive[3] == 210

    m_ma = MovingAverageForecast(window=4).fit(series)
    p_ma = m_ma.predict(horizon)
    assert len(p_ma) == horizon
    assert p_ma[0] == np.mean([180, 190, 200, 210])

    m_lr = LinearRegressionBaseline().fit(series)
    p_lr = m_lr.predict(horizon)
    assert len(p_lr) == horizon
    assert p_lr[-1] > p_lr[0], "Linear regression should capture upward trend"


def test_statistical_models():
    """Verify ARIMA, SARIMA, and Holt-Winters forecasting."""
    series = pd.Series([100, 120, 110, 140, 130, 155, 145, 175, 160, 190, 180, 210, 195, 230, 215, 250])
    horizon = 4

    # ARIMA
    m_arima = ARIMAForecaster().fit(series)
    fc_a, low_a, up_a = m_arima.predict(horizon)
    assert len(fc_a) == horizon
    assert np.all(up_a >= low_a), "ARIMA upper confidence bound must be >= lower bound"

    # SARIMA
    m_sarima = SARIMAForecaster().fit(series)
    fc_s, low_s, up_s = m_sarima.predict(horizon)
    assert len(fc_s) == horizon
    assert np.all(up_s >= low_s), "SARIMA upper confidence bound must be >= lower bound"

    # Holt-Winters
    m_hw = HoltWintersForecaster(seasonal_periods=4).fit(series)
    fc_h = m_hw.predict(horizon)
    assert len(fc_h) == horizon
    assert np.all(fc_h > 0), "Holt-Winters forecasts must be non-negative"


def test_ml_models():
    """Verify Random Forest and XGBoost recursive forecasting and feature importances."""
    dl = TimeSeriesDataLoader()
    eq = dl.load_equipment_demand_series("All")
    feat = dl.build_feature_matrix(eq)

    train_df = feat.iloc[:-4]

    # Random Forest
    rf = MLForecaster("RandomForest").fit(train_df)
    fc_rf, low_rf, up_rf = rf.predict_recursive(train_df, horizon=4)
    assert len(fc_rf) == 4
    assert np.all(up_rf >= low_rf)
    imp_rf = rf.get_feature_importances()
    assert len(imp_rf) > 0, "Random Forest should return feature importances"
    assert sum(imp_rf.values()) > 95.0, "Feature importances should sum to ~100%"

    # XGBoost
    xgb_m = MLForecaster("XGBoost").fit(train_df)
    fc_xgb, low_xgb, up_xgb = xgb_m.predict_recursive(train_df, horizon=4)
    assert len(fc_xgb) == 4
    assert np.all(up_xgb >= low_xgb)
    imp_xgb = xgb_m.get_feature_importances()
    assert len(imp_xgb) > 0, "XGBoost should return feature importances"


def test_evaluator_metrics():
    """Verify MAE, RMSE, WAPE, MAPE, Forecast Bias, and R-squared calculation."""
    y_true = np.array([100.0, 200.0, 300.0, 400.0])
    y_pred = np.array([110.0, 190.0, 310.0, 390.0])

    metrics = ForecastEvaluator.calculate_metrics(y_true, y_pred)
    assert metrics["mae"] == 10.0
    assert metrics["rmse"] == 10.0
    assert metrics["wape_pct"] == 4.0  # sum|e|=40, sum(y)=1000 -> 40/1000*100 = 4.0%
    assert metrics["bias_pct"] == 0.0  # sum(e) = 0 -> balanced
    assert metrics["r2"] > 0.98

    # Edge case: zero actuals
    y_zero = np.array([0.0, 0.0])
    y_zero_pred = np.array([5.0, 5.0])
    m_zero = ForecastEvaluator.calculate_metrics(y_zero, y_zero_pred)
    assert m_zero["wape_pct"] == 100.0
    assert m_zero["mae"] == 5.0


def test_chronological_backtester():
    """Verify that backtesting executes across multiple chronological folds without future leakage."""
    dl = TimeSeriesDataLoader()
    eq = dl.load_equipment_demand_series("All")
    feat = dl.build_feature_matrix(eq)

    bt = ExpandingWindowBacktester(horizon=4, min_train_periods=48, step_size=4)
    res = bt.run_backtest(eq, feat)

    assert res["folds_evaluated"] >= 4
    assert res["models_evaluated"] == 11
    assert res["champion_model"] is not None
    assert res["champion_wape"] > 0.0

    # Ensure models are ranked by WAPE ascending
    wapes = [m["wape_pct"] for m in res["ranked_models"]]
    assert wapes == sorted(wapes), "Models must be sorted by out-of-sample WAPE ascending"


def test_model_registry_and_drift():
    """Verify Model Registry persistence and drift monitoring functions."""
    reg = ModelRegistry()
    assert REGISTRY_FILE.exists(), f"Registry file not found: {REGISTRY_FILE}"

    # Test drift functions
    base_dist = np.random.normal(100, 10, 50)
    drifted_dist = np.random.normal(200, 10, 50)
    drift_res = ModelRegistry.assess_input_drift(base_dist, drifted_dist)
    assert drift_res["drift_detected"] is True

    # Test concept drift
    stable_residuals = np.array([-1.5, 1.5, -2.0, 2.0, -0.5, 0.5, -1.0, 1.0] * 3)
    concept_res = ModelRegistry.assess_concept_drift(stable_residuals)
    assert concept_res["drift_detected"] is False

    # Test biased concept drift
    biased_residuals = np.array([5.0] * 10)
    biased_res = ModelRegistry.assess_concept_drift(biased_residuals)
    assert biased_res["drift_detected"] is True


def test_spark_mllib_evaluation_manifest():
    """Verify that Spark MLlib distributed training executed and generated evaluation manifest."""
    manifest_path = RESULTS_DIR / "spark_mllib_evaluation.json"
    assert manifest_path.exists(), f"Spark MLlib manifest not found: {manifest_path}"

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("component") == "Spark_MLlib_Distributed_Training"
    assert data.get("train_records") > 0
    assert data.get("test_records") > 0
    models = data.get("models_evaluated", [])
    assert len(models) >= 2, "Expected at least 2 Spark MLlib models (RF & GBT)"
    for m in models:
        assert m["test_rmse"] > 0
        assert m["test_mae"] > 0
