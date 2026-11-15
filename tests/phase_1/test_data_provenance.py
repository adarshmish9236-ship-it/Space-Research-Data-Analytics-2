"""
Unit Test: Data Provenance and Origin Classification
Verifies that all validated and public records explicitly carry data_origin tags
('real' or 'synthetic') and are registered in ProvenanceManager.
"""

import unittest
from pathlib import Path
import json
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.provenance_manager import ProvenanceManager
from modules.phase_1.schema_registry import SchemaRegistry

class TestDataProvenance(unittest.TestCase):
    def setUp(self):
        self.val_dir = BASE_DIR / "datasets" / "validated"
        self.public_dir = BASE_DIR / "datasets" / "raw" / "public"
        self.prov_mgr = ProvenanceManager(BASE_DIR / "datasets" / "metadata")

    def test_provenance_registry_exists_and_contains_all_datasets(self):
        reg = self.prov_mgr.load_registry()
        for d_name in SchemaRegistry.list_datasets():
            self.assertIn(d_name, reg, f"Dataset {d_name} not registered in Provenance Registry.")
            self.assertEqual(reg[d_name]["data_origin"], "synthetic")
            self.assertTrue(reg[d_name]["is_synthetic"])

    def test_public_datasets_labeled_real(self):
        pub_file = self.public_dir / "nasa_public_space_missions.csv"
        if pub_file.exists():
            df_pub = pd.read_csv(pub_file)
            self.assertIn("data_origin", df_pub.columns)
            self.assertTrue((df_pub["data_origin"] == "real").all())

    def test_synthetic_datasets_labeled_synthetic(self):
        for d_name in SchemaRegistry.list_datasets():
            val_file = self.val_dir / f"{d_name}_validated.csv"
            df = pd.read_csv(val_file)
            self.assertIn("data_origin", df.columns)
            self.assertTrue((df["data_origin"] == "synthetic").all())

if __name__ == "__main__":
    unittest.main()

