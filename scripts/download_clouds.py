import urllib.request
import os

cloud_urls = [
    "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_clouds.png",
    "https://raw.githubusercontent.com/stemkoski/stemkoski.github.com/master/Three.js/images/clouds.jpg",
    "https://raw.githubusercontent.com/jeromeetienne/threex.planets/master/images/earthclouds4k.png",
    "https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_clouds.png"
]

for url in cloud_urls:
    try:
        print(f"Trying {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open("frontend/assets/textures/earth_clouds.png", "wb") as f:
                f.write(data)
            print(f"SUCCESS: earth_clouds.png saved ({len(data)} bytes) from {url}")
            break
    except Exception as e:
        print(f"Failed {url}: {e}")
