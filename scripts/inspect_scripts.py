with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', text, re.IGNORECASE)
print(f"Total script blocks: {len(scripts)}")
for i, s in enumerate(scripts):
    print(f"Block {i}: length {len(s)} chars, preview: {s[:100].strip()}...")
