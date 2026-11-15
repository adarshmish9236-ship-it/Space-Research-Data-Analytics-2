import urllib.request
import json

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/missions/analytics")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())

print("Missions Analytics Keys:", list(data.keys()))
print("Sample agency record:", data['agencies'][0] if 'agencies' in data and data['agencies'] else "No agencies")
print("Sample mission type:", data['mission_types'][0] if 'mission_types' in data and data['mission_types'] else "No types")
print("Other fields:", {k: v for k, v in data.items() if k not in ('agencies', 'mission_types')})
