"""
Unit Test: Dataset Schemas and Required Columns
Verifies that all 9 datasets adhere strictly to SchemaRegistry definitions.
"""

import unittest
from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.schema_registry import SchemaRegistry

class TestDatasetSchema(unittest.TestCase):
    def setUp(self):
        self.val_dir = BASE_DIR / "datasets" / "validated"

    def test_all_nine_datasets_exist_in_schema_registry(self):
        datasets = SchemaRegistry.list_datasets()
        self.assertEqual(len(datasets), 9)
        self.assertIn("space_missions", datasets)
        self.assertIn("equipment_component_demand", datasets)
        self.assertIn("resource_consumption", datasets)

    def test_validated_files_contain_required_columns(self):
        for d_name in SchemaRegistry.list_datasets():
            val_file = self.val_dir / f"{d_name}_validated.csv"
            self.assertTrue(val_file.exists(), f"Validated file for {d_name} must exist.")
            df = pd.read_csv(val_file, nrows=10)
            schema = SchemaRegistry.get_schema(d_name)
            for req_col in schema["required_columns"]:
                self.assertIn(req_col, df.columns, f"Dataset {d_name} missing required column '{req_col}'")

if __name__ == "__main__":
    unittest.main()

