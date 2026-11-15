import urllib.request
import json

urls = [
    ("CesiumJS jsdelivr", "https://cdn.jsdelivr.net/npm/cesium@1.114.0/Build/Cesium/Cesium.js"),
    ("satellite.js cdnjs", "https://cdnjs.cloudflare.com/ajax/libs/satellite.js/5.0.0/satellite.min.js"),
    ("CelesTrak GP API", "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json")
]

for name, url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            print(f"[OK] {name}: HTTP {resp.status} (Length: {resp.headers.get('Content-Length', 'chunked')})")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
