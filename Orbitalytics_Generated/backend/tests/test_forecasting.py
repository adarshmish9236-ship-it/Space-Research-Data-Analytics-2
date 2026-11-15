"""
Orbitalytics - Forecasting Tests
"""
from starlette.testclient import TestClient
from app.main import app
from app.services.demand_forecaster import DemandForecaster

client = TestClient(app)
forecaster = DemandForecaster()

def test_forecasting_targets():
    res = client.get("/api/forecasting/targets")
    assert res.status_code == 200
    targets = res.json()
    assert len(targets) >= 4

def test_random_forest_forecast():
    res = client.get("/api/forecasting/predict?target=equipment&horizon_months=12&model=RandomForest")
    assert res.status_code == 200
    data = res.json()
    assert len(data["future_forecasts"]) == 12
    assert "evaluation_metrics" in data
    assert data["evaluation_metrics"]["accuracy_pct"] > 50.0
    assert len(data["historical_actuals"]) > 0

def test_gradient_boosting_forecast():
    res = client.get("/api/forecasting/predict?target=launches&horizon_months=6&model=GradientBoosting")
    assert res.status_code == 200
    data = res.json()
    assert len(data["future_forecasts"]) == 6

def test_scenario_analysis():
    payload = {
        "target": "equipment",
        "horizon_months": 12,
        "investment_growth_pct": 10.0,
        "launch_activity_growth_pct": 5.0,
        "cost_variation_pct": -2.0
    }
    res = client.post("/api/forecasting/scenario", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "scenarios" in data
    assert len(data["scenarios"]) == 12
    # Optimistic should be >= Baseline
    assert data["scenarios"][-1]["optimistic"] >= data["scenarios"][-1]["baseline"]

