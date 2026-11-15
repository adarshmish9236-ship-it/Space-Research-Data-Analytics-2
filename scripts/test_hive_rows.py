import urllib.request
import json

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/hive/query?query_id=agency_missions")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print("Number of rows in data:", len(data.get('data', [])))
if data.get('data'):
    print("First row:", data['data'][0])
