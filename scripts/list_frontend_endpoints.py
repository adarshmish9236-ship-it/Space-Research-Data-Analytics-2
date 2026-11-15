with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'`\$\{API_BASE\}(/[^`"\'\s]+)`', text)
matches += re.findall(r'"\$\{API_BASE\}(/[^`"\'\s]+)"', text)
matches += re.findall(r'\'\$\{API_BASE\}(/[^`"\'\s]+)\'', text)

print(f"Total API endpoints in frontend: {len(matches)}")
unique_eps = sorted(set(matches))
for u in unique_eps:
    print(f"  {u}")
