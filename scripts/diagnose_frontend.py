import re
from pathlib import Path

content = Path("frontend/index.html").read_text(encoding="utf-8")
for line in content.splitlines():
    if "API_BASE" in line:
        print(line.strip())
