with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'.{0,60}mapreduce.{0,60}', text, re.IGNORECASE)
print(f"Total mapreduce occurrences: {len(matches)}")
for m in matches[:15]:
    print("  ", m.strip())
