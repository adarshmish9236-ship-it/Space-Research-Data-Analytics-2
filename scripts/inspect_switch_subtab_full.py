with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re
subtab_fn = re.search(r'function switchSubTab\(tabId\)[\s\S]*?(?=\n\s{4}//|\n\s{4}function\s+\w+|$)', text)
if subtab_fn:
    print(subtab_fn.group(0))
