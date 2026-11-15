with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
# Find all divs with id starting with "tab-" or class containing tab
tab_divs = re.findall(r'<div[^>]+id=[\'"]([^\'"]*tab[^\'"]*|[^\'"]*research[^\'"]*|[^\'"]*eng[^\'"]*)[\'"][^>]*>', text)
print(f"Tab-like IDs in index.html ({len(tab_divs)}):")
for t in tab_divs:
    print("  ", t)
