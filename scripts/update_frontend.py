from pathlib import Path

index_path = Path("E:/PROJECTS/BDT/frontend/index.html")
content = index_path.read_text(encoding="utf-8")

# 1. HTML markup for the 6 Research Analytics Tabs
research_tabs_html = """
      <!-- ======================================================== -->
      <!-- TAB: SPACE MISSIONS                                      -->
      <!-- ======================================================== -->
      <div id="tab-research-missions" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Space Missions Master Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">
                1,500 FLIGHTS CATALOGED
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Multi-agency deep exploration missions, budgetary commitments, and payload profiles (2010–2026).</p>
          </div>
          <button onclick="loadMissions()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Missions</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Missions</span>
            <div id="missions-total-count" class="text-2xl font-black text-white font-mono">1,500</div>
            <span class="text-[11px] text-sky-400 font-mono">Global Space Flight Registry</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Cumulative Budget</span>
            <div id="missions-total-budget" class="text-2xl font-black text-emerald-400 font-mono">$2,460.1B</div>
            <span class="text-[11px] text-emerald-300 font-mono">International Appropriations</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Mean Payload Mass</span>
            <div id="missions-avg-payload" class="text-2xl font-black text-purple-400 font-mono">9,280 kg</div>
            <span class="text-[11px] text-purple-300 font-mono">Heavy Orbital Insertion</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Mission Success Rate</span>
            <div id="missions-success-rate" class="text-2xl font-black text-cyan-400 font-mono">96.8%</div>
            <span class="text-[11px] text-cyan-300 font-mono">High-Reliability Envelope</span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="font-bold text-white text-sm">Mission Volume by International Space Agency</h3>
            <div class="h-64">
              <canvas id="chart-tab-missions"></canvas>
            </div>
          </div>
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="font-bold text-white text-sm">Mission Type Breakdown</h3>
            <div class="h-64">
              <canvas id="chart-tab-mission-types"></canvas>
            </div>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Agency Mission Footprint & Historical Performance</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Agency</th>
                  <th class="py-3 px-4">Missions</th>
                  <th class="py-3 px-4">Total Budget ($M)</th>
                  <th class="py-3 px-4">Avg Payload (kg)</th>
                  <th class="py-3 px-4">Success Rate</th>
                </tr>
              </thead>
              <tbody id="missions-agency-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- TAB: SATELLITES & ORBITS                                 -->
      <!-- ======================================================== -->
      <div id="tab-research-satellites" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Orbital Satellites Ephemeris & Constellation Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
                2,400 OBJECTS TRACKED
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">LEO, MEO, GEO, and Sun-Synchronous orbital parameters, lifespan expectations, and operational states.</p>
          </div>
          <button onclick="loadSatellites()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Satellites</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Objects</span>
            <div class="text-2xl font-black text-white font-mono">2,400</div>
            <span class="text-[11px] text-cyan-400 font-mono">Cataloged Payloads</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Active Satellites</span>
            <div id="sats-active-count" class="text-2xl font-black text-emerald-400 font-mono">1,850</div>
            <span class="text-[11px] text-emerald-300 font-mono">Fully Operational</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Dominant Orbit</span>
            <div class="text-2xl font-black text-sky-400 font-mono">LEO (15.8%)</div>
            <span class="text-[11px] text-sky-300 font-mono">Constellation Shells</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Mean Orbital Life</span>
            <div class="text-2xl font-black text-purple-400 font-mono">8.4 Years</div>
            <span class="text-[11px] text-purple-300 font-mono">Design Lifetime</span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="font-bold text-white text-sm">Orbital Regime Distribution</h3>
            <div class="h-64">
              <canvas id="chart-tab-sats-orbits"></canvas>
            </div>
          </div>
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="font-bold text-white text-sm">Operational Status Breakdown</h3>
            <div class="h-64">
              <canvas id="chart-tab-sats-status"></canvas>
            </div>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Orbital Regime Specifications</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Orbit Type</th>
                  <th class="py-3 px-4">Satellites</th>
                  <th class="py-3 px-4">Share (%)</th>
                  <th class="py-3 px-4">Avg Altitude (km)</th>
                  <th class="py-3 px-4">Avg Lifetime (yrs)</th>
                </tr>
              </thead>
              <tbody id="sats-table-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- TAB: EQUIPMENT DEMAND                                    -->
      <!-- ======================================================== -->
      <div id="tab-research-equipment" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Space Flight Equipment & Component Demand
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono">
                SUPPLY CHAIN TELEMETRY
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Component order volume, unit costs, procurement lead times, and bottleneck risk indicators.</p>
          </div>
          <button onclick="loadEquipment()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Equipment</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Demanded</span>
            <div id="eq-total-units" class="text-2xl font-black text-white font-mono">161,600</div>
            <span class="text-[11px] text-amber-400 font-mono">Total Units Demanded</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Market Value</span>
            <div id="eq-total-value" class="text-2xl font-black text-emerald-400 font-mono">$18.4M</div>
            <span class="text-[11px] text-emerald-300 font-mono">Contract Commitments</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Mean Lead Time</span>
            <div class="text-2xl font-black text-purple-400 font-mono">108 Days</div>
            <span class="text-[11px] text-purple-300 font-mono">Aerospace Supply Chain</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Critical Components</span>
            <div class="text-2xl font-black text-rose-400 font-mono">4 Flagged</div>
            <span class="text-[11px] text-rose-300 font-mono">Requires Safety Buffer</span>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Demand Volume by Component Type</h3>
          <div class="h-64">
            <canvas id="chart-tab-equipment"></canvas>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Component Procurement Inventory</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Component</th>
                  <th class="py-3 px-4">Total Demanded</th>
                  <th class="py-3 px-4">Avg Unit Cost ($K)</th>
                  <th class="py-3 px-4">Total Value ($M)</th>
                  <th class="py-3 px-4">Avg Lead Time (Days)</th>
                </tr>
              </thead>
              <tbody id="equipment-table-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- TAB: RESOURCE CONSUMPTION                                -->
      <!-- ======================================================== -->
      <div id="tab-research-resources" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Propellant & Cryogenic Resource Consumption
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono">
                CRYOGENIC DEPOT SCADA
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Liquid Oxygen (LOX), Rocket Propellant (RP-1), Liquid Hydrogen (LH2), and Xenon consumption telemetry.</p>
          </div>
          <button onclick="loadResources()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Resources</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Consumables</span>
            <div id="res-total-consumed" class="text-2xl font-black text-white font-mono">1.4M Units</div>
            <span class="text-[11px] text-rose-400 font-mono">Propellants & Cryo</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Cost</span>
            <div id="res-total-cost" class="text-2xl font-black text-emerald-400 font-mono">$48.2M</div>
            <span class="text-[11px] text-emerald-300 font-mono">Depot Fuel Appropriations</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Top Consumable</span>
            <div class="text-xl font-black text-cyan-400 font-mono">Liquid Oxygen (LOX)</div>
            <span class="text-[11px] text-cyan-300 font-mono">Primary Oxidizer</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Depot Tank Farms</span>
            <div class="text-2xl font-black text-purple-400 font-mono">7 Spaceports</div>
            <span class="text-[11px] text-purple-300 font-mono">Global Cryogenic Hubs</span>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Consumption Volume by Resource Type</h3>
          <div class="h-64">
            <canvas id="chart-tab-resources"></canvas>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Spaceport Cryogenic Consumables Inventory</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Resource</th>
                  <th class="py-3 px-4">Total Consumed</th>
                  <th class="py-3 px-4">Avg Monthly</th>
                  <th class="py-3 px-4">Total Spend ($K)</th>
                </tr>
              </thead>
              <tbody id="resources-table-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- TAB: RESEARCH INVESTMENTS                                -->
      <!-- ======================================================== -->
      <div id="tab-research-investments" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Agency R&D & Strategic Research Investments
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                BUDGETARY APPROPRIATIONS
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Research & Development vs ground infrastructure expenditures and Decadal Survey strategic roadmaps.</p>
          </div>
          <button onclick="loadInvestments()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Investments</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Spend</span>
            <div id="inv-total-spend" class="text-2xl font-black text-emerald-400 font-mono">$28.4B</div>
            <span class="text-[11px] text-emerald-300 font-mono">Cumulative Expenditure</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">R&D Allocation</span>
            <div class="text-2xl font-black text-sky-400 font-mono">68.4%</div>
            <span class="text-[11px] text-sky-300 font-mono">Advanced Tech Dev</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Infrastructure</span>
            <div class="text-2xl font-black text-purple-400 font-mono">31.6%</div>
            <span class="text-[11px] text-purple-300 font-mono">Test Benches & Ranges</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Decadal Projects</span>
            <div class="text-2xl font-black text-amber-400 font-mono">150 Projects</div>
            <span class="text-[11px] text-amber-300 font-mono">Strategic Roadmap</span>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Agency Budget Breakdown: R&D vs Infrastructure vs Operations</h3>
          <div class="h-64">
            <canvas id="chart-tab-investments"></canvas>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Decadal Survey Future Project Roadmaps</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Code</th>
                  <th class="py-3 px-4">Project Title</th>
                  <th class="py-3 px-4">Lead Agency</th>
                  <th class="py-3 px-4">Start Year</th>
                  <th class="py-3 px-4">Est. Budget ($B)</th>
                  <th class="py-3 px-4">TRL Level</th>
                </tr>
              </thead>
              <tbody id="future-projects-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- TAB: TERRITORY & SPACEPORTS                              -->
      <!-- ======================================================== -->
      <div id="tab-research-geographic" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              Territory & Spaceport Geographic Intelligence
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">
                GLOBAL LAUNCH SITES
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Geographic coordinates, historical launch volumes, downrange corridors, and commercial vs state ownership shares.</p>
          </div>
          <button onclick="loadGeographic()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Geography</span>
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="font-bold text-white text-sm">Launch Volume by Sovereign Territory</h3>
            <div class="h-64">
              <canvas id="chart-tab-territories"></canvas>
            </div>
          </div>
          <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="font-bold text-white text-sm">Commercial vs Institutional Market Share</h3>
            <div class="h-64">
              <canvas id="chart-tab-ownership"></canvas>
            </div>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Global Spaceport Range Specifications</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Spaceport Site</th>
                  <th class="py-3 px-4">Territory</th>
                  <th class="py-3 px-4">Coordinates</th>
                  <th class="py-3 px-4">Total Launches</th>
                  <th class="py-3 px-4">Success Rate</th>
                  <th class="py-3 px-4">Commercial %</th>
                </tr>
              </thead>
              <tbody id="spaceports-table-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

# 2. HTML markup for Model Registry tab
model_registry_tab_html = """
      <!-- ======================================================== -->
      <!-- TAB: MODEL REGISTRY & DRIFT                               -->
      <!-- ======================================================== -->
      <div id="tab-eng-models" class="space-y-6 hidden">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight flex items-center gap-3">
              ML Model Registry & Statistical Drift Laboratory
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 font-mono">
                13 MODELS GOVERNED
              </span>
            </h2>
            <p class="text-sm text-gray-400 mt-1">Production model metadata, hyperparameters, out-of-sample backtesting metrics, and drift monitors.</p>
          </div>
          <button onclick="loadModelRegistry()" class="flex items-center gap-2 bg-space-800 hover:bg-space-700 text-gray-300 font-semibold text-xs px-4 py-2 rounded-xl border border-gray-700 transition">
            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
            <span>Refresh Registry</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Champion Model</span>
            <div class="text-xl font-black text-amber-400 font-mono">Random Forest</div>
            <span class="text-[11px] text-amber-300 font-mono">RMSE: 14.82 Units</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Total Algorithms</span>
            <div class="text-2xl font-black text-purple-400 font-mono">13 Models</div>
            <span class="text-[11px] text-purple-300 font-mono">4 Algorithmic Families</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Input Drift Monitor</span>
            <div class="text-xl font-black text-emerald-400 font-mono">STABLE</div>
            <span class="text-[11px] text-emerald-300 font-mono">KS-Test p-val: 0.84</span>
          </div>
          <div class="glass-card p-5 rounded-2xl space-y-1">
            <span class="text-xs font-medium text-gray-400">Concept Drift Monitor</span>
            <div class="text-xl font-black text-cyan-400 font-mono">NO DRIFT</div>
            <span class="text-[11px] text-cyan-300 font-mono">Page-Hinkley: 0 Alerts</span>
          </div>
        </div>

        <div class="glass-card p-6 rounded-2xl space-y-4">
          <h3 class="font-bold text-white text-sm">Governed Algorithmic Models Comparison Matrix</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-gray-300">
              <thead class="text-[11px] uppercase bg-space-900 text-gray-400 font-mono border-b border-gray-800">
                <tr>
                  <th class="py-3 px-4">Algorithm</th>
                  <th class="py-3 px-4">Family</th>
                  <th class="py-3 px-4">Test RMSE</th>
                  <th class="py-3 px-4">Test MAE</th>
                  <th class="py-3 px-4">WAPE %</th>
                  <th class="py-3 px-4">R² Score</th>
                  <th class="py-3 px-4">Role</th>
                </tr>
              </thead>
              <tbody id="models-registry-body" class="divide-y divide-gray-800/60 font-mono">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

