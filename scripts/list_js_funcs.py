import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_js_start = html.find('<!-- JAVASCRIPT APPLICATION CORE -->')
js_block = html[pos_js_start:]

funcs = re.findall(r'(?:async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(', js_block)
print(f"Total function definitions in JS block: {len(funcs)}")
for f in funcs:
    print(" -", f)
