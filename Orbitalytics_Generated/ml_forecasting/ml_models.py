"""
ORBITALYTICS Phase 8 — Task 4: Machine Learning Forecasting Models
Implements:
  1. Random Forest Regressor (ensemble bagged decision trees)
  2. XGBoost Regressor (extreme gradient boosted trees)
  3. Gradient Boosting Regressor (stochastic gradient boosting)
  4. Recursive Multi-Step Auto-Regressive Forecasting Engine
  5. Feature Importance Extraction & Empirical Prediction Intervals
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb

FEATURE_COLS = [
    "time_index", "sin_q", "cos_q", "q_1", "q_2", "q_3", "q_4",
    "lag_1", "lag_2", "lag_3", "lag_4",
    "rolling_mean_4", "rolling_std_4", "rolling_mean_2",
    "seasonal_lag_4", "prior_growth_rate"
]


class MLForecaster:
    def __init__(self, model_type: str = "RandomForest", **hyperparams):
        self.model_type = model_type
        self.hyperparams = hyperparams
        self.feature_cols = FEATURE_COLS
        self.model = None
        self.fitted = False
        self.residual_std = 1.0
        self.feature_importances_dict = {}

        if model_type == "RandomForest":
            self.name = "Random_Forest_Regressor"
            self.model = RandomForestRegressor(
                n_estimators=hyperparams.get("n_estimators", 150),
                max_depth=hyperparams.get("max_depth", 6),
                min_samples_split=hyperparams.get("min_samples_split", 3),
                random_state=42
            )
        elif model_type == "XGBoost":
            self.name = "XGBoost_Regressor"
            self.model = xgb.XGBRegressor(
                n_estimators=hyperparams.get("n_estimators", 120),
                max_depth=hyperparams.get("max_depth", 4),
                learning_rate=hyperparams.get("learning_rate", 0.05),
                subsample=hyperparams.get("subsample", 0.85),
                colsample_bytree=hyperparams.get("colsample_bytree", 0.85),
                random_state=42,
                verbosity=0
            )
        elif model_type == "GradientBoosting":
            self.name = "Gradient_Boosting_Regressor"
            self.model = GradientBoostingRegressor(
                n_estimators=hyperparams.get("n_estimators", 120),
                max_depth=hyperparams.get("max_depth", 4),
                learning_rate=hyperparams.get("learning_rate", 0.05),
                random_state=42
            )
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")

    def fit(self, train_df: pd.DataFrame):
        """Fits model on feature matrix and calculates training residual standard error."""
        X = train_df[self.feature_cols]
        y = train_df["target"]

        self.model.fit(X, y)
        self.fitted = True

        # Compute in-sample residuals for prediction interval estimation
        preds_train = self.model.predict(X)
        residuals = y.values - preds_train
        self.residual_std = max(1.0, float(np.std(residuals)))

        # Extract feature importances
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
            total = np.sum(importances)
            norm_imp = importances / total if total > 0 else importances
            self.feature_importances_dict = {
                col: round(float(val) * 100.0, 2)
                for col, val in sorted(zip(self.feature_cols, norm_imp), key=lambda x: x[1], reverse=True)
            }
        return self

    def predict_recursive(self, history_df: pd.DataFrame, horizon: int = 4) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Executes multi-step recursive forecasting:
        At each step h:
          1. Constructs the feature vector using predicted prior values
          2. Predicts point forecast y_hat_{t+h}
          3. Dynamically updates lag and rolling statistics
          4. Computes 80% and 95% confidence bounds
        """
        if not self.fitted:
            raise RuntimeError("Model must be fitted before predict()")

        curr = history_df.copy().reset_index(drop=True)
        forecasts = []
        lower_95 = []
        upper_95 = []

        last_idx = int(curr["time_index"].iloc[-1])
        last_year = int(curr["year"].iloc[-1])
        last_q = int(curr["quarter"].iloc[-1])

        # Historical tail values for recursive state
        hist_targets = list(curr["target"].values)

        for step in range(1, horizon + 1):
            next_idx = last_idx + step
            # Calculate next calendar quarter
            total_q = (last_year * 4 + (last_q - 1)) + step
            next_year = total_q // 4
            next_q = (total_q % 4) + 1

            # Build feature vector
            sin_q = np.sin(2 * np.pi * next_q / 4.0)
            cos_q = np.cos(2 * np.pi * next_q / 4.0)
            q_indicators = {f"q_{q}": 1 if next_q == q else 0 for q in [1, 2, 3, 4]}

            l1 = hist_targets[-1]
            l2 = hist_targets[-2] if len(hist_targets) >= 2 else l1
            l3 = hist_targets[-3] if len(hist_targets) >= 3 else l2
            l4 = hist_targets[-4] if len(hist_targets) >= 4 else l3

            rm4 = float(np.mean(hist_targets[-4:]))
            rstd4 = float(np.std(hist_targets[-4:])) if len(hist_targets) >= 4 else 1.0
            rm2 = float(np.mean(hist_targets[-2:]))
            s_lag4 = hist_targets[-4] if len(hist_targets) >= 4 else l1
            growth = (l1 - l2) / l2 if l2 > 0 else 0.0

            row_dict = {
                "time_index": next_idx,
                "sin_q": sin_q,
                "cos_q": cos_q,
                **q_indicators,
                "lag_1": l1,
                "lag_2": l2,
                "lag_3": l3,
                "lag_4": l4,
                "rolling_mean_4": rm4,
                "rolling_std_4": rstd4,
                "rolling_mean_2": rm2,
                "seasonal_lag_4": s_lag4,
                "prior_growth_rate": growth
            }

            X_step = pd.DataFrame([row_dict])[self.feature_cols]
            pred = float(self.model.predict(X_step)[0])
            pred = max(0.0, pred)
            forecasts.append(pred)

            # Prediction intervals widen with horizon: sigma_h = sigma * sqrt(1 + (h-1)/4)
            h_expansion = math.sqrt(1.0 + (step - 1) * 0.25)
            z_95 = 1.96
            margin = z_95 * self.residual_std * h_expansion
            lower_95.append(max(0.0, pred - margin))
            upper_95.append(pred + margin)

            # Append prediction to history for next recursive steps
            hist_targets.append(pred)

        return np.array(forecasts), np.array(lower_95), np.array(upper_95)

    def get_feature_importances(self) -> Dict[str, float]:
        """Returns top feature importances."""
        return self.feature_importances_dict
