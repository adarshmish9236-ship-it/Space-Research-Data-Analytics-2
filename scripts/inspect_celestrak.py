import urllib.request
import json

url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Orbitalytics/2.0 (aerospace research)'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"Total stations returned: {len(data)}")
        print("Sample station record:")
        print(json.dumps(data[0], indent=2))
except Exception as e:
    print(f"Error: {e}")
