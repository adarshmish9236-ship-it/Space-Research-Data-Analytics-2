import urllib.request
import urllib.error
import json
import traceback

BASE = "http://127.0.0.1:8000"

endpoints = [
    # Research Overview
    "/api/v1/overview/kpis",
    "/api/v1/overview/insights",
    "/api/v1/missions/analytics",
    "/api/v1/satellites/analytics",
    # Launches
    "/api/v1/launches/analytics",
    "/api/v1/geographic/analytics",
    # Equipment
    "/api/v1/equipment/analytics",
    # Resources
    "/api/v1/resources/analytics",
    # Investments
    "/api/v1/investments/analytics",
    # Geographic
    "/api/v1/geographic/analytics",
    # Forecasting
    "/api/v1/forecasting/models",
    # Optimization
    "/api/v1/optimization/shortages",
    "/api/v1/optimization/summary",
    # Scenarios
    "/api/v1/scenarios/sensitivity",
    # Explorer
    "/api/v1/hive/query?query_id=agency_missions",
    # Reports
    "/api/v1/reports/raw/csv?dataset_name=space_missions"
]

print("Testing all Research Layer endpoints over HTTP:")
for ep in endpoints:
    url = BASE + ep
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            status = resp.status
            print(f"[OK {status}] {ep:<45} ({len(data)} bytes)")
    except urllib.error.HTTPError as e:
        print(f"[FAIL {e.code}] {ep:<45} -> {e.read().decode('utf-8', errors='replace')[:100]}")
    except Exception as e:
        print(f"[ERR] {ep:<45} -> {str(e)}")
