import urllib.request
import json

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/scenarios/run",
    data=json.dumps({"budget_growth_pct": 10.0, "launch_cadence_change_pct": 5.0, "equipment_price_inflation_pct": 3.0}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print("Scenarios Run Keys:", list(data.keys()))
for k, v in data.items():
    print(f"Scenario {k}: {v['scenario_name']} | budget={v['simulated_annual_budget_billion_usd']}")

req2 = urllib.request.Request("http://127.0.0.1:8000/api/v1/scenarios/sensitivity")
with urllib.request.urlopen(req2) as resp2:
    data2 = json.loads(resp2.read().decode())
print("Sensitivity factors count:", len(data2.get('factors', [])))
