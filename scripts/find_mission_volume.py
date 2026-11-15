with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer(r'Mission Volume by International Space Agency', html)]
print(f"Occurrences found: {len(matches)}")
for idx, pos in enumerate(matches):
    print(f"\n--- Match {idx+1} at char {pos} (line {html[:pos].count(chr(10))+1}) ---")
    print(html[pos-100:pos+300])
