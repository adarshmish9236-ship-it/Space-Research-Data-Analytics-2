"""
ORBITALYTICS Phase 8 — Task 2: Baseline Forecasting Models
Implements:
  1. Naive Forecast: y_hat_{t+h} = y_t
  2. Seasonal Naive Forecast: y_hat_{t+h} = y_{t+h-m} (m=4 for quarterly)
  3. Moving Average Forecast: y_hat_{t+h} = (1/k) * sum_{i=0}^{k-1} y_{t-i} (k=4)
  4. Linear Regression Baseline: Ordinary Least Squares on time index
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional


class BaseForecaster:
    def __init__(self, name: str):
        self.name = name
        self.history = None
        self.fitted = False

    def fit(self, y: pd.Series):
        raise NotImplementedError

    def predict(self, horizon: int) -> np.ndarray:
        raise NotImplementedError


class NaiveForecast(BaseForecaster):
    """
    Naive (Random Walk) Forecast:
    Assumes future values equal the most recent observed value.
    """
    def __init__(self):
        super().__init__("Naive_Baseline")

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        self.last_value = self.history[-1] if len(self.history) > 0 else 0.0
        self.fitted = True
        return self

    def predict(self, horizon: int) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Model must be fitted before predict()")
        return np.full(horizon, self.last_value)


class SeasonalNaiveForecast(BaseForecaster):
    """
    Seasonal Naive Forecast:
    Forecasts equal the value from the corresponding season in the prior annual cycle (m=4 quarters).
    """
    def __init__(self, season_length: int = 4):
        super().__init__("Seasonal_Naive_Baseline")
        self.season_length = season_length

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        self.fitted = True
        return self

    def predict(self, horizon: int) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Model must be fitted before predict()")
        m = self.season_length
        if len(self.history) < m:
            # Fallback to naive if history is shorter than seasonal cycle
            return np.full(horizon, self.history[-1])

        last_cycle = self.history[-m:]
        preds = []
        for step in range(horizon):
            idx = step % m
            preds.append(last_cycle[idx])
        return np.array(preds)


class MovingAverageForecast(BaseForecaster):
    """
    Trailing Moving Average Forecast:
    Forecasts equal the arithmetic mean of the last k observed periods (default k=4).
    """
    def __init__(self, window: int = 4):
        super().__init__(f"Moving_Average_k{window}")
        self.window = window

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        k = min(self.window, len(self.history))
        self.ma_value = float(np.mean(self.history[-k:]))
        self.fitted = True
        return self

    def predict(self, horizon: int) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Model must be fitted before predict()")
        return np.full(horizon, self.ma_value)


class LinearRegressionBaseline(BaseForecaster):
    """
    Deterministic Linear Trend Baseline:
    y_hat_t = beta_0 + beta_1 * t
    """
    def __init__(self):
        super().__init__("Linear_Regression_Baseline")
        self.slope = 0.0
        self.intercept = 0.0
        self.n_obs = 0

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        self.n_obs = len(self.history)
        t = np.arange(self.n_obs)
        # OLS closed form: slope = cov(t, y)/var(t)
        t_mean = np.mean(t)
        y_mean = np.mean(self.history)
        denom = np.sum((t - t_mean) ** 2)
        if denom > 0:
            self.slope = float(np.sum((t - t_mean) * (self.history - y_mean)) / denom)
            self.intercept = float(y_mean - self.slope * t_mean)
        else:
            self.slope = 0.0
            self.intercept = float(y_mean)
        self.fitted = True
        return self

    def predict(self, horizon: int) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Model must be fitted before predict()")
        future_t = np.arange(self.n_obs, self.n_obs + horizon)
        preds = self.intercept + self.slope * future_t
        # Components and resource consumption are non-negative
        return np.maximum(0.0, preds)
