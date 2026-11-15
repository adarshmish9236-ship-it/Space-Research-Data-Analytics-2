"""
ORBITALYTICS Phase 10 — Benchmarking Service
Provides REST API access to Phase 10 empirical benchmarking results,
comparison matrices, scaling speedups, and system configurations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DOCS_PHASE10 = PROJECT_ROOT / "docs" / "phase_10"
RESULTS_DIR = DOCS_PHASE10 / "results"

RESULTS_MATRIX_CSV = RESULTS_DIR / "benchmark_results_matrix.csv"
SCALING_ANALYSIS_CSV = RESULTS_DIR / "scaling_analysis.csv"
SUMMARY_JSON = RESULTS_DIR / "engine_comparison_summary.json"
MANIFEST_JSON = RESULTS_DIR / "benchmark_manifest.json"


class BenchmarkingService:
    """Service providing benchmark analytics and comparison metrics."""

    def __init__(self):
        self.results_dir = RESULTS_DIR

    def get_summary(self) -> Dict[str, Any]:
        if SUMMARY_JSON.exists():
            with open(SUMMARY_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"error": "Benchmark summary not generated yet"}

    def get_manifest(self) -> Dict[str, Any]:
        if MANIFEST_JSON.exists():
            with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"error": "Benchmark manifest not generated yet"}

    def get_results_matrix(self) -> List[Dict[str, Any]]:
        if RESULTS_MATRIX_CSV.exists():
            df = pd.read_csv(RESULTS_MATRIX_CSV)
            return df.to_dict(orient="records")
        return []

    def get_scaling_analysis(self) -> List[Dict[str, Any]]:
        if SCALING_ANALYSIS_CSV.exists():
            df = pd.read_csv(SCALING_ANALYSIS_CSV)
            return df.to_dict(orient="records")
        return []
