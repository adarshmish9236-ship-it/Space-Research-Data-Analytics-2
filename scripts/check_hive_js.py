with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(4980, 5015):
    print(f"{i+1}: {lines[i]}", end='')
