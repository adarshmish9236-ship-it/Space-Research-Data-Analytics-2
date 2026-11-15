with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tabs = [
    'tab-research-geographic',
    'tab-research-forecasting',
    'tab-research-optimization',
    'tab-research-scenario',
    'tab-research-explorer',
    'tab-research-reports'
]

for t in tabs:
    pos = html.find(f'id="{t}"')
    print(f"\n==================== {t} ====================")
    print(html[pos:pos+900])
