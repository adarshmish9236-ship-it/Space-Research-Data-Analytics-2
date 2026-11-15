"""
Unit Test: Synthetic Data Generation Reproducibility and Scale Profiles
Verifies that synthetic data generation is reproducible under fixed seeds
and produces configurable profiles ('small', 'medium').
"""

import unittest
from pathlib import Path
import tempfile
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.synthetic_data_generator import SyntheticDataGenerator

class TestSyntheticGeneration(unittest.TestCase):
    def test_reproducibility_with_fixed_seed(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            gen1 = SyntheticDataGenerator(base_dir=tmp_path, seed=42)
            res1 = gen1.generate_profile("small")

            gen2 = SyntheticDataGenerator(base_dir=tmp_path, seed=42)
            res2 = gen2.generate_profile("small")

            self.assertEqual(res1["total_records"], res2["total_records"])
            self.assertEqual(res1["counts"], res2["counts"])

    def test_scale_profile_multipliers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            gen = SyntheticDataGenerator(base_dir=tmp_path, seed=42)
            res = gen.generate_profile("small")
            self.assertGreaterEqual(res["total_records"], 10000)
            self.assertIn("equipment_component_demand", res["counts"])

if __name__ == "__main__":
    unittest.main()
