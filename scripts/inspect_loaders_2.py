with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
for fn in ["loadExplorerData", "loadPipelineStages", "loadCatalog", "loadQualityCenter"]:
    m = re.search(rf'async function {fn}\s*\([^)]*\)\s*\{{[\s\S]*?(?=\n\s*(?:async )?function|\n\s*//\s*\d+|$)', text)
    if m:
        print(f"=== {fn} ===")
        print(m.group(0)[:1000])
        print("...\n")
