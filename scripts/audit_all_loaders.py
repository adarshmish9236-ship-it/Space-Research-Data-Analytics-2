import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# All IDs in HTML
all_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

# Let's inspect the loader functions defined at the end of the file (lines 5270 to 5690)
# and also any defined between 4032 and 5270.
funcs = [
    'loadOverview', 'loadMissions', 'loadSatellites', 'loadLaunches',
    'loadEquipment', 'loadResources', 'loadInvestments', 'loadGeographic',
    'runForecast', 'runProcurementOptimization', 'runScenarioAnalysis', 'loadExplorerData'
]

print("=== CHECKING DOM IDS USED IN EACH FUNCTION ===")
for fn in funcs:
    # Find all occurrences of this function body
    matches = list(re.finditer(rf'async function {fn}\s*\([^)]*\)\s*\{{', html))
    if not matches:
        matches = list(re.finditer(rf'function {fn}\s*\([^)]*\)\s*\{{', html))
    
    print(f"\nFunction: {fn} (found {len(matches)} definitions)")
    for idx, m in enumerate(matches):
        start = m.start()
        # Find closing brace by counting braces
        brace_count = 0
        end = start
        for i, char in enumerate(html[start:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = start + i + 1
                    break
        
        body = html[start:end]
        line_num = html[:start].count('\n') + 1
        ids_in_body = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", body)
        canvases = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)\.getContext", body)
        missing = [i for i in ids_in_body if i not in all_ids]
        print(f"  Def #{idx+1} at Line {line_num}:")
        print(f"    IDs accessed: {ids_in_body}")
        print(f"    Canvases accessed: {canvases}")
        print(f"    MISSING IDs: {missing}")
