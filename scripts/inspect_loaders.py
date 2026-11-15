with open("E:/PROJECTS/BDT/frontend/index.html", encoding="utf-8") as f:
    text = f.read()

import re

functions = [
    "loadOverview", "loadLaunches", "runForecast", "runProcurementOptimization",
    "runScenarioAnalysis", "loadExplorerData", "loadPipelineStages", "loadCatalog",
    "loadQualityCenter", "runBenchmarkLaboratory", "loadYarnStatus", "loadHdfsOverview", "runHiveQuery"
]

for fn in functions:
    m = re.search(rf'async function {fn}\s*\([^)]*\)\s*\{{[\s\S]*?(?=\n\s*(?:async )?function|\n\s*//\s*\d+|$)', text)
    if m:
        first_30 = "\n".join(m.group(0).splitlines()[:25])
        print(f"=== {fn} ===")
        print(first_30)
        print("...")
