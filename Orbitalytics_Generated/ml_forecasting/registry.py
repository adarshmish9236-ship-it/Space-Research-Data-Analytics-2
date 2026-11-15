"""
ORBITALYTICS Phase 8 — Task 10: Model Registry & Drift Monitoring Architecture
Implements:
  - Central Model Registry with metadata versioning
  - In-memory and JSON persistence
  - Statistical Drift Monitoring protocol (Kolmogorov-Smirnov feature drift & Tracking Signal residual drift)
"""

import os
import json
import joblib
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from scipy.stats import ks_2samp

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DIR = PROJECT_ROOT / "docs" / "phase_8"
REGISTRY_FILE = REGISTRY_DIR / "model_registry.json"
MODELS_DIR = PROJECT_ROOT / "ml_forecasting" / "saved_models"


class ModelRegistry:
    def __init__(self):
        REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        self.registry_file = REGISTRY_FILE
        self.models_dir = MODELS_DIR
        self.registry_data = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "registry_version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "models": {}
        }

    def register_model(self,
                       model_id: str,
                       target_domain: str,
                       target_name: str,
                       model_family: str,
                       model_name: str,
                       version: str,
                       hyperparams: Dict[str, Any],
                       metrics: Dict[str, Any],
                       feature_importances: Optional[Dict[str, float]] = None,
                       model_obj: Any = None) -> Dict[str, Any]:
        """Registers a model with versioned metadata and optionally saves serialized artifact."""
        artifact_path = None
        if model_obj is not None:
            filename = f"{model_id}_{version}.joblib"
            artifact_file = self.models_dir / filename
            try:
                joblib.dump(model_obj, artifact_file)
                artifact_path = str(artifact_file)
            except Exception:
                artifact_path = None

        record = {
            "model_id": model_id,
            "target_domain": target_domain,
            "target_name": target_name,
            "model_family": model_family,
            "model_name": model_name,
            "version": version,
            "status": "ACTIVE",
            "registered_at": datetime.now().isoformat(),
            "hyperparameters": hyperparams,
            "evaluation_metrics": metrics,
            "feature_importances": feature_importances or {},
            "artifact_path": artifact_path,
            "drift_monitoring": {
                "input_drift_method": "Kolmogorov-Smirnov (KS-test alpha=0.05)",
                "concept_drift_method": "Cumulative Tracking Signal (threshold=+/-4.0 MAD)",
                "status": "HEALTHY",
                "last_drift_check": datetime.now().isoformat()
            }
        }

        self.registry_data["models"][model_id] = record
        self.registry_data["last_updated"] = datetime.now().isoformat()
        self._save_registry()
        return record

    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        return self.registry_data["models"].get(model_id)

    def list_models(self) -> List[Dict[str, Any]]:
        return list(self.registry_data["models"].values())

    def _save_registry(self):
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.registry_data, f, indent=2)

    @staticmethod
    def assess_input_drift(baseline_samples: np.ndarray, current_samples: np.ndarray) -> Dict[str, Any]:
        """Performs two-sample Kolmogorov-Smirnov test to detect covariate/input distribution shift."""
        if len(baseline_samples) < 5 or len(current_samples) < 5:
            return {"drift_detected": False, "p_value": 1.0, "ks_stat": 0.0, "note": "Insufficient sample size"}
        stat, p_val = ks_2samp(baseline_samples, current_samples)
        drift = p_val < 0.05
        return {
            "drift_detected": bool(drift),
            "p_value": round(float(p_val), 5),
            "ks_statistic": round(float(stat), 5),
            "threshold_alpha": 0.05,
            "interpretation": "STATISTICALLY_SIGNIFICANT_DRIFT" if drift else "NO_DRIFT_DETECTED"
        }

    @staticmethod
    def assess_concept_drift(residuals: np.ndarray) -> Dict[str, Any]:
        """Calculates Tracking Signal (cumulative error / Mean Absolute Deviation)."""
        if len(residuals) == 0:
            return {"drift_detected": False, "tracking_signal": 0.0}
        cum_error = float(np.sum(residuals))
        mad = float(np.mean(np.abs(residuals)))
        ts = round(cum_error / mad, 2) if mad > 0 else 0.0
        drift = abs(ts) > 4.0
        return {
            "drift_detected": bool(drift),
            "tracking_signal": ts,
            "threshold_critical": 4.0,
            "interpretation": "PERSISTENT_BIAS_DRIFT" if drift else "STABLE_STOCHASTIC_ERRORS"
        }
