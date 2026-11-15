import urllib.request
import json

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/forecasting/predict",
    data=json.dumps({"target": "equipment_rad_cpu", "algorithm": "auto", "horizon_months": 12, "scenario": "baseline"}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print("Forecasting Predict Keys:", list(data.keys()))
for k, v in data.items():
    if isinstance(v, list):
        print(f"{k} (count {len(v)}): sample: {v[0] if v else 'empty'}")
    else:
        print(f"{k}: {v}")
