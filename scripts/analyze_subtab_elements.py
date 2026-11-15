import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

subtabs = [
    'tab-research-overview',
    'tab-research-missions',
    'tab-research-satellites',
    'tab-research-launches',
    'tab-research-equipment',
    'tab-research-resources',
    'tab-research-investments',
    'tab-research-geographic',
    'tab-research-forecasting',
    'tab-research-optimization',
    'tab-research-scenario',
    'tab-research-explorer',
    'tab-research-reports'
]

print("=== CURRENT CARDS AND CANVAS PER SECTION ===")
for st in subtabs:
    pos = html.find(f'id="{st}"')
    next_pos = len(html)
    for other in subtabs + ['tab-eng-pipeline']:
        p = html.find(f'id="{other}"')
        if p > pos and p < next_pos:
            next_pos = p
    sec = html[pos:next_pos]
    canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\']', sec)
    tables = re.findall(r'<tbody[^>]*id=["\']([^"\']+)["\']', sec)
    inputs = re.findall(r'<(?:input|select|button)[^>]*id=["\']([^"\']+)["\']', sec)
    print(f"\n{st}:")
    print(f"  Canvases ({len(canvases)}): {canvases}")
    print(f"  Table bodies ({len(tables)}): {tables}")
    print(f"  Controls ({len(inputs)}): {inputs[:8]}...")
