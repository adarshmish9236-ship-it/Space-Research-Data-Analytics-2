import re
from pathlib import Path

content = Path("frontend/index.html").read_text(encoding="utf-8")

# Let's inspect switchLayer
idx_layer = content.find("function switchLayer")
if idx_layer != -1:
    print("--- switchLayer ---")
    print(content[idx_layer:idx_layer+1200])

# Let's inspect init / onload / DOMContentLoaded
idx_init = content.find("DOMContentLoaded")
if idx_init != -1:
    print("\n--- DOMContentLoaded ---")
    print(content[idx_init-100:idx_init+1200])
else:
    # search for init() or window.onload
    print("\nDOMContentLoaded NOT FOUND. Searching for init() or window.onload:")
    for line in content.splitlines():
        if "onload" in line or "init(" in line or "loadOverview()" in line:
            print("  ", line.strip()[:100])
