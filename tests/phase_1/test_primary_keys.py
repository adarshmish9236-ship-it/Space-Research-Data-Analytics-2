"""
Unit Test: Primary Key Uniqueness
Verifies that primary key columns exist, contain no nulls, and are 100% unique.
"""

import unittest
from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.schema_registry import SchemaRegistry

class TestPrimaryKeys(unittest.TestCase):
    def setUp(self):
        self.val_dir = BASE_DIR / "datasets" / "validated"

    def test_primary_keys_uniqueness_and_non_null(self):
        for d_name in SchemaRegistry.list_datasets():
            schema = SchemaRegistry.get_schema(d_name)
            pk = schema.get("primary_key")
            val_file = self.val_dir / f"{d_name}_validated.csv"
            df = pd.read_csv(val_file)

            self.assertIn(pk, df.columns, f"Primary key '{pk}' missing from {d_name}")
            self.assertEqual(df[pk].isna().sum(), 0, f"Primary key '{pk}' contains nulls in {d_name}")
            self.assertEqual(df[pk].duplicated().sum(), 0, f"Primary key '{pk}' contains duplicates in {d_name}")

if __name__ == "__main__":
    unittest.main()

