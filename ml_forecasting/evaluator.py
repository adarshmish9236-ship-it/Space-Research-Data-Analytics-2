"""
ORBITALYTICS Phase 8 — Task 7: Comprehensive Forecasting Metrics Evaluator
Calculates:
  - MAE: Mean Absolute Error
  - RMSE: Root Mean Squared Error
  - WAPE: Weighted Absolute Percentage Error (sum|e| / sum(y) * 100)
  - MAPE: Mean Absolute Percentage Error (with near-zero safeguard)
  - Forecast Bias: Mean Error / Total Demand Ratio (identifies over/under forecasting)
  - R-squared (R²): Explained variance ratio

Documents metric limits when actuals approach zero.
"""

import math
import numpy as np
from typing import Dict, Any, List, Union


class ForecastEvaluator:
    @staticmethod
    def calculate_metrics(y_true: Union[np.ndarray, List[float]],
                          y_pred: Union[np.ndarray, List[float]]) -> Dict[str, float]:
        """
        Computes the complete suite of accuracy, error, and bias metrics.
        """
        y_t = np.array(y_true, dtype=float)
        y_p = np.array(y_pred, dtype=float)

        if len(y_t) == 0 or len(y_p) == 0 or len(y_t) != len(y_p):
            raise ValueError(f"Arrays must be non-empty and of equal length. Got {len(y_t)} and {len(y_p)}")

        n = len(y_t)
        errors = y_p - y_t
        abs_errors = np.abs(errors)
        sq_errors = errors ** 2

        # 1. MAE
        mae = float(np.mean(abs_errors))

        # 2. RMSE
        rmse = float(math.sqrt(np.mean(sq_errors)))

        # 3. WAPE (Weighted Absolute Percentage Error)
        sum_actuals = float(np.sum(y_t))
        sum_abs_errors = float(np.sum(abs_errors))
        if sum_actuals > 0:
            wape = float((sum_abs_errors / sum_actuals) * 100.0)
        else:
            wape = 0.0 if sum_abs_errors == 0 else 100.0

        # 4. MAPE (Mean Absolute Percentage Error) with safety epsilon
        # For actuals close to zero, MAPE explodes; we use max(actual, 1.0)
        safe_actuals = np.maximum(y_t, 1.0)
        mape = float(np.mean(abs_errors / safe_actuals) * 100.0)

        # 5. Forecast Bias (Tracking Signal / Mean Percentage Error)
        # Positive = Over-forecasting (excess supply), Negative = Under-forecasting (shortage risk)
        sum_errors = float(np.sum(errors))
        if sum_actuals > 0:
            bias_pct = float((sum_errors / sum_actuals) * 100.0)
        else:
            bias_pct = 0.0

        # 6. R-squared (R²)
        y_mean = np.mean(y_t)
        ss_tot = np.sum((y_t - y_mean) ** 2)
        ss_res = np.sum(sq_errors)
        if ss_tot > 0:
            r2 = float(max(-1.0, 1.0 - (ss_res / ss_tot)))
        else:
            r2 = 1.0 if ss_res == 0 else 0.0

        return {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "wape_pct": round(wape, 2),
            "mape_pct": round(mape, 2),
            "bias_pct": round(bias_pct, 2),
            "r2": round(r2, 4)
        }

    @staticmethod
    def get_bias_assessment(bias_pct: float) -> str:
        """Translates numeric bias percentage into operational risk assessment."""
        if bias_pct > 15.0:
            return "SEVERE_OVERFORECAST (High Capital Tie-Up & Inventory Storage Risk)"
        elif bias_pct > 5.0:
            return "MODERATE_OVERFORECAST (Slight Surplus Buffer)"
        elif bias_pct < -15.0:
            return "SEVERE_UNDERFORECAST (Critical Stockout & Mission Disruption Risk)"
        elif bias_pct < -5.0:
            return "MODERATE_UNDERFORECAST (Potential Supply Chain Strain)"
        else:
            return "BALANCED (Within +/-5% Variance Tolerance)"
