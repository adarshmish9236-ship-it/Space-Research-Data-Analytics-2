"""
ORBITALYTICS - Phase 1 Synthetic Data Generation CLI
Generates configurable scale profiles ('small', 'medium', 'large')
with strict seed control, valid relational integrity, and explicit data_origin='synthetic'.
"""

import sys
import argparse
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.synthetic_data_generator import SyntheticDataGenerator

def main():
    parser = argparse.ArgumentParser(description="Orbitalytics Synthetic Space Data Generator")
    parser.add_argument("--profile", choices=["small", "medium", "large"], default="small",
                        help="Scale profile: small (~10k rows), medium (~100k rows), large (~1M rows)")
    parser.add_argument("--seed", type=int, default=42, help="Fixed random seed for scientific reproducibility")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent.parent
    generator = SyntheticDataGenerator(base_dir=base_dir, seed=args.seed)
    summary = generator.generate_profile(profile=args.profile)

    print("\n--- Generation Summary ---")
    print(f"Profile: {summary['profile']}")
    print(f"Seed: {summary['seed']}")
    print(f"Total Records Generated: {summary['total_records']}")
    for k, v in summary["counts"].items():
        print(f"  - {k:40s}: {v:7d} records")
    print("\nAll datasets written to datasets/raw/synthetic/ with explicit data_origin='synthetic'.\n")

if __name__ == "__main__":
    main()
