with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in frontend/index.html: {len(lines)}")
print("Line 1 to 10:")
for i in range(10):
    print(f"{i+1}: {lines[i]}", end='')

print("\nLine 1700 to 1725:")
for i in range(1699, 1725):
    print(f"{i+1}: {lines[i]}", end='')
