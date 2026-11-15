#!/usr/bin/env python3
"""
ORBITALYTICS Phase 7 — Task 1: Spark Data Access & Schema Verification
Reads all Silver Parquet datasets from HDFS, validates schemas, counts, and storage paths.
Submits as a standalone spark-submit job.
"""

import sys
import json
import time
from datetime import datetime

sys.path.insert(0, "/opt/spark_analytics")
from spark_session import get_spark_session, stop_spark, SILVER_BASE, GOLD_BASE

SILVER_DATASETS = {
    "missions":             f"{SILVER_BASE}/missions",
    "satellites":           f"{SILVER_BASE}/satellites",
    "launches":             f"{SILVER_BASE}/launches",
    "equipment_demand":     f"{SILVER_BASE}/equipment_demand",
    "resource_consumption": f"{SILVER_BASE}/resource_consumption",
    "manufacturing":        f"{SILVER_BASE}/manufacturing",
    "research_investment":  f"{SILVER_BASE}/agency_expenditure",
    "infrastructure":       f"{SILVER_BASE}/infrastructure",
}

MANIFEST_PATH = "/tmp/phase7_data_access_manifest.json"


def verify_datasets(spark):
    print("\n" + "="*80)
    print("PHASE 7 — TASK 1: SPARK SILVER DATASET VERIFICATION")
    print("="*80)

    manifest = []
    for name, path in SILVER_DATASETS.items():
        print(f"\n[{name.upper()}]  Path: {path}")
        t0 = time.time()
        try:
            df = spark.read.parquet(path)
            count = df.count()
            elapsed = round(time.time() - t0, 2)
            schema_fields = [(f.name, str(f.dataType)) for f in df.schema.fields]
            print(f"  Records:   {count:,}")
            print(f"  Columns:   {len(schema_fields)}")
            print(f"  Read time: {elapsed}s")
            print(f"  Schema preview:")
            for col_name, col_type in schema_fields[:6]:
                print(f"    - {col_name}: {col_type}")
            if len(schema_fields) > 6:
                print(f"    ... and {len(schema_fields) - 6} more columns")

            manifest.append({
                "dataset": name,
                "hdfs_path": path,
                "status": "ACCESSIBLE",
                "record_count": count,
                "column_count": len(schema_fields),
                "columns": [f[0] for f in schema_fields],
                "read_time_seconds": elapsed,
                "storage_format": "PARQUET",
                "verified_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"  ERROR: Failed to read {name} from {path}: {e}")
            manifest.append({
                "dataset": name,
                "hdfs_path": path,
                "status": "FAILED",
                "error": str(e),
                "verified_at": datetime.now().isoformat()
            })

    print("\n" + "="*80)
    print("DATA ACCESS VERIFICATION SUMMARY")
    print("="*80)
    accessible = sum(1 for m in manifest if m["status"] == "ACCESSIBLE")
    total_records = sum(m.get("record_count", 0) for m in manifest)
    print(f"Datasets Verified: {accessible} / {len(SILVER_DATASETS)}")
    print(f"Total HDFS Records Accessible: {total_records:,}")
    for m in manifest:
        status_sym = "[OK]" if m["status"] == "ACCESSIBLE" else "[FAIL]"
        records = f"{m.get('record_count', 0):,} rows" if m["status"] == "ACCESSIBLE" else m.get("error", "")
        print(f"  {status_sym} {m['dataset']:25} {records}")
    print("="*80 + "\n")

    return manifest


if __name__ == "__main__":
    spark = get_spark_session(app_name="ORBITALYTICS-P7-DataAccess")
    try:
        manifest = verify_datasets(spark)
        with open(MANIFEST_PATH, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"Manifest written to {MANIFEST_PATH}")
        failed = [m["dataset"] for m in manifest if m["status"] != "ACCESSIBLE"]
        if failed:
            print(f"CRITICAL: The following datasets could not be accessed: {failed}")
            sys.exit(1)
        else:
            print("SUCCESS: All 8 Silver Parquet datasets verified and accessible.")
    finally:
        stop_spark(spark)
