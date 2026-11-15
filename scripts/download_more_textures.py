import urllib.request
import os

items = {
    'frontend/assets/textures/earth_clouds.png': 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_clouds_1024.png',
    'frontend/assets/textures/earth_atmos.jpg': 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_atmos_2048.jpg',
    'frontend/assets/textures/earth_lights.png': 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_lights_2048.png',
    'frontend/assets/textures/earth_specular.jpg': 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_specular_2048.jpg',
    'frontend/assets/textures/earth_normal.jpg': 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_normal_2048.jpg'
}

for path, url in items.items():
    print(f"Downloading {url} to {path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(path, 'wb') as f:
                f.write(data)
        print(f"Success: {path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {path}: {e}")