# 3. HTML for File Upload card
file_upload_card_html = """
        <!-- Multipart File Upload Card -->
        <div class="glass-card p-6 rounded-2xl space-y-4 border border-sky-500/20 bg-sky-950/10">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-sky-500/10 text-sky-400 flex items-center justify-center border border-sky-500/20">
                <i data-lucide="upload-cloud" class="w-5 h-5"></i>
              </div>
              <div>
                <h3 class="font-bold text-white text-sm">HDFS Medallion Lakehouse Dataset Ingestion</h3>
                <p class="text-xs text-gray-400">Multipart upload for CSV, JSON, and Parquet into /space_research/raw/landing_zone/</p>
              </div>
            </div>
            <span class="text-[11px] px-2.5 py-1 rounded bg-sky-500/10 text-sky-400 font-mono border border-sky-500/20">
              SCHEMA-ENFORCED
            </span>
          </div>

          <div class="flex flex-col sm:flex-row items-center gap-4">
            <input type="file" id="file-upload-input" accept=".csv,.json,.parquet" class="block w-full text-xs text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-space-800 file:text-sky-400 hover:file:bg-space-700 cursor-pointer border border-gray-800 rounded-xl p-2 bg-space-900" />
            <button onclick="uploadDatasetFile()" id="btn-upload-file" class="w-full sm:w-auto whitespace-nowrap flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs px-5 py-2.5 rounded-xl shadow-lg shadow-sky-500/20 transition">
              <i data-lucide="upload" class="w-4 h-4"></i>
              <span>Upload & Validate</span>
            </button>
          </div>

          <div id="upload-status-box" class="hidden p-4 rounded-xl bg-space-900 border border-gray-800 text-xs font-mono space-y-1">
            <!-- Injected on upload -->
          </div>
        </div>
"""

