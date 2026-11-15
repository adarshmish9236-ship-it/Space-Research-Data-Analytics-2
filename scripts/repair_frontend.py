import re
import os

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. Clean head
head_start = orig.find('<head>') + len('<head>')
style_start = orig.find('<style>')

clean_head_scripts = """
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ORBITALYTICS 2.0 | Space Big Data Analytics & Predictive Optimization Platform</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
"""

# Extract the style block and body markup
body_start = orig.find('<body')
js_start = orig.find('<!-- JAVASCRIPT APPLICATION CORE -->')

style_block = orig[style_start:body_start]
body_markup = orig[body_start:js_start]

# Check if kpi-missions is in body_markup
if 'id="kpi-missions"' not in body_markup:
    # Add Big Data Executive KPI cards right below the 4 Top Hero OrbitTrack KPI Cards
    hero_cards_marker = '<!-- Middle Section: 3D Globe OrbitTrack & Activity Feed (Reference Image 1) -->'
    kpi_bar_html = """
        <!-- Module 1: Big Data Platform Executive Telemetry Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div class="glass-card p-4 rounded-xl border-sky-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Missions Analysed</span>
            <div id="kpi-missions" class="text-xl font-black text-white font-mono">1,500</div>
            <span class="text-[10px] text-sky-400 font-mono">Cataloged Flights</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-cyan-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Active In Orbit</span>
            <div id="kpi-satellites" class="text-xl font-black text-cyan-400 font-mono">1,850</div>
            <span class="text-[10px] text-cyan-300 font-mono">Operational Constellation</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-emerald-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Launch Reliability</span>
            <div id="kpi-launch-rate" class="text-xl font-black text-emerald-400 font-mono">94.8%</div>
            <span class="text-[10px] text-emerald-300 font-mono">Mission Success</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-purple-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Processed Records</span>
            <div id="kpi-records" class="text-xl font-black text-purple-400 font-mono">9,746</div>
            <span class="text-[10px] text-purple-300 font-mono">HDFS Lakehouse</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-amber-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Cumulative Budget</span>
            <div id="kpi-budget" class="text-xl font-black text-amber-400 font-mono">$184.5B</div>
            <span class="text-[10px] text-amber-300 font-mono">Research Capital</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-rose-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Component Demand</span>
            <div id="kpi-equipment" class="text-xl font-black text-rose-400 font-mono">8,420</div>
            <span class="text-[10px] text-rose-300 font-mono">Units Required</span>
          </div>
        </div>

        """
    body_markup = body_markup.replace(hero_cards_marker, kpi_bar_html + hero_cards_marker)

# Ensure orbittrack-data-records and orbittrack-launch-rate have IDs in the 4 hero cards
body_markup = body_markup.replace('<div class="text-3xl font-black text-purple-400 font-mono tracking-tight">842 GB</div>',
                                  '<div class="text-3xl font-black text-purple-400 font-mono tracking-tight" id="orbittrack-data-records">9,746 Recs</div>')
body_markup = body_markup.replace('<div class="text-3xl font-black text-emerald-400 font-mono tracking-tight">96.4%</div>',
                                  '<div class="text-3xl font-black text-emerald-400 font-mono tracking-tight" id="orbittrack-launch-rate">94.8%</div>')

print("Body markup prepared.")
