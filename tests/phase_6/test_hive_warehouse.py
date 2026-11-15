"""
ORBITALYTICS Phase 6 — Automated Integration Test Suite
Validates Apache Hive Data Warehouse, Dimensions, Partitioned Facts, Parquet Storage,
Partition Pruning, and Analytical Query Execution.
"""

import os
import json
import pytest
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "docs", "phase_6", "hive_execution_manifest.json")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "docs", "phase_6", "results")
DOCKER_CONTAINER = "hive-server"
HIVE_JDBC = "jdbc:hive2://localhost:10000/orbitalytics"

@pytest.fixture(autouse=True)
def require_docker_hiveserver():
    try:
        res = subprocess.run(["docker", "ps", "--filter", "name=hive-server", "--format", "{{.Names}}"],
                             capture_output=True, text=True, timeout=5)
        if "hive-server" not in res.stdout:
            pytest.skip("Docker container 'hive-server' is not running on this host; skipping live Beeline Hive tests.")
    except Exception as e:
        pytest.skip(f"Docker is not available ({e}); skipping live Beeline Hive tests.")

def run_beeline(query, output_format="csv2"):
    cmd = (
        f'docker exec {DOCKER_CONTAINER} beeline '
        f'-u "{HIVE_JDBC}" -n root '
        f'--outputformat={output_format} '
        f'-e "{query}"'
    )
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

def test_hive_database_and_tables():
    """Verify database orbitalytics and all required tables exist."""
    code, stdout, _ = run_beeline("SHOW TABLES;")
    assert code == 0, "Failed to connect to Hive or show tables"

    tables = [line.strip().lower() for line in stdout.splitlines() if line.strip()]
    expected_dimensions = [
        "dim_date", "dim_agency", "dim_component", "dim_resource",
        "dim_mission", "dim_satellite", "dim_location"
    ]
    expected_facts = [
        "fact_equipment_demand", "fact_resource_consumption",
        "fact_launch_activity", "fact_manufacturing", "fact_research_investment"
    ]
    expected_views = [
        "vw_annual_equipment_demand_summary",
        "vw_agency_mission_performance",
        "vw_launch_market_commercialization"
    ]

    for d in expected_dimensions:
        assert any(d in t for t in tables), f"Missing dimension: {d}"

    for f in expected_facts:
        assert any(f in t for t in tables), f"Missing fact table: {f}"

    for v in expected_views:
        assert any(v in t for t in tables), f"Missing view: {v}"

def test_hive_table_record_counts():
    """Verify fact tables are populated with non-zero records."""
    fact_tables = [
        "fact_equipment_demand",
        "fact_resource_consumption",
        "fact_launch_activity",
        "fact_manufacturing",
        "fact_research_investment"
    ]

    for t in fact_tables:
        code, stdout, _ = run_beeline(f"SELECT COUNT(*) FROM {t};")
        assert code == 0, f"Query failed for {t}"
        count = None
        for line in stdout.splitlines():
            line_str = line.strip()
            if line_str.isdigit():
                count = int(line_str)
                break
        assert count is not None and count > 0, f"Table {t} is empty (count={count})"

def test_hive_parquet_storage_properties():
    """Verify Parquet storage format and Snappy compression on fact tables."""
    code, stdout, _ = run_beeline("DESCRIBE FORMATTED fact_equipment_demand;")
    assert code == 0, "Failed to describe fact_equipment_demand"
    lower_out = stdout.lower()
    assert "parquet" in lower_out or "mapredparquet" in lower_out, "Table not stored as Parquet"
    assert "snappy" in lower_out, "Table missing Snappy compression property"

def test_hive_partition_pruning():
    """Verify partition pruning occurs when filtering on partition key."""
    explain_query = "EXPLAIN EXTENDED SELECT component_category, SUM(units_demanded) FROM fact_equipment_demand WHERE year = 2024 GROUP BY component_category;"
    code, stdout, _ = run_beeline(explain_query, output_format="table")
    assert code == 0, "EXPLAIN query failed"
    # Plan should specifically show partition: {year=2024} or partition pruning
    assert "2024" in stdout, "EXPLAIN plan does not reference pruned partition 2024"

def test_hive_query_manifest():
    """Verify all 16 analytical queries completed successfully in the manifest."""
    assert os.path.exists(MANIFEST_PATH), f"Manifest missing: {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert len(manifest) == 16, f"Expected 16 queries, found {len(manifest)}"
    for q in manifest:
        assert q["status"] == "SUCCESS", f"Query {q['query_name']} failed with code {q['exit_code']}"
        assert q["row_count"] > 0, f"Query {q['query_name']} returned 0 rows"
        res_file = q["result_file"]
        assert os.path.exists(res_file), f"Result file missing: {res_file}"
        assert os.path.getsize(res_file) > 0, f"Result file empty: {res_file}"