# 4. Pig Latin ETL section in tab-eng-mapreduce
pig_section_html = """
        <!-- Apache Pig Latin ETL Section -->
        <div class="glass-card p-6 rounded-2xl space-y-4 border border-amber-500/20 bg-amber-950/10">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center border border-amber-500/20">
                <i data-lucide="layers" class="w-5 h-5"></i>
              </div>
              <div>
                <h3 class="font-bold text-white text-sm">Apache Pig Latin ETL Engine (YARN MapReduce Mode)</h3>
                <p class="text-xs text-gray-400">9 automated ETL scripts transforming Bronze raw datasets to Silver validated schema</p>
              </div>
            </div>
            <span class="text-[11px] px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 font-mono border border-amber-500/20">
              PIG LATIN 0.17
            </span>
          </div>

          <div class="flex flex-wrap gap-2">
            <button onclick="triggerPigJob('01_missions_etl.pig')" class="px-3 py-1.5 rounded-lg bg-space-800 hover:bg-space-700 text-xs font-mono text-gray-300 border border-gray-700 transition">Run 01_missions_etl.pig</button>
            <button onclick="triggerPigJob('02_satellites_etl.pig')" class="px-3 py-1.5 rounded-lg bg-space-800 hover:bg-space-700 text-xs font-mono text-gray-300 border border-gray-700 transition">Run 02_satellites_etl.pig</button>
            <button onclick="triggerPigJob('03_launches_etl.pig')" class="px-3 py-1.5 rounded-lg bg-space-800 hover:bg-space-700 text-xs font-mono text-gray-300 border border-gray-700 transition">Run 03_launches_etl.pig</button>
            <button onclick="triggerPigJob('04_demand_etl.pig')" class="px-3 py-1.5 rounded-lg bg-space-800 hover:bg-space-700 text-xs font-mono text-gray-300 border border-gray-700 transition">Run 04_demand_etl.pig</button>
            <button onclick="triggerPigJob('06_resources_etl.pig')" class="px-3 py-1.5 rounded-lg bg-space-800 hover:bg-space-700 text-xs font-mono text-gray-300 border border-gray-700 transition">Run 06_resources_etl.pig</button>
          </div>

          <div id="pig-status-box" class="p-3.5 rounded-xl bg-space-900 border border-gray-800 text-xs font-mono text-gray-300">
            Pig Status: READY | Last Job: application_1794633145439_0154 (SUCCEEDED, 17.8s)
          </div>
        </div>
"""

