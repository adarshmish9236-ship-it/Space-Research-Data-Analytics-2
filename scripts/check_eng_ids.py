with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_pipeline = html.find('id="tab-eng-pipeline"')
pos_js = html.find('<!-- JAVASCRIPT APPLICATION CORE -->')
eng_html = html[pos_pipeline:pos_js]

print(f"Length of eng_html: {len(eng_html)}")
import re
eng_ids = set(re.findall(r'id=["\']([^"\']+)["\']', eng_html))
print("IDs in engineering markup:")
for i in sorted(eng_ids):
    print(" ", i)
