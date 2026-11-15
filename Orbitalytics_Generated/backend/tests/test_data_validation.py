"""
Orbitalytics - Data Validation Tests
"""
from app.services.data_validation_service import DataValidationService

validator = DataValidationService()

def test_validate_single_dataset():
    rep = validator.validate_dataset("space_missions")
    assert rep["dataset_name"] == "space_missions"
    assert rep["total_records"] > 0
    assert rep["completeness_score_pct"] >= 90.0

def test_validate_all_datasets():
    reports = validator.validate_all_datasets()
    assert len(reports) == 9
    for r in reports:
        assert r["completeness_score_pct"] > 80.0

