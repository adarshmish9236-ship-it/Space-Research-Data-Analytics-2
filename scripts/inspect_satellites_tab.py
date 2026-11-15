with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="tab-research-satellites"')
end = html.find('id="tab-research-equipment"')
sats_html = html[start:end]

print('Length of sats_html:', len(sats_html))
import re
ids = re.findall(r'id=["\']([^"\']+)["\']', sats_html)
print('IDs in tab-research-satellites:', ids)

for l in sats_html.splitlines()[:50]:
    print(l)
