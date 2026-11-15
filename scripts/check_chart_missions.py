with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

for term in ['chart-tab-missions', 'chart-missions-agency', 'renderMissionsChart', 'loadMissions']:
    matches = [m.start() for m in re.finditer(term, html)]
    print(f"\n=== Term: {term} (count {len(matches)}) ===")
    for pos in matches:
        line_no = html[:pos].count('\n') + 1
        # print surrounding line
        start_line = html.rfind('\n', 0, pos) + 1
        end_line = html.find('\n', pos)
        print(f"  Line {line_no}: {html[start_line:end_line].strip()}")
