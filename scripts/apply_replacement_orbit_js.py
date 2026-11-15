with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('scripts/replacement_orbit_js.js', 'r', encoding='utf-8') as f:
    replacement = f.read()

start_marker = "    // 17. OrbitTrack 3D Orbital Celestial Globe Animation"
end_marker = "    // Live UTC Clock"

idx_start = html.find(start_marker)
idx_end = html.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print(f"Error: markers not found! start={idx_start}, end={idx_end}")
    exit(1)

new_html = html[:idx_start] + replacement + "\n\n" + html[idx_end:]

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully replaced orbit js in frontend/index.html!")
