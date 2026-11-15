import urllib.request
import json

base_url = 'http://localhost:8000/api/v1'
endpoints = [
    '/overview/kpis',
    '/overview/insights',
    '/missions/analytics',
    '/satellites/analytics',
    '/launches/analytics',
    '/equipment/analytics',
    '/resources/analytics',
    '/investments/analytics',
    '/geographic/analytics',
    '/forecasting/models'
]

print("=== CHECKING BACKEND TELEMETRY KEYS ===")
for ep in endpoints:
    try:
        with urllib.request.urlopen(base_url + ep, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            keys = list(data.keys()) if isinstance(data, dict) else f"list({len(data)})"
            print(f"{ep}: {keys}")
    except Exception as e:
        print(f"{ep}: ERROR {e}")
