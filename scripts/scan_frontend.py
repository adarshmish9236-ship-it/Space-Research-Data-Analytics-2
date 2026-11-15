import re

with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

fetches = re.findall(r'fetch\([\'"`]([^\'"`]+)[\'"`]', text)
print(f"Total fetch calls: {len(fetches)}")
for u in sorted(set(fetches)):
    print(f"  - {u}")
