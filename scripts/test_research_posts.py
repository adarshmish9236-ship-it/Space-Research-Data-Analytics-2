import urllib.request
import urllib.error
import json

BASE = "http://127.0.0.1:8000"

posts = [
    (
        "/api/v1/forecasting/predict",
        {"target": "equipment", "algorithm": "RandomForest", "horizon_months": 12, "scenario": "Baseline"}
    ),
    (
        "/api/v1/optimization/procurement",
        {"budget_ceiling_usd": 60000000.0, "criticality_penalty_weight": 2.5}
    ),
    (
        "/api/v1/scenarios/run",
        {"budget_growth_pct": 5.0, "launch_cadence_change_pct": 10.0, "equipment_price_inflation_pct": 2.0}
    ),
    (
        "/api/v1/scenarios/monte-carlo",
        {"iterations": 100, "confidence_interval": 0.95}
    )
]

print("Testing Research Layer POST endpoints:")
for ep, payload in posts:
    url = BASE + ep
    data_bytes = json.dumps(payload).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            print(f"[OK {resp.status}] {ep:<35} ({len(data)} bytes)")
    except urllib.error.HTTPError as e:
        print(f"[FAIL {e.code}] {ep:<35} -> {e.read().decode('utf-8', errors='replace')[:150]}")
    except Exception as e:
        print(f"[ERR] {ep:<35} -> {str(e)}")
