"""
ORBITALYTICS - Phase 1 Dataset Profiling & Readiness Runner
Profiles all validated datasets in datasets/validated/ and executes
the Forecasting Target Readiness Analyzer.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

import json
import pandas as pd
from modules.phase_1.dataset_profiler import DatasetProfiler
from modules.phase_1.forecasting_readiness_analyzer import ForecastingReadinessAnalyzer

def run_profiling():
    print("=" * 70)
    print("   ORBITALYTICS - PHASE 1: DATASET PROFILING & READINESS RUNNER")
    print("=" * 70)

    val_dir = BASE_DIR / "datasets" / "validated"
    profiler = DatasetProfiler(BASE_DIR / "datasets" / "profiling")
    readiness_analyzer = ForecastingReadinessAnalyzer(BASE_DIR / "datasets" / "metadata")

    files = sorted(val_dir.glob("*_validated.csv"))
    print(f"\n[INFO] Found {len(files)} validated datasets to profile...")

    for f in files:
        df = pd.read_csv(f, low_memory=False)
        d_name = f.stem.replace("_validated", "")
        p_res = profiler.profile_dataframe(df, d_name)
        print(f" -> Profiled {d_name:40s} | Rows: {p_res['row_count']:6d} | Cols: {p_res['column_count']:2d} | Size: {p_res['memory_usage_kb']:.1f} KB")

    # Forecasting Target Readiness
    print("\n--- Executing Forecasting Target Readiness Assessment ---")
    demand_f = val_dir / "equipment_component_demand_validated.csv"
    resource_f = val_dir / "resource_consumption_validated.csv"

    if demand_f.exists() and resource_f.exists():
        df_dem = pd.read_csv(demand_f, low_memory=False)
        df_res = pd.read_csv(resource_f, low_memory=False)
        r_audit = readiness_analyzer.run_full_readiness_audit(df_dem, df_res)
        print("Forecasting Target 1 (Equipment Demand):", r_audit["executive_summary"]["primary_target_1"][:80], "...")
        print("Forecasting Target 2 (Resource Consumption):", r_audit["executive_summary"]["primary_target_2"][:80], "...")
        print("Recommended Horizon:", r_audit["executive_summary"]["recommended_forecast_horizon"])

    print(f"\n[SUCCESS] Profiling and Forecasting Target Readiness Analysis Complete!\n")

if __name__ == "__main__":
    run_profiling()
