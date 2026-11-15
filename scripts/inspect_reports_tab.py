with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="tab-research-reports"')
end = html.find('id="tab-eng-pipeline"')
reports_html = html[start:end]

print('Length of reports_html:', len(reports_html))
for line in reports_html.splitlines():
    print(line)
