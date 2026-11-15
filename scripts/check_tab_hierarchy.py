import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

subtabs = [
    'research-overview', 'research-missions', 'research-satellites', 'research-launches',
    'research-equipment', 'research-resources', 'research-investments', 'research-geographic',
    'research-forecasting', 'research-optimization', 'research-scenario', 'research-explorer',
    'research-reports',
    'eng-pipeline', 'eng-catalog', 'eng-quality', 'eng-lineage',
    'eng-hdfs', 'eng-hive', 'eng-mapreduce', 'eng-spark', 'eng-benchmarks', 'eng-yarn', 'eng-models'
]

print("=== TAB POSITIONS IN HTML ===")
tab_positions = []
for st in subtabs:
    pos = html.find(f'id="tab-{st}"')
    line_no = html[:pos].count('\n') + 1 if pos != -1 else -1
    print(f"tab-{st:25} : index = {pos:7} (line {line_no:5})")
    if pos != -1:
        tab_positions.append((pos, line_no, st))

tab_positions.sort()
print("\n=== ORDER IN FILE ===")
for p, l, st in tab_positions:
    print(f"Line {l:5}: tab-{st}")
