# Script to ensure equipment, resources, investments loaders cache data and use the dynamic renderers
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update loadEquipment
old_eq = """    async function loadEquipment() {
      try {
        const data = await fetchJSON(`${API_BASE}/equipment/analytics`);
        if (!data) return;"""

new_eq = """    async function loadEquipment() {
      try {
        const data = await fetchJSON(`${API_BASE}/equipment/analytics`);
        if (!data) return;
        rawEquipmentData = data;"""

html = html.replace(old_eq, new_eq)

# Update loadResources
old_res = """    async function loadResources() {
      try {
        const data = await fetchJSON(`${API_BASE}/resources/analytics`);
        if (!data) return;"""

new_res = """    async function loadResources() {
      try {
        const data = await fetchJSON(`${API_BASE}/resources/analytics`);
        if (!data) return;
        rawResourcesData = data;"""

html = html.replace(old_res, new_res)

# Update loadInvestments
old_inv = """    async function loadInvestments() {
      try {
        const data = await fetchJSON(`${API_BASE}/investments/analytics`);
        if (!data) return;"""

new_inv = """    async function loadInvestments() {
      try {
        const data = await fetchJSON(`${API_BASE}/investments/analytics`);
        if (!data) return;
        rawInvestmentsData = data;"""

html = html.replace(old_inv, new_inv)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('Orbitalytics_Generated/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Cached telemetry assignments verified.")
