"""
ORBITALYTICS Phase 8 — Task 3: Statistical Time-Series Models
Implements:
  1. Auto/Standard ARIMA: Autoregressive Integrated Moving Average
  2. Seasonal ARIMA (SARIMA): ARIMA with quarterly seasonal lag (m=4)
  3. Simple Exponential Smoothing: Single parameter alpha smoothing
  4. Holt-Winters Exponential Smoothing: Level, trend, and seasonal components
"""

import warnings
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing


class ARIMAForecaster:
    """
    ARIMA(p, d, q) Forecaster:
    Captures temporal autoregression, differencing for stationarity, and moving average errors.
    """
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)):
        self.order = order
        self.name = f"ARIMA{order}"
        self.model_res = None
        self.history = None
        self.fitted = False

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = ARIMA(self.history, order=self.order)
                self.model_res = model.fit()
            self.fitted = True
        except Exception:
            # Fallback to simple differencing model if optimization fails
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = ARIMA(self.history, order=(1, 1, 0))
                    self.model_res = model.fit()
                self.fitted = True
            except Exception:
                self.fitted = False
        return self

    def predict(self, horizon: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns (forecast, lower_95, upper_95)
        """
        if not self.fitted or self.model_res is None:
            # Fallback to naive if fit failed
            last = self.history[-1] if len(self.history) > 0 else 0.0
            fc = np.full(horizon, last)
            return fc, fc * 0.8, fc * 1.2

        try:
            forecast_res = self.model_res.get_forecast(steps=horizon)
            fc = np.array(forecast_res.predicted_mean, dtype=float)
            conf = forecast_res.conf_int(alpha=0.05)
            lower = np.array(conf[:, 0], dtype=float)
            upper = np.array(conf[:, 1], dtype=float)

            last = self.history[-1] if len(self.history) > 0 else 100.0
            if np.any(np.isnan(fc)) or np.any(fc <= 0.0) or np.any(fc > last * 5.0):
                fc = np.full(horizon, last)
                lower = np.maximum(0.0, fc * 0.85)
                upper = fc * 1.15
            else:
                lower = np.maximum(0.0, lower)
            return fc, lower, upper
        except Exception:
            last = self.history[-1] if len(self.history) > 0 else 100.0
            fc = np.full(horizon, last)
            return fc, np.maximum(0.0, fc * 0.8), fc * 1.2


class SARIMAForecaster:
    """
    Seasonal ARIMA(p, d, q)x(P, D, Q)[s] Forecaster:
    Specifically models annual quarterly cycles (s=4).
    """
    def __init__(self, order=(1, 1, 1), seasonal_order=(1, 0, 0, 4)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.name = f"SARIMA{order}x{seasonal_order[:3]}[{seasonal_order[3]}]"
        self.model_res = None
        self.history = None
        self.fitted = False

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = SARIMAX(
                    self.history,
                    order=self.order,
                    seasonal_order=self.seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )
                self.model_res = model.fit(disp=False, maxiter=50)
            self.fitted = True
        except Exception:
            # Fallback to ARIMA without seasonal if SARIMAX fails to converge
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = ARIMA(self.history, order=self.order)
                    self.model_res = model.fit()
                self.fitted = True
            except Exception:
                self.fitted = False
        return self

    def predict(self, horizon: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if not self.fitted or self.model_res is None:
            last = self.history[-1] if len(self.history) > 0 else 0.0
            fc = np.full(horizon, last)
            return fc, fc * 0.8, fc * 1.2

        try:
            forecast_res = self.model_res.get_forecast(steps=horizon)
            fc = np.array(forecast_res.predicted_mean, dtype=float)
            conf = forecast_res.conf_int(alpha=0.05)
            lower = np.array(conf[:, 0], dtype=float)
            upper = np.array(conf[:, 1], dtype=float)

            last = self.history[-1] if len(self.history) > 0 else 100.0
            if np.any(np.isnan(fc)) or np.any(fc <= 0.0) or np.any(fc > last * 5.0):
                # Fallback to seasonal naive
                fc = np.array([self.history[-4 + (i % 4)] if len(self.history) >= 4 else last for i in range(horizon)])
                lower = np.maximum(0.0, fc * 0.85)
                upper = fc * 1.15
            else:
                lower = np.maximum(0.0, lower)
            return fc, lower, upper
        except Exception:
            last = self.history[-1] if len(self.history) > 0 else 100.0
            fc = np.full(horizon, last)
            return fc, np.maximum(0.0, fc * 0.8), fc * 1.2


class ExponentialSmoothingForecaster:
    """
    Simple Exponential Smoothing (SES) for series with level and no obvious trend.
    """
    def __init__(self):
        self.name = "Simple_Exponential_Smoothing"
        self.model_res = None
        self.history = None
        self.fitted = False

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = SimpleExpSmoothing(self.history, initialization_method="estimated")
                self.model_res = model.fit()
            self.fitted = True
        except Exception:
            self.fitted = False
        return self

    def predict(self, horizon: int) -> np.ndarray:
        if not self.fitted or self.model_res is None:
            return np.full(horizon, self.history[-1])
        try:
            preds = self.model_res.forecast(horizon)
            return np.maximum(0.0, np.array(preds))
        except Exception:
            return np.full(horizon, self.history[-1])


class HoltWintersForecaster:
    """
    Triple Exponential Smoothing (Holt-Winters):
    Models Level, Trend (additive), and Seasonality (additive, cycle=4).
    """
    def __init__(self, seasonal_periods: int = 4):
        self.seasonal_periods = seasonal_periods
        self.name = f"Holt_Winters_Additive_s{seasonal_periods}"
        self.model_res = None
        self.history = None
        self.fitted = False

    def fit(self, y: pd.Series):
        self.history = np.array(y, dtype=float)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Need at least 2 full seasonal cycles (8 periods)
                if len(self.history) >= 2 * self.seasonal_periods:
                    model = ExponentialSmoothing(
                        self.history,
                        trend="add",
                        seasonal="add",
                        seasonal_periods=self.seasonal_periods,
                        initialization_method="estimated"
                    )
                else:
                    # Fallback to Holt's Linear (level + trend only)
                    model = ExponentialSmoothing(
                        self.history,
                        trend="add",
                        seasonal=None,
                        initialization_method="estimated"
                    )
                self.model_res = model.fit(damping_trend=False)
            self.fitted = True
        except Exception:
            # Fallback to simple exponential smoothing
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = SimpleExpSmoothing(self.history, initialization_method="estimated")
                    self.model_res = model.fit()
                self.fitted = True
            except Exception:
                self.fitted = False
        return self

    def predict(self, horizon: int) -> np.ndarray:
        if not self.fitted or self.model_res is None:
            return np.full(horizon, self.history[-1])
        try:
            preds = self.model_res.forecast(horizon)
            return np.maximum(0.0, np.array(preds))
        except Exception:
            return np.full(horizon, self.history[-1])
