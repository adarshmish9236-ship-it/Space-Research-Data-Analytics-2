# Builder for Standardized & Advanced Research Layer (All 13 Subtabs)
import os

research_layer_html = """      <!-- ======================================================== -->
      <!-- SUBTAB 1: EXECUTIVE OVERVIEW                           -->
      <!-- ======================================================== -->
      <div id="tab-research-overview" class="space-y-8">
        <!-- Top Command Header -->
        <div class="glass-card p-6 rounded-2xl border-sky-500/20 bg-gradient-to-r from-space-900/90 via-space-950/80 to-space-900/90 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span class="text-[11px] font-mono font-bold text-emerald-400 uppercase tracking-widest">OrbitTrack Operational Command • System Online</span>
            </div>
            <h2 class="text-2xl font-black text-white tracking-tight flex items-center gap-3">
              Good afternoon, Commander Alex
            </h2>
            <p class="text-sm text-gray-400 mt-1">Global space fleet telemetry, orbital tracking, demand forecasting & algorithmic procurement dispatch.</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-xs font-mono px-3 py-1.5 rounded-lg bg-space-850 border border-gray-800 text-gray-400">
              UTC: <span id="live-utc-clock" class="text-sky-400">--:--:--</span>
            </span>
            <button onclick="downloadReport('pdf')" class="flex items-center gap-2 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold text-xs px-4 py-2.5 rounded-xl shadow-lg shadow-sky-500/20 transition">
              <i data-lucide="download" class="w-4 h-4"></i>
              <span>Export Executive Whitepaper</span>
            </button>
          </div>
        </div>

        <!-- 4 Top Hero OrbitTrack KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-sky-500/20 hover:border-sky-500/40 transition">
            <div class="flex items-center justify-between">
              <span class="text-gray-400 text-xs font-semibold uppercase tracking-wider">Total Satellites</span>
              <div class="w-8 h-8 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center">
                <i data-lucide="satellite" class="w-4 h-4"></i>
              </div>
            </div>
            <div class="text-3xl font-black text-white font-mono tracking-tight" id="orbittrack-total-sats">1,850</div>
            <div class="text-[11px] text-gray-400 flex items-center gap-2 pt-1 border-t border-gray-800/80 font-mono">
              <span class="text-emerald-400 font-semibold" id="orbittrack-operational-sats">1,688 Operational</span>
              <span>•</span>
              <span class="text-amber-400">420 Maint</span>
              <span>•</span>
              <span class="text-rose-400">292 Offline</span>
            </div>
          </div>

          <div class="glass-card p-5 rounded-2xl space-y-2 border-indigo-500/20 hover:border-indigo-500/40 transition">
            <div class="flex items-center justify-between">
              <span class="text-gray-400 text-xs font-semibold uppercase tracking-wider">Active Missions</span>
              <div class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
                <i data-lucide="rocket" class="w-4 h-4"></i>
              </div>
            </div>
            <div class="text-3xl font-black text-sky-400 font-mono tracking-tight" id="orbittrack-active-missions">142</div>
            <div class="text-[11px] text-gray-400 flex items-center gap-2 pt-1 border-t border-gray-800/80 font-mono">
              <span class="text-sky-300 font-semibold">88 In Progress</span>
              <span>•</span>
              <span class="text-indigo-300">54 Scheduled</span>
            </div>
          </div>

          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20 hover:border-purple-500/40 transition">
            <div class="flex items-center justify-between">
              <span class="text-gray-400 text-xs font-semibold uppercase tracking-wider">Lakehouse Storage</span>
              <div class="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
                <i data-lucide="database" class="w-4 h-4"></i>
              </div>
            </div>
            <div class="text-3xl font-black text-purple-400 font-mono tracking-tight" id="orbittrack-data-records">8,130 Recs</div>
            <div class="text-[11px] text-emerald-400 flex items-center gap-1.5 pt-1 border-t border-gray-800/80 font-mono">
              <i data-lucide="trending-up" class="w-3.5 h-3.5"></i>
              <span>+18% Ingestion Today</span>
              <span class="text-gray-500 ml-auto font-normal">HDFS Lakehouse</span>
            </div>
          </div>

          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20 hover:border-emerald-500/40 transition">
            <div class="flex items-center justify-between">
              <span class="text-gray-400 text-xs font-semibold uppercase tracking-wider">Global Constellation Sweep</span>
              <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                <i data-lucide="globe" class="w-4 h-4"></i>
              </div>
            </div>
            <div class="text-3xl font-black text-emerald-400 font-mono tracking-tight" id="orbittrack-launch-rate">92.3%</div>
            <div class="text-[11px] text-emerald-400 flex items-center gap-1.5 pt-1 border-t border-gray-800/80 font-mono">
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span class="font-semibold">Optimal Orbital Sweep</span>
            </div>
          </div>
        </div>

        <!-- 6 Executive Platform Telemetry Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div class="glass-card p-4 rounded-xl border-sky-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Missions Analysed</span>
            <div id="kpi-missions" class="text-xl font-black text-white font-mono">1,500</div>
            <span class="text-[10px] text-sky-400 font-mono">Cataloged Flights</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-cyan-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Active In Orbit</span>
            <div id="kpi-satellites" class="text-xl font-black text-cyan-400 font-mono">1,688</div>
            <span class="text-[10px] text-cyan-300 font-mono">Operational Constellation</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-emerald-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Launch Reliability</span>
            <div id="kpi-launch-rate" class="text-xl font-black text-emerald-400 font-mono">92.3%</div>
            <span class="text-[10px] text-emerald-300 font-mono">Mission Success</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-purple-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Processed Records</span>
            <div id="kpi-records" class="text-xl font-black text-purple-400 font-mono">8,130</div>
            <span class="text-[10px] text-purple-300 font-mono">HDFS Lakehouse</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-amber-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Cumulative Budget</span>
            <div id="kpi-budget" class="text-xl font-black text-amber-400 font-mono">$2,460.05B</div>
            <span class="text-[10px] text-amber-300 font-mono">Research Capital</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-rose-500/20 space-y-1">
            <span class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Component Demand</span>
            <div id="kpi-equipment" class="text-xl font-black text-rose-400 font-mono">161,600</div>
            <span class="text-[10px] text-rose-300 font-mono">Units Required</span>
          </div>
        </div>

        <!-- 3D Orbit Globe & Constellation Streams -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div class="glass-card p-6 rounded-2xl lg:col-span-7 space-y-4 relative overflow-hidden flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <i data-lucide="orbit" class="w-4 h-4 text-sky-400"></i>
                  Live 3D Orbital Trajectory & Ephemeris Visualization
                </h3>
                <p class="text-xs text-gray-400">Planetary projection with real-time LEO, MEO, GEO & Sun-Sync satellites</p>
              </div>
              <div class="flex items-center gap-3 text-xs font-mono">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span> Active (1,688)</span>
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-400"></span> Maint (420)</span>
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-rose-400"></span> Offline (292)</span>
              </div>
            </div>

            <div class="relative h-80 rounded-xl bg-space-950 border border-gray-800/80 flex items-center justify-center overflow-hidden">
              <canvas id="canvas-orbit-globe" class="w-full h-full cursor-grab"></canvas>
              <div class="absolute top-4 left-4 bg-space-900/90 backdrop-blur border border-sky-500/30 px-3 py-1.5 rounded-lg text-xs font-mono text-sky-300 shadow-lg">
                <span class="text-white font-bold">ORBIT-02:</span> 542 km • LEO Sun-Sync (Starlink / OneWeb)
              </div>
              <div class="absolute bottom-4 left-4 bg-space-900/90 backdrop-blur border border-emerald-500/30 px-3 py-1.5 rounded-lg text-xs font-mono text-emerald-300 shadow-lg">
                <span class="text-white font-bold">ORBIT-03:</span> 860 km • Polar Circular (Earth Observation)
              </div>
              <div class="absolute top-4 right-4 bg-space-900/90 backdrop-blur border border-purple-500/30 px-3 py-1.5 rounded-lg text-xs font-mono text-purple-300 shadow-lg">
                <span class="text-white font-bold">ORBIT-01:</span> 518 km • Equatorial LEO (ISS / Tiangong)
              </div>
            </div>

            <div class="flex items-center justify-between text-xs text-gray-400 font-mono pt-2 border-t border-gray-800">
              <span>Projection: WGS84 Geodetic • Epoch J2026.4</span>
              <span class="text-sky-400">Constellations: Starlink, OneWeb, GPS III, Galileo, NavIC</span>
            </div>
          </div>

          <!-- Earth Observation & Telemetry Feed -->
          <div class="glass-card p-6 rounded-2xl lg:col-span-5 space-y-4 flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="bar-chart-2" class="w-4 h-4 text-emerald-400"></i>
                Mission & Sensor Telemetry Metrics
              </h3>
              <span class="text-[11px] font-mono text-emerald-400">LIVE FEED</span>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-xl bg-space-900/90 border border-gray-800">
                <span class="text-gray-400 text-[11px]">Downlinked Frames</span>
                <div class="text-lg font-black text-white font-mono mt-0.5">14,248 frames</div>
                <span class="text-[10px] text-emerald-400 font-mono">↑ 14.2% daily yield</span>
              </div>
              <div class="p-3 rounded-xl bg-space-900/90 border border-gray-800">
                <span class="text-gray-400 text-[11px]">Data Processed</span>
                <div class="text-lg font-black text-sky-400 font-mono mt-0.5">8.42 TB / Day</div>
                <span class="text-[10px] text-sky-300 font-mono">↑ 28% PySpark Speedup</span>
              </div>
              <div class="p-3 rounded-xl bg-space-900/90 border border-gray-800">
                <span class="text-gray-400 text-[11px]">Optical Resolution</span>
                <div class="text-lg font-black text-indigo-400 font-mono mt-0.5">0.31 m / px</div>
                <span class="text-[10px] text-indigo-300 font-mono">Multi-spectral SAR</span>
              </div>
              <div class="p-3 rounded-xl bg-space-900/90 border border-gray-800">
                <span class="text-gray-400 text-[11px]">Pipeline Latency</span>
                <div class="text-lg font-black text-emerald-400 font-mono mt-0.5">1.82 sec</div>
                <span class="text-[10px] text-emerald-300 font-mono">Real-Time Ingestion</span>
              </div>
            </div>

            <div class="space-y-2 pt-2 border-t border-gray-800">
              <div class="flex justify-between text-xs font-mono">
                <span class="text-gray-400">Data Stream Distribution</span>
                <span class="text-white">100% Total Bandwidth</span>
              </div>
              <div class="w-full bg-space-950 rounded-full h-3 flex overflow-hidden border border-gray-800">
                <div class="bg-sky-500 h-full" style="width: 52%" title="Imagery 52%"></div>
                <div class="bg-indigo-500 h-full" style="width: 28%" title="Telemetry 28%"></div>
                <div class="bg-purple-500 h-full" style="width: 20%" title="Other 20%"></div>
              </div>
              <div class="flex justify-between text-[10px] text-gray-400 font-mono">
                <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-sky-500"></span> Synthetic Aperture Radar (SAR) 52%</span>
                <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-indigo-500"></span> Health Telemetry 28%</span>
                <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-purple-500"></span> Deep-Space Signals 20%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- High-Impact Dual Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="bar-chart-3" class="w-4 h-4 text-sky-400"></i>
                Mission Flight Distribution by Major Space Agency
              </h3>
              <span class="text-[11px] font-mono text-gray-400">Fact Table Aggregation</span>
            </div>
            <div class="h-64">
              <canvas id="chart-missions-agency"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="pie-chart" class="w-4 h-4 text-indigo-400"></i>
                Active Satellite Orbit Regime Proportions
              </h3>
              <span class="text-[11px] font-mono text-gray-400">Constellation Ephemeris</span>
            </div>
            <div class="h-64">
              <canvas id="chart-satellites-orbit"></canvas>
            </div>
          </div>
        </div>

        <!-- Strategic Intelligence Insights Feed -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-white text-sm flex items-center gap-2">
              <i data-lucide="sparkles" class="w-4 h-4 text-amber-400"></i>
              Strategic Analytics & Actionable Intelligence Feed
            </h3>
            <span class="text-xs text-sky-400 font-mono">Automated Lakehouse Synthesizer</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4" id="insights-container">
            <!-- Dynamically populated via loadOverview() -->
          </div>
        </div>
      </div>
"""

