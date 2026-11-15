with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="tab-research-missions"')
end = html.find('id="tab-research-satellites"')
missions_html = html[start:end]

print('Length of missions_html:', len(missions_html))
import re
ids = re.findall(r'id=["\']([^"\']+)["\']', missions_html)
print('IDs in tab-research-missions:', ids)

for l in missions_html.splitlines()[:50]:
    print(l)
