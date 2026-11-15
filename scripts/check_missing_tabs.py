with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'.{0,50}(research-missions|research-satellites|research-equipment|research-resources|research-investments|research-geographic|eng-mapreduce|eng-spark).{0,50}', text)
print(f"Total mentions: {len(matches)}")
for m in matches[:20]:
    print("  ", m.strip())
