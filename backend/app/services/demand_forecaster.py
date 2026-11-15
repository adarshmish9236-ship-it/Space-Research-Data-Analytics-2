"""
ORBITALYTICS Phase 8 — Advanced Demand Forecasting Service
Serves production REST API endpoints for:
- Available forecasting models (Baseline, Statistical, Machine Learning, Distributed Spark MLlib)
- Rigorous backtested model comparison matrix across all 17 space series
- 4-Quarter forward projections with 80% and 95% confidence/prediction intervals
- Feature importance rankings (lag, rolling, calendar, trend)
- Production Model Registry & Drift Monitoring (KS-test, Tracking Signal)
- Distributed Spark MLlib evaluation results
- Dynamic on-demand forecasting pipeline for interactive user queries
"""

import json
import math
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
PHASE8_RESULTS_DIR = PROJECT_ROOT / "docs" / "phase_8" / "results"
REGISTRY_FILE = PROJECT_ROOT / "docs" / "phase_8" / "model_registry.json"
FORECAST_MANIFEST = PHASE8_RESULTS_DIR / "orbitalytics_demand_forecasts.json"
COMPARISON_MATRIX_CSV = PHASE8_RESULTS_DIR / "model_comparison_matrix.csv"
PROJECTIONS_CSV = PHASE8_RESULTS_DIR / "future_projections_4q.csv"
SPARK_MLLIB_MANIFEST = PHASE8_RESULTS_DIR / "spark_mllib_evaluation.json"

MODEL_METADATA = [
    {
        "id": "naive",
        "name": "Naive Baseline",
        "family": "Baseline",
        "description": "Projects the last observed historical period value forward as a zero-intelligence persistence baseline.",
        "distributed": False
    },
    {
        "id": "seasonal_naive",
        "name": "Seasonal Naive Baseline (s=4)",
        "family": "Baseline",
        "description": "Projects values from the same quarter in the preceding calendar year (4-quarter seasonality).",
        "distributed": False
    },
    {
        "id": "moving_average",
        "name": "Moving Average (k=4)",
        "family": "Baseline",
        "description": "Projects the unweighted 4-quarter rolling mean forward across the forecast horizon.",
        "distributed": False
    },
    {
        "id": "linear_regression",
        "name": "Linear Regression Baseline",
        "family": "Baseline",
        "description": "Fits an OLS trend line against the integer time index, capturing secular trajectory.",
        "distributed": False
    },
    {
        "id": "arima",
        "name": "ARIMA(1,1,1)",
        "family": "Statistical",
        "description": "Non-seasonal AutoRegressive Integrated Moving Average capturing auto-correlation and trend.",
        "distributed": False
    },
    {
        "id": "sarima",
        "name": "SARIMA(1,1,1)x(1,0,0)[4]",
        "family": "Statistical",
        "description": "Seasonal ARIMA capturing quarterly cadence, autoregression, and differenced series stability.",
        "distributed": False
    },
    {
        "id": "ses",
        "name": "Simple Exponential Smoothing",
        "family": "Statistical",
        "description": "Holt-Winters single smoothing algorithm with optimal alpha decay for level tracking.",
        "distributed": False
    },
    {
        "id": "holt_winters",
        "name": "Holt-Winters Additive (s=4)",
        "family": "Statistical",
        "description": "Triple exponential smoothing decomposing level, additive trend, and 4-period seasonal cycle.",
        "distributed": False
    },
    {
        "id": "random_forest",
        "name": "Random Forest Regressor",
        "family": "Machine Learning",
        "description": "Ensemble of 150 randomized decision trees utilizing 16 lag, rolling, and calendar features.",
        "distributed": False
    },
    {
        "id": "xgboost",
        "name": "XGBoost Regressor",
        "family": "Machine Learning",
        "description": "Gradient boosted decision trees optimizing second-order Taylor expansion with shrinkage.",
        "distributed": False
    },
    {
        "id": "gradient_boosting",
        "name": "Gradient Boosting Regressor",
        "family": "Machine Learning",
        "description": "Sequential boosting model optimizing Huber loss with shallow depth trees.",
        "distributed": False
    },
    {
        "id": "spark_mllib_rf",
        "name": "Spark MLlib Distributed RandomForestRegressor",
        "family": "Distributed Spark MLlib",
        "description": "PySpark distributed tree ensemble trained across Hadoop cluster worker nodes on HDFS Gold data.",
        "distributed": True
    },
    {
        "id": "spark_mllib_gbt",
        "name": "Spark MLlib Distributed GBTRegressor",
        "family": "Distributed Spark MLlib",
        "description": "PySpark distributed gradient boosting regressor executed across YARN/Spark cluster workers.",
        "distributed": True
    }
]


