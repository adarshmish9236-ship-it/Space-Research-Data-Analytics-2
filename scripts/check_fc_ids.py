with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'fc-[a-zA-Z0-9_-]+', html)
print('All fc- occurrences in HTML:', set(matches))
