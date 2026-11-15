"""
ORBITALYTICS Phase 8 — Task 6: Chronological Expanding-Window Backtester
Performs rigorous rolling-origin evaluation without target leakage:
  - Folds evaluate out-of-sample 4-quarter horizons
  - Never shuffles time series records
  - Compares all model families (Baseline, Statistical, ML) on the same splits
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

from ml_forecasting.baseline_models import (
    NaiveForecast, SeasonalNaiveForecast, MovingAverageForecast, LinearRegressionBaseline
)
from ml_forecasting.statistical_models import (
    ARIMAForecaster, SARIMAForecaster, ExponentialSmoothingForecaster, HoltWintersForecaster
)
from ml_forecasting.ml_models import MLForecaster
from ml_forecasting.evaluator import ForecastEvaluator


class ExpandingWindowBacktester:
    def __init__(self, horizon: int = 4, min_train_periods: int = 44, step_size: int = 4):
        """
        horizon: number of periods to forecast per fold (default 4 quarters = 1 year)
        min_train_periods: initial window size (44 quarters = 11 years: 2010 to 2020)
        step_size: step size between folds (default 4 quarters = annual evaluation folds)
        """
        self.horizon = horizon
        self.min_train_periods = min_train_periods
        self.step_size = step_size
        self.evaluator = ForecastEvaluator()

    def run_backtest(self,
                     raw_df: pd.DataFrame,
                     feat_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Executes expanding-window backtesting across all candidate models.
        Returns aggregated out-of-sample metrics per model and step-by-step predictions.
        """
        n_obs = len(raw_df)
        if n_obs < self.min_train_periods + self.horizon:
            raise ValueError(f"Insufficient observations for backtesting ({n_obs} < {self.min_train_periods + self.horizon})")

        # Models to evaluate
        model_names = [
            "Naive_Baseline",
            "Seasonal_Naive_Baseline",
            "Moving_Average_k4",
            "Linear_Regression_Baseline",
            "ARIMA(1,1,1)",
            "SARIMA(1,1,1)x(1,0,0)[4]",
            "Simple_Exponential_Smoothing",
            "Holt_Winters_Additive_s4",
            "Random_Forest_Regressor",
            "XGBoost_Regressor",
            "Gradient_Boosting_Regressor"
        ]

        # Accumulator for predictions and true values across all folds
        fold_results = {name: {"y_true": [], "y_pred": []} for name in model_names}
        fold_details = []

        split_points = list(range(self.min_train_periods, n_obs - self.horizon + 1, self.step_size))
        # Ensure the final split point reaches the end of the series
        if split_points[-1] < n_obs - self.horizon:
            split_points.append(n_obs - self.horizon)

        fold_idx = 1
        for train_end in split_points:
            test_start = train_end
            test_end = train_end + self.horizon

            train_raw = raw_df.iloc[:train_end]
            test_raw = raw_df.iloc[test_start:test_end]

            y_train = train_raw["target"]
            y_test = test_raw["target"].values
            test_periods = test_raw["period"].tolist()

            # Corresponding feature slices for ML models
            # Note: feat_df starts 4 periods later due to lag_4 dropna
            # Match by period to prevent index mismatch
            train_periods_set = set(train_raw["period"])
            train_feat = feat_df[feat_df["period"].isin(train_periods_set)].copy()

            fold_preds = {}

            # 1. Baseline Models
            m_naive = NaiveForecast().fit(y_train)
            pred_naive = m_naive.predict(self.horizon)
            fold_results["Naive_Baseline"]["y_true"].extend(y_test)
            fold_results["Naive_Baseline"]["y_pred"].extend(pred_naive)
            fold_preds["Naive_Baseline"] = pred_naive.tolist()

            m_snaive = SeasonalNaiveForecast(season_length=4).fit(y_train)
            pred_snaive = m_snaive.predict(self.horizon)
            fold_results["Seasonal_Naive_Baseline"]["y_true"].extend(y_test)
            fold_results["Seasonal_Naive_Baseline"]["y_pred"].extend(pred_snaive)
            fold_preds["Seasonal_Naive_Baseline"] = pred_snaive.tolist()

            m_ma = MovingAverageForecast(window=4).fit(y_train)
            pred_ma = m_ma.predict(self.horizon)
            fold_results["Moving_Average_k4"]["y_true"].extend(y_test)
            fold_results["Moving_Average_k4"]["y_pred"].extend(pred_ma)
            fold_preds["Moving_Average_k4"] = pred_ma.tolist()

            m_lr = LinearRegressionBaseline().fit(y_train)
            pred_lr = m_lr.predict(self.horizon)
            fold_results["Linear_Regression_Baseline"]["y_true"].extend(y_test)
            fold_results["Linear_Regression_Baseline"]["y_pred"].extend(pred_lr)
            fold_preds["Linear_Regression_Baseline"] = pred_lr.tolist()

            # 2. Statistical Models
            m_arima = ARIMAForecaster(order=(1, 1, 1)).fit(y_train)
            pred_arima, _, _ = m_arima.predict(self.horizon)
            fold_results["ARIMA(1,1,1)"]["y_true"].extend(y_test)
            fold_results["ARIMA(1,1,1)"]["y_pred"].extend(pred_arima)
            fold_preds["ARIMA(1,1,1)"] = pred_arima.tolist()

            m_sarima = SARIMAForecaster(order=(1, 1, 1), seasonal_order=(1, 0, 0, 4)).fit(y_train)
            pred_sarima, _, _ = m_sarima.predict(self.horizon)
            fold_results["SARIMA(1,1,1)x(1,0,0)[4]"]["y_true"].extend(y_test)
            fold_results["SARIMA(1,1,1)x(1,0,0)[4]"]["y_pred"].extend(pred_sarima)
            fold_preds["SARIMA(1,1,1)x(1,0,0)[4]"] = pred_sarima.tolist()

            m_ses = ExponentialSmoothingForecaster().fit(y_train)
            pred_ses = m_ses.predict(self.horizon)
            fold_results["Simple_Exponential_Smoothing"]["y_true"].extend(y_test)
            fold_results["Simple_Exponential_Smoothing"]["y_pred"].extend(pred_ses)
            fold_preds["Simple_Exponential_Smoothing"] = pred_ses.tolist()

            m_hw = HoltWintersForecaster(seasonal_periods=4).fit(y_train)
            pred_hw = m_hw.predict(self.horizon)
            fold_results["Holt_Winters_Additive_s4"]["y_true"].extend(y_test)
            fold_results["Holt_Winters_Additive_s4"]["y_pred"].extend(pred_hw)
            fold_preds["Holt_Winters_Additive_s4"] = pred_hw.tolist()

            # 3. Machine Learning Models
            if len(train_feat) >= 12:
                m_rf = MLForecaster("RandomForest").fit(train_feat)
                pred_rf, _, _ = m_rf.predict_recursive(train_feat, horizon=self.horizon)
                fold_results["Random_Forest_Regressor"]["y_true"].extend(y_test)
                fold_results["Random_Forest_Regressor"]["y_pred"].extend(pred_rf)
                fold_preds["Random_Forest_Regressor"] = pred_rf.tolist()

                m_xgb = MLForecaster("XGBoost").fit(train_feat)
                pred_xgb, _, _ = m_xgb.predict_recursive(train_feat, horizon=self.horizon)
                fold_results["XGBoost_Regressor"]["y_true"].extend(y_test)
                fold_results["XGBoost_Regressor"]["y_pred"].extend(pred_xgb)
                fold_preds["XGBoost_Regressor"] = pred_xgb.tolist()

                m_gbm = MLForecaster("GradientBoosting").fit(train_feat)
                pred_gbm, _, _ = m_gbm.predict_recursive(train_feat, horizon=self.horizon)
                fold_results["Gradient_Boosting_Regressor"]["y_true"].extend(y_test)
                fold_results["Gradient_Boosting_Regressor"]["y_pred"].extend(pred_gbm)
                fold_preds["Gradient_Boosting_Regressor"] = pred_gbm.tolist()

            fold_details.append({
                "fold": fold_idx,
                "train_range": f"{train_raw['period'].iloc[0]} -> {train_raw['period'].iloc[-1]} ({len(train_raw)} qtrs)",
                "test_range": f"{test_periods[0]} -> {test_periods[-1]} ({len(test_periods)} qtrs)",
                "actuals": y_test.tolist()
            })
            fold_idx += 1

        # Calculate aggregated out-of-sample metrics across all folds
        summary_metrics = {}
        for name, data in fold_results.items():
            if len(data["y_true"]) > 0 and len(data["y_pred"]) == len(data["y_true"]):
                metrics = self.evaluator.calculate_metrics(data["y_true"], data["y_pred"])
                metrics["bias_assessment"] = self.evaluator.get_bias_assessment(metrics["bias_pct"])
                metrics["eval_observations"] = len(data["y_true"])
                summary_metrics[name] = metrics

        # Sort models by WAPE (lowest error first)
        ranked_models = sorted(summary_metrics.items(), key=lambda x: x[1]["wape_pct"])

        return {
            "folds_evaluated": len(fold_details),
            "fold_details": fold_details,
            "models_evaluated": len(summary_metrics),
            "model_performance": summary_metrics,
            "ranked_models": [{"model": k, **v} for k, v in ranked_models],
            "champion_model": ranked_models[0][0] if ranked_models else None,
            "champion_wape": ranked_models[0][1]["wape_pct"] if ranked_models else None
        }
