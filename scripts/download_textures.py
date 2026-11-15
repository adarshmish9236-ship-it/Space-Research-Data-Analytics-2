import urllib.request
import os

urls = {
    'frontend/assets/textures/earth_day.jpg': 'https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg',
    'frontend/assets/textures/earth_night.jpg': 'https://unpkg.com/three-globe/example/img/earth-night.jpg',
    'frontend/assets/textures/earth_clouds.png': 'https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_clouds_2048.png',
    'frontend/assets/textures/earth_specular.jpg': 'https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_specular_2048.jpg',
    'frontend/assets/three.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',
    'frontend/assets/OrbitControls.js': 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js'
}

for path, url in urls.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
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
