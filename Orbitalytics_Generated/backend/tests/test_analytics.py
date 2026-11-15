"""
Orbitalytics - Analytics Tests
"""
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_mission_analytics():
    res = client.get("/api/analytics/missions")
    assert res.status_code == 200
    data = res.json()
    assert "agencies" in data
    assert len(data["agencies"]) > 0

def test_satellite_analytics():
    res = client.get("/api/analytics/satellites")
    assert res.status_code == 200
    data = res.json()
    assert "orbit_distribution" in data
    assert len(data["orbit_distribution"]) > 0

def test_launch_analytics():
    res = client.get("/api/analytics/launches")
    assert res.status_code == 200
    data = res.json()
    assert "yearly_trends" in data
    assert "vehicles" in data

def test_equipment_demand():
    res = client.get("/api/analytics/equipment-demand")
    assert res.status_code == 200
    data = res.json()
    assert "components" in data
    assert len(data["components"]) > 0

def test_geographic_distribution():
    res = client.get("/api/analytics/geographic-distribution")
    assert res.status_code == 200
    data = res.json()
    assert "territories" in data
    assert "spaceports" in data
    assert len(data["spaceports"]) == 7

