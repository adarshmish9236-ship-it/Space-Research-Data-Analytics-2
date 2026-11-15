"""
ORBITALYTICS Phase 4 — Automated Test Suite: Apache Pig ETL & Lakehouse Verification
Verifies actual execution results of Pig Latin pipelines on HDFS.
"""

import os
import json
import pytest
import subprocess


DOMAINS = [
    "missions",
    "satellites",
    "launches",
    "equipment_demand",
    "agency_expenditure",
    "resource_consumption",
    "manufacturing",
    "infrastructure",
    "research_projects"
]


def hdfs_path_exists(path: str) -> bool:
    """Check if an HDFS path exists via docker exec."""
    cmd = f'docker exec hadoop-namenode hdfs dfs -test -e {path}'
    res = subprocess.run(cmd, shell=True, capture_output=True)
    return res.returncode == 0


def hdfs_get_line_count(path: str) -> int:
    """Return non-empty line count of an HDFS directory or file."""
    cmd = f'docker exec hadoop-namenode bash -c "hdfs dfs -cat {path}/* 2>/dev/null | grep -v \'^$\' | wc -l"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip().isdigit()]
        if lines:
            return int(lines[-1])
    return 0


def test_pig_scripts_exist():
    """Verify all 9 Pig Latin ETL scripts exist in the repository."""
    pig_dir = r"E:\PROJECTS\BDT\pig_etl"
    for idx, domain in enumerate(DOMAINS, 1):
        script_name = f"{idx:02d}_{domain}_etl.pig"
        script_path = os.path.join(pig_dir, script_name)
        assert os.path.isfile(script_path), f"Missing Pig script: {script_name}"
        assert os.path.getsize(script_path) > 200, f"Script {script_name} is suspiciously small"


def test_pig_silver_lakehouse_outputs():
    """Verify that all 9 Silver Lakehouse destinations exist in HDFS."""
    for domain in DOMAINS:
        silver_path = f"/orbitalytics/silver/pig_{domain}"
        assert hdfs_path_exists(silver_path), f"Silver path does not exist: {silver_path}"
        
        # Verify _SUCCESS marker
        success_marker = f"{silver_path}/_SUCCESS"
        assert hdfs_path_exists(success_marker), f"Missing _SUCCESS marker in {silver_path}"
        
        # Verify data rows exist
        count = hdfs_get_line_count(silver_path)
        assert count > 0, f"Silver dataset {domain} has 0 records!"


def test_pig_quarantine_lakehouse_outputs():
    """Verify that all 9 Quarantine Lakehouse directories exist in HDFS."""
    for domain in DOMAINS:
        quarantine_path = f"/orbitalytics/quarantine/pig_{domain}_rejected"
        assert hdfs_path_exists(quarantine_path), f"Quarantine path does not exist: {quarantine_path}"


def test_pig_gold_analytics_marts():
    """Verify key Gold Lakehouse analytics aggregations exist and contain data."""
    gold_marts = [
        "/orbitalytics/gold/pig_mission_analytics",
        "/orbitalytics/gold/pig_satellite_analytics",
        "/orbitalytics/gold/pig_launch_analytics",
        "/orbitalytics/gold/pig_equipment_demand_analytics",
        "/orbitalytics/gold/pig_agency_expenditure_analytics",
        "/orbitalytics/gold/pig_resource_analytics",
        "/orbitalytics/gold/pig_manufacturing_analytics",
        "/orbitalytics/gold/pig_infrastructure_analytics",
        "/orbitalytics/gold/pig_research_projects_analytics"
    ]
    for mart in gold_marts:
        assert hdfs_path_exists(mart), f"Gold mart does not exist: {mart}"
        count = hdfs_get_line_count(mart)
        assert count > 0, f"Gold mart {mart} is empty!"


def test_zero_silent_deletion_rule():
    """Verify that Bronze records = Silver records + Quarantine records across domains."""
    manifest_path = r"E:\PROJECTS\BDT\docs\phase_4\pig_etl_execution_manifest.json"
    if not os.path.exists(manifest_path):
        pytest.skip("Manifest not generated yet")
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    for rec in records:
        bronze = rec["bronze_input_rows"]
        silver = rec["silver_output_rows"]
        quarantine = rec["quarantine_output_rows"]
        assert bronze == silver + quarantine, (
            f"Domain {rec['domain']} violated zero silent deletion rule! "
            f"Bronze: {bronze}, Silver: {silver}, Quarantine: {quarantine}"
        )

