"""
ORBITALYTICS Phase 7 — Automated Verification Test Suite
Validates Apache Spark & PySpark Analytics Layer, Multi-Dataset Integration,
Time-Series Feature Engineering, HDFS Gold Parquet Datasets, and Spark SQL Execution.
"""

import os
import json
import pytest
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_PHASE7 = PROJECT_ROOT / "docs" / "phase_7"
MANIFEST_FILE = DOCS_PHASE7 / "phase7_execution_manifest.json"


def run_docker_cmd(cmd):
    """Run command on docker and return returncode, stdout, stderr."""
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout, res.stderr


def test_phase7_execution_manifest():
    """Verify all 4 PySpark jobs executed successfully in the master manifest."""
    assert MANIFEST_FILE.exists(), f"Phase 7 manifest not found: {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("phase") == 7, "Manifest phase identifier mismatch"
    assert data.get("total_jobs") == 4, f"Expected 4 jobs, got {data.get('total_jobs')}"
    assert data.get("successful_jobs") == 4, f"Expected 4 successful jobs, got {data.get('successful_jobs')}"

    jobs = data.get("jobs", [])
    assert len(jobs) == 4, f"Expected 4 job entries, got {len(jobs)}"
    for j in jobs:
        assert j["status"] == "SUCCESS", f"Job {j['job_id']} ({j['job_name']}) failed with exit code {j['exit_code']}"
        assert j["exit_code"] == 0
        assert os.path.exists(j["log_file"]), f"Log file missing: {j['log_file']}"
        assert os.path.getsize(j["log_file"]) > 0, f"Log file empty: {j['log_file']}"


def test_gold_datasets_in_hdfs():
    """Verify all required Gold Parquet datasets are persisted in HDFS with partitions and success markers."""
    gold_paths = [
        "/orbitalytics/gold/demand_analytics/annual_equipment_demand_trend",
        "/orbitalytics/gold/demand_analytics/component_demand_summary",
        "/orbitalytics/gold/resource_analytics/annual_resource_consumption_trend",
        "/orbitalytics/gold/mission_analytics/annual_launch_trends",
        "/orbitalytics/gold/research_analytics/annual_research_investment",
        "/orbitalytics/gold/forecast_features/equipment_demand_features",
        "/orbitalytics/gold/forecast_features/train_dataset",
        "/orbitalytics/gold/forecast_features/test_dataset",
    ]

    for p in gold_paths:
        code, stdout, _ = run_docker_cmd(f"docker exec hadoop-namenode hdfs dfs -test -e {p}")
        assert code == 0, f"Gold dataset path does not exist in HDFS: {p}"

        code, stdout, _ = run_docker_cmd(f"docker exec hadoop-namenode hdfs dfs -ls -R {p}")
        assert code == 0, f"Failed to list Gold dataset: {p}"
        assert "_SUCCESS" in stdout or "part-" in stdout, f"Gold dataset has no partition or part files: {p}"


def test_feature_engineering_integrity():
    """Verify feature dataset records, temporal split proportions, and feature dimensions."""
    # Check log for feature engineering job
    feat_log = DOCS_PHASE7 / "logs" / "03_Time-Series_Feature_Engineering_Pipeline.log"
    assert feat_log.exists(), f"Feature log missing: {feat_log}"

    content = feat_log.read_text(encoding="utf-8")
    assert "Training observations: 728" in content, "Expected 728 training observations"
    assert "Test observations:     168" in content, "Expected 168 test observations"
    assert "Train ratio: 81.2%" in content, "Expected ~81.2% train ratio"
    assert "Total features: 24" in content, "Expected 24 engineered features"

    # Assert no future leakage features
    expected_features = [
        "lag_1_units", "lag_2_units", "lag_3_units", "lag_4_units",
        "rolling_3yr_mean", "rolling_3yr_std", "yoy_growth_pct",
        "prev_yr_mission_count", "prev_yr_launch_count", "prev_yr_satellite_deploy_count"
    ]
    for feat in expected_features:
        assert feat in content, f"Missing expected feature: {feat}"


def test_spark_sql_execution():
    """Verify Spark SQL query execution and metrics."""
    code, stdout, _ = run_docker_cmd("docker exec spark-master cat /tmp/phase7_sparksql_manifest.json")
    assert code == 0, "Spark SQL manifest missing in spark-master container"
    manifest = json.loads(stdout)
    assert manifest.get("queries_executed") >= 6, "Expected at least 6 Spark SQL queries executed"
    for r in manifest.get("results", []):
        assert r["rows"] > 0, f"Spark SQL query {r['query']} returned 0 rows"
        assert r["time_s"] >= 0.0
