import urllib.request
import json

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/optimization/procurement",
    data=json.dumps({"budget_constraint_usd": 15000000.0, "cleanroom_capacity_hours": 12000.0, "priority_weight": 0.8}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print("Optimization Procurement Keys:", list(data.keys()))
for k, v in data.items():
    if isinstance(v, list):
        print(f"{k} (count {len(v)}): sample: {v[0] if v else 'empty'}")
    else:
        print(f"{k}: {v}")
