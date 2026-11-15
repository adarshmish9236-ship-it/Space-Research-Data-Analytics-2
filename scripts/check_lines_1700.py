with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 1700 to 1735:")
for i in range(1700, 1735):
    print(f"{i+1}: {lines[i]}", end='')
