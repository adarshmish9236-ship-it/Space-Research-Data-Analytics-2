import urllib.request
import json

groups = ["stations", "visual", "gps-ops", "geo", "resource"]
results = {}

for g in groups:
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={g}&FORMAT=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Orbitalytics/2.0'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results[g] = len(data)
    except Exception as e:
        results[g] = f"Error: {e}"

print("CelesTrak Group Counts:", results)
