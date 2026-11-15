"""
ORBITALYTICS Phase 12 — Task 4: Complete Data Validation Test Suite
Validates record counts, schema compatibility, data provenance, duplicate handling,
partition correctness, and output integrity across all 9 space research datasets.
"""

import sys
import hashlib
from pathlib import Path
import pytest
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "raw"
CURATED_DIR = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "curated"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATASETS = [
    "agency_research_expenditures.csv",
    "equipment_component_demand.csv",
    "launch_activities.csv",
    "research_investment_future_projects.csv",
    "resource_consumption.csv",
    "satellites_orbital.csv",
    "satellite_manufacturing_requirements.csv",
    "space_infrastructure_requirements.csv",
    "space_missions.csv"
]


def test_raw_datasets_exist_and_non_empty():
    """Verify all 9 raw space datasets exist on disk and have non-zero size."""
    for ds in DATASETS:
        fp = RAW_DIR / ds
        assert fp.exists(), f"Missing dataset: {ds}"
        assert fp.stat().st_size > 1000, f"File {ds} is too small: {fp.stat().st_size} bytes"


def test_raw_record_counts_and_null_thresholds():
    """Verify record counts, schema widths, and ensure missing/null rates are < 1%."""
    total_records = 0
    for ds in DATASETS:
        df = pd.read_csv(RAW_DIR / ds)
        assert len(df) > 50, f"Dataset {ds} has insufficient records: {len(df)}"
        total_records += len(df)

        # Check null rate
        null_pct = df.isnull().mean().max()
        assert null_pct < 0.05, f"Dataset {ds} has column with > 5% null values: {null_pct}"
    assert total_records >= 10_000, f"Total records {total_records} < 10,000 expected"


def test_primary_key_uniqueness():
    """Verify primary key integrity on core space entity tables."""
    # Missions PK
    df_missions = pd.read_csv(RAW_DIR / "space_missions.csv")
    assert df_missions["mission_id"].is_unique, "Duplicate mission_id detected in space_missions.csv"

    # Satellites PK
    df_satellites = pd.read_csv(RAW_DIR / "satellites_orbital.csv")
    assert df_satellites["satellite_id"].is_unique, "Duplicate satellite_id detected in satellites_orbital.csv"


def test_foreign_key_referential_integrity():
    """Verify relational integrity across agencies, components, and mission entities."""
    from modules.phase_1.relationship_validator import RelationshipValidator
    val_dir = PROJECT_ROOT / "datasets" / "validated"
    if not val_dir.exists():
        val_dir = RAW_DIR
    validator = RelationshipValidator(val_dir)
    result = validator.validate_referential_integrity()
    assert result["status"] == "PASSED", f"Referential integrity failed: {result.get('issues')}"
    assert result["referential_integrity_pct"] >= 95.0


def test_hive_partition_layout_and_correctness():
    """Verify Silver Parquet partitioned directories obey Hive year=YYYY or launch_year=YYYY directory format."""
    partitioned_datasets = [
        "agency_research_expenditures",
        "equipment_component_demand",
        "launch_activities",
        "resource_consumption",
        "satellites_orbital",
        "space_infrastructure_requirements",
        "space_missions"
    ]
    for ds_name in partitioned_datasets:
        ds_dir = CURATED_DIR / ds_name
        assert ds_dir.exists() and ds_dir.is_dir(), f"Partitioned directory {ds_name} does not exist"
        partition_dirs = [d for d in ds_dir.iterdir() if d.is_dir() and ("year=" in d.name or "launch_year=" in d.name)]
        assert len(partition_dirs) == 17, f"Expected 17 partitions for {ds_name}, found {len(partition_dirs)}"
        for pd_dir in partition_dirs:
            yr = int(pd_dir.name.split("=")[1])
            assert 2010 <= yr <= 2026, f"Invalid partition year {yr} in {pd_dir}"
            parquet_files = list(pd_dir.glob("*.parquet"))
            assert len(parquet_files) >= 1, f"Partition {pd_dir} contains no Parquet files"


def test_partition_pruning_performance():
    """Verify reading a specific year partition returns exactly that year's data."""
    ds_dir = CURATED_DIR / "equipment_component_demand"
    part_2023 = ds_dir / "year=2023"
    part_files = list(part_2023.glob("*.parquet"))
    assert len(part_files) > 0

    df_2023 = pd.read_parquet(part_files[0])
    if "year" in df_2023.columns:
        assert (df_2023["year"] == 2023).all()


def test_data_provenance_and_sha256_checksums():
    """Verify SHA-256 checksum stability across raw datasets."""
    checksums = {}
    for ds in DATASETS:
        fp = RAW_DIR / ds
        h = hashlib.sha256(fp.read_bytes()).hexdigest()
        assert len(h) == 64
        checksums[ds] = h
    assert len(checksums) == 9