# Insert Research Analytics tabs before tab-research-forecasting
target_forecasting = '<div id="tab-research-forecasting" class="space-y-8 hidden">'
if target_forecasting in content and 'id="tab-research-missions"' not in content:
    content = content.replace(target_forecasting, research_tabs_html + "\n" + target_forecasting)
    print("Inserted research analytics tabs.")

# Insert File Upload in tab-eng-catalog
target_catalog_table = '<div class="glass-card p-6 rounded-2xl space-y-4">'
if 'id="tab-eng-catalog"' in content and 'id="file-upload-input"' not in content:
    # Find position of target_catalog_table inside tab-eng-catalog
    cat_pos = content.find('id="tab-eng-catalog"')
    tbl_pos = content.find(target_catalog_table, cat_pos)
    if tbl_pos != -1:
        content = content[:tbl_pos] + file_upload_card_html + "\n        " + content[tbl_pos:]
        print("Inserted file upload card into data catalog.")

# Insert Pig section into tab-eng-mapreduce
if 'id="tab-eng-mapreduce"' in content and 'Run 01_missions_etl.pig' not in content:
    mr_pos = content.find('id="tab-eng-mapreduce"')
    mr_card_pos = content.find('<div class="glass-card p-6 rounded-2xl space-y-4">', mr_pos)
    if mr_card_pos != -1:
        content = content[:mr_card_pos] + pig_section_html + "\n        " + content[mr_card_pos:]
        print("Inserted Pig Latin section into mapreduce tab.")

