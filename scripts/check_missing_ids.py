import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

all_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

# Find calls in JS
pos_js = html.find('<!-- JAVASCRIPT APPLICATION CORE -->')
js_code = html[pos_js:]

calls_dom = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", js_code))
calls_text = set(re.findall(r"setText\(['\"]([^'\"]+)['\"]", js_code))
calls_canvas = set(re.findall(r"getCanvasContext\(['\"]([^'\"]+)['\"]", js_code))

all_calls = calls_dom | calls_text | calls_canvas

missing = [c for c in all_calls if c not in all_ids]
print(f"Total element IDs referenced in JS: {len(all_calls)}")
print(f"Total unique IDs in HTML markup: {len(all_ids)}")
print(f"Missing IDs: {missing}")

for m in missing:
    # search where m is in HTML
    count = html.count(m)
    print(f"  Missing '{m}': occurrences in HTML = {count}")
