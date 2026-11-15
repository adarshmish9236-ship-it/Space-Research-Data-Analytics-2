"""
Unit Test: Temporal Consistency and Chronological Continuity
Verifies that time-series datasets have valid ISO dates (YYYY-MM-DD),
strict monthly cadences, and no temporal gaps.
"""

import unittest
from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

class TestTemporalConsistency(unittest.TestCase):
    def setUp(self):
        self.val_dir = BASE_DIR / "datasets" / "validated"

    def test_equipment_demand_monthly_continuity(self):
        dem_file = self.val_dir / "equipment_component_demand_validated.csv"
        df = pd.read_csv(dem_file)
        self.assertIn("date", df.columns)
        df["date"] = pd.to_datetime(df["date"])

        # Check unique monthly timestamps
        unique_dates = sorted(df["date"].unique())
        self.assertGreaterEqual(len(unique_dates), 100, "Expected at least 100 monthly time periods")

        # Verify regular monthly diffs (28-31 days)
        date_series = pd.Series(unique_dates)
        diffs = date_series.diff().dt.days.dropna()
        self.assertTrue(((diffs >= 28) & (diffs <= 31)).all(), "Temporal gaps or non-monthly spacing detected in component demand")

    def test_resource_consumption_monthly_continuity(self):
        res_file = self.val_dir / "resource_consumption_validated.csv"
        df = pd.read_csv(res_file)
        df["date"] = pd.to_datetime(df["date"])

        unique_dates = sorted(df["date"].unique())
        self.assertGreaterEqual(len(unique_dates), 100)

        date_series = pd.Series(unique_dates)
        diffs = date_series.diff().dt.days.dropna()
        self.assertTrue(((diffs >= 28) & (diffs <= 31)).all(), "Temporal gaps detected in resource consumption")

if __name__ == "__main__":
    unittest.main()

