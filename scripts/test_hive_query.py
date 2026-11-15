import urllib.request
import json

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/hive/query?query_id=agency_missions")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print("Hive query keys:", list(data.keys()))
print("Columns:", data.get('columns'))
print("Sample record:", data.get('records', [])[0] if data.get('records') else 'none')
