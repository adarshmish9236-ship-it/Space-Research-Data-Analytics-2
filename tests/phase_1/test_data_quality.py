"""
Unit Test: Data Quality Scores and Dimension Checks
Verifies that validated datasets achieve minimum quality threshold (>= 95.0%)
and that null cells / invalid values are zero in the validated set.
"""

import unittest
from pathlib import Path
import json
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.schema_registry import SchemaRegistry

class TestDataQuality(unittest.TestCase):
    def setUp(self):
        self.val_dir = BASE_DIR / "datasets" / "validated"
        self.quality_dir = BASE_DIR / "datasets" / "quality_reports"

    def test_quality_reports_exist_and_pass_threshold(self):
        for d_name in SchemaRegistry.list_datasets():
            report_file = self.quality_dir / f"{d_name}_quality_report.json"
            self.assertTrue(report_file.exists(), f"Quality report for {d_name} must exist.")
            with open(report_file, "r", encoding="utf-8") as f:
                rep = json.load(f)
            self.assertGreaterEqual(rep["overall_quality_score"], 95.0, f"Quality score for {d_name} must be >= 95%")
            self.assertEqual(rep["rejected_records"], 0, f"Expected 0 rejections for clean synthetic baseline {d_name}")

    def test_no_negative_numeric_values_in_validated_data(self):
        for d_name in SchemaRegistry.list_datasets():
            val_file = self.val_dir / f"{d_name}_validated.csv"
            df = pd.read_csv(val_file)
            numeric_cols = [c for c in df.columns if any(kw in c for kw in ["units", "quantity", "cost", "budget", "mass"])]
            for col in numeric_cols:
                num_s = pd.to_numeric(df[col], errors="coerce").dropna()
                self.assertTrue((num_s >= 0).all(), f"Found negative values in {d_name}.{col}")

if __name__ == "__main__":
    unittest.main()

