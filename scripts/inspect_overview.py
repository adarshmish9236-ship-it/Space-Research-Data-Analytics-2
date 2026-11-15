import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="tab-research-overview"')
end = html.find('id="tab-research-missions"')
overview_html = html[start:end]

print('Length of overview_html:', len(overview_html))
ids = re.findall(r'id=["\']([^"\']+)["\']', overview_html)
print('IDs in tab-research-overview:', ids)

print("\n--- HTML content sample of tab-research-overview ---")
for line in overview_html.splitlines()[:60]:
    print(line)
