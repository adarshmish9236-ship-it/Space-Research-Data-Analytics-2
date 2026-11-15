import urllib.request
import json
import time

endpoints = [
    "/api/v1/overview/kpis",
    "/api/v1/overview/insights",
    "/api/v1/data/inventory",
    "/api/v1/governance/catalog",
    "/api/v1/governance/quality",
    "/api/v1/pipeline/history",
    "/api/v1/ecosystem/health",
    "/api/v1/hdfs/overview",
    "/api/v1/yarn/status",
    "/api/v1/mapreduce/jobs",
    "/api/v1/spark/jobs",
    "/api/v1/pig/jobs",
    "/api/v1/hive/query?query_id=01_total_demand_by_component",
    "/api/v1/missions/analytics",
    "/api/v1/satellites/analytics",
    "/api/v1/launches/analytics",
    "/api/v1/equipment/analytics",
    "/api/v1/resources/analytics",
    "/api/v1/manufacturing/analytics",
    "/api/v1/investments/analytics",
    "/api/v1/geographic/analytics",
    "/api/v1/forecasting/models",
    "/api/v1/forecasting/series",
    "/api/v1/forecasting/comparison",
    "/api/v1/benchmarks/summary",
    "/api/v1/benchmarks/matrix",
    "/api/v1/benchmarks/scaling",
    "/api/v1/benchmarks/manifest",
    "/api/v1/scenarios/sensitivity"
]

print("Probing endpoints on http://127.0.0.1:8000...")
success = 0
for ep in endpoints:
    url = f"http://127.0.0.1:8000{ep}"
    t0 = time.time()
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            elapsed = round((time.time() - t0) * 1000, 1)
            print(f"[OK 200] {ep} ({len(data)} bytes, {elapsed}ms)")
            success += 1
    except Exception as e:
        print(f"[FAIL] {ep}: {e}")

print(f"\nSummary: {success}/{len(endpoints)} passed.")
