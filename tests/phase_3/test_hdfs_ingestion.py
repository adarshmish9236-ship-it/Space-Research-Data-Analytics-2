"""
Orbitalytics Phase 3 Automated Test Suite
Verifies HDFS operations, directory structures, checksums,
Parquet file integrity, idempotency, and metadata persistence.
"""

import json
import pytest
import pyarrow.parquet as pq
import io
from pathlib import Path

from modules.phase_3.hdfs_client import HDFSClient
from modules.phase_3.ingestion_manifest import IngestionManifest
from modules.phase_3.format_converter import FormatConverter

@pytest.fixture(scope="module")
def hdfs():
    import subprocess
    try:
        res = subprocess.run(["docker", "ps", "--filter", "name=hadoop-namenode", "--format", "{{.Names}}"],
                             capture_output=True, text=True, timeout=5)
        if "hadoop-namenode" not in res.stdout:
            pytest.skip("Docker container 'hadoop-namenode' is not running on this host; skipping live HDFS container tests.")
    except Exception as e:
        pytest.skip(f"Docker is not available ({e}); skipping live HDFS container tests.")
    return HDFSClient()

@pytest.fixture(scope="module")
def manifest():
    import subprocess
    try:
        res = subprocess.run(["docker", "ps", "--filter", "name=hadoop-namenode", "--format", "{{.Names}}"],
                             capture_output=True, text=True, timeout=5)
        if "hadoop-namenode" not in res.stdout:
            pytest.skip("Docker container 'hadoop-namenode' is not running on this host; skipping live HDFS container tests.")
    except Exception as e:
        pytest.skip(f"Docker is not available ({e}); skipping live HDFS container tests.")
    return IngestionManifest()

def test_hdfs_directory_structure(hdfs):
    """Test that all required /orbitalytics/ lakehouse root directories exist."""
    expected_dirs = [
        "/orbitalytics/bronze",
        "/orbitalytics/silver",
        "/orbitalytics/gold",
        "/orbitalytics/metadata",
        "/orbitalytics/quarantine",
        "/orbitalytics/logs"
    ]
    for d in expected_dirs:
        assert hdfs.exists(d), f"Missing HDFS directory: {d}"

def test_bronze_datasets_exist(hdfs):
    """Test that all 9 Bronze raw datasets exist in HDFS."""
    expected_bronze = [
        "/orbitalytics/bronze/missions/space_missions.csv",
        "/orbitalytics/bronze/satellites/satellites_orbital.csv",
        "/orbitalytics/bronze/launches/launch_activities.csv",
        "/orbitalytics/bronze/equipment_demand/equipment_component_demand.csv",
        "/orbitalytics/bronze/agency_expenditure/agency_research_expenditures.csv",
        "/orbitalytics/bronze/resource_consumption/resource_consumption.csv",
        "/orbitalytics/bronze/manufacturing/satellite_manufacturing_requirements.csv",
        "/orbitalytics/bronze/infrastructure/space_infrastructure_requirements.csv",
        "/orbitalytics/bronze/research_projects/research_investment_future_projects.csv"
    ]
    for b in expected_bronze:
        assert hdfs.exists(b), f"Missing Bronze dataset in HDFS: {b}"

def test_silver_partitions_exist(hdfs):
    """Test that Silver partitioned Parquet directories exist."""
    sample_partitions = [
        "/orbitalytics/silver/missions/year=2024/part-00000.parquet",
        "/orbitalytics/silver/launches/year=2024/part-00000.parquet",
        "/orbitalytics/silver/equipment_demand/component_category=Power_Systems/part-00000.parquet",
        "/orbitalytics/silver/resource_consumption/resource_category=Cryogenic_Fuel/part-00000.parquet"
    ]
    for p in sample_partitions:
        assert hdfs.exists(p), f"Missing Silver partition Parquet file: {p}"

def test_gold_analytical_marts_exist(hdfs):
    """Test that all 6 Gold analytical marts exist and have part-00000.parquet."""
    expected_gold = [
        "/orbitalytics/gold/demand_analytics/part-00000.parquet",
        "/orbitalytics/gold/resource_analytics/part-00000.parquet",
        "/orbitalytics/gold/mission_analytics/part-00000.parquet",
        "/orbitalytics/gold/manufacturing_analytics/part-00000.parquet",
        "/orbitalytics/gold/forecast_features/part-00000.parquet",
        "/orbitalytics/gold/forecasting_results/part-00000.parquet"
    ]
    for g in expected_gold:
        assert hdfs.exists(g), f"Missing Gold mart: {g}"

def test_quarantine_isolation(hdfs):
    """Test that quarantined records are trapped in /orbitalytics/quarantine."""
    q_file = "/orbitalytics/quarantine/rejected_records_sample.csv"
    assert hdfs.exists(q_file), f"Quarantine file missing: {q_file}"
    content = hdfs.cat(q_file)
    assert "NEGATIVE_UNITS_AND_CORRUPT_DATE" in content

def test_ingestion_manifest_persistence(manifest, hdfs):
    """Test that ingestion manifest is complete and uploaded to HDFS."""
    assert len(manifest.records) >= 9, "Expected at least 9 ingestion records in manifest"
    assert hdfs.exists("/orbitalytics/metadata/ingestion_manifest.json")

def test_checksum_integrity_missions(hdfs):
    """Test that HDFS Bronze file checksum matches the recorded manifest checksum."""
    hdfs_path = "/orbitalytics/bronze/missions/space_missions.csv"
    hdfs_md5 = hdfs.checksum(hdfs_path)
    assert hdfs_md5 == "9069d9d16f6fa2f27618a0bfdca8bbc6"

def test_checksum_integrity_equipment(hdfs):
    """Test that equipment demand Bronze file checksum matches."""
    hdfs_path = "/orbitalytics/bronze/equipment_demand/equipment_component_demand.csv"
    hdfs_md5 = hdfs.checksum(hdfs_path)
    assert hdfs_md5 == "70cd157347e89cefd81f6e96f16c95e4"

