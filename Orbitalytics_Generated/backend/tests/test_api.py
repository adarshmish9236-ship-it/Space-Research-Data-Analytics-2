"""
Orbitalytics - Backend API Tests
"""
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert "Orbitalytics" in data["platform"]

def test_overview_kpis():
    res = client.get("/api/overview/kpis")
    assert res.status_code == 200
    data = res.json()
    assert data["total_missions"] > 0
    assert data["total_satellites_cataloged"] > 0
    assert data["launch_success_rate_pct"] > 80.0

def test_datasets_list():
    res = client.get("/api/datasets")
    assert res.status_code == 200
    datasets = res.json()
    assert len(datasets) == 9
    names = [d["name"] for d in datasets]
    assert "space_missions" in names
    assert "satellites_orbital" in names

def test_dataset_preview():
    res = client.get("/api/datasets/space_missions/preview?page=1&page_size=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data["records"]) == 5
    assert "columns" in data

def test_system_status():
    res = client.get("/api/system/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["datasets_ready"] is True

