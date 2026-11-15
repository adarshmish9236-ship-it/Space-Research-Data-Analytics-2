import urllib.request
import json
import time

OPENAPI_URL = "http://localhost:8000/openapi.json"
BASE_URL = "http://localhost:8000"

try:
    with urllib.request.urlopen(OPENAPI_URL, timeout=10) as resp:
        openapi = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print(f"Failed to fetch openapi.json: {e}")
    exit(1)

paths = openapi.get("paths", {})
print(f"Found {len(paths)} unique path definitions in OpenAPI spec.")

results = []
success_count = 0
fail_count = 0

for path, methods in paths.items():
    if "get" not in methods:
        continue
    
    # Skip endpoints with path parameters for bulk check, or test with sensible defaults
    test_path = path
    if "{" in path:
        if "{satellite_id}" in path:
            test_path = path.replace("{satellite_id}", "25544")
        elif "{dataset_name}" in path:
            test_path = path.replace("{dataset_name}", "space_missions")
        elif "{script_name}" in path:
            test_path = path.replace("{script_name}", "01_equipment_demand_etl.pig")
        elif "{job_name}" in path:
            test_path = path.replace("{job_name}", "01_equipment_demand")
        elif "{table_name}" in path:
            test_path = path.replace("{table_name}", "space_missions")
        else:
            continue

    url = f"{BASE_URL}{test_path}"
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OrbitalyticsProbe/1.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            elapsed_ms = int((time.time() - t0) * 1000)
            data = res.read()
            status = res.status
            results.append({"path": test_path, "status": status, "ms": elapsed_ms, "bytes": len(data), "ok": True})
            success_count += 1
            print(f"  [200 OK] ({elapsed_ms:>4}ms, {len(data):>7}b) GET {test_path}", flush=True)
    except urllib.error.HTTPError as he:
        elapsed_ms = int((time.time() - t0) * 1000)
        results.append({"path": test_path, "status": he.code, "ms": elapsed_ms, "error": str(he), "ok": False})
        fail_count += 1
        print(f"  [FAIL {he.code}] ({elapsed_ms:>4}ms) GET {test_path} -> {he}", flush=True)
    except Exception as ex:
        elapsed_ms = int((time.time() - t0) * 1000)
        results.append({"path": test_path, "status": 0, "ms": elapsed_ms, "error": str(ex), "ok": False})
        fail_count += 1
        print(f"  [ERROR] ({elapsed_ms:>4}ms) GET {test_path} -> {ex}", flush=True)

print("\n" + "="*60, flush=True)
print(f"API PROBE COMPLETE: {success_count} SUCCEEDED, {fail_count} FAILED out of {len(results)} GET endpoints tested.", flush=True)
print("="*60, flush=True)
