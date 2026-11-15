with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2060, 2330, 20):
    print(f"--- Line {i+1} ---")
    for j in range(i, min(i+15, len(lines))):
        print(f"{j+1}: {lines[j]}", end='')
