with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(4595, 4635):
    print(f"{i+1}: {lines[i]}", end='')
