import urllib.request

html = urllib.request.urlopen("http://127.0.0.1:8000/").read().decode("utf-8")
print("HTML length:", len(html))
print("has missions tab:", "tab-research-missions" in html)
print("has satellites tab:", "tab-research-satellites" in html)
print("has equipment tab:", "tab-research-equipment" in html)
print("has resources tab:", "tab-research-resources" in html)
print("has investments tab:", "tab-research-investments" in html)
print("has geographic tab:", "tab-research-geographic" in html)
print("has models tab:", "tab-eng-models" in html)
print("has upload input:", "file-upload-input" in html)
print("has pig section:", "Run 01_missions_etl.pig" in html)
print("has loadMissions JS:", "async function loadMissions" in html)
