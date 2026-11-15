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

print("=== RESEARCH LAYER SUBTABS IN FRONTEND ===")
for i, st in enumerate(subtabs, 1):
    pos = html.find(f'id="{st}"')
    # find next subtab or end
    next_pos = len(html)
    for other in subtabs + ['tab-eng-pipeline']:
        p = html.find(f'id="{other}"')
        if p > pos and p < next_pos:
            next_pos = p
    length = next_pos - pos if pos != -1 else 0
    print(f"{i}. {st}: pos={pos}, length={length} chars")