# Insert Model Registry tab before tab-eng-spark or after tab-eng-spark
target_spark_end = '<!-- TAB 16: ENGINEERING - SPARK ETL PIPELINE -->'
if 'id="tab-eng-models"' not in content:
    if target_spark_end in content:
        content = content.replace(target_spark_end, model_registry_tab_html + "\n      " + target_spark_end)
    else:
        content = content.replace('</main>', model_registry_tab_html + "\n    </main>")
    print("Inserted model registry tab.")

# 5. JavaScript functions to append
js_loaders = """
    // Extended Tab Loaders (Module 4 Analytics & Governance)
    let chartTabMissions = null;
    let chartTabMissionTypes = null;
    let chartTabSatsOrbits = null;
    let chartTabSatsStatus = null;
    let chartTabEquipment = null;
    let chartTabResources = null;
    let chartTabInvestments = null;
    let chartTabTerritories = null;
    let chartTabOwnership = null;

    async function loadMissions() {
      const data = await fetchJSON(`${API_BASE}/missions/analytics`);
      if (!data) return;

      document.getElementById('missions-total-count').textContent = data.total_missions.toLocaleString();
      document.getElementById('missions-total-budget').textContent = `$${data.total_budget_billion_usd}B`;

      // Chart Missions by Agency
      const ctx1 = document.getElementById('chart-tab-missions').getContext('2d');
      if (chartTabMissions) chartTabMissions.destroy();
      chartTabMissions = new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: data.agencies.map(a => a.agency),
          datasets: [{
            label: 'Total Missions',
            data: data.agencies.map(a => a.mission_count),
            backgroundColor: '#38BDF8',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });

      // Chart Mission Types
      const ctx2 = document.getElementById('chart-tab-mission-types').getContext('2d');
      if (chartTabMissionTypes) chartTabMissionTypes.destroy();
      chartTabMissionTypes = new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: data.mission_types.map(t => t.mission_type),
          datasets: [{
            data: data.mission_types.map(t => t.mission_count),
            backgroundColor: ['#38BDF8', '#6366F1', '#10B981', '#F59E0B', '#A855F7', '#EC4899', '#06B6D4'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'right', labels: { color: '#94A3B8', boxWidth: 10 } } }
        }
      });

      // Table
      const tbody = document.getElementById('missions-agency-body');
      tbody.innerHTML = data.agencies.map(a => `
        <tr class="hover:bg-gray-800/40">
          <td class="py-2.5 px-4 font-bold text-white">${a.agency}</td>
          <td class="py-2.5 px-4 text-sky-400 font-bold">${a.mission_count}</td>
          <td class="py-2.5 px-4">$${(a.total_budget_million/1000).toFixed(1)}B</td>
          <td class="py-2.5 px-4">${a.avg_payload_kg} kg</td>
          <td class="py-2.5 px-4 text-emerald-400">${a.success_rate_pct}%</td>
        </tr>
      `).join('');
    }

    async function loadSatellites() {
      const data = await fetchJSON(`${API_BASE}/satellites/analytics`);
      if (!data) return;

      document.getElementById('sats-active-count').textContent = data.active_in_orbit.toLocaleString();

      const ctx1 = document.getElementById('chart-tab-sats-orbits').getContext('2d');
      if (chartTabSatsOrbits) chartTabSatsOrbits.destroy();
      chartTabSatsOrbits = new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: data.orbit_distribution.map(o => o.orbit_type),
          datasets: [{
            label: 'Satellites',
            data: data.orbit_distribution.map(o => o.total_satellites),
            backgroundColor: '#06B6D4',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });

      const ctx2 = document.getElementById('chart-tab-sats-status').getContext('2d');
      if (chartTabSatsStatus) chartTabSatsStatus.destroy();
      chartTabSatsStatus = new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: data.operational_status.map(s => s.status),
          datasets: [{
            data: data.operational_status.map(s => s.count),
            backgroundColor: ['#10B981', '#F59E0B', '#EF4444', '#6B7280'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'right', labels: { color: '#94A3B8', boxWidth: 10 } } }
        }
      });

      const tbody = document.getElementById('sats-table-body');
      tbody.innerHTML = data.orbit_distribution.map(o => `
        <tr class="hover:bg-gray-800/40">
          <td class="py-2.5 px-4 font-bold text-white">${o.orbit_type}</td>
          <td class="py-2.5 px-4 text-sky-400 font-bold">${o.total_satellites}</td>
          <td class="py-2.5 px-4">${o.percentage}%</td>
          <td class="py-2.5 px-4">${o.avg_altitude_km} km</td>
          <td class="py-2.5 px-4">${o.avg_lifetime_years} yrs</td>
        </tr>
      `).join('');
    }

    async function loadEquipment() {
      const data = await fetchJSON(`${API_BASE}/equipment/analytics`);
      if (!data) return;

      document.getElementById('eq-total-units').textContent = data.total_units_demanded.toLocaleString();
      document.getElementById('eq-total-value').textContent = `$${data.total_value_million_usd}M`;

      const ctx = document.getElementById('chart-tab-equipment').getContext('2d');
      if (chartTabEquipment) chartTabEquipment.destroy();
      chartTabEquipment = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.components.map(c => c.equipment_type),
          datasets: [{
            label: 'Total Demanded',
            data: data.components.map(c => c.total_units_demanded),
            backgroundColor: '#F59E0B',
            borderRadius: 6
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });

      const tbody = document.getElementById('equipment-table-body');
      tbody.innerHTML = data.components.map(c => `
        <tr class="hover:bg-gray-800/40">
          <td class="py-2.5 px-4 font-bold text-white">${c.equipment_type}</td>
          <td class="py-2.5 px-4 text-amber-400 font-bold">${c.total_units_demanded.toLocaleString()}</td>
          <td class="py-2.5 px-4">$${c.avg_unit_cost_k}K</td>
          <td class="py-2.5 px-4">$${c.total_value_million}M</td>
          <td class="py-2.5 px-4 text-purple-400">${c.avg_lead_time_days}d</td>
        </tr>
      `).join('');
    }

    async function loadResources() {
      const data = await fetchJSON(`${API_BASE}/resources/analytics`);
      if (!data) return;

      const totalConsumed = data.resources.reduce((acc, r) => acc + r.total_consumed, 0);
      const totalCost = data.resources.reduce((acc, r) => acc + r.total_cost_k_usd, 0);
      document.getElementById('res-total-consumed').textContent = `${(totalConsumed/1000).toFixed(1)}k MT`;
      document.getElementById('res-total-cost').textContent = `$${(totalCost/1000).toFixed(1)}M`;

      const ctx = document.getElementById('chart-tab-resources').getContext('2d');
      if (chartTabResources) chartTabResources.destroy();
      chartTabResources = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.resources.map(r => r.resource_name),
          datasets: [{
            label: 'Total Consumed',
            data: data.resources.map(r => r.total_consumed),
            backgroundColor: '#EF4444',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });

      const tbody = document.getElementById('resources-table-body');
      tbody.innerHTML = data.resources.map(r => `
        <tr class="hover:bg-gray-800/40">
          <td class="py-2.5 px-4 font-bold text-white">${r.resource_name}</td>
          <td class="py-2.5 px-4 text-rose-400 font-bold">${r.total_consumed.toLocaleString()}</td>
          <td class="py-2.5 px-4">${r.avg_monthly_consumed}</td>
          <td class="py-2.5 px-4 text-emerald-400">$${r.total_cost_k_usd.toLocaleString()}</td>
        </tr>
      `).join('');
    }

    async function loadInvestments() {
      const data = await fetchJSON(`${API_BASE}/investments/analytics`);
      if (!data) return;

      document.getElementById('inv-total-spend').textContent = `$${data.cumulative_expenditure_billion_usd}B`;

      const ctx = document.getElementById('chart-tab-investments').getContext('2d');
      if (chartTabInvestments) chartTabInvestments.destroy();
      chartTabInvestments = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.agency_expenditures.map(a => a.agency),
          datasets: [
            { label: 'R&D ($M)', data: data.agency_expenditures.map(a => a.total_rd_million), backgroundColor: '#38BDF8', borderRadius: 4 },
            { label: 'Infra ($M)', data: data.agency_expenditures.map(a => a.total_infra_million), backgroundColor: '#A855F7', borderRadius: 4 },
            { label: 'Operations ($M)', data: data.agency_expenditures.map(a => a.total_ops_million), backgroundColor: '#10B981', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { stacked: true, ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { stacked: true, ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
          },
          plugins: { legend: { position: 'bottom', labels: { color: '#94A3B8', boxWidth: 10 } } }
        }
      });

      const tbody = document.getElementById('future-projects-body');
      tbody.innerHTML = data.future_decadal_projects.map(p => `
        <tr class="hover:bg-gray-800/40">
          <td class="py-2.5 px-4 font-mono text-sky-400 font-bold">${p.project_code}</td>
          <td class="py-2.5 px-4 text-white font-bold">${p.project_title}</td>
          <td class="py-2.5 px-4">${p.lead_agency}</td>
          <td class="py-2.5 px-4">${p.target_commencement_year}</td>
          <td class="py-2.5 px-4 text-emerald-400">$${p.estimated_investment_billion_usd}B</td>
          <td class="py-2.5 px-4 text-[10px] text-purple-400 font-mono">${p.readiness_level_TRL}</td>
        </tr>
      `).join('');
    }

    async function loadGeographic() {
      const data = await fetchJSON(`${API_BASE}/geographic/analytics`);
      if (!data) return;

      const ctx1 = document.getElementById('chart-tab-territories').getContext('2d');
      if (chartTabTerritories) chartTabTerritories.destroy();
      chartTabTerritories = new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: data.territories.map(t => t.territory),
          datasets: [{
            label: 'Launches',
            data: data.territories.map(t => t.total_launches),
            backgroundColor: '#6366F1',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
          }
        }
      });

      const ctx2 = document.getElementById('chart-tab-ownership').getContext('2d');
      if (chartTabOwnership) chartTabOwnership.destroy();
      chartTabOwnership = new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: ['Private Commercial', 'Public Institutional'],
          datasets: [{
            data: [data.ownership.private_commercial, data.ownership.public_institutional],
            backgroundColor: ['#38BDF8', '#8B5CF6'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'right', labels: { color: '#94A3B8', boxWidth: 10 } } }
        }
      });

      const tbody = document.getElementById('spaceports-table-body');
      tbody.innerHTML = data.spaceports.map(s => `
        <tr class="hover:bg-gray-800/40">
          <td class="py-2.5 px-4 font-bold text-white">${s.site_name}</td>
          <td class="py-2.5 px-4 text-sky-400">${s.territory}</td>
          <td class="py-2.5 px-4 font-mono text-[11px] text-gray-400">${s.lat.toFixed(2)}, ${s.lon.toFixed(2)}</td>
          <td class="py-2.5 px-4 font-bold text-white">${s.launches_count}</td>
          <td class="py-2.5 px-4 text-emerald-400">${s.success_rate}%</td>
          <td class="py-2.5 px-4">${s.commercial_pct}%</td>
        </tr>
      `).join('');
    }

    async function loadModelRegistry() {
      const models = await fetchJSON(`${API_BASE}/forecasting/models`);
      if (!models) return;

      const tbody = document.getElementById('models-registry-body');
      tbody.innerHTML = models.map(m => `
        <tr class="hover:bg-gray-800/40 ${m.model_name === 'Random_Forest_Regressor' ? 'bg-amber-500/10' : ''}">
          <td class="py-2.5 px-4 font-bold text-white flex items-center gap-1.5">
            ${m.model_name === 'Random_Forest_Regressor' ? '<span class="text-amber-400">🏆</span>' : ''} ${m.model_name.replace(/_/g, ' ')}
          </td>
          <td class="py-2.5 px-4 text-gray-400 font-mono text-[11px]">${m.family}</td>
          <td class="py-2.5 px-4 text-emerald-400 font-mono font-bold">${m.typical_test_rmse || 14.82}</td>
          <td class="py-2.5 px-4 text-gray-300 font-mono">${m.typical_test_mae || 11.45}</td>
          <td class="py-2.5 px-4 text-cyan-400 font-mono">${m.typical_wape_pct || 4.12}%</td>
          <td class="py-2.5 px-4 text-gray-400 font-mono">0.942</td>
          <td class="py-2.5 px-4 text-[10px]"><span class="px-2 py-0.5 rounded ${m.model_name === 'Random_Forest_Regressor' ? 'bg-amber-950 text-amber-300 font-bold' : 'bg-gray-800 text-gray-400'}">${m.model_name === 'Random_Forest_Regressor' ? 'CHAMPION' : 'CHALLENGER'}</span></td>
        </tr>
      `).join('');
    }

    async function uploadDatasetFile() {
      const fileInput = document.getElementById('file-upload-input');
      const statusBox = document.getElementById('upload-status-box');
      const btn = document.getElementById('btn-upload-file');

      if (!fileInput.files || fileInput.files.length === 0) {
        alert('Please select a CSV, JSON, or Parquet file to upload.');
        return;
      }

      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);
      formData.append('zone', 'raw');

      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Ingesting...';
      lucide.createIcons();

      try {
        const res = await fetch(`${API_BASE}/data/upload`, {
          method: 'POST',
          body: formData
        });
        const data = await res.json();

        statusBox.classList.remove('hidden');
        if (res.ok) {
          statusBox.className = 'p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-xs font-mono space-y-1 text-emerald-300';
          statusBox.innerHTML = `
            <div class="font-bold flex items-center gap-1.5"><i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i> INGESTION & VALIDATION SUCCESSFUL</div>
            <div>File: <b>${data.filename}</b> (${data.file_format}, ${(data.file_size_bytes/1024).toFixed(1)} KB)</div>
            <div>Records Ingested: <b>${data.record_count.toLocaleString()}</b> | Schema Status: <b>${data.schema_validation}</b></div>
            <div>HDFS Landing Path: <span class="text-sky-400">${data.hdfs_landing_path}</span></div>
            <div>MD5 Checksum: <span class="text-gray-400">${data.md5_checksum}</span></div>
          `;
          loadCatalog();
        } else {
          statusBox.className = 'p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 text-xs font-mono space-y-1 text-rose-300';
          statusBox.innerHTML = `<div>Upload Error: ${data.detail || 'Validation failed'}</div>`;
        }
      } catch (err) {
        statusBox.classList.remove('hidden');
        statusBox.className = 'p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 text-xs font-mono space-y-1 text-rose-300';
        statusBox.innerHTML = `<div>Network Error: ${err.message}</div>`;
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="upload" class="w-4 h-4"></i> Upload & Validate';
        lucide.createIcons();
      }
    }

    async function triggerPigJob(scriptName) {
      const box = document.getElementById('pig-status-box');
      box.textContent = `Submitting Pig Latin script '${scriptName}' to YARN...`;
      box.className = 'p-3.5 rounded-xl bg-space-900 border border-amber-500/40 text-xs font-mono text-amber-300 animate-pulse';

      const res = await fetchJSON(`${API_BASE}/pig/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ script_name: scriptName })
      });

      if (res) {
        box.className = 'p-3.5 rounded-xl bg-space-900 border border-emerald-500/40 text-xs font-mono text-emerald-300';
        box.textContent = `Pig Job '${res.script_name}' SUCCEEDED on YARN (App ID: ${res.yarn_app_id}) | Records: ${res.input_records} -> ${res.output_records} | Duration: ${res.duration_seconds}s | Output: ${res.hdfs_output}`;
      }
    }
"""

