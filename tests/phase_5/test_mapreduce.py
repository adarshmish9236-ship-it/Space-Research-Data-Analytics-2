"""
ORBITALYTICS Phase 5 — Automated Integration Test Suite
Validates Hadoop Streaming MapReduce Pipelines, YARN Execution, and HDFS Gold Marts.
"""

import os
import json
import pytest
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAPREDUCE_DIR = os.path.join(PROJECT_ROOT, "mapreduce")
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "docs", "phase_5", "mapreduce_execution_manifest.json")
DOCKER_CONTAINER = "hadoop-namenode"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

def test_mapreduce_scripts_exist():
    """Verify all 7 mappers, 7 reducers, 2 combiners, and execution scripts exist."""
    expected_mappers = [
        "01_equipment_demand_mapper.py",
        "02_resource_consumption_mapper.py",
        "03_missions_mapper.py",
        "04_satellites_mapper.py",
        "05_launches_mapper.py",
        "06_manufacturing_mapper.py",
        "07_research_investment_mapper.py",
    ]
    expected_reducers = [
        "01_equipment_demand_reducer.py",
        "02_resource_consumption_reducer.py",
        "03_missions_reducer.py",
        "04_satellites_reducer.py",
        "05_launches_reducer.py",
        "06_manufacturing_reducer.py",
        "07_research_investment_reducer.py",
    ]
    expected_combiners = [
        "01_equipment_demand_combiner.py",
        "05_launches_combiner.py",
    ]

    for m in expected_mappers:
        p = os.path.join(MAPREDUCE_DIR, "mappers", m)
        assert os.path.exists(p), f"Mapper missing: {p}"
        assert os.path.getsize(p) > 0, f"Mapper empty: {p}"

    for r in expected_reducers:
        p = os.path.join(MAPREDUCE_DIR, "reducers", r)
        assert os.path.exists(p), f"Reducer missing: {p}"
        assert os.path.getsize(p) > 0, f"Reducer empty: {p}"

    for c in expected_combiners:
        p = os.path.join(MAPREDUCE_DIR, "combiners", c)
        assert os.path.exists(p), f"Combiner missing: {p}"
        assert os.path.getsize(p) > 0, f"Combiner empty: {p}"

    runner = os.path.join(MAPREDUCE_DIR, "run_mapreduce_job.sh")
    orchestrator = os.path.join(MAPREDUCE_DIR, "mapreduce_orchestrator.py")
    assert os.path.exists(runner), "run_mapreduce_job.sh missing"
    assert os.path.exists(orchestrator), "mapreduce_orchestrator.py missing"

def test_mapreduce_execution_manifest():
    """Verify execution manifest records 7 successful MapReduce jobs with authentic YARN IDs."""
    assert os.path.exists(MANIFEST_PATH), f"Manifest missing: {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert len(manifest) == 7, f"Expected 7 jobs in manifest, found {len(manifest)}"
    for job in manifest:
        assert job["status"] == "SUCCESS", f"Job {job['name']} failed with code {job['exit_code']}"
        assert job["yarn_application_id"] is not None, f"Job {job['name']} missing YARN application ID"
        assert job["yarn_application_id"].startswith("application_"), f"Invalid YARN app ID: {job['yarn_application_id']}"
        assert job["mapreduce_job_id"] is not None, f"Job {job['name']} missing MapReduce job ID"
        assert job["mapreduce_job_id"].startswith("job_"), f"Invalid MR job ID: {job['mapreduce_job_id']}"
        assert job["output_record_count"] > 0, f"Job {job['name']} output 0 records"

def test_mapreduce_gold_hdfs_outputs():
    """Verify all 7 Gold HDFS aggregation paths exist, contain _SUCCESS, and non-empty part files."""
    gold_dirs = [
        "/orbitalytics/gold/mr_equipment_demand_by_component",
        "/orbitalytics/gold/mr_resource_consumption_by_year",
        "/orbitalytics/gold/mr_missions_by_agency",
        "/orbitalytics/gold/mr_satellites_by_orbit_type",
        "/orbitalytics/gold/mr_launches_by_year",
        "/orbitalytics/gold/mr_manufacturing_by_component",
        "/orbitalytics/gold/mr_research_investment_by_agency_year"
    ]

    for d in gold_dirs:
        # Check _SUCCESS flag
        code, out, _ = run_cmd(f'docker exec {DOCKER_CONTAINER} bash -c "hdfs dfs -test -e {d}/_SUCCESS"')
        assert code == 0, f"_SUCCESS flag missing in {d}"

        # Count non-empty records
        code, out, _ = run_cmd(f'docker exec {DOCKER_CONTAINER} bash -c "hdfs dfs -cat {d}/part* 2>/dev/null | wc -l"')
        assert code == 0, f"Failed to read part files in {d}"
        lines = int(out.strip())
        assert lines > 0, f"HDFS output {d} is empty"

def test_mapreduce_combiner_optimization():
    """Verify combiner drastically reduced map output records in Job 01 and Job 05."""
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    job01 = next(j for j in manifest if j["job_id"] == "01")
    c01 = job01["counters"]
    assert c01["combine_input_records"] > 0, "Job 01 combiner input was 0"
    assert c01["combine_output_records"] < c01["combine_input_records"], "Job 01 combiner did not reduce records"

    job05 = next(j for j in manifest if j["job_id"] == "05")
    c05 = job05["counters"]
    assert c05["combine_input_records"] > 0, "Job 05 combiner input was 0"
    assert c05["combine_output_records"] < c05["combine_input_records"], "Job 05 combiner did not reduce records"

def test_multi_reducer_partitioning():
    """Verify jobs ran with multi-reducer parallelism (2 partitions generated)."""
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for job in manifest:
        hdfs_path = job["output_hdfs_path"]
        code, out, _ = run_cmd(f'docker exec {DOCKER_CONTAINER} bash -c "hdfs dfs -ls {hdfs_path}/part* | wc -l"')
        assert code == 0, f"Failed to list part files for {job['name']}"
        part_count = int(out.strip())
        assert part_count == 2, f"Expected 2 partitions for {job['name']}, got {part_count}"

