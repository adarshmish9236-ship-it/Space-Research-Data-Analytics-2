"""
Unit Test: Foreign Key Referential Integrity
Verifies referential integrity between child and parent datasets using RelationshipValidator.
"""

import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.phase_1.relationship_validator import RelationshipValidator

class TestForeignKeys(unittest.TestCase):
    def setUp(self):
        self.val_dir = BASE_DIR / "datasets" / "validated"
        self.validator = RelationshipValidator(self.val_dir)

    def test_referential_integrity_passes(self):
        result = self.validator.validate_referential_integrity()
        self.assertEqual(result["status"], "PASSED", f"Referential integrity failed: {result['issues']}")
        self.assertEqual(result["referential_integrity_pct"], 100.0)

if __name__ == "__main__":
    unittest.main()