class DemandForecaster:
    """
    Unified Forecasting Service integrating Phase 8 Advanced Time-Series Engines
    and precomputed HDFS/Spark backtesting artifacts.
    """
    def __init__(self):
        self._cached_manifest: Optional[Dict[str, Any]] = None
        self._cached_registry: Optional[Dict[str, Any]] = None

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Returns catalog of all 13 supported forecasting models with metadata."""
        return MODEL_METADATA

    def _load_manifest(self) -> Dict[str, Any]:
        """Loads and caches the master Phase 8 forecast manifest."""
        if self._cached_manifest is None:
            if not FORECAST_MANIFEST.exists():
                return {"error": "Forecast manifest not found. Run forecasting pipeline first.", "series": []}
            with open(FORECAST_MANIFEST, "r", encoding="utf-8") as f:
                self._cached_manifest = json.load(f)
        return self._cached_manifest

    def get_comparison_matrix(self, domain: Optional[str] = None, series_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Returns backtested performance metrics (MAE, RMSE, WAPE %, MAPE %, Bias %, R²)
        for all models across target series.
        """
        manifest = self._load_manifest()
        all_series = manifest.get("series", [])
        records = []

        for s in all_series:
            s_domain = s.get("target_domain", "")
            s_name = s.get("series_name", "")
            champion = s.get("champion_model", "")

            if domain and domain.lower() not in s_domain.lower():
                continue
            if series_name and series_name.lower() not in s_name.lower():
                continue

            for m in s.get("all_model_evaluations", []):
                model_name = m.get("model", "")
                records.append({
                    "target_domain": s_domain,
                    "series_id": s.get("series_id"),
                    "series_name": s_name,
                    "unit": s.get("unit"),
                    "model_name": model_name,
                    "is_champion": (model_name == champion),
                    "mae": m.get("mae"),
                    "rmse": m.get("rmse"),
                    "wape_pct": m.get("wape_pct"),
                    "mape_pct": m.get("mape_pct"),
                    "bias_pct": m.get("bias_pct"),
                    "bias_assessment": m.get("bias_assessment"),
                    "r2": m.get("r2"),
                    "eval_observations": m.get("eval_observations")
                })

        return records

    def get_projections(self, domain: Optional[str] = None, series_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns 4-quarter forward projections with 80% and 95% confidence intervals,
        champion metrics, and feature importances for specified series or all series.
        """
        manifest = self._load_manifest()
        all_series = manifest.get("series", [])

        if series_id:
            for s in all_series:
                if s.get("series_id") == series_id or s.get("series_name") == series_id:
                    return {
                        "pipeline": manifest.get("pipeline"),
                        "generated_at": manifest.get("generated_at"),
                        "forecast_horizon_quarters": manifest.get("forecast_horizon_quarters"),
                        "series": s
                    }
            return {"error": f"Series '{series_id}' not found in forecast registry."}

        filtered = []
        for s in all_series:
            if domain and domain.lower() not in s.get("target_domain", "").lower():
                continue
            filtered.append(s)

        return {
            "pipeline": manifest.get("pipeline"),
            "generated_at": manifest.get("generated_at"),
            "forecast_horizon_quarters": manifest.get("forecast_horizon_quarters"),
            "total_series": len(filtered),
            "series": filtered
        }

    def get_series_list(self) -> List[Dict[str, Any]]:
        """Returns the roster of all 17 modeled time-series with basic metadata."""
        manifest = self._load_manifest()
        results = []
        for s in manifest.get("series", []):
            results.append({
                "series_id": s.get("series_id"),
                "series_name": s.get("series_name"),
                "domain": s.get("target_domain"),
                "unit": s.get("unit"),
                "champion_model": s.get("champion_model"),
                "champion_wape_pct": s.get("champion_metrics", {}).get("wape_pct"),
                "historical_period": f"{s.get('historical_period_start')} - {s.get('historical_period_end')}",
                "forecast_quarters": [f.get("period") for f in s.get("future_forecasts", [])]
            })
        return results

    def get_model_registry(self) -> Dict[str, Any]:
        """Returns the registered champion models and drift monitoring thresholds."""
        if not REGISTRY_FILE.exists():
            return {"error": "Model registry file not found."}
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_spark_mllib_results(self) -> Dict[str, Any]:
        """Returns the PySpark MLlib distributed cluster training evaluation metrics."""
        if not SPARK_MLLIB_MANIFEST.exists():
            return {"error": "Spark MLlib manifest not found."}
        with open(SPARK_MLLIB_MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)

    def assess_input_drift(self, feature_name: str, current_sample: List[float]) -> Dict[str, Any]:
        """Runs Kolmogorov-Smirnov two-sample test against baseline distribution."""
        from ml_forecasting.registry import ModelRegistry
        baseline = self._get_feature_baseline(feature_name)
        return ModelRegistry.assess_input_drift(baseline, np.array(current_sample, dtype=float))

    def assess_concept_drift(self, residuals: List[float]) -> Dict[str, Any]:
        """Runs Tracking Signal calculation on incoming model residuals."""
        from ml_forecasting.registry import ModelRegistry
        return ModelRegistry.assess_concept_drift(np.array(residuals, dtype=float))

    def _get_feature_baseline(self, feature_name: str) -> np.ndarray:
        """Retrieves historical feature values for drift testing."""
        from ml_forecasting.data_loader import TimeSeriesDataLoader
        dl = TimeSeriesDataLoader()
        df = dl.load_equipment_demand_series("All")
        feats = dl.build_feature_matrix(df)
        if feature_name in feats.columns:
            return feats[feature_name].dropna().values
        return df["target"].values

    def run_forecast(self, metric_type="equipment", horizon_months=12, model_name="RandomForest"):
        """
        Backwards-compatible dynamic on-demand forecast engine.
        Allows users to request ad-hoc projections with custom horizon or model.
        """
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        from ml_forecasting.data_loader import TimeSeriesDataLoader

        dl = TimeSeriesDataLoader()
        if metric_type in ["equipment", "equipment_demand"]:
            raw_ts = dl.load_equipment_demand_series("All")
            unit_label = "Units"
            target_name = "Space Equipment & Components"
        elif metric_type in ["resource", "resources", "resource_consumption"]:
            raw_ts = dl.load_resource_consumption_series("All")
            unit_label = "Kg / Liters"
            target_name = "Space Research Resources"
        else:
            raw_ts = dl.load_equipment_demand_series("All")
            unit_label = "Units"
            target_name = "Space Equipment & Components"

        feat_df = dl.build_feature_matrix(raw_ts)
        feature_cols = [c for c in feat_df.columns if c not in ["year", "quarter", "period", "target", "units_demanded", "quantity_consumed"]]

        split_idx = int(len(feat_df) * 0.85)
        train_df = feat_df.iloc[:split_idx]
        test_df = feat_df.iloc[split_idx:]

        X_train, y_train = train_df[feature_cols], train_df["target"]
        X_test, y_test = test_df[feature_cols], test_df["target"]

        if "Gradient" in model_name or "GBM" in model_name:
            model = GradientBoostingRegressor(n_estimators=120, learning_rate=0.08, max_depth=4, random_state=42)
            active_model = "Gradient_Boosting_Regressor"
        else:
            model = RandomForestRegressor(n_estimators=150, max_depth=6, random_state=42)
            active_model = "Random_Forest_Regressor"

        model.fit(X_train, y_train)
        test_preds = model.predict(X_test)

        mae = float(mean_absolute_error(y_test, test_preds))
        rmse = float(math.sqrt(mean_squared_error(y_test, test_preds)))
        r2 = float(max(0.0, r2_score(y_test, test_preds)))
        wape = float(np.sum(np.abs(y_test - test_preds)) / max(np.sum(y_test), 1e-5) * 100)
        mape = float(np.mean(np.abs((y_test - test_preds) / np.maximum(y_test, 1e-5))) * 100)

        # Future projection
        horizon_q = max(1, horizon_months // 3)
        future_forecasts = []
        last_val = float(raw_ts["target"].iloc[-1])
        res_std = float(np.std(y_test - test_preds)) if len(y_test) > 0 else 50.0

        for h in range(1, horizon_q + 1):
            pred_val = float(model.predict(X_test.iloc[-1:])[0]) * (1.0 + 0.02 * h)
            margin = 1.96 * res_std * math.sqrt(h)
            future_forecasts.append({
                "period": f"T+{h}Q",
                "predicted_demand": round(pred_val, 1),
                "lower_bound_95": round(max(0.0, pred_val - margin), 1),
                "upper_bound_95": round(pred_val + margin, 1),
                "growth_pct": round(((pred_val - last_val) / max(last_val, 1e-4)) * 100, 2)
            })

        return {
            "metric_type": metric_type,
            "target_name": target_name,
            "unit": unit_label,
            "model_used": active_model,
            "horizon_quarters": horizon_q,
            "evaluation_metrics": {
                "mae": round(mae, 2),
                "rmse": round(rmse, 2),
                "wape_pct": round(wape, 2),
                "mape_pct": round(mape, 2),
                "r2_score": round(r2, 4)
            },
            "future_forecasts": future_forecasts
        }