print("Executive overview HTML snippet ready.")
import os
import re

# We will generate a complete, production-grade, advanced Research Layer with all 13 subtabs.
# Each subtab includes:
# 1. Advanced Header with real-time operational badges and controls.
# 2. Advanced 4-KPI Telemetry Metric Grid with delta/trend indicators.
# 3. Interactive Filter Bar (Agency/Orbit/Risk/Date filters and dynamic search input).
# 4. Multi-Chart Interactive Visualizations (e.g. Bar, Doughnut, Line, Scatter, Stacked).
# 5. Searchable, Paginated, Rich-Data Table with color-coded badges, progress bars, and CSV export.
# 6. Deep Analytical Breakdown or Diagnostics panel.

p2_missions = """
      <!-- ======================================================== -->
      <!-- SUBTAB 2: SPACE MISSIONS MASTER INTELLIGENCE           -->
      <!-- ======================================================== -->
      <div id="tab-research-missions" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-sky-400"></span>
              <span class="text-[11px] font-mono font-bold text-sky-400 uppercase tracking-widest">Global Space Flight Registry (2010–2026)</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Space Missions Master Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">
                1,500 FLIGHTS CATALOGED
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Multi-agency deep exploration missions, budgetary commitments, payload profiles, and mission success classification.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('missions-agency-body', 'space_missions_analytics.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadMissions()" class="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-sky-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Missions</span>
            </button>
          </div>
        </div>

        <!-- 4 Advanced KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-sky-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Cataloged Missions</span>
              <i data-lucide="rocket" class="w-4 h-4 text-sky-400"></i>
            </div>
            <div id="missions-total-count" class="text-3xl font-black text-white font-mono">1,500</div>
            <div class="text-[11px] text-emerald-400 font-mono flex items-center gap-1">
              <i data-lucide="check-circle-2" class="w-3 h-3"></i>
              <span>100% Ingested into Silver/Gold Lakehouse</span>
            </div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Cumulative Budget</span>
              <i data-lucide="dollar-sign" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div id="missions-total-budget" class="text-3xl font-black text-emerald-400 font-mono">$2,460.1B</div>
            <div class="text-[11px] text-gray-400 font-mono">International Appropriations</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Mean Payload Mass</span>
              <i data-lucide="weight" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div id="missions-avg-payload" class="text-3xl font-black text-purple-400 font-mono">9,280 kg</div>
            <div class="text-[11px] text-purple-300 font-mono">Heavy Lift Capability Tier</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-cyan-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Mission Success Rate</span>
              <i data-lucide="shield-check" class="w-4 h-4 text-cyan-400"></i>
            </div>
            <div id="missions-success-rate" class="text-3xl font-black text-cyan-400 font-mono">96.8%</div>
            <div class="text-[11px] text-emerald-400 font-mono">High-Reliability Envelope</div>
          </div>
        </div>

        <!-- Interactive Filter & Search Bar -->
        <div class="glass-card p-4 rounded-xl flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="relative">
              <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
              <input type="text" id="filter-mission-search" oninput="filterMissionsTable()" placeholder="Search agency or mission..." class="bg-space-900 border border-gray-800 rounded-lg pl-9 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:border-sky-500 outline-none w-56 font-mono">
            </div>
            <select id="filter-mission-agency" onchange="filterMissionsTable()" class="bg-space-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-sky-500 outline-none">
              <option value="ALL">All Space Agencies</option>
              <option value="NASA">NASA (USA)</option>
              <option value="ISRO">ISRO (India)</option>
              <option value="ESA">ESA (Europe)</option>
              <option value="Roscosmos">Roscosmos (Russia)</option>
              <option value="CNSA">CNSA (China)</option>
              <option value="JAXA">JAXA (Japan)</option>
            </select>
            <select id="filter-mission-tier" onchange="filterMissionsTable()" class="bg-space-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-sky-500 outline-none">
              <option value="ALL">All Budget Tiers</option>
              <option value="HIGH">> $400B Portfolio</option>
              <option value="MED">$200B - $400B</option>
              <option value="LOW">< $200B</option>
            </select>
          </div>
          <div class="text-xs font-mono text-gray-400 flex items-center gap-2">
            <span>Sort by:</span>
            <button onclick="sortMissionsTable('volume')" class="px-2.5 py-1 rounded bg-space-800 text-sky-400 font-bold hover:bg-space-700 transition">Volume ↓</button>
            <button onclick="sortMissionsTable('budget')" class="px-2.5 py-1 rounded bg-space-800 text-gray-300 hover:text-white transition">Budget</button>
            <button onclick="sortMissionsTable('reliability')" class="px-2.5 py-1 rounded bg-space-800 text-gray-300 hover:text-white transition">Reliability</button>
          </div>
        </div>

        <!-- Dual Analytical Visualizations -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="bar-chart-3" class="w-4 h-4 text-sky-400"></i>
                Mission Volume by International Space Agency
              </h3>
              <span class="text-[11px] font-mono text-sky-400">Categorical Bar Analysis</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-missions"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="pie-chart" class="w-4 h-4 text-purple-400"></i>
                Mission Type Breakdown (Astrophysics, Crewed, Earth Obs)
              </h3>
              <span class="text-[11px] font-mono text-purple-400">Doughnut Share</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-mission-types"></canvas>
            </div>
          </div>
        </div>

        <!-- Master Agency Missions Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Agency Mission Operations Profile</h3>
              <p class="text-xs text-gray-400 mt-0.5">Aggregated flight counts, total appropriations, mean payload mass, and validated success percentages.</p>
            </div>
            <span class="text-xs font-mono text-gray-400" id="missions-table-count">Showing 7 International Agencies</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Space Agency</th>
                  <th class="py-3 px-4">Mission Flights</th>
                  <th class="py-3 px-4">Allocated Budget</th>
                  <th class="py-3 px-4">Mean Payload</th>
                  <th class="py-3 px-4">Success Reliability</th>
                  <th class="py-3 px-4">Operational Status</th>
                </tr>
              </thead>
              <tbody id="missions-agency-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

p3_satellites = """
      <!-- ======================================================== -->
      <!-- SUBTAB 3: SATELLITES & ORBITS INTELLIGENCE               -->
      <!-- ======================================================== -->
      <div id="tab-research-satellites" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
              <span class="text-[11px] font-mono font-bold text-cyan-400 uppercase tracking-widest">Constellation Ephemeris & Orbital Mechanics</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Orbital Satellites Ephemeris & Constellation Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
                2,400 OBJECTS TRACKED
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">LEO, MEO, GEO, and Sun-Synchronous orbital parameters, lifespan expectations, operational status and constellation decay telemetry.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('sats-table-body', 'satellite_constellations.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadSatellites()" class="flex items-center gap-2 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-cyan-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Satellites</span>
            </button>
          </div>
        </div>

        <!-- 4 Satellites KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-cyan-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Total Cataloged Payloads</span>
              <i data-lucide="satellite" class="w-4 h-4 text-cyan-400"></i>
            </div>
            <div class="text-3xl font-black text-white font-mono">2,400</div>
            <div class="text-[11px] text-cyan-400 font-mono">Norad & Space-Track Synced</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Active In Orbit</span>
              <i data-lucide="activity" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div id="sats-active-count" class="text-3xl font-black text-emerald-400 font-mono">1,688</div>
            <div class="text-[11px] text-emerald-300 font-mono">70.3% Fully Operational</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-amber-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Maintenance & Standby</span>
              <i data-lucide="wrench" class="w-4 h-4 text-amber-400"></i>
            </div>
            <div class="text-3xl font-black text-amber-400 font-mono">420</div>
            <div class="text-[11px] text-amber-300 font-mono">Attitude & Deorbit Thrusters</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Mean Orbital Lifespan</span>
              <i data-lucide="clock" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div class="text-3xl font-black text-purple-400 font-mono">10.2 Years</div>
            <div class="text-[11px] text-purple-300 font-mono">Radiation Tolerant Bus</div>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="glass-card p-4 rounded-xl flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="relative">
              <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
              <input type="text" id="filter-sat-search" oninput="filterSatellitesTable()" placeholder="Search orbit regime..." class="bg-space-900 border border-gray-800 rounded-lg pl-9 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:border-cyan-500 outline-none w-56 font-mono">
            </div>
            <select id="filter-sat-regime" onchange="filterSatellitesTable()" class="bg-space-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-cyan-500 outline-none">
              <option value="ALL">All Regimes</option>
              <option value="LEO">LEO (Low Earth Orbit)</option>
              <option value="SSO">SSO (Sun-Synchronous)</option>
              <option value="MEO">MEO (Medium Earth Orbit)</option>
              <option value="GEO">GEO (Geostationary)</option>
              <option value="HEO">HEO (Highly Elliptical)</option>
            </select>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono text-gray-400">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> 70% Active
            <span class="w-2.5 h-2.5 rounded-full bg-amber-400 ml-2"></span> 18% Maint
            <span class="w-2.5 h-2.5 rounded-full bg-rose-400 ml-2"></span> 12% Decommissioned
          </div>
        </div>

        <!-- Dual Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="layers" class="w-4 h-4 text-cyan-400"></i>
                Orbital Regime Distribution (SSO, LEO, GEO, Polar)
              </h3>
              <span class="text-[11px] font-mono text-cyan-400">Object Density</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-sats-orbits"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
                Operational Status Breakdown
              </h3>
              <span class="text-[11px] font-mono text-emerald-400">Health Telemetry</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-sats-status"></canvas>
            </div>
          </div>
        </div>

        <!-- Satellites Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Orbital Regimes & Constellation Ephemeris</h3>
              <p class="text-xs text-gray-400 mt-0.5">Altitude profiles, design lifespan, and constellation share across all cataloged orbits.</p>
            </div>
            <span class="text-xs font-mono text-gray-400" id="sats-table-count">6 Orbital Regimes</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Orbit Regime</th>
                  <th class="py-3 px-4">Satellites Count</th>
                  <th class="py-3 px-4">Mean Altitude (km)</th>
                  <th class="py-3 px-4">Mean Lifespan</th>
                  <th class="py-3 px-4">Constellation Share</th>
                  <th class="py-3 px-4">Regime Status</th>
                </tr>
              </thead>
              <tbody id="sats-table-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

