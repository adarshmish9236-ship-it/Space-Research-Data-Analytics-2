import urllib.request
import json
import time

tests = [
    ("POST", "/api/v1/forecasting/predict", {"target": "equipment", "algorithm": "RandomForest", "horizon_months": 12, "scenario": "baseline"}),
    ("POST", "/api/v1/optimization/procurement", {"budget_ceiling_usd": 60000000.0, "criticality_penalty_weight": 2.5}),
    ("POST", "/api/v1/optimization/demand-gap", {"category": "Equipment", "horizon_months": 12}),
    ("POST", "/api/v1/optimization/inventory", {"item_name": "Solar Panel Array High Efficiency", "lead_time_days": 90, "service_level": 0.95}),
    ("POST", "/api/v1/scenarios/run", {"budget_growth_pct": 10.0, "launch_cadence_change_pct": 15.0, "equipment_price_inflation_pct": 5.0}),
    ("POST", "/api/v1/scenarios/monte-carlo", {"iterations": 300, "volatility_pct": 15.0}),
    ("POST", "/api/v1/benchmarks/run", {"workload": "agency_mission_aggregation", "dataset_name": "space_missions"}),
    ("POST", "/api/v1/pipeline/run", {}),
    ("POST", "/api/v1/mapreduce/run", {"job_name": "missions_aggregation"}),
    ("POST", "/api/v1/spark/run", {"job_name": "01_data_access_verification"}),
    ("POST", "/api/v1/pig/run", {"script_name": "01_missions_etl.pig"}),
    ("GET", "/api/v1/reports/executive/pdf", None),
    ("GET", "/api/v1/reports/lakehouse/excel", None),
    ("GET", "/api/v1/reports/raw/csv?dataset_name=space_missions", None),
    ("GET", "/api/v1/reports/download/pdf", None),
    ("GET", "/api/v1/reports/download/csv", None),
]

print("Testing POST and Report endpoints on http://127.0.0.1:8000...")
success = 0
for method, ep, body in tests:
    url = f"http://127.0.0.1:8000{ep}"
    t0 = time.time()
    try:
        headers = {}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            elapsed = round((time.time() - t0) * 1000, 1)
            ctype = resp.headers.get("Content-Type", "")
            print(f"[OK 200] {method} {ep} ({len(content)} bytes, {ctype}, {elapsed}ms)")
            success += 1
    except Exception as e:
        print(f"[FAIL] {method} {ep}: {e}")

print(f"\nSummary: {success}/{len(tests)} passed.")
