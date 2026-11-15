with open('scripts/apply_frontend_repair.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Make switchSubTab async
text = text.replace(
    "function switchSubTab(tabId) {",
    "async function switchSubTab(tabId) {"
)
text = text.replace(
    "loadOverview().then(() => setTimeout(initOrbitGlobe, 120));",
    "await loadOverview(); setTimeout(initOrbitGlobe, 120);"
)
text = text.replace("loadMissions();", "await loadMissions();")
text = text.replace("loadSatellites();", "await loadSatellites();")
text = text.replace("loadLaunches();", "await loadLaunches();")
text = text.replace("loadEquipment();", "await loadEquipment();")
text = text.replace("loadResources();", "await loadResources();")
text = text.replace("loadInvestments();", "await loadInvestments();")
text = text.replace("loadGeographic();", "await loadGeographic();")
text = text.replace("runForecast();", "await runForecast();")
text = text.replace("runProcurementOptimization();", "await runProcurementOptimization();")
text = text.replace("runScenarioAnalysis();", "await runScenarioAnalysis();")
text = text.replace("loadExplorerData();", "await loadExplorerData();")
text = text.replace("loadReports();", "await loadReports();")

# Safe requestAnimationFrame
text = text.replace(
    "let globeAnimId = null;",
    "let globeAnimId = null;\n    const reqAnim = (typeof requestAnimationFrame !== 'undefined') ? requestAnimationFrame : (cb => setTimeout(cb, 16));\n    const cancelAnim = (typeof cancelAnimationFrame !== 'undefined') ? cancelAnimationFrame : (id => clearTimeout(id));"
)
text = text.replace(
    "globeAnimId = requestAnimationFrame(render);",
    "globeAnimId = reqAnim(render);"
)
text = text.replace(
    "if (globeAnimId) cancelAnimationFrame(globeAnimId);",
    "if (globeAnimId) cancelAnim(globeAnimId);"
)

with open('scripts/apply_frontend_repair.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated apply_frontend_repair.py with async switchSubTab and safe reqAnim.")