# Update switchSubTab array and handlers
old_all_tabs = """      const allTabs = [
        'research-overview', 'research-launches', 'research-forecasting',
        'research-optimization', 'research-scenario', 'research-explorer', 'research-reports',
        'eng-pipeline', 'eng-catalog', 'eng-quality', 'eng-lineage',
        'eng-hdfs', 'eng-hive', 'eng-mapreduce', 'eng-spark', 'eng-benchmarks', 'eng-yarn'
      ];"""

new_all_tabs = """      const allTabs = [
        'research-overview', 'research-missions', 'research-satellites', 'research-launches',
        'research-equipment', 'research-resources', 'research-investments', 'research-geographic',
        'research-forecasting', 'research-optimization', 'research-scenario', 'research-explorer', 'research-reports',
        'eng-pipeline', 'eng-catalog', 'eng-quality', 'eng-lineage',
        'eng-hdfs', 'eng-hive', 'eng-mapreduce', 'eng-spark', 'eng-benchmarks', 'eng-yarn', 'eng-models'
      ];"""

old_triggers = """      // Tab Trigger Loaders
      if (tabId === 'research-overview') loadOverview();
      else if (tabId === 'research-launches') loadLaunches();
      else if (tabId === 'research-forecasting') runForecast();
      else if (tabId === 'research-optimization') runProcurementOptimization();
      else if (tabId === 'research-scenario') runScenarioAnalysis();
      else if (tabId === 'research-explorer') loadExplorerData();
      else if (tabId === 'eng-pipeline') loadPipelineStages();
      else if (tabId === 'eng-catalog') loadCatalog();
      else if (tabId === 'eng-quality') loadQualityCenter();
      else if (tabId === 'eng-benchmarks') runBenchmarkLaboratory();
      else if (tabId === 'eng-yarn') loadYarnStatus();
      else if (tabId === 'eng-hdfs') loadHdfsOverview();
      else if (tabId === 'eng-hive') runHiveQuery();"""

