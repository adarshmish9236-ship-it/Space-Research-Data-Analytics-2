with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 4030 to 4060:")
for i in range(4029, 4060):
    print(f"{i+1}: {lines[i]}", end='')
