with open('scripts/apply_frontend_repair.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Make updateEspiPeriod, toggleEspiFilter, resetEspiFilters async
text = text.replace("function updateEspiPeriod(year) {", "async function updateEspiPeriod(year) {")
text = text.replace("function toggleEspiFilter(filterType, val) {", "async function toggleEspiFilter(filterType, val) {")
text = text.replace("function resetEspiFilters() {", "async function resetEspiFilters() {")

with open('scripts/apply_frontend_repair.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated apply_frontend_repair.py with async ESPI filter functions.")