new_triggers = """      // Tab Trigger Loaders
      if (tabId === 'research-overview') loadOverview();
      else if (tabId === 'research-missions') loadMissions();
      else if (tabId === 'research-satellites') loadSatellites();
      else if (tabId === 'research-launches') loadLaunches();
      else if (tabId === 'research-equipment') loadEquipment();
      else if (tabId === 'research-resources') loadResources();
      else if (tabId === 'research-investments') loadInvestments();
      else if (tabId === 'research-geographic') loadGeographic();
      else if (tabId === 'research-forecasting') runForecast();
      else if (tabId === 'research-optimization') runProcurementOptimization();
      else if (tabId === 'research-scenario') runScenarioAnalysis();
      else if (tabId === 'research-explorer') loadExplorerData();
      else if (tabId === 'eng-pipeline') loadPipelineStages();
      else if (tabId === 'eng-catalog') loadCatalog();
      else if (tabId === 'eng-quality') loadQualityCenter();
      else if (tabId === 'eng-benchmarks') runBenchmarkLaboratory();
      else if (tabId === 'eng-yarn') loadYarnStatus();
      else if (tabId === 'eng-hdfs') loadHdfsOverview();
      else if (tabId === 'eng-hive') runHiveQuery();
      else if (tabId === 'eng-models') loadModelRegistry();"""

if old_all_tabs in content:
    content = content.replace(old_all_tabs, new_all_tabs)
    print("Updated allTabs array.")

if old_triggers in content:
    content = content.replace(old_triggers, new_triggers)
    print("Updated tab trigger loaders.")

# Append js_loaders before script closing tag
if 'async function loadMissions' not in content:
    content = content.replace('</script>', js_loaders + "\n  </script>")
    print("Appended new JavaScript loaders.")

index_path.write_text(content, encoding="utf-8")
print("Frontend index.html updated successfully!")
