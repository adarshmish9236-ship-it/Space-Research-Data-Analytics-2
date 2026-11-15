"""
ORBITALYTICS - Phase 1 Data Audit Runner
Scans existing datasets in datasets/raw/existing, runs inventory, evaluates schemas,
checks quality problems, and outputs the baseline audit report.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

import json
import pandas as pd
from modules.phase_1.dataset_inventory import DatasetInventory
from modules.phase_1.schema_registry import SchemaRegistry

def run_audit():
    print("=" * 70)
    print("   ORBITALYTICS - PHASE 1: DATA AUDIT RUNNER")
    print("=" * 70)

    inventory_service = DatasetInventory(BASE_DIR)
    inv = inventory_service.scan_inventory()
    print(f"\n[OK] Scanned {inv['total_files']} dataset files ({inv['total_records_cataloged']} records).")

    print("\n--- Auditing Existing Raw Datasets ---")
    existing_dir = BASE_DIR / "datasets" / "raw" / "existing"
    audit_findings = []

    for f in sorted(existing_dir.glob("*.csv")):
        df = pd.read_csv(f, low_memory=False)
        nulls = int(df.isna().sum().sum())
        dups = int(df.duplicated().sum())
        base_name = f.stem

        has_origin = "data_origin" in df.columns
        origin_val = df["data_origin"].iloc[0] if has_origin and len(df) > 0 else "unspecified (synthetic generator origin)"

        finding = {
            "dataset": f.name,
            "rows": len(df),
            "columns": len(df.columns),
            "null_cells": nulls,
            "duplicate_rows": dups,
            "has_data_origin_tag": has_origin,
            "detected_origin": origin_val,
            "status": "VALID_LEGACY_RAW" if nulls == 0 and dups == 0 else "CONTAINS_QUALITY_DEFECTS"
        }
        audit_findings.append(finding)
        print(f" -> {f.name:45s} | Rows: {len(df):6d} | Nulls: {nulls:4d} | Dups: {dups:3d} | Origin: {origin_val}")

    out_file = BASE_DIR / "datasets" / "metadata" / "audit_findings.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_findings, f, indent=2)

    print(f"\n[SUCCESS] Audit completed. Audit report saved to {out_file}\n")

if __name__ == "__main__":
    run_audit()