p4_launches = """
      <!-- ======================================================== -->
      <!-- SUBTAB 4: LAUNCH INTELLIGENCE (ESPI FULL DASHBOARD)      -->
      <!-- ======================================================== -->
      <div id="tab-research-launches" class="space-y-6 hidden">
        <!-- ESPI Master Header -->
        <div class="glass-card p-5 rounded-2xl border-amber-500/20 bg-gradient-to-r from-space-950 via-space-900 to-space-950 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 font-bold text-lg">
              <i data-lucide="rocket" class="w-6 h-6"></i>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-black tracking-widest text-amber-400 font-mono">ESPI SPECIFICATION</span>
                <span class="text-[10px] px-2 py-0.5 rounded bg-gray-800 text-gray-300 font-mono">Global Space Activity 2000–2026</span>
              </div>
              <h2 class="text-2xl font-black text-white tracking-tight mt-0.5">Orbital Launches Intelligence</h2>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('launch-vehicles-body', 'launch_vehicles.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="resetEspiFilters()" class="text-xs font-mono text-gray-400 hover:text-white px-3 py-1.5 rounded-lg border border-gray-800 hover:border-gray-700 transition">
              Reset Filters
            </button>
          </div>
        </div>

        <!-- ESPI Interactive Dynamic Filter Bar -->
        <div class="glass-card p-5 rounded-2xl space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-gray-800">
            <div class="space-y-1">
              <span class="text-xs font-semibold text-gray-300 uppercase tracking-wider">Analysis Observation Window</span>
              <div class="text-lg font-black text-white font-mono" id="espi-period-label">2000 — 2026</div>
            </div>
            <div class="flex-1 max-w-md">
              <input type="range" id="espi-period-slider" min="2005" max="2026" value="2026" oninput="updateEspiPeriod(this.value)" class="w-full accent-amber-500 cursor-pointer">
              <div class="flex justify-between text-[10px] text-gray-500 font-mono mt-1">
                <span>2000</span><span>2005</span><span>2010</span><span>2015</span><span>2020</span><span>2026</span>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap items-center justify-between gap-4 text-xs font-mono">
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-gray-400 mr-1">Territories:</span>
              <button onclick="toggleEspiFilter('territory', 'USA')" class="px-2.5 py-1 rounded-lg bg-sky-500/20 text-sky-400 border border-sky-500/30 font-bold">USA</button>
              <button onclick="toggleEspiFilter('territory', 'India')" class="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">India</button>
              <button onclick="toggleEspiFilter('territory', 'Russia')" class="px-2.5 py-1 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 font-bold">Russia</button>
              <button onclick="toggleEspiFilter('territory', 'China')" class="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">China</button>
              <button onclick="toggleEspiFilter('territory', 'Europe')" class="px-2.5 py-1 rounded-lg bg-purple-500/20 text-purple-400 border border-purple-500/30 font-bold">Europe</button>
              <button onclick="toggleEspiFilter('territory', 'Japan')" class="px-2.5 py-1 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/30 font-bold">Japan</button>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-gray-400 mr-1">Sector:</span>
              <button onclick="toggleEspiFilter('ownership', 'Private')" class="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">Commercial</button>
              <button onclick="toggleEspiFilter('ownership', 'Public')" class="px-2.5 py-1 rounded-lg bg-sky-500/20 text-sky-400 border border-sky-500/30 font-bold">Institutional</button>
            </div>
          </div>
        </div>

        <!-- 4 ESPI Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Orbital Launches by Outcome</h3>
                <p class="text-xs text-gray-400">Success vs Partial vs Catastrophic Failure</p>
              </div>
              <span class="text-[11px] font-mono text-emerald-400">92.3% Success</span>
            </div>
            <div class="h-60">
              <canvas id="chart-espi-outcome"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Launch Provider Distribution (Private vs Public)</h3>
                <p class="text-xs text-gray-400">Commercial dominance over institutional flights</p>
              </div>
              <span class="text-[11px] font-mono text-amber-400">65% Commercial</span>
            </div>
            <div class="h-60">
              <canvas id="chart-espi-provider"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Cumulative Launches by Sovereign Territory</h3>
                <p class="text-xs text-gray-400">National spaceport launch tallies</p>
              </div>
              <span class="text-[11px] font-mono text-sky-400">Top 6 Powers</span>
            </div>
            <div class="h-60">
              <canvas id="chart-espi-territory-bar"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Annual Territory Trend Progression</h3>
                <p class="text-xs text-gray-400">Longitudinal flight cadence across key nations</p>
              </div>
              <span class="text-[11px] font-mono text-purple-400">2010–2026 Trend</span>
            </div>
            <div class="h-60">
              <canvas id="chart-espi-territory-trend"></canvas>
            </div>
          </div>
        </div>

        <!-- Launch Vehicles Master Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Launch Vehicle Reliability & Payload Economics</h3>
              <p class="text-xs text-gray-400 mt-0.5">Heavy, Medium, and Small launch vehicles with total mass inserted and cost per mission.</p>
            </div>
            <span class="text-xs font-mono text-gray-400">10 Primary Vehicle Families</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Vehicle Family</th>
                  <th class="py-3 px-4">Total Launches</th>
                  <th class="py-3 px-4">Success Reliability</th>
                  <th class="py-3 px-4">Total Payload Mass</th>
                  <th class="py-3 px-4">Mean Launch Cost</th>
                  <th class="py-3 px-4">Cadence Status</th>
                </tr>
              </thead>
              <tbody id="launch-vehicles-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

print("Missions, Satellites, Launches HTML ready.")
p5_equipment = """
      <!-- ======================================================== -->
      <!-- SUBTAB 5: EQUIPMENT & COMPONENT DEMAND                  -->
      <!-- ======================================================== -->
      <div id="tab-research-equipment" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-amber-400"></span>
              <span class="text-[11px] font-mono font-bold text-amber-400 uppercase tracking-widest">Supply Chain & Avionics Manufacturing</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Space Flight Equipment & Component Demand
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono">
                SUPPLY CHAIN TELEMETRY
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Component order volume, unit costs, procurement lead times, supplier bottlenecks, and shortage risk metrics.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('equipment-table-body', 'equipment_demand_components.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadEquipment()" class="flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-amber-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Equipment</span>
            </button>
          </div>
        </div>

        <!-- 4 Equipment KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-amber-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Total Units Demanded</span>
              <i data-lucide="cpu" class="w-4 h-4 text-amber-400"></i>
            </div>
            <div id="eq-total-units" class="text-3xl font-black text-white font-mono">162,725</div>
            <div class="text-[11px] text-amber-300 font-mono">1,616 Ingested Order Lines</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Cumulative Economic Value</span>
              <i data-lucide="badge-dollar-sign" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div id="eq-total-value" class="text-3xl font-black text-emerald-400 font-mono">$87.3B</div>
            <div class="text-[11px] text-emerald-300 font-mono">Precision Avionics & Solar Array</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-rose-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>High Shortage Risk Lines</span>
              <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400"></i>
            </div>
            <div class="text-3xl font-black text-rose-400 font-mono">38 Critical</div>
            <div class="text-[11px] text-rose-300 font-mono">745 Medium • 833 Low</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Mean Lead Time</span>
              <i data-lucide="clock" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div class="text-3xl font-black text-purple-400 font-mono">214 Days</div>
            <div class="text-[11px] text-purple-300 font-mono">Cleanroom Fabrication Cycle</div>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="glass-card p-4 rounded-xl flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="relative">
              <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
              <input type="text" id="filter-eq-search" oninput="filterEquipmentTable()" placeholder="Search component..." class="bg-space-900 border border-gray-800 rounded-lg pl-9 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:border-amber-500 outline-none w-56 font-mono">
            </div>
            <select id="filter-eq-risk" onchange="filterEquipmentTable()" class="bg-space-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-amber-500 outline-none">
              <option value="ALL">All Risk Tiers</option>
              <option value="CRITICAL">High Bottleneck Risk</option>
              <option value="MEDIUM">Medium Risk</option>
              <option value="OPTIMAL">Low / Optimal Supply</option>
            </select>
          </div>
          <div class="text-xs font-mono text-gray-400 flex items-center gap-2">
            <span>Sort by:</span>
            <button onclick="sortEquipmentTable('units')" class="px-2.5 py-1 rounded bg-space-800 text-amber-400 font-bold hover:bg-space-700 transition">Units Demanded ↓</button>
            <button onclick="sortEquipmentTable('value')" class="px-2.5 py-1 rounded bg-space-800 text-gray-300 hover:text-white transition">Total Value</button>
            <button onclick="sortEquipmentTable('leadtime')" class="px-2.5 py-1 rounded bg-space-800 text-gray-300 hover:text-white transition">Lead Time</button>
          </div>
        </div>

        <!-- Component Demand Visualization -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div class="glass-card p-6 rounded-2xl lg:col-span-8 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="bar-chart-2" class="w-4 h-4 text-amber-400"></i>
                Component Unit Demand by Category
              </h3>
              <span class="text-[11px] font-mono text-amber-400">Supply Requirement</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-equipment"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl lg:col-span-4 space-y-4 flex flex-col justify-between">
            <div>
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="shield-alert" class="w-4 h-4 text-rose-400"></i>
                Critical Supply Bottlenecks
              </h3>
              <p class="text-xs text-gray-400 mt-1">Lead time anomalies & cleanroom constraints</p>
            </div>
            <div class="space-y-3 font-mono text-xs">
              <div class="p-3 rounded-xl bg-space-900 border border-rose-500/30 flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">Rad-750 Space CPUs</div>
                  <div class="text-[10px] text-rose-400">Lead time: 252 days</div>
                </div>
                <span class="px-2 py-0.5 rounded bg-rose-950 text-rose-300 text-[10px]">CRITICAL</span>
              </div>
              <div class="p-3 rounded-xl bg-space-900 border border-amber-500/30 flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">Solar Array Panels</div>
                  <div class="text-[10px] text-amber-400">Lead time: 198 days</div>
                </div>
                <span class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 text-[10px]">WARNING</span>
              </div>
              <div class="p-3 rounded-xl bg-space-900 border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <div class="font-bold text-white">Xenon Thruster Coils</div>
                  <div class="text-[10px] text-emerald-400">Lead time: 112 days</div>
                </div>
                <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 text-[10px]">OPTIMAL</span>
              </div>
            </div>
            <div class="text-[11px] text-gray-400 font-mono pt-2 border-t border-gray-800">
              <span>Optimization: Run HiGHS dispatch in Subtab 10</span>
            </div>
          </div>
        </div>

        <!-- Equipment Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Avionics, Propulsion & Scientific Hardware Registry</h3>
              <p class="text-xs text-gray-400 mt-0.5">Component order volume, unit costs, procurement lead times, and bottleneck risk indicators.</p>
            </div>
            <span class="text-xs font-mono text-gray-400">8 Standard Categories</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Component Classification</th>
                  <th class="py-3 px-4">Units Demanded</th>
                  <th class="py-3 px-4">Mean Unit Cost</th>
                  <th class="py-3 px-4">Total Portfolio Value</th>
                  <th class="py-3 px-4">Mean Lead Time</th>
                  <th class="py-3 px-4">Supply Bottleneck</th>
                </tr>
              </thead>
              <tbody id="equipment-table-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

p6_resources = """
      <!-- ======================================================== -->
      <!-- SUBTAB 6: RESOURCE CONSUMPTION TELEMETRY                 -->
      <!-- ======================================================== -->
      <div id="tab-research-resources" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-rose-400"></span>
              <span class="text-[11px] font-mono font-bold text-rose-400 uppercase tracking-widest">Cryogenic Propellants & Life Support Commodities</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Propellant & Cryogenic Resource Consumption
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono">
                CRYOGENIC DEPOT SCADA
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Liquid Oxygen (LOX), Rocket Propellant (RP-1), Liquid Hydrogen (LH2), and Xenon consumption telemetry and inventory burn-rates.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('resources-table-body', 'resource_consumption.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadResources()" class="flex items-center gap-2 bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-rose-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Resources</span>
            </button>
          </div>
        </div>

        <!-- 4 Resources KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-rose-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Total Consumables</span>
              <i data-lucide="flame" class="w-4 h-4 text-rose-400"></i>
            </div>
            <div id="res-total-consumed" class="text-3xl font-black text-white font-mono">280.2k Units</div>
            <div class="text-[11px] text-rose-300 font-mono">1,414 Ingested SCADA Batches</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Cumulative Commodity Value</span>
              <i data-lucide="coins" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div id="res-total-cost" class="text-3xl font-black text-purple-400 font-mono">$8,420M</div>
            <div class="text-[11px] text-purple-300 font-mono">Refined Cryogenic Propellants</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-amber-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Monthly Burn Rate</span>
              <i data-lucide="gauge" class="w-4 h-4 text-amber-400"></i>
            </div>
            <div class="text-3xl font-black text-amber-400 font-mono">24.5k Units / Mo</div>
            <div class="text-[11px] text-amber-300 font-mono">High Launch Cadence Envelope</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Depot Buffer Reserve</span>
              <i data-lucide="shield" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div class="text-3xl font-black text-emerald-400 font-mono">92.4% Optimal</div>
            <div class="text-[11px] text-emerald-300 font-mono">Boil-Off Losses Under 0.8%</div>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="glass-card p-4 rounded-xl flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="relative">
              <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
              <input type="text" id="filter-res-search" oninput="filterResourcesTable()" placeholder="Search propellant / commodity..." class="bg-space-900 border border-gray-800 rounded-lg pl-9 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:border-rose-500 outline-none w-56 font-mono">
            </div>
            <select id="filter-res-type" onchange="filterResourcesTable()" class="bg-space-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-rose-500 outline-none">
              <option value="ALL">All Propellants & Gases</option>
              <option value="LOX">Liquid Oxygen (LOX)</option>
              <option value="RP1">Rocket Propellant (RP-1)</option>
              <option value="LH2">Liquid Hydrogen (LH2)</option>
              <option value="Xenon">High-Purity Xenon</option>
            </select>
          </div>
          <div class="text-xs font-mono text-gray-400">
            <span>Aggregated from 7 Cryogenic Launch Sites</span>
          </div>
        </div>

        <!-- Visualizations -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div class="glass-card p-6 rounded-2xl lg:col-span-8 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="bar-chart" class="w-4 h-4 text-rose-400"></i>
                Resource Consumption by Commodity Name
              </h3>
              <span class="text-[11px] font-mono text-rose-400">Burn Volume</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-resources"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl lg:col-span-4 space-y-4 flex flex-col justify-between">
            <div>
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="battery-charging" class="w-4 h-4 text-emerald-400"></i>
                Depot Storage & Safety Stock
              </h3>
              <p class="text-xs text-gray-400 mt-1">Cryogenic storage tank telemetry</p>
            </div>
            <div class="space-y-3 font-mono text-xs">
              <div>
                <div class="flex justify-between mb-1"><span>Liquid Oxygen (LOX)</span><span class="text-emerald-400">94%</span></div>
                <div class="w-full bg-space-950 rounded-full h-2"><div class="bg-emerald-400 h-full rounded-full" style="width: 94%"></div></div>
              </div>
              <div>
                <div class="flex justify-between mb-1"><span>Liquid Hydrogen (LH2)</span><span class="text-amber-400">76%</span></div>
                <div class="w-full bg-space-950 rounded-full h-2"><div class="bg-amber-400 h-full rounded-full" style="width: 76%"></div></div>
              </div>
              <div>
                <div class="flex justify-between mb-1"><span>Xenon Gas Reserve</span><span class="text-sky-400">88%</span></div>
                <div class="w-full bg-space-950 rounded-full h-2"><div class="bg-sky-400 h-full rounded-full" style="width: 88%"></div></div>
              </div>
            </div>
            <div class="text-[11px] text-gray-400 font-mono pt-2 border-t border-gray-800">
              <span>Automatic Top-Off Protocol Active</span>
            </div>
          </div>
        </div>

        <!-- Resources Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Space Research Resource & Propellant Inventory</h3>
              <p class="text-xs text-gray-400 mt-0.5">Total units consumed, monthly burn averages, and total commodity cost valuations.</p>
            </div>
            <span class="text-xs font-mono text-gray-400">7 Primary Commodities</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Commodity / Resource Name</th>
                  <th class="py-3 px-4">Total Consumed (Units)</th>
                  <th class="py-3 px-4">Mean Monthly Burn</th>
                  <th class="py-3 px-4">Cumulative Valuation</th>
                  <th class="py-3 px-4">Supply Health</th>
                </tr>
              </thead>
              <tbody id="resources-table-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

print("Equipment and Resources HTML ready.")
p7_investments = """
      <!-- ======================================================== -->
      <!-- SUBTAB 7: RESEARCH INVESTMENTS & DECADAL BUDGETS         -->
      <!-- ======================================================== -->
      <div id="tab-research-investments" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
              <span class="text-[11px] font-mono font-bold text-indigo-400 uppercase tracking-widest">Capital Expenditures & Decadal Portfolios</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Space Research Investment Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">
                LONG-TERM CAPITAL BUDGETS
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Multi-agency decadal research appropriations, R&D vs infrastructure vs operations splits, and future exploratory mission commitments.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('future-projects-body', 'decadal_research_projects.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadInvestments()" class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-indigo-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Investments</span>
            </button>
          </div>
        </div>

        <!-- 4 Investments KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-indigo-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Cumulative Expenditure</span>
              <i data-lucide="wallet" class="w-4 h-4 text-indigo-400"></i>
            </div>
            <div id="inv-total-spend" class="text-3xl font-black text-white font-mono">$332.9B</div>
            <div class="text-[11px] text-indigo-300 font-mono">1,414 Validated Budget Lines</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-sky-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Lead Agency Expenditure</span>
              <i data-lucide="building-2" class="w-4 h-4 text-sky-400"></i>
            </div>
            <div class="text-3xl font-black text-sky-400 font-mono">$108.9B</div>
            <div class="text-[11px] text-sky-300 font-mono">NASA (R&D, Ops, Deep Space)</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Decadal Flagship Projects</span>
              <i data-lucide="sparkles" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div class="text-3xl font-black text-purple-400 font-mono">10 Active</div>
            <div class="text-[11px] text-purple-300 font-mono">TRL-6 to TRL-8 Readiness</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Mean Decadal Budget</span>
              <i data-lucide="trending-up" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div class="text-3xl font-black text-emerald-400 font-mono">$5.82B</div>
            <div class="text-[11px] text-emerald-300 font-mono">Per Strategic Mission</div>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="glass-card p-4 rounded-xl flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="relative">
              <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
              <input type="text" id="filter-inv-search" oninput="filterInvestmentsTable()" placeholder="Search decadal project..." class="bg-space-900 border border-gray-800 rounded-lg pl-9 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:border-indigo-500 outline-none w-56 font-mono">
            </div>
            <select id="filter-inv-trl" onchange="filterInvestmentsTable()" class="bg-space-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-indigo-500 outline-none">
              <option value="ALL">All Readiness Levels (TRL)</option>
              <option value="HIGH">TRL 7-8 (Flight Proven / Ready)</option>
              <option value="MID">TRL 5-6 (Prototype / Validation)</option>
              <option value="LOW">TRL 3-4 (Concept Lab Study)</option>
            </select>
          </div>
          <div class="text-xs font-mono text-gray-400 flex items-center gap-2">
            <span>Funding Distribution:</span>
            <span class="text-sky-400 font-bold">45% R&D</span>
            <span class="text-indigo-400 font-bold ml-1">30% Infra</span>
            <span class="text-purple-400 font-bold ml-1">25% Ops</span>
          </div>
        </div>

        <!-- Stacked Expenditure Visualizations -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-sm">Decadal Expenditure Composition by Agency (R&D, Infra, Ops)</h3>
              <p class="text-xs text-gray-400 mt-0.5">Stacked breakdown of sovereign research investments in millions USD</p>
            </div>
            <span class="text-[11px] font-mono text-indigo-400">Stacked Bar Analysis</span>
          </div>
          <div class="h-72">
            <canvas id="chart-tab-investments"></canvas>
          </div>
        </div>

        <!-- Future Projects Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Decadal Deep-Space Exploration Projects</h3>
              <p class="text-xs text-gray-400 mt-0.5">Target commencement timeline, estimated capital budgets, priority tier, and technology readiness level (TRL).</p>
            </div>
            <span class="text-xs font-mono text-gray-400">10 Flagship Missions</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Project Identifier</th>
                  <th class="py-3 px-4">Mission Title</th>
                  <th class="py-3 px-4">Lead Agency / Consortium</th>
                  <th class="py-3 px-4">Est. Investment</th>
                  <th class="py-3 px-4">Launch Year</th>
                  <th class="py-3 px-4">TRL Level</th>
                  <th class="py-3 px-4">Execution Phase</th>
                </tr>
              </thead>
              <tbody id="future-projects-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

p8_geographic = """
      <!-- ======================================================== -->
      <!-- SUBTAB 8: TERRITORY & SPACEPORTS GEOGRAPHIC            -->
      <!-- ======================================================== -->
      <div id="tab-research-geographic" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span class="text-[11px] font-mono font-bold text-emerald-400 uppercase tracking-widest">Geopolitical Spaceports & Launch Infrastructure</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Territory & Spaceport Geographic Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                GLOBAL LAUNCH BASES
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Geographic coordinates, historical launch volumes, downrange corridors, and commercial vs sovereign state ownership shares.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('spaceports-table-body', 'spaceports_registry.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadGeographic()" class="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-emerald-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Territory</span>
            </button>
          </div>
        </div>

        <!-- 4 Geo KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-2 border-emerald-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Sovereign Spaceports Tracked</span>
              <i data-lucide="map-pin" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div class="text-3xl font-black text-white font-mono">7 Global Bases</div>
            <div class="text-[11px] text-emerald-300 font-mono">Baikonur, KSC, Sriharikota, Kourou, Jiuquan</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-sky-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Leading Launch Territory</span>
              <i data-lucide="flag" class="w-4 h-4 text-sky-400"></i>
            </div>
            <div class="text-3xl font-black text-sky-400 font-mono">USA (307 Launches)</div>
            <div class="text-[11px] text-sky-300 font-mono">25.6% Global Launch Share</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-amber-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Commercial Sector Share</span>
              <i data-lucide="trending-up" class="w-4 h-4 text-amber-400"></i>
            </div>
            <div class="text-3xl font-black text-amber-400 font-mono">65.2%</div>
            <div class="text-[11px] text-amber-300 font-mono">782 Commercial vs 418 State</div>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-2 border-purple-500/20">
            <div class="flex justify-between items-center text-xs font-medium text-gray-400">
              <span>Total Mass Inserted</span>
              <i data-lucide="weight" class="w-4 h-4 text-purple-400"></i>
            </div>
            <div class="text-3xl font-black text-purple-400 font-mono">14.8M kg</div>
            <div class="text-[11px] text-purple-300 font-mono">14,800 Metric Tons to Orbit</div>
          </div>
        </div>

        <!-- Dual Geographic Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="bar-chart-2" class="w-4 h-4 text-emerald-400"></i>
                Total Orbital Launches by Sovereign Territory
              </h3>
              <span class="text-[11px] font-mono text-emerald-400">Sovereign Volumes</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-territories"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm flex items-center gap-2">
                <i data-lucide="pie-chart" class="w-4 h-4 text-sky-400"></i>
                Private Commercial vs Public Institutional Share
              </h3>
              <span class="text-[11px] font-mono text-sky-400">Ownership Doughnut</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tab-ownership"></canvas>
            </div>
          </div>
        </div>

        <!-- Spaceports Registry Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Global Orbital Launch Spaceport Registry</h3>
              <p class="text-xs text-gray-400 mt-0.5">Geographic coordinates, historical launch volumes, success rates, and commercial ownership percentages.</p>
            </div>
            <span class="text-xs font-mono text-gray-400">7 Active Spaceports</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Spaceport Complex</th>
                  <th class="py-3 px-4">Territory</th>
                  <th class="py-3 px-4">Sovereign Country</th>
                  <th class="py-3 px-4">Total Launches</th>
                  <th class="py-3 px-4">Success Reliability</th>
                  <th class="py-3 px-4">Commercial Share</th>
                  <th class="py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody id="spaceports-table-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

print("Investments and Geographic HTML ready.")
p9_forecasting = """
      <!-- ======================================================== -->
      <!-- SUBTAB 9: PREDICTIVE FORECASTING STUDIO                 -->
      <!-- ======================================================== -->
      <div id="tab-research-forecasting" class="space-y-8 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
              <span class="text-[11px] font-mono font-bold text-cyan-400 uppercase tracking-widest">Multi-Model Autoregressive & Machine Learning Engine</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Predictive Demand Forecasting Studio
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
                CHAMPION / CHALLENGER ML
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Multi-target time series forecasting with statistically grounded 90%/95% prediction intervals, backtesting metrics, and feature attribution.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="runForecast()" class="flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-sky-600 hover:from-cyan-400 hover:to-sky-500 text-white font-semibold text-xs px-4 py-2.5 rounded-xl shadow-lg shadow-cyan-500/20 transition">
              <i data-lucide="play" class="w-4 h-4"></i>
              <span>Generate Forecast</span>
            </button>
          </div>
        </div>

        <!-- Controls Card with Dynamic Presets -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div>
              <label class="block text-gray-400 font-medium mb-1.5">Forecasting Target</label>
              <select id="fc-target" class="w-full bg-space-900 border border-gray-800 rounded-lg p-2.5 text-white font-mono focus:border-cyan-500 outline-none">
                <option value="equipment_rad_cpu">Space Flight Equipment (CPUs, Avionics)</option>
                <option value="resource_propellant">Propellant & Cryogenics (LOX, LH2)</option>
                <option value="satellites_launch">Satellite Orbital Insertion Demand</option>
                <option value="research_budget">Deep Space Decadal Appropriations</option>
              </select>
            </div>
            <div>
              <label class="block text-gray-400 font-medium mb-1.5">Algorithm Architecture</label>
              <select id="fc-model" class="w-full bg-space-900 border border-gray-800 rounded-lg p-2.5 text-white font-mono focus:border-cyan-500 outline-none">
                <option value="auto">🏆 Auto Champion Selection (Lowest RMSE)</option>
                <option value="random_forest">Random Forest Regressor (Ensemble)</option>
                <option value="xgboost">XGBoost Gradient Boosting</option>
                <option value="arima">ARIMA / SARIMAX (p=2, d=1, q=2)</option>
                <option value="holt_winters">Holt-Winters Triple Exponential Smoothing</option>
                <option value="linear">Baseline Trend Projection</option>
              </select>
            </div>
            <div>
              <label class="block text-gray-400 font-medium mb-1.5">Forecast Horizon</label>
              <select id="fc-horizon" class="w-full bg-space-900 border border-gray-800 rounded-lg p-2.5 text-white font-mono focus:border-cyan-500 outline-none">
                <option value="4">4 Future Quarters (1 Year Horizon)</option>
                <option value="8">8 Future Quarters (2 Years Horizon)</option>
                <option value="12">12 Future Quarters (3 Years Horizon)</option>
                <option value="20">20 Future Quarters (5-Year Strategic Outlook)</option>
              </select>
            </div>
            <div>
              <label class="block text-gray-400 font-medium mb-1.5">Geopolitical Scenario</label>
              <select id="fc-scenario" class="w-full bg-space-900 border border-gray-800 rounded-lg p-2.5 text-white font-mono focus:border-cyan-500 outline-none">
                <option value="baseline">Baseline (Historical Growth Trajectory)</option>
                <option value="accelerated">Accelerated (Decadal Expansion +25%)</option>
                <option value="constrained">Constrained (Fiscal Austerity -15%)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 4 Key ML Metric Badges -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
          <div class="glass-card p-4 rounded-xl border-cyan-500/20">
            <span class="text-[11px] text-gray-400 uppercase">Selected Target</span>
            <div id="fc-chart-title" class="text-lg font-black text-white mt-0.5">Space Flight Equipment (Units)</div>
            <span class="text-[10px] text-cyan-400">Quarterly Aggregation</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-amber-500/20">
            <span class="text-[11px] text-gray-400 uppercase">Model Hierarchy</span>
            <div id="fc-champion-badge" class="text-lg font-black text-amber-400 mt-0.5">Champion: RANDOM FOREST</div>
            <span class="text-[10px] text-amber-300">Autoregressive Feature Pipeline</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-emerald-500/20">
            <span class="text-[11px] text-gray-400 uppercase">Generalization Accuracy</span>
            <div id="fc-test-rmse" class="text-lg font-black text-emerald-400 mt-0.5">Test RMSE: 424.38 Units</div>
            <span class="text-[10px] text-emerald-300">WAPE: 9.3% • MAPE: 9.08%</span>
          </div>
          <div class="glass-card p-4 rounded-xl border-purple-500/20">
            <span class="text-[11px] text-gray-400 uppercase">Confidence Interval</span>
            <div class="text-lg font-black text-purple-400 mt-0.5">95% Two-Sided Band</div>
            <span class="text-[10px] text-purple-300">Heteroskedastic Variance</span>
          </div>
        </div>

        <!-- Master Forecast Line Chart with Confidence Bands -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-white text-base">Historical Observations vs Machine Learning Forecast (with 95% Confidence Interval)</h3>
              <p class="text-xs text-gray-400 mt-0.5" id="fc-explanation">Autoregressive tree ensemble trained on 16 historical quarters with feature lagged covariates.</p>
            </div>
            <div class="flex items-center gap-3 text-xs font-mono">
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span> Historical</span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span> Predicted Mean</span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-sky-500/30"></span> 95% Confidence Band</span>
            </div>
          </div>
          <div class="h-80">
            <canvas id="chart-forecast"></canvas>
          </div>
        </div>

        <!-- Leaderboard & Feature Importance Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- Model Leaderboard Table (Col 7) -->
          <div class="glass-card p-6 rounded-2xl lg:col-span-7 space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Forecasting Model Tournament Leaderboard</h3>
                <p class="text-xs text-gray-400">Comparative backtesting metrics across Statistical, ML & Baseline algorithms</p>
              </div>
              <span class="text-xs font-mono text-cyan-400">Chronological Split</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs font-mono">
                <thead class="text-gray-400 border-b border-gray-800">
                  <tr>
                    <th class="py-2.5 px-3">Algorithm</th>
                    <th class="py-2.5 px-3">Family</th>
                    <th class="py-2.5 px-3">RMSE</th>
                    <th class="py-2.5 px-3">MAE</th>
                    <th class="py-2.5 px-3">WAPE</th>
                    <th class="py-2.5 px-3">Tournament Status</th>
                  </tr>
                </thead>
                <tbody id="fc-leaderboard-body" class="divide-y divide-gray-800/60">
                  <!-- Injected via JS -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- Feature Importance Chart (Col 5) -->
          <div class="glass-card p-6 rounded-2xl lg:col-span-5 space-y-4 flex flex-col justify-between">
            <div>
              <h3 class="font-bold text-white text-sm">Feature Importance Attribution</h3>
              <p class="text-xs text-gray-400">Permutation feature weights in the Champion model</p>
            </div>
            <div class="h-60">
              <canvas id="chart-feature-importance"></canvas>
            </div>
            <div class="text-[11px] text-gray-500 font-mono pt-2 border-t border-gray-800">
              <span>Primary Driver: Prior quarter cleanroom demand + 4-quarter rolling mean</span>
            </div>
          </div>
        </div>
      </div>
"""

p10_optimization = """
      <!-- ======================================================== -->
      <!-- SUBTAB 10: OPTIMIZATION & SHORTAGE STUDIO               -->
      <!-- ======================================================== -->
      <div id="tab-research-optimization" class="space-y-8 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span class="text-[11px] font-mono font-bold text-emerald-400 uppercase tracking-widest">Mathematical Operations Research & Prescriptive Planning</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Demand-to-Capacity Optimization Studio
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                PRESCRIPTIVE HiGHS SOLVER
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Constrained linear optimization (SciPy HiGHS) balancing budget ceilings, supplier lead-time bottlenecks, and mission criticality penalties.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('opt-allocations-body', 'procurement_allocations.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export Allocations</span>
            </button>
            <button onclick="runProcurementOptimization()" class="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-semibold text-xs px-4 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition">
              <i data-lucide="calculator" class="w-4 h-4"></i>
              <span>Run HiGHS Solver</span>
            </button>
          </div>
        </div>

        <!-- 3 Quick Optimization Trigger Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-3 border-emerald-500/20">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm">Constrained Procurement Dispatch</h3>
              <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono font-bold">CORE LP</span>
            </div>
            <p class="text-xs text-gray-400 leading-relaxed">
              Solves bounded linear program minimizing shortage penalty subject to $60M budget ceiling and supplier lead-time capacity.
            </p>
            <button onclick="runProcurementOptimization()" class="w-full bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs py-2 rounded-xl font-semibold transition flex items-center justify-center gap-2">
              <i data-lucide="play" class="w-3.5 h-3.5"></i> Execute HiGHS Dispatch
            </button>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-3 border-rose-500/20">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm">Supply-Demand Deficit Audit</h3>
              <span class="text-[10px] px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-mono font-bold">GAP ANALYSIS</span>
            </div>
            <p class="text-xs text-gray-400 leading-relaxed">
              Examines projected shortage vs expected supply lines, categorizing risk into CRITICAL, MODERATE, and OPTIMAL.
            </p>
            <button onclick="runDemandGap()" class="w-full bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs py-2 rounded-xl font-semibold transition flex items-center justify-center gap-2">
              <i data-lucide="search" class="w-3.5 h-3.5"></i> Audit Deficit Gaps
            </button>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-3 border-sky-500/20">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-white text-sm">Stochastic Safety Stock Planner</h3>
              <span class="text-[10px] px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 font-mono font-bold">ROP CALC</span>
            </div>
            <p class="text-xs text-gray-400 leading-relaxed">
              Calculates safety stock & Reorder Point (ROP) with 95% service level protection against cleanroom supply delays.
            </p>
            <button onclick="runInventoryPlan()" class="w-full bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 text-xs py-2 rounded-xl font-semibold transition flex items-center justify-center gap-2">
              <i data-lucide="layers" class="w-3.5 h-3.5"></i> Compute Safety Stock
            </button>
          </div>
        </div>

        <!-- Optimization Results Header Card -->
        <div class="glass-card p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span id="opt-solver-status" class="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                OPTIMAL_SOLVED
              </span>
              <span id="opt-runtime" class="text-xs text-gray-400 font-mono">Runtime: 4.2 ms</span>
            </div>
            <h3 id="opt-results-title" class="text-lg font-black text-white">Constrained Procurement Allocation (SciPy HiGHS Solver)</h3>
            <p id="opt-results-subtitle" class="text-xs text-gray-400 font-mono">Total Spend: $104.98M of $60.0M Budget | Overall Fulfillment: 100.0%</p>
          </div>
          <div class="flex items-center gap-3 font-mono text-xs">
            <div class="p-3 rounded-xl bg-space-900 border border-gray-800 text-center">
              <span class="text-gray-400 text-[10px] block">CRITICAL PENALTY</span>
              <span class="text-amber-400 font-bold">2.5x Weight</span>
            </div>
            <div class="p-3 rounded-xl bg-space-900 border border-gray-800 text-center">
              <span class="text-gray-400 text-[10px] block">BUDGET CONSTRAIN</span>
              <span class="text-emerald-400 font-bold">Active Upper Bound</span>
            </div>
          </div>
        </div>

        <!-- Master Procurement Allocations Table -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-white text-base">Optimal Component Procurement & Safety Buffer Schedule</h3>
            <span class="text-xs font-mono text-gray-400">8 Constrained Hardware Items</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
              <thead class="text-gray-400 border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Component Item</th>
                  <th class="py-3 px-4">Forecast Demand</th>
                  <th class="py-3 px-4">Allocated Units</th>
                  <th class="py-3 px-4">Optimized Cost</th>
                  <th class="py-3 px-4">Fulfillment %</th>
                  <th class="py-3 px-4">Net Shortage</th>
                  <th class="py-3 px-4">Criticality Tier</th>
                  <th class="py-3 px-4">Bottleneck Status</th>
                </tr>
              </thead>
              <tbody id="opt-allocations-body" class="divide-y divide-gray-800/60">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

print("Forecasting and Optimization HTML ready.")
p11_scenario = """
      <!-- ======================================================== -->
      <!-- SUBTAB 11: DIGITAL TWIN & SCENARIO STUDIO                -->
      <!-- ======================================================== -->
      <div id="tab-research-scenario" class="space-y-8 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
              <span class="text-[11px] font-mono font-bold text-indigo-400 uppercase tracking-widest">Stochastic Simulation & Policy Sensitivity</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Space Research Digital Twin & Scenario Studio
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">
                MONTE CARLO & SENSITIVITY
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Interactive policy sliders, stochastic Monte Carlo simulations (500 draws), and Tornado sensitivity ranking of key system stressors.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="runScenarioAnalysis()" class="flex items-center gap-2 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-semibold text-xs px-4 py-2.5 rounded-xl shadow-lg shadow-indigo-500/20 transition">
              <i data-lucide="play" class="w-4 h-4"></i>
              <span>Simulate Scenarios</span>
            </button>
          </div>
        </div>

        <!-- Interactive Policy Sliders -->
        <div class="glass-card p-6 rounded-2xl space-y-6">
          <h3 class="font-bold text-white text-sm flex items-center gap-2">
            <i data-lucide="sliders" class="w-4 h-4 text-indigo-400"></i>
            Digital Twin Policy Levers & Stress Test Parameters
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="space-y-2">
              <div class="flex justify-between text-xs font-mono">
                <span class="text-gray-400">Budget Growth Rate</span>
                <span class="text-sky-400 font-bold" id="val-slider-budget">10%</span>
              </div>
              <input type="range" id="slider-budget" min="-30" max="50" value="10" oninput="updateScenarioSliders()" class="w-full accent-sky-500 cursor-pointer">
              <div class="flex justify-between text-[10px] text-gray-500 font-mono">
                <span>-30% Austerity</span>
                <span>0% Stable</span>
                <span>+50% Decadal Surge</span>
              </div>
            </div>

            <div class="space-y-2">
              <div class="flex justify-between text-xs font-mono">
                <span class="text-gray-400">Launch Cadence Multiplier</span>
                <span class="text-indigo-400 font-bold" id="val-slider-cadence">5%</span>
              </div>
              <input type="range" id="slider-cadence" min="-25" max="40" value="5" oninput="updateScenarioSliders()" class="w-full accent-indigo-500 cursor-pointer">
              <div class="flex justify-between text-[10px] text-gray-500 font-mono">
                <span>-25% Slowdown</span>
                <span>0% Steady</span>
                <span>+40% Mega-Constellation</span>
              </div>
            </div>

            <div class="space-y-2">
              <div class="flex justify-between text-xs font-mono">
                <span class="text-gray-400">Supply Chain Price Inflation</span>
                <span class="text-rose-400 font-bold" id="val-slider-inflation">3%</span>
              </div>
              <input type="range" id="slider-inflation" min="0" max="25" value="3" oninput="updateScenarioSliders()" class="w-full accent-rose-500 cursor-pointer">
              <div class="flex justify-between text-[10px] text-gray-500 font-mono">
                <span>0% Normal</span>
                <span>+10% Moderate</span>
                <span>+25% Severe Disruption</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Scenario Cards Grid -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-white text-sm">Simulated Mission Trajectories vs System Stress Index</h3>
            <span class="text-xs text-gray-400 font-mono">4 Discrete Policy Futures</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="scenario-cards-container">
            <!-- Populated via runScenarioAnalysis() -->
          </div>
        </div>

        <!-- Dual Stochastic & Tornado Visualizations -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Sensitivity Tornado Analysis (Expenditure Swing in $M)</h3>
                <p class="text-xs text-gray-400">Parameter influence ranking on annual budget variance</p>
              </div>
              <span class="text-[11px] font-mono text-rose-400">Tornado Swing</span>
            </div>
            <div class="h-64">
              <canvas id="chart-tornado"></canvas>
            </div>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Monte Carlo Distribution (500 Iteration Draws)</h3>
                <p class="text-xs text-gray-400">Stochastic budget outcome probability density</p>
              </div>
              <button onclick="runMonteCarloSimulation()" class="text-xs font-mono text-purple-400 hover:text-purple-300">Re-sample</button>
            </div>
            <div class="h-64">
              <canvas id="chart-monte-carlo"></canvas>
            </div>
          </div>
        </div>
      </div>
"""

p12_explorer = """
      <!-- ======================================================== -->
      <!-- SUBTAB 12: LAKEHOUSE DATA EXPLORER                       -->
      <!-- ======================================================== -->
      <div id="tab-research-explorer" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-sky-400"></span>
              <span class="text-[11px] font-mono font-bold text-sky-400 uppercase tracking-widest">Hive & Parquet Schema Inspector</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Lakehouse Data Explorer
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">
                INTERACTIVE PARQUET VIEWER
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Browse, filter, and inspect raw CSV, Silver cleansed, and Gold partitioned Parquet space research tables.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="exportTableToCSV('explorer-body', 'lakehouse_data_export.csv')" class="flex items-center gap-2 bg-space-850 hover:bg-space-800 text-gray-300 font-semibold text-xs px-3.5 py-2 rounded-xl border border-gray-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Export CSV</span>
            </button>
            <button onclick="loadExplorerData()" class="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs px-4 py-2 rounded-xl shadow-lg shadow-sky-600/20 transition">
              <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              <span>Refresh Explorer</span>
            </button>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3 w-full sm:w-auto">
              <label class="text-xs font-mono text-gray-400 whitespace-nowrap">Lakehouse Table:</label>
              <select id="explorer-dataset-select" onchange="loadExplorerData()" class="bg-space-900 border border-gray-800 rounded-lg p-2.5 text-xs text-white font-mono focus:border-sky-500 outline-none w-full sm:w-80">
                <option value="agency_missions">hive_space_dw.fact_space_missions (Gold Parquet)</option>
                <option value="satellites">hive_space_dw.dim_orbital_regimes (Gold Parquet)</option>
                <option value="equipment">hive_space_dw.agg_equipment_demand (Gold Parquet)</option>
                <option value="resources">hive_space_dw.agg_resource_burn (Gold Parquet)</option>
                <option value="investments">hive_space_dw.agg_decadal_investments (Gold Parquet)</option>
              </select>
            </div>
            <div class="flex items-center gap-3">
              <div class="relative">
                <i data-lucide="search" class="w-3.5 h-3.5 text-gray-400 absolute left-3 top-2.5"></i>
                <input type="text" id="filter-explorer-search" oninput="filterExplorerTable()" placeholder="Quick filter rows..." class="bg-space-900 border border-gray-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-gray-500 focus:border-sky-500 outline-none w-48 font-mono">
              </div>
              <span id="explorer-row-count" class="text-xs text-gray-400 font-mono">Showing 15 sample records</span>
            </div>
          </div>

          <div class="overflow-x-auto border border-gray-800/80 rounded-xl">
            <table class="w-full text-left text-xs font-mono">
              <thead id="explorer-head" class="text-gray-400 bg-space-900/60 border-b border-gray-800">
                <!-- Dynamically generated headers -->
              </thead>
              <tbody id="explorer-body" class="divide-y divide-gray-800/60">
                <!-- Dynamically populated via loadExplorerData() -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

p13_reports = """
      <!-- ======================================================== -->
      <!-- SUBTAB 13: RESEARCH REPORTS & LAKEHOUSE EXPORTS          -->
      <!-- ======================================================== -->
      <div id="tab-research-reports" class="space-y-8 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span class="text-[11px] font-mono font-bold text-emerald-400 uppercase tracking-widest">Enterprise Document Generation & Lakehouse Dispatch</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Research Reports & Data Lakehouse Exports
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                ONE-CLICK SYNTHESIS
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Download formal PDF whitepapers, multi-sheet analytical Excel workbooks, or raw validated CSV data extracts.</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4 border-rose-500/20 flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-12 h-12 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center">
                <i data-lucide="file-text" class="w-6 h-6"></i>
              </div>
              <h3 class="font-bold text-white text-base">Executive Research Whitepaper</h3>
              <p class="text-xs text-gray-400 leading-relaxed">
                Formal multi-page PDF generated via ReportLab containing mission telemetry, satellite ephemeris, time-series forecasting benchmarks, and HiGHS optimization schedules.
              </p>
              <div class="p-3 rounded-xl bg-space-900 border border-gray-800 text-[11px] font-mono text-gray-400 space-y-1">
                <div>Format: <span class="text-white">PDF Document (.pdf)</span></div>
                <div>Engine: <span class="text-rose-400">ReportLab Flowable Canvas</span></div>
                <div>Security: <span class="text-emerald-400">SHA-256 Checksummed</span></div>
              </div>
            </div>
            <button onclick="downloadReport('pdf')" class="w-full bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs py-2.5 rounded-xl font-semibold transition flex items-center justify-center gap-2">
              <i data-lucide="download" class="w-4 h-4"></i> Download PDF Whitepaper
            </button>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4 border-emerald-500/20 flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                <i data-lucide="table" class="w-6 h-6"></i>
              </div>
              <h3 class="font-bold text-white text-base">Lakehouse Analytical Workbook</h3>
              <p class="text-xs text-gray-400 leading-relaxed">
                Multi-sheet Excel workbook generated via openpyxl featuring 9 dataset summaries, HDFS lakehouse blocks, Hive analytical query results, and formatted pivot tables.
              </p>
              <div class="p-3 rounded-xl bg-space-900 border border-gray-800 text-[11px] font-mono text-gray-400 space-y-1">
                <div>Format: <span class="text-white">Excel Spreadsheet (.xlsx)</span></div>
                <div>Engine: <span class="text-emerald-400">openpyxl Styled Engine</span></div>
                <div>Sheets: <span class="text-sky-400">9 Lakehouse Domains</span></div>
              </div>
            </div>
            <button onclick="downloadReport('excel')" class="w-full bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs py-2.5 rounded-xl font-semibold transition flex items-center justify-center gap-2">
              <i data-lucide="download" class="w-4 h-4"></i> Download Excel Workbook
            </button>
          </div>

          <div class="glass-card p-6 rounded-2xl space-y-4 border-sky-500/20 flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-12 h-12 rounded-xl bg-sky-500/10 text-sky-400 flex items-center justify-center">
                <i data-lucide="database" class="w-6 h-6"></i>
              </div>
              <h3 class="font-bold text-white text-base">Curated CSV Lakehouse Extract</h3>
              <p class="text-xs text-gray-400 leading-relaxed">
                Direct CSV extract of sanitized, schema-validated space research datasets for offline statistical analysis or ingestion into external BI suites.
              </p>
              <div class="p-3 rounded-xl bg-space-900 border border-gray-800 text-[11px] font-mono text-gray-400 space-y-1">
                <div>Format: <span class="text-white">Delimited Text (.csv)</span></div>
                <div>Standard: <span class="text-sky-400">RFC 4180 Compliant</span></div>
                <div>Dataset: <span class="text-amber-400">Active Selected Domain</span></div>
              </div>
            </div>
            <button onclick="downloadReport('csv')" class="w-full bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 text-xs py-2.5 rounded-xl font-semibold transition flex items-center justify-center gap-2">
              <i data-lucide="download" class="w-4 h-4"></i> Download Curated CSV
            </button>
          </div>
        </div>
      </div>
"""

full_research_layer = research_layer_html + p2_missions + p3_satellites + p4_launches + p5_equipment + p6_resources + p7_investments + p8_geographic + p9_forecasting + p10_optimization + p11_scenario + p12_explorer + p13_reports

print(f"Full research layer constructed: {len(full_research_layer)} characters.")

# Now replace the research layer in frontend/index.html
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

start_marker = '<div id="tab-research-overview"'
end_marker = '<!-- ======================================================== -->\n      <!-- TAB 8: ENGINEERING - PIPELINE ORCHESTRATOR'
if end_marker not in orig:
    end_marker = 'id="tab-eng-pipeline"'

pos_start = orig.find(start_marker)
pos_end = orig.find(end_marker)

rebuilt_html = orig[:pos_start] + full_research_layer + "\n      " + orig[pos_end:]

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)

with open('Orbitalytics_Generated/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt_html)

print("Saved updated frontend/index.html and Orbitalytics_Generated/frontend/index.html successfully!")
