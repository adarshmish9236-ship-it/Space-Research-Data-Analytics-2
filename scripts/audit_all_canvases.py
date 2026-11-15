with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find all canvas IDs in HTML
canvas_ids = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\']', html)
print(f"Total canvas elements in HTML: {len(canvas_ids)}")

pos_js = html.find('<!-- JAVASCRIPT APPLICATION CORE -->')
js_code = html[pos_js:]

print("\n=== AUDITING EVERY CANVAS ELEMENT ===")
for cid in canvas_ids:
    count_in_js = len(re.findall(rf"['\"]{cid}['\"]", js_code))
    has_render = f"getCanvasContext('{cid}')" in js_code or f'getCanvasContext("{cid}")' in js_code or f"getElementById('{cid}')" in js_code or f'getElementById("{cid}")' in js_code
    print(f"Canvas id='{cid}': referenced in JS = {count_in_js} times | Has getCanvasContext = {has_render}")
