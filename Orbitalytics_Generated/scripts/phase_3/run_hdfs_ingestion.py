"""
Orbitalytics Phase 3 Runner: Execute Full HDFS Data Lake Ingestion
Transfers validated Phase 1 datasets to live HDFS in Docker,
generates Bronze (Raw), Silver (Snappy Parquet), and Gold (Analytics) tiers,
and registers complete metadata manifest.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.phase_3.hdfs_ingestion_engine import HDFSIngestionEngine

def main():
    print("=" * 70)
    print("  ORBITALYTICS PHASE 3: PRODUCTION HDFS DATA LAKE INGESTION")
    print("=" * 70)
    print()

    engine = HDFSIngestionEngine()
    result = engine.run_full_lakehouse_ingestion(force=True)

    print()
    print("=" * 70)
    print("  INGESTION SUMMARY & TELEMETRY")
    print("=" * 70)
    print(f"Status:             {result['status']}")
    print(f"Datasets Ingested:  {result['ingested_count']}")
    print(f"Errors Encountered: {result['error_count']}")
    print(f"Gold Marts Built:   {len(result['gold_marts'])}")
    print(f"Total HDFS Files:   {result['telemetry']['hdfs_storage']['total_files']}")
    print(f"Total HDFS Size:    {result['telemetry']['hdfs_storage']['total_size_formatted']}")
    print()

    print("--- HDFS Zones Breakdown ---")
    for zone, metrics in result["telemetry"]["hdfs_storage"]["zones"].items():
        print(f"  • {zone.upper():12}: {metrics.get('file_count', 0)} files, {metrics.get('size_formatted', '0 B')} ({metrics.get('path', '')})")

    # Save summary report
    summary_path = PROJECT_ROOT / "datasets" / "metadata" / "phase_3_ingestion_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print()
    print(f"[OK] Summary report saved to: {summary_path}")

if __name__ == "__main__":
    main()
