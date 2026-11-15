import re
import json

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check all IDs in html
all_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
print(f"Total unique IDs in HTML: {len(all_ids)}")

# Research tabs
research_tabs = {
    'research-overview': 'loadOverview',
    'research-missions': 'loadMissions',
    'research-satellites': 'loadSatellites',
    'research-launches': 'loadLaunches',
    'research-equipment': 'loadEquipment',
    'research-resources': 'loadResources',
    'research-investments': 'loadInvestments',
    'research-geographic': 'loadGeographic',
    'research-forecasting': 'runForecast',
    'research-optimization': 'runProcurementOptimization',
    'research-scenario': 'runScenarioAnalysis',
    'research-explorer': 'loadExplorerData',
    'research-reports': 'loadReports' # or downloadReport
}

print("\n--- Subtab container check ---")
for tab_id, func_name in research_tabs.items():
    container_id = f"tab-{tab_id}"
    btn_id = f"sub-btn-{tab_id}"
    print(f"Tab: {tab_id:25} | Container '{container_id}' exists: {container_id in all_ids} | Button '{btn_id}' exists: {btn_id in all_ids}")

# Extract JavaScript code starting from line 4032
lines = html.splitlines()
js_lines = lines[4031:] # from <script>
js_text = "\n".join(js_lines)

# Find all document.getElementById calls in the main JS
dom_get_calls = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", js_text)
print(f"\nTotal document.getElementById calls in main script: {len(dom_get_calls)}")
missing_ids = [elem_id for elem_id in set(dom_get_calls) if elem_id not in all_ids]
print(f"Missing IDs called by JS: {missing_ids}")
