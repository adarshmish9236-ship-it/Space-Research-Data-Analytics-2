import urllib.request
urls = [
    'http://localhost:8000/assets/textures/earth_day.jpg',
    'http://localhost:8000/assets/textures/earth_night.jpg',
    'http://localhost:8000/assets/textures/earth_clouds.png',
    'http://localhost:8000/assets/textures/earth_specular.jpg',
    'http://localhost:8000/assets/textures/earth_normal.jpg',
    'http://localhost:8000/assets/three.min.js',
    'http://localhost:8000/assets/OrbitControls.js',
    'http://localhost:8000/'
]
for url in urls:
    try:
        r = urllib.request.urlopen(url)
        cl = r.getheader('Content-Length') or '?'
        name = url.split('/')[-1] or 'index'
        print(f'OK {r.status} {cl:>10} {name}')
    except Exception as e:
        print(f'FAIL {url}: {e}')
