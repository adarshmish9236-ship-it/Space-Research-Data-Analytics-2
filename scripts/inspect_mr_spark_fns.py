with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'(?:async )?function\s+(?:run|load)?(?:MapReduce|Spark|MR)[a-zA-Z0-9_]*\s*\([^)]*\)\s*\{[\s\S]*?(?=\n\s*(?:async )?function|\n\s*//\s*\d+|$)', text, re.IGNORECASE)
print(f"Total matching functions: {len(matches)}")
for m in matches:
    print(m[:500])
    print("...\n")
