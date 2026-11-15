"""
ORBITALYTICS - Phase 1 Data Standardization, Validation & Integrity Pipeline
Runs the end-to-end Phase 1 validation pipeline:
1. Loads datasets from datasets/raw/synthetic/ (and public data)
2. Runs DataStandardizer (dates, agency mapping, snake_case)
3. Runs DataValidator (completeness, uniqueness, validity, domain boundaries)
4. Segregates clean records to datasets/validated/ and errors to datasets/rejected/
5. Runs RelationshipValidator to verify referential integrity
6. Generates comprehensive quality reports.
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

import json
import pandas as pd
from modules.phase_1.schema_registry import SchemaRegistry
from modules.phase_1.data_standardizer import DataStandardizer
from modules.phase_1.data_validator import DataValidator
from modules.phase_1.relationship_validator import RelationshipValidator
from modules.phase_1.provenance_manager import ProvenanceManager

def run_validation_pipeline():
    print("=" * 70)
    print("   ORBITALYTICS - PHASE 1: STANDARDIZATION & VALIDATION PIPELINE")
    print("=" * 70)

    raw_synthetic_dir = BASE_DIR / "datasets" / "raw" / "synthetic"
    standardizer = DataStandardizer(BASE_DIR / "datasets" / "reference")
    validator = DataValidator(BASE_DIR)
    provenance_mgr = ProvenanceManager(BASE_DIR / "datasets" / "metadata")

    datasets_to_validate = SchemaRegistry.list_datasets()
    overall_reports = []

    for d_name in datasets_to_validate:
        file_path = raw_synthetic_dir / f"{d_name}.csv"
        if not file_path.exists():
            print(f"[WARN] File {file_path.name} not found. Skipping.")
            continue

        print(f"\n[PROCESSING] {d_name}...")
        df_raw = pd.read_csv(file_path, low_memory=False)

        # 1. Standardize
        df_std = standardizer.standardize_dataframe(df_raw, d_name)

        # 2. Validate
        metrics = validator.validate_dataset(df_std, d_name)
        overall_reports.append(metrics)

        # 3. Provenance
        provenance_mgr.record_provenance(
            dataset_name=d_name,
            data_origin="synthetic",
            record_count=metrics["accepted_records"],
            source_publisher="Orbitalytics Research Big Data Engineering Team",
            licence="Apache-2.0 / Academic Research Use",
            transformation_pipeline=["DataStandardizer", "DataValidator", "SchemaEnforcement"],
            additional_metadata={"quality_score": metrics["overall_quality_score"]}
        )

        print(f" -> Input: {metrics['input_records']:6d} | Accepted: {metrics['accepted_records']:6d} | Rejected: {metrics['rejected_records']:4d} | Quality: {metrics['overall_quality_score']:.1f}%")

    # 4. Referential Integrity
    print("\n--- Verifying Referential Integrity ---")
    rel_validator = RelationshipValidator(BASE_DIR / "datasets" / "validated")
    rel_results = rel_validator.validate_referential_integrity()
    print(f"Referential Integrity Status: {rel_results['status']} ({rel_results['referential_integrity_pct']}%)")
    if rel_results["issues"]:
        for issue in rel_results["issues"]:
            print(f"  [ISSUE] {issue['relationship']}: {issue['details']}")

    # Save consolidated report
    summary_path = BASE_DIR / "datasets" / "quality_reports" / "phase_1_consolidated_quality_summary.json"
    summary_data = {
        "pipeline": "Orbitalytics Phase 1 Validation",
        "datasets_validated": len(overall_reports),
        "dataset_metrics": overall_reports,
        "referential_integrity": rel_results
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    print(f"\n[SUCCESS] Phase 1 Validation Pipeline Finished. Report saved to {summary_path}\n")

if __name__ == "__main__":
    run_validation_pipeline()
