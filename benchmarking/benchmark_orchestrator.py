"""
ORBITALYTICS Phase 10 — Master Benchmark Orchestrator
Coordinates execution and metric collection across all 5 data-processing systems:
  1. Local Python / Pandas (In-Memory Vectorized Baseline)
  2. Apache Spark / PySpark (Distributed In-Memory Cluster)
  3. Apache Hive (HiveQL / HiveServer2 on YARN)
  4. Hadoop MapReduce (Streaming Python on YARN)
  5. Apache Pig (Pig Latin on YARN)

Collects controlled measurements across 3 dataset tiers:
  - Small  (1x scale:  ~7,144 records, ~0.7 MB)
  - Medium (15x scale: ~107,160 records, ~10.5 MB)
  - Large  (60x scale: ~428,640 records, ~42.0 MB)

Generates standardized CSV matrices, JSON execution manifests, and scaling metrics.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DOCS_PHASE10 = PROJECT_ROOT / "docs" / "phase_10"
RESULTS_DIR = DOCS_PHASE10 / "results"
LOGS_DIR = DOCS_PHASE10 / "logs"

RESULTS_MATRIX_CSV = RESULTS_DIR / "benchmark_results_matrix.csv"
SCALING_ANALYSIS_CSV = RESULTS_DIR / "scaling_analysis.csv"
SUMMARY_JSON = RESULTS_DIR / "engine_comparison_summary.json"
MANIFEST_JSON = RESULTS_DIR / "benchmark_manifest.json"

from benchmarking.pandas_benchmark import PandasBenchmarkRunner
from benchmarking.spark_benchmark import SparkBenchmarkRunner
from benchmarking.hive_benchmark import HiveBenchmarkRunner
from benchmarking.mapreduce_benchmark import MapReduceBenchmarkRunner
from benchmarking.pig_benchmark import PigBenchmarkRunner


class BenchmarkOrchestrator:
    """Master controller executing multi-engine benchmarking suite."""

    def __init__(self):
        self.results_dir = RESULTS_DIR
        self.results_dir.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def run_all(self, engines: List[str] = None) -> Dict[str, Any]:
        if engines is None:
            engines = ["pandas", "spark", "hive", "mapreduce", "pig"]

        start_time = time.time()
        print("=" * 80)
        print("ORBITALYTICS PHASE 10: MASTER BENCHMARK ORCHESTRATION")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Engines to benchmark: {', '.join(engines).upper()}")
        print("=" * 80)

        all_records: List[Dict[str, Any]] = []

        # 1. Local Pandas
        if "pandas" in engines:
            try:
                p_runner = PandasBenchmarkRunner()
                p_res = p_runner.run_all_benchmarks(n_trials=3)
                all_records.extend(p_res)
            except Exception as e:
                print(f"[ERROR] Pandas benchmark failed: {e}")

        # 2. Apache Spark
        if "spark" in engines:
            try:
                s_runner = SparkBenchmarkRunner()
                s_res = s_runner.run_all_benchmarks()
                all_records.extend(s_res)
            except Exception as e:
                print(f"[ERROR] Spark benchmark failed: {e}")

        # 3. Apache Hive
        if "hive" in engines:
            try:
                h_runner = HiveBenchmarkRunner()
                h_res = h_runner.run_all_benchmarks(n_trials=3)
                all_records.extend(h_res)
            except Exception as e:
                print(f"[ERROR] Hive benchmark failed: {e}")

        # 4. Hadoop MapReduce
        if "mapreduce" in engines:
            try:
                mr_runner = MapReduceBenchmarkRunner()
                mr_res = mr_runner.run_all_benchmarks(n_trials=3)
                all_records.extend(mr_res)
            except Exception as e:
                print(f"[ERROR] MapReduce benchmark failed: {e}")

        # 5. Apache Pig
        if "pig" in engines:
            try:
                pig_runner = PigBenchmarkRunner()
                pig_res = pig_runner.run_all_benchmarks(n_trials=3)
                all_records.extend(pig_res)
            except Exception as e:
                print(f"[ERROR] Pig benchmark failed: {e}")

        elapsed_total = round(time.time() - start_time, 2)
        print(f"\n[ORCHESTRATOR] Benchmarks complete in {elapsed_total}s. Aggregating {len(all_records)} trial sets ...")

        # Create master DataFrame
        df_matrix = pd.DataFrame(all_records)
        df_matrix.to_csv(RESULTS_MATRIX_CSV, index=False)
        print(f"[SAVED] Results matrix written to: {RESULTS_MATRIX_CSV}")

        # Generate scaling analysis
        scaling_df = self._generate_scaling_analysis(df_matrix)
        scaling_df.to_csv(SCALING_ANALYSIS_CSV, index=False)
        print(f"[SAVED] Scaling analysis written to: {SCALING_ANALYSIS_CSV}")

        # Generate summary JSON
        summary = self._generate_summary(df_matrix, elapsed_total)
        with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"[SAVED] Summary JSON written to: {SUMMARY_JSON}")

        # Generate manifest
        manifest = self._generate_manifest(df_matrix, elapsed_total)
        with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"[SAVED] Manifest JSON written to: {MANIFEST_JSON}")

        return summary

    def _generate_scaling_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculates scaling speedup and time ratios from Small to Medium and Large."""
        rows = []
        for (engine, wl), group in df.groupby(["engine", "workload_id"]):
            s_row = group[group["scale_tier"] == "small"]
            m_row = group[group["scale_tier"] == "medium"]
            l_row = group[group["scale_tier"] == "large"]

            if not s_row.empty and not m_row.empty and not l_row.empty:
                t_s = s_row["warm_execution_time_seconds"].values[0]
                t_m = m_row["warm_execution_time_seconds"].values[0]
                t_l = l_row["warm_execution_time_seconds"].values[0]

                rec_s = s_row["input_records"].values[0]
                rec_m = m_row["input_records"].values[0]
                rec_l = l_row["input_records"].values[0]

                # Data scale multipliers
                data_mult_m = round(rec_m / max(rec_s, 1), 1)
                data_mult_l = round(rec_l / max(rec_s, 1), 1)

                # Time scale multipliers
                time_mult_m = round(t_m / max(t_s, 1e-4), 2)
                time_mult_l = round(t_l / max(t_s, 1e-4), 2)

                # Sub-linear scaling efficiency: ideal is 1.0; < 1.0 means super-efficient amortizing fixed cost
                scaling_efficiency_l = round((time_mult_l / data_mult_l) if data_mult_l > 0 else 1.0, 3)

                rows.append({
                    "engine": engine,
                    "workload_id": wl,
                    "small_time_sec": t_s,
                    "medium_time_sec": t_m,
                    "large_time_sec": t_l,
                    "data_growth_small_to_large": f"{data_mult_l}x",
                    "time_growth_small_to_large": f"{time_mult_l}x",
                    "scaling_overhead_ratio": scaling_efficiency_l,
                    "scaling_behavior": "Sub-linear (Fixed Overhead Amortized)" if scaling_efficiency_l < 0.5 else ("Linear" if scaling_efficiency_l <= 1.2 else "Super-linear (Bottlenecked)")
                })

        return pd.DataFrame(rows)

    def _generate_summary(self, df: pd.DataFrame, elapsed_total: float) -> Dict[str, Any]:
        engine_stats = {}
        for engine, group in df.groupby("engine"):
            engine_stats[engine] = {
                "workloads_tested": int(len(group)),
                "mean_cold_time_sec": round(float(group["cold_execution_time_seconds"].mean()), 3),
                "mean_warm_time_sec": round(float(group["warm_execution_time_seconds"].mean()), 3),
                "avg_throughput_records_per_sec": round(float(group["throughput_records_per_sec"].mean())),
                "avg_throughput_mb_per_sec": round(float(group["throughput_mb_per_sec"].mean()), 2),
                "avg_peak_memory_mb": round(float(group["peak_rss_memory_mb"].mean()), 1),
                "avg_cpu_time_sec": round(float(group["cpu_time_seconds"].mean()), 3),
                "total_shuffle_bytes": int(group["shuffle_bytes"].sum())
            }

        return {
            "orchestrator_version": "2.0.0",
            "phase": "Phase 10 — Big Data Performance Benchmarking",
            "timestamp": datetime.now().isoformat(),
            "total_orchestration_time_seconds": elapsed_total,
            "total_trials_evaluated": int(len(df)),
            "engine_summaries": engine_stats
        }

    def _generate_manifest(self, df: pd.DataFrame, elapsed_total: float) -> Dict[str, Any]:
        return {
            "project": "ORBITALYTICS 2.0",
            "phase": "Phase 10",
            "description": "Controlled Empirical Big Data Performance Benchmarking across Local Pandas, Spark, Hive, MapReduce, and Pig",
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "host_os": "Windows 11 Home (Build 26200)",
                "cpu_cores": 8,
                "ram_gb": 15.4,
                "docker_engine": "Docker Desktop Linux Containers (WSL2 backend)",
                "container_memory_limit_gib": 7.455,
                "hadoop_version": "Apache Hadoop 3.2.1",
                "spark_version": "Apache Spark 3.1.2",
                "hive_version": "Apache Hive 2.3.2",
                "pig_version": "Apache Pig 0.17.0",
                "python_version": "Python 3.14.0 (host) / Python 3.5.3 (containers)"
            },
            "scale_tiers": {
                "small": {"multiplier": "1x", "approx_records": 7144, "size_mb": 0.67},
                "medium": {"multiplier": "15x", "approx_records": 107160, "size_mb": 10.5},
                "large": {"multiplier": "60x", "approx_records": 428640, "size_mb": 42.0}
            },
            "workloads": [
                "WL1_EQUIPMENT_DEMAND",
                "WL2_RESOURCE_CONSUMPTION",
                "WL3_MISSIONS_BY_AGENCY",
                "WL4_MANUFACTURING_SUMMARY",
                "WL5_MULTI_DATASET_JOIN"
            ],
            "engines_evaluated": list(df["engine"].unique()),
            "total_benchmark_records": len(df),
            "artifacts_generated": [
                "docs/phase_10/results/benchmark_results_matrix.csv",
                "docs/phase_10/results/scaling_analysis.csv",
                "docs/phase_10/results/engine_comparison_summary.json",
                "docs/phase_10/results/benchmark_manifest.json"
            ]
        }


if __name__ == "__main__":
    orchestrator = BenchmarkOrchestrator()
    summary = orchestrator.run_all()
    print("\n[OK] Phase 10 Benchmarking Orchestration Finished.")
