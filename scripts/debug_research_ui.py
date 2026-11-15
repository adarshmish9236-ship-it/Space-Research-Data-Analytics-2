import re
import json

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Total HTML length: {len(html)} chars, lines: {len(html.splitlines())}")

# Search for switchSubTab definition and usage
subtab_switch = re.search(r'function switchSubTab\([^{]+\)\{(?:[^{}]*\{[^{}]*\})*?[^}]*\}', html)
if not subtab_switch:
    # let's find switchSubTab line number
    for i, line in enumerate(html.splitlines()):
        if 'switchSubTab' in line:
            print(f"Line {i+1}: {line}")

# Find all subtab IDs
subtabs = [
    'research-overview', 'research-missions', 'research-satellites', 'research-launches',
    'research-equipment', 'research-resources', 'research-investments', 'research-geographic',
    'research-forecasting', 'research-optimization', 'research-scenario', 'research-explorer',
    'research-reports'
]

print("\n--- Subtab Element Checks ---")
for st in subtabs:
    # check for div with that ID
    pattern = rf'id=["\']({st}|tab-{st}|subtab-{st}|research-tab-{st})["\']'
    matches = re.findall(pattern, html)
    print(f"{st}: matches {matches}")

# Also check button data-subtab or onclick
print("\n--- Button / Navigation Triggers ---")
for st in subtabs:
    found = st in html
    occurrences = html.count(st)
    print(f"{st}: occurrences = {occurrences}")
