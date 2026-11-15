with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2060, 2364):
    l = lines[i]
    if 'id=' in l or '<h' in l or 'canvas' in l:
        print(f"{i+1}: {l.strip()}")
