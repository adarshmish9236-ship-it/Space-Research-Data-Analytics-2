with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', text, re.IGNORECASE)
main_script = scripts[4]

lines = main_script.splitlines()
print(f"Total lines in script: {len(lines)}")
for i, line in enumerate(lines[:60]):
    print(f"{i+1}: {line}")

# Find all occurrences of API_BASE or fetch or axios
api_lines = [l.strip() for l in lines if "API_BASE" in l or "fetch" in l or "axios" in l or "http" in l]
print(f"\nAPI Lines ({len(api_lines)}):")
for l in api_lines[:30]:
    print("  ", l)
