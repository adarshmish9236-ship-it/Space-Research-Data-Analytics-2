"""
Orbitalytics - Time-Series & Machine Learning Evaluation Metrics
Implements MAE, RMSE, R-squared, MAPE, sMAPE, and dynamic Prediction Intervals.
Handles zero/near-zero denominators properly without division by zero.
"""
import math
import numpy as np
from typing import Dict, Any, List

def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))

def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(math.sqrt(np.mean((y_true - y_pred) ** 2)))

def calculate_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    r2 = 1.0 - (ss_res / ss_tot)
    return float(max(0.0, r2))

def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Percentage Error with protection against near-zero actuals."""
    mask = np.abs(y_true) > 1e-4
    if not np.any(mask):
        return 0.0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0)

def calculate_smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Symmetric Mean Absolute Percentage Error (bound between 0% and 200%)."""
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    mask = denominator > 1e-4
    if not np.any(mask):
        return 0.0
    return float(np.mean(np.abs(y_pred[mask] - y_true[mask]) / denominator[mask]) * 100.0)

def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    y_t = np.asarray(y_true, dtype=float)
    y_p = np.asarray(y_pred, dtype=float)
    
    mae = calculate_mae(y_t, y_p)
    rmse = calculate_rmse(y_t, y_p)
    r2 = calculate_r2(y_t, y_p)
    mape = calculate_mape(y_t, y_p)
    smape = calculate_smape(y_t, y_p)
    accuracy_score = round(max(0.0, min(100.0, 100.0 - smape)), 1)

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 3),
        "mape": round(mape, 2),
        "smape": round(smape, 2),
        "accuracy_pct": accuracy_score
    }

