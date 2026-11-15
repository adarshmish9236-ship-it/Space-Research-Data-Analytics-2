import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'id=["\'](kpi-[^"\']+)["\']', html)
print('KPI IDs found in entire HTML:', matches)

matches_all_kpi = re.findall(r'kpi-[a-zA-Z0-9_-]+', html)
print('Any kpi- references in entire HTML:', set(matches_all_kpi))
