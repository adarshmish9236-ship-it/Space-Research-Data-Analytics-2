"""
ORBITALYTICS Phase 10 — Spark Benchmark Runner
Coordinates execution of Spark workloads against the live Spark cluster,
extracts real execution metrics, and produces structured benchmark records.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPARK_JOB_LOCAL = PROJECT_ROOT / "benchmarking" / "spark_benchmark_job.py"
SPARK_CONTAINER = "spark-master"
SPARK_CONTAINER_PATH = "/opt/spark_benchmark_job.py"
SPARK_SUBMIT_PATH = "/spark/bin/spark-submit"


class SparkBenchmarkRunner:
    """Orchestrates Spark benchmarks on the cluster."""

    def __init__(self, master_url: str = "spark://spark-master:7077"):
        self.master_url = master_url

    def run_all_benchmarks(self) -> List[Dict[str, Any]]:
        print("\n" + "=" * 80)
        print("RUNNING ENGINE BENCHMARKS: APACHE SPARK (PYSPARK CLUSTER)")
        print("=" * 80)

        # 1. Sync script to spark-master container
        print(f"[SYNC] Copying {SPARK_JOB_LOCAL} to {SPARK_CONTAINER}:{SPARK_CONTAINER_PATH} ...")
        cmd_cp = f'docker cp "{SPARK_JOB_LOCAL}" {SPARK_CONTAINER}:{SPARK_CONTAINER_PATH}'
        cp_res = subprocess.run(cmd_cp, shell=True, capture_output=True, text=True)
        if cp_res.returncode != 0:
            raise RuntimeError(f"Failed to copy spark benchmark script: {cp_res.stderr}")

        # 2. Execute spark-submit inside container
        cmd_submit = (
            f'docker exec {SPARK_CONTAINER} {SPARK_SUBMIT_PATH} '
            f'--master {self.master_url} '
            f'--driver-memory 1024m '
            f'--executor-memory 1536m '
            f'{SPARK_CONTAINER_PATH}'
        )
        print(f"[EXEC] Running spark-submit on {SPARK_CONTAINER} ...")
        t0 = time.time()
        res = subprocess.run(cmd_submit, shell=True, capture_output=True, text=True)
        elapsed = round(time.time() - t0, 2)

        if res.returncode != 0:
            print(f"[ERROR] spark-submit failed (code {res.returncode}):\n{res.stderr}")
            raise RuntimeError(f"Spark benchmark execution failed: {res.stderr}")

        # 3. Parse JSON output
        stdout = res.stdout
        marker_start = "###BENCHMARK_RESULTS_JSON_START###"
        marker_end = "###BENCHMARK_RESULTS_JSON_END###"

        if marker_start in stdout and marker_end in stdout:
            json_str = stdout.split(marker_start)[1].split(marker_end)[0].strip()
            benchmark_data = json.loads(json_str)
            print(f"[SUCCESS] Spark benchmark completed in {elapsed}s ({len(benchmark_data)} workloads evaluated).")
            return benchmark_data
        else:
            print(f"[WARN] Marker not found in output. Full stdout:\n{stdout[-1000:]}")
            raise ValueError("Could not parse benchmark JSON output from Spark.")


if __name__ == "__main__":
    runner = SparkBenchmarkRunner()
    results = runner.run_all_benchmarks()
    print(f"Collected {len(results)} Spark benchmark results.")
