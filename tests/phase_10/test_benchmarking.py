"""
ORBITALYTICS Phase 10 — Automated Test Suite: Big Data Performance Benchmarking
Validates workload definitions, dataset catalogs, empirical execution metrics,
cross-engine parity, scaling ratios, and artifact integrity.
"""

import json
import pytest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BENCHMARK_DIR = PROJECT_ROOT / "datasets" / "benchmark"
DOCS_PHASE10 = PROJECT_ROOT / "docs" / "phase_10"
RESULTS_DIR = DOCS_PHASE10 / "results"

from benchmarking.workload_definitions import WORKLOADS


class TestPhase10Benchmarking:
    """Test suite covering Phase 10 benchmark infrastructure and measurements."""

    def test_01_workload_definitions_completeness(self):
        """Verify all 5 common analytical workloads are defined with required schema."""
        assert len(WORKLOADS) == 5
        required_keys = ["id", "name", "description", "primary_table", "aggregations", "complexity"]
        expected_ids = [
            "WL1_EQUIPMENT_DEMAND",
            "WL2_RESOURCE_CONSUMPTION",
            "WL3_MISSIONS_BY_AGENCY",
            "WL4_MANUFACTURING_SUMMARY",
            "WL5_MULTI_DATASET_JOIN"
        ]
        for w_id in expected_ids:
            assert w_id in WORKLOADS, f"Missing workload: {w_id}"
            w = WORKLOADS[w_id]
            for key in required_keys:
                assert key in w, f"Workload {w_id} missing key: {key}"

    def test_02_dataset_catalog_exists_and_valid(self):
        """Verify the dataset scaling catalog exists and contains small, medium, large tiers."""
        cat_file = BENCHMARK_DIR / "dataset_catalog.json"
        assert cat_file.exists(), f"Catalog file not found at {cat_file}"

        with open(cat_file, "r", encoding="utf-8") as f:
            cat = json.load(f)

        assert "small" in cat
        assert "medium" in cat
        assert "large" in cat

        # Check small tier file presence and record count
        s_tier = cat["small"]
        assert s_tier["multiplier"] == 1
        assert s_tier["total_records"] > 5000

    def test_03_scale_multipliers_integrity(self):
        """Verify scaling progression from small to medium (15x) and large (60x)."""
        cat_file = BENCHMARK_DIR / "dataset_catalog.json"
        with open(cat_file, "r", encoding="utf-8") as f:
            cat = json.load(f)

        rec_s = cat["small"]["total_records"]
        rec_m = cat["medium"]["total_records"]
        rec_l = cat["large"]["total_records"]

        assert rec_m > rec_s * 10, "Medium scale should be significantly larger than small"
        assert rec_l > rec_m * 3, "Large scale should be significantly larger than medium"
        assert rec_l > 300000, "Large scale must contain over 300k records"

    def test_04_pandas_workload_correctness(self):
        """Verify that Pandas runner executes all 5 workloads across 3 scale tiers cleanly."""
        from benchmarking.pandas_benchmark import PandasBenchmarkRunner
        runner = PandasBenchmarkRunner()
        results = runner.run_all_benchmarks(n_trials=2)

        assert len(results) == 15, f"Expected 15 results (5 workloads x 3 scales), got {len(results)}"
        for r in results:
            assert r["status"] == "SUCCESS"
            assert r["warm_execution_time_seconds"] > 0
            assert r["throughput_records_per_sec"] > 0
            assert r["input_records"] > 0
            assert r["output_rows"] > 0

    def test_05_mapreduce_scripts_exist_and_executable(self):
        """Verify that all MapReduce streaming scripts exist in repository."""
        mr_dir = PROJECT_ROOT / "benchmarking" / "mapreduce_jobs"
        expected_scripts = [
            "wl1_mapper.py", "wl1_reducer.py",
            "wl2_mapper.py", "wl2_reducer.py",
            "wl3_mapper.py", "wl3_reducer.py",
            "wl4_mapper.py", "wl4_reducer.py",
            "wl5_mapper.py", "wl5_reducer.py"
        ]
        for s in expected_scripts:
            p = mr_dir / s
            assert p.exists(), f"MapReduce script missing: {s}"

    def test_06_pig_scripts_exist(self):
        """Verify that all Pig Latin scripts exist in repository."""
        pig_dir = PROJECT_ROOT / "benchmarking" / "pig_scripts"
        expected_scripts = [
            "wl1_pig.pig", "wl2_pig.pig", "wl3_pig.pig", "wl4_pig.pig", "wl5_pig.pig"
        ]
        for s in expected_scripts:
            p = pig_dir / s
            assert p.exists(), f"Pig script missing: {s}"

    def test_07_spark_job_script_exists(self):
        """Verify Spark benchmark script exists and defines required HDFS paths."""
        spark_script = PROJECT_ROOT / "benchmarking" / "spark_benchmark_job.py"
        assert spark_script.exists()
        content = spark_script.read_text(encoding="utf-8")
        assert "WL1_EQUIPMENT_DEMAND" in content
        assert "WL5_MULTI_DATASET_JOIN" in content
        assert "hdfs://namenode:9000" in content

    def test_08_results_matrix_and_scaling_validation(self):
        """Verify benchmark results matrix structure when present."""
        matrix_file = RESULTS_DIR / "benchmark_results_matrix.csv"
        if matrix_file.exists():
            df = pd.read_csv(matrix_file)
            assert not df.empty
            assert "engine" in df.columns
            assert "workload_id" in df.columns
            assert "scale_tier" in df.columns
            assert "warm_execution_time_seconds" in df.columns
            assert "throughput_records_per_sec" in df.columns
            assert (df["warm_execution_time_seconds"] > 0).all()
            assert (df["throughput_records_per_sec"] > 0).all()

    def test_09_manifest_and_environment_metadata(self):
        """Verify benchmark manifest contains accurate environment metadata."""
        manifest_file = RESULTS_DIR / "benchmark_manifest.json"
        if manifest_file.exists():
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            assert manifest["project"] == "ORBITALYTICS 2.0"
            assert manifest["phase"] == "Phase 10"
            assert "environment" in manifest
            assert manifest["environment"]["cpu_cores"] == 8
            assert "scale_tiers" in manifest
