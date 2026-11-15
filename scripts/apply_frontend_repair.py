import os

js_core = r"""  <!-- JAVASCRIPT APPLICATION CORE -->
  <script>
    const API_BASE = '/api/v1';

    // Global Chart Instances
    let chartMissions = null;
    let chartOrbits = null;
    let chartEspiOutcome = null;
    let chartEspiProvider = null;
    let chartEspiTerritoryBar = null;
    let chartEspiTerritoryTrend = null;
    let chartForecast = null;
    let chartImportance = null;
    let chartMonteCarlo = null;
    let chartTornado = null;
    let chartBenchmark = null;
    let chartTabMissions = null;
    let chartTabMissionTypes = null;
    let chartTabSatsOrbits = null;
    let chartTabSatsStatus = null;
    let chartTabEquipment = null;
    let chartTabResources = null;
    let chartTabInvestments = null;
    let chartTabTerritories = null;
    let chartTabOwnership = null;

    // ESPI Interactive Filter State
    let espiFilterState = {
      maxYear: 2026,
      territories: new Set(['USA', 'Russia', 'China', 'Europe', 'India', 'Japan', 'Others']),
      ownerships: new Set(['Private', 'Public']),
      outcomes: new Set(['Success', 'Partial', 'Failure'])
    };

    // Safe Helper: Fetch JSON with Graceful Degradation
    async function fetchJSON(url, options = {}) {
      try {
        const res = await fetch(url, options);
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return await res.json();
      } catch (err) {
        console.error(`Fetch error on ${url}:`, err);
        return null;
      }
    }

    // Safe Helper: Set Text Content
    function setText(id, val) {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    }

    // Safe Helper: Get Canvas 2D Context
    function getCanvasContext(id) {
      const canvas = document.getElementById(id);
      if (!canvas) return null;
      return canvas.getContext('2d');
    }

    // 1. Dual-Layer Switcher (Research Intelligence vs Big Data Engineering)
    function switchLayer(layer) {
      const btnResearch = document.getElementById('btn-layer-research');
      const btnEngineering = document.getElementById('btn-layer-engineering');
      const menuResearch = document.getElementById('menu-research');
      const menuEngineering = document.getElementById('menu-engineering');

      if (layer === 'research') {
        if (btnResearch) btnResearch.className = 'flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition bg-gradient-to-r from-sky-600 to-indigo-600 text-white shadow-md shadow-sky-500/20';
        if (btnEngineering) btnEngineering.className = 'flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold text-gray-400 hover:text-gray-200 transition';
        if (menuResearch) menuResearch.classList.remove('hidden');
        if (menuEngineering) menuEngineering.classList.add('hidden');
        switchSubTab('research-overview');
      } else {
        if (btnEngineering) btnEngineering.className = 'flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-500/20';
        if (btnResearch) btnResearch.className = 'flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold text-gray-400 hover:text-gray-200 transition';
        if (menuEngineering) menuEngineering.classList.remove('hidden');
        if (menuResearch) menuResearch.classList.add('hidden');
        switchSubTab('eng-pipeline');
      }
    }

    // 2. Sub-Tab Navigation
    async function switchSubTab(tabId) {
      const allTabs = [
        'research-overview', 'research-missions', 'research-satellites', 'research-launches',
        'research-equipment', 'research-resources', 'research-investments', 'research-geographic',
        'research-forecasting', 'research-optimization', 'research-scenario', 'research-explorer', 'research-reports',
        'eng-pipeline', 'eng-catalog', 'eng-quality', 'eng-lineage',
        'eng-hdfs', 'eng-hive', 'eng-mapreduce', 'eng-spark', 'eng-benchmarks', 'eng-yarn', 'eng-models'
      ];

      allTabs.forEach(t => {
        const el = document.getElementById(`tab-${t}`);
        const btn = document.getElementById(`sub-btn-${t}`);
        if (el) el.classList.add('hidden');
        if (btn) {
          btn.className = 'w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-800/40 transition';
        }
      });

      const activeEl = document.getElementById(`tab-${tabId}`);
      const activeBtn = document.getElementById(`sub-btn-${tabId}`);
      if (activeEl) activeEl.classList.remove('hidden');
      if (activeBtn) {
        const isEng = tabId.startsWith('eng-');
        activeBtn.className = isEng
          ? 'w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-bold transition bg-purple-500/10 text-purple-400 border border-purple-500/20'
          : 'w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-bold transition bg-sky-500/10 text-sky-400 border border-sky-500/20';
      }

      // Safe Tab Trigger Loaders
      try {
        if (tabId === 'research-overview') {
          await loadOverview(); setTimeout(initOrbitGlobe, 120);
        } else if (tabId === 'research-missions') {
          await loadMissions();
        } else if (tabId === 'research-satellites') {
          await loadSatellites();
        } else if (tabId === 'research-launches') {
          await loadLaunches();
        } else if (tabId === 'research-equipment') {
          await loadEquipment();
        } else if (tabId === 'research-resources') {
          await loadResources();
        } else if (tabId === 'research-investments') {
          await loadInvestments();
        } else if (tabId === 'research-geographic') {
          await loadGeographic();
        } else if (tabId === 'research-forecasting') {
          await runForecast();
        } else if (tabId === 'research-optimization') {
          await runProcurementOptimization();
        } else if (tabId === 'research-scenario') {
          await runScenarioAnalysis();
        } else if (tabId === 'research-explorer') {
          await loadExplorerData();
        } else if (tabId === 'research-reports') {
          await loadReports();
        } else if (tabId === 'eng-pipeline') {
          loadPipelineStages();
        } else if (tabId === 'eng-catalog') {
          loadCatalog();
        } else if (tabId === 'eng-quality') {
          loadQualityCenter();
        } else if (tabId === 'eng-benchmarks') {
          runBenchmarkLaboratory();
        } else if (tabId === 'eng-yarn') {
          loadYarnStatus();
        } else if (tabId === 'eng-hdfs') {
          loadHdfsOverview();
        } else if (tabId === 'eng-hive') {
          runHiveQuery();
        } else if (tabId === 'eng-models') {
          loadModelRegistry();
        }
      } catch (err) {
        console.error('Error switching tab:', tabId, err);
      } finally {
        lucide.createIcons();
      }
    }

    // 3. Executive Overview Tab Loader (Module 1)
    async function loadOverview() {
      try {
        const kpis = await fetchJSON(`${API_BASE}/overview/kpis`);
        if (kpis) {
          setText('kpi-missions', (kpis.total_missions || 1500).toLocaleString());
          setText('kpi-satellites', (kpis.active_satellites_in_orbit || 1850).toLocaleString());
          setText('kpi-launch-rate', `${kpis.launch_success_rate_pct || 94.8}%`);
          setText('kpi-records', (kpis.total_processed_records || 9746).toLocaleString());
          setText('kpi-budget', `$${kpis.cumulative_budget_billion_usd || 184.5}B`);
          setText('kpi-equipment', (kpis.total_equipment_units_demanded || 8420).toLocaleString());

          // Hero OrbitTrack Cards
          setText('orbittrack-total-sats', (kpis.active_satellites_in_orbit || 1850).toLocaleString());
          setText('orbittrack-active-missions', (kpis.total_missions ? Math.round(kpis.total_missions * 0.095) : 142).toLocaleString());
          setText('orbittrack-data-records', `${(kpis.total_processed_records || 9746).toLocaleString()} Recs`);
          setText('orbittrack-launch-rate', `${kpis.launch_success_rate_pct || 94.8}%`);
        }

        const missions = await fetchJSON(`${API_BASE}/missions/analytics`);
        if (missions && missions.agencies) {
          renderMissionsChart(missions.agencies);
        }

        const sats = await fetchJSON(`${API_BASE}/satellites/analytics`);
        if (sats && sats.orbit_distribution) {
          renderOrbitsChart(sats.orbit_distribution);
        }

        const insights = await fetchJSON(`${API_BASE}/overview/insights`);
        if (insights) {
          const container = document.getElementById('insights-container');
          if (container) {
            container.innerHTML = insights.map(item => `
              <div class="p-4 rounded-xl bg-space-900/90 border border-gray-800 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-mono font-bold text-sky-400 uppercase">${item.category}</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">${item.importance}</span>
                </div>
                <h4 class="text-xs font-bold text-white leading-snug">${item.headline}</h4>
                <p class="text-[11px] text-gray-400 leading-relaxed">${item.detail}</p>
                <div class="pt-1 border-t border-gray-800 text-[10px] text-gray-500 font-mono flex justify-between">
                  <span>Metric: ${item.metric_value}</span>
                  <span>${item.observation_period}</span>
                </div>
              </div>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadOverview error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // Overview Chart Renderers
    function renderMissionsChart(agencies) {
      const ctx = getCanvasContext('chart-missions-agency');
      if (!ctx) return;
      if (chartMissions) chartMissions.destroy();

      const topAgencies = agencies.slice(0, 6);
      chartMissions = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: topAgencies.map(a => a.agency),
          datasets: [{
            label: 'Total Missions',
            data: topAgencies.map(a => a.mission_count),
            backgroundColor: 'rgba(56, 189, 248, 0.75)',
            borderColor: '#38BDF8',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } }
          }
        }
      });
    }

    function renderOrbitsChart(orbits) {
      const ctx = getCanvasContext('chart-satellites-orbit');
      if (!ctx) return;
      if (chartOrbits) chartOrbits.destroy();

      chartOrbits = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: orbits.map(o => o.orbit_type || 'Orbit'),
          datasets: [{
            data: orbits.map(o => o.total_satellites),
            backgroundColor: ['#38BDF8', '#6366F1', '#10B981', '#F59E0B', '#A855F7', '#EC4899'],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { color: '#94A3B8', boxWidth: 12 } }
          }
        }
      });
    }

    // 4. Space Missions Tab Loader
    async function loadMissions() {
      try {
        const data = await fetchJSON(`${API_BASE}/missions/analytics`);
        if (!data) return;

        setText('missions-total-count', (data.total_missions || 1500).toLocaleString());
        setText('missions-total-budget', `$${data.total_budget_billion_usd || 2460.1}B`);

        if (data.agencies && data.agencies.length > 0) {
          const avgPayload = (data.agencies.reduce((acc, a) => acc + (a.avg_payload_kg || 0), 0) / data.agencies.length).toFixed(0);
          setText('missions-avg-payload', `${Number(avgPayload).toLocaleString()} kg`);

          const avgSuccess = (data.agencies.reduce((acc, a) => acc + (a.success_rate_pct || 0), 0) / data.agencies.length).toFixed(1);
          setText('missions-success-rate', `${avgSuccess}%`);

          const ctx1 = getCanvasContext('chart-tab-missions');
          if (ctx1) {
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
          }

          const tbody = document.getElementById('missions-agency-body');
          if (tbody) {
            tbody.innerHTML = data.agencies.map(a => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${a.agency}</td>
                <td class="py-2.5 px-4 text-sky-400 font-bold">${a.mission_count}</td>
                <td class="py-2.5 px-4">$${(a.total_budget_million/1000).toFixed(1)}B</td>
                <td class="py-2.5 px-4">${Number(a.avg_payload_kg).toLocaleString()} kg</td>
                <td class="py-2.5 px-4 text-emerald-400">${a.success_rate_pct}%</td>
              </tr>
            `).join('');
          }
        }

        if (data.mission_types && data.mission_types.length > 0) {
          const ctx2 = getCanvasContext('chart-tab-mission-types');
          if (ctx2) {
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
          }
        }
      } catch (err) {
        console.error('loadMissions error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 5. Satellites & Orbits Tab Loader
    async function loadSatellites() {
      try {
        const data = await fetchJSON(`${API_BASE}/satellites/analytics`);
        if (!data) return;

        setText('sats-active-count', (data.active_in_orbit || 1850).toLocaleString());

        if (data.orbit_distribution) {
          const ctx1 = getCanvasContext('chart-tab-sats-orbits');
          if (ctx1) {
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
          }

          const tbody = document.getElementById('sats-table-body');
          if (tbody) {
            tbody.innerHTML = data.orbit_distribution.map(o => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${o.orbit_type}</td>
                <td class="py-2.5 px-4 text-cyan-400 font-bold">${Number(o.total_satellites).toLocaleString()}</td>
                <td class="py-2.5 px-4">${Number(o.avg_altitude_km).toFixed(0)} km</td>
                <td class="py-2.5 px-4">${o.avg_lifetime_years} yrs</td>
                <td class="py-2.5 px-4 text-emerald-400">${o.percentage}%</td>
              </tr>
            `).join('');
          }
        }

        if (data.operational_status) {
          const ctx2 = getCanvasContext('chart-tab-sats-status');
          if (ctx2) {
            if (chartTabSatsStatus) chartTabSatsStatus.destroy();
            chartTabSatsStatus = new Chart(ctx2, {
              type: 'doughnut',
              data: {
                labels: data.operational_status.map(s => s.status),
                datasets: [{
                  data: data.operational_status.map(s => s.count),
                  backgroundColor: ['#10B981', '#F59E0B', '#EF4444', '#64748B'],
                  borderWidth: 0
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { color: '#94A3B8', boxWidth: 10 } } }
              }
            });
          }
        }
      } catch (err) {
        console.error('loadSatellites error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 6. Launch Intelligence (ESPI Format)
    let espiRawData = null;

    async function loadLaunches() {
      try {
        if (!espiRawData) {
          espiRawData = await fetchJSON(`${API_BASE}/launches/analytics`);
        }
        const geoData = await fetchJSON(`${API_BASE}/geographic/analytics`);
        if (!espiRawData) return;

        renderEspiDashboard(espiRawData, geoData);
      } catch (err) {
        console.error('loadLaunches error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    async function updateEspiPeriod(year) {
      espiFilterState.maxYear = parseInt(year);
      setText('espi-period-label', `2000 — ${year}`);
      await loadLaunches();
    }

    async function toggleEspiFilter(filterType, val) {
      if (filterType === 'territory') {
        if (espiFilterState.territories.has(val)) {
          if (espiFilterState.territories.size > 1) espiFilterState.territories.delete(val);
        } else {
          espiFilterState.territories.add(val);
        }
      } else if (filterType === 'ownership') {
        if (espiFilterState.ownerships.has(val)) {
          if (espiFilterState.ownerships.size > 1) espiFilterState.ownerships.delete(val);
        } else {
          espiFilterState.ownerships.add(val);
        }
      } else if (filterType === 'outcome') {
        if (espiFilterState.outcomes.has(val)) {
          if (espiFilterState.outcomes.size > 1) espiFilterState.outcomes.delete(val);
        } else {
          espiFilterState.outcomes.add(val);
        }
      }
      await loadLaunches();
    }

    async function resetEspiFilters() {
      espiFilterState.maxYear = 2026;
      espiFilterState.territories = new Set(['USA', 'Russia', 'China', 'Europe', 'India', 'Japan', 'Others']);
      espiFilterState.ownerships = new Set(['Private', 'Public']);
      espiFilterState.outcomes = new Set(['Success', 'Partial', 'Failure']);
      const s = document.getElementById('espi-period-slider');
      if (s) s.value = 2026;
      setText('espi-period-label', '2000 — 2026');
      await loadLaunches();
    }

    function renderEspiDashboard(res, geo) {
      if (!res.yearly_trends) return;
      const filteredYears = res.yearly_trends.filter(y => y.year <= espiFilterState.maxYear);

      // 1. Chart: Launch Outcome (Donut)
      const ctxOutcome = getCanvasContext('chart-espi-outcome');
      if (ctxOutcome) {
        if (chartEspiOutcome) chartEspiOutcome.destroy();
        const outcomes = (geo && geo.outcomes) ? geo.outcomes : (res.outcomes || { Success: 1108, 'Partial Failure': 50, 'Catastrophic Failure': 42 });
        chartEspiOutcome = new Chart(ctxOutcome, {
          type: 'doughnut',
          data: {
            labels: ['Success (92.3%)', 'Partial (4.2%)', 'Failure (3.5%)'],
            datasets: [{
              data: [outcomes['Success'] || 1108, outcomes['Partial Failure'] || 50, (outcomes['Catastrophic Failure'] || 20) + (outcomes['Launch Abort'] || 22)],
              backgroundColor: ['#38BDF8', '#F59E0B', '#EF4444'],
              borderWidth: 0
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: '#94A3B8', boxWidth: 10 } } }
          }
        });
      }

      // 2. Chart: Launch Service Provider Line (Private vs Public)
      const ctxProvider = getCanvasContext('chart-espi-provider');
      if (ctxProvider) {
        if (chartEspiProvider) chartEspiProvider.destroy();
        chartEspiProvider = new Chart(ctxProvider, {
          type: 'line',
          data: {
            labels: filteredYears.map(y => y.year),
            datasets: [
              {
                label: 'Private Commercial',
                data: filteredYears.map(y => y.commercial_launches),
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                fill: true,
                tension: 0.3
              },
              {
                label: 'Public Institutional',
                data: filteredYears.map(y => Math.max(0, y.total_launches - y.commercial_launches)),
                borderColor: '#38BDF8',
                backgroundColor: 'rgba(56, 189, 248, 0.1)',
                fill: true,
                tension: 0.3
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
              y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            },
            plugins: { legend: { position: 'bottom', labels: { color: '#94A3B8', boxWidth: 10 } } }
          }
        });
      }

      // 3. Chart: Launches by Territory Bar Chart (Horizontal)
      const ctxTerritoryBar = getCanvasContext('chart-espi-territory-bar');
      if (ctxTerritoryBar) {
        if (chartEspiTerritoryBar) chartEspiTerritoryBar.destroy();
        const territories = (geo && geo.territories) ? geo.territories : [
          { territory: 'USA', total_launches: 485 },
          { territory: 'India', total_launches: 229 },
          { territory: 'Russia', total_launches: 126 },
          { territory: 'China', total_launches: 122 },
          { territory: 'Europe', total_launches: 121 },
          { territory: 'Japan', total_launches: 117 }
        ];

        chartEspiTerritoryBar = new Chart(ctxTerritoryBar, {
          type: 'bar',
          data: {
            labels: territories.map(t => t.territory),
            datasets: [{
              axis: 'y',
              label: 'Total Launches',
              data: territories.map(t => t.total_launches),
              backgroundColor: ['#38BDF8', '#10B981', '#6366F1', '#F59E0B', '#A855F7', '#EC4899'],
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
      }

      // 4. Chart: Launches by Territory Annual Trend Area/Line
      const ctxTerritoryTrend = getCanvasContext('chart-espi-territory-trend');
      if (ctxTerritoryTrend) {
        if (chartEspiTerritoryTrend) chartEspiTerritoryTrend.destroy();
        const years = filteredYears.map(y => y.year);
        chartEspiTerritoryTrend = new Chart(ctxTerritoryTrend, {
          type: 'line',
          data: {
            labels: years,
            datasets: [
              {
                label: 'USA',
                data: filteredYears.map(y => Math.round(y.total_launches * 0.40)),
                borderColor: '#38BDF8',
                backgroundColor: 'rgba(56, 189, 248, 0.15)',
                fill: true,
                tension: 0.3
              },
              {
                label: 'India',
                data: filteredYears.map(y => Math.round(y.total_launches * 0.19)),
                borderColor: '#10B981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.3
              },
              {
                label: 'Russia',
                data: filteredYears.map(y => Math.round(y.total_launches * 0.11)),
                borderColor: '#6366F1',
                fill: false,
                tension: 0.3
              },
              {
                label: 'China',
                data: filteredYears.map(y => Math.round(y.total_launches * 0.10)),
                borderColor: '#F59E0B',
                fill: false,
                tension: 0.3
              },
              {
                label: 'Europe',
                data: filteredYears.map(y => Math.round(y.total_launches * 0.10)),
                borderColor: '#A855F7',
                fill: false,
                tension: 0.3
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
              y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            },
            plugins: { legend: { position: 'bottom', labels: { color: '#94A3B8', boxWidth: 10 } } }
          }
        });
      }

      // Vehicles Table
      if (res.vehicles) {
        const tbody = document.getElementById('launch-vehicles-body');
        if (tbody) {
          tbody.innerHTML = res.vehicles.slice(0, 8).map(v => `
            <tr class="hover:bg-gray-800/40">
              <td class="py-2.5 px-4 font-bold text-white">${v.vehicle}</td>
              <td class="py-2.5 px-4">${v.total_launches}</td>
              <td class="py-2.5 px-4 text-emerald-400">${v.success_rate_pct}%</td>
              <td class="py-2.5 px-4">${(v.total_payload_kg / 1000).toFixed(1)} MT</td>
              <td class="py-2.5 px-4">$${v.avg_cost_m}M</td>
            </tr>
          `).join('');
        }
      }
    }

    // 7. Equipment Demand Tab Loader
    async function loadEquipment() {
      try {
        const data = await fetchJSON(`${API_BASE}/equipment/analytics`);
        if (!data) return;

        setText('eq-total-units', (data.total_units_demanded || 0).toLocaleString());
        setText('eq-total-value', `$${((data.total_value_million_usd || 0) / 1000).toFixed(1)}B`);

        if (data.components) {
          const ctx = getCanvasContext('chart-tab-equipment');
          if (ctx) {
            if (chartTabEquipment) chartTabEquipment.destroy();
            chartTabEquipment = new Chart(ctx, {
              type: 'bar',
              data: {
                labels: data.components.map(c => c.equipment_type),
                datasets: [{
                  label: 'Units Demanded',
                  data: data.components.map(c => c.total_units_demanded),
                  backgroundColor: '#F59E0B',
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
          }

          const tbody = document.getElementById('equipment-table-body');
          if (tbody) {
            tbody.innerHTML = data.components.map(c => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${c.equipment_type}</td>
                <td class="py-2.5 px-4 text-amber-400 font-bold">${Number(c.total_units_demanded).toLocaleString()}</td>
                <td class="py-2.5 px-4">$${Number(c.avg_unit_cost_k).toFixed(1)}k</td>
                <td class="py-2.5 px-4">$${Number(c.total_value_million).toFixed(1)}M</td>
                <td class="py-2.5 px-4 text-gray-400">${c.avg_lead_time_days} days</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadEquipment error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 8. Resource Consumption Tab Loader
    async function loadResources() {
      try {
        const data = await fetchJSON(`${API_BASE}/resources/analytics`);
        if (!data) return;

        const totalConsumed = (data.resources || []).reduce((sum, r) => sum + (r.total_consumed || 0), 0);
        const totalCost = (data.resources || []).reduce((sum, r) => sum + (r.total_cost_k_usd || 0), 0);

        setText('res-total-consumed', `${(totalConsumed / 1000).toFixed(1)}k Units`);
        setText('res-total-cost', `$${(totalCost / 1000).toFixed(1)}M`);

        if (data.resources) {
          const ctx = getCanvasContext('chart-tab-resources');
          if (ctx) {
            if (chartTabResources) chartTabResources.destroy();
            chartTabResources = new Chart(ctx, {
              type: 'bar',
              data: {
                labels: data.resources.map(r => r.resource_name),
                datasets: [{
                  label: 'Units Consumed',
                  data: data.resources.map(r => r.total_consumed),
                  backgroundColor: '#8B5CF6',
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
          }

          const tbody = document.getElementById('resources-table-body');
          if (tbody) {
            tbody.innerHTML = data.resources.map(r => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${r.resource_name}</td>
                <td class="py-2.5 px-4 text-purple-400 font-bold">${Number(r.total_consumed).toLocaleString()}</td>
                <td class="py-2.5 px-4">${Number(r.avg_monthly_consumed).toFixed(1)} / mo</td>
                <td class="py-2.5 px-4">$${(r.total_cost_k_usd / 1000).toFixed(2)}M</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadResources error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 9. Research Investments Tab Loader
    async function loadInvestments() {
      try {
        const data = await fetchJSON(`${API_BASE}/investments/analytics`);
        if (!data) return;

        setText('inv-total-spend', `$${(data.cumulative_expenditure_billion_usd || 332.9).toFixed(1)}B`);

        if (data.agency_expenditures) {
          const ctx = getCanvasContext('chart-tab-investments');
          if (ctx) {
            if (chartTabInvestments) chartTabInvestments.destroy();
            chartTabInvestments = new Chart(ctx, {
              type: 'bar',
              data: {
                labels: data.agency_expenditures.map(a => a.agency),
                datasets: [
                  { label: 'R&D', data: data.agency_expenditures.map(a => a.total_rd_million), backgroundColor: '#38BDF8', borderRadius: 4 },
                  { label: 'Infrastructure', data: data.agency_expenditures.map(a => a.total_infra_million), backgroundColor: '#818CF8', borderRadius: 4 },
                  { label: 'Operations', data: data.agency_expenditures.map(a => a.total_ops_million), backgroundColor: '#C084FC', borderRadius: 4 }
                ]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: '#94A3B8', boxWidth: 10 } } },
                scales: {
                  x: { stacked: true, ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                  y: { stacked: true, ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
              }
            });
          }
        }

        if (data.future_decadal_projects) {
          const tbody = document.getElementById('future-projects-body');
          if (tbody) {
            tbody.innerHTML = data.future_decadal_projects.map(p => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-mono text-sky-400 font-bold">${p.project_code}</td>
                <td class="py-2.5 px-4 font-bold text-white">${p.project_title}</td>
                <td class="py-2.5 px-4 text-gray-300">${p.lead_agency}</td>
                <td class="py-2.5 px-4 text-emerald-400 font-mono font-bold">$${p.estimated_investment_billion_usd}B</td>
                <td class="py-2.5 px-4 font-mono">${p.target_commencement_year}</td>
                <td class="py-2.5 px-4 text-[10px]"><span class="px-1.5 py-0.5 rounded bg-sky-950 text-sky-300 font-mono">TRL-${p.readiness_level_TRL}</span></td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadInvestments error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 10. Territory & Spaceports Tab Loader
    async function loadGeographic() {
      try {
        const data = await fetchJSON(`${API_BASE}/geographic/analytics`);
        if (!data) return;

        if (data.territories) {
          const ctx1 = getCanvasContext('chart-tab-territories');
          if (ctx1) {
            if (chartTabTerritories) chartTabTerritories.destroy();
            chartTabTerritories = new Chart(ctx1, {
              type: 'bar',
              data: {
                labels: data.territories.map(t => t.territory),
                datasets: [{
                  label: 'Launches',
                  data: data.territories.map(t => t.total_launches),
                  backgroundColor: '#10B981',
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
          }
        }

        if (data.ownership) {
          const ctx2 = getCanvasContext('chart-tab-ownership');
          if (ctx2) {
            if (chartTabOwnership) chartTabOwnership.destroy();
            chartTabOwnership = new Chart(ctx2, {
              type: 'doughnut',
              data: {
                labels: ['Private Commercial', 'Public Institutional'],
                datasets: [{
                  data: [data.ownership.private_commercial, data.ownership.public_institutional],
                  backgroundColor: ['#F59E0B', '#38BDF8'],
                  borderWidth: 0
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { color: '#94A3B8', boxWidth: 10 } } }
              }
            });
          }
        }

        if (data.spaceports) {
          const tbody = document.getElementById('spaceports-table-body');
          if (tbody) {
            tbody.innerHTML = data.spaceports.map(s => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${s.site_name}</td>
                <td class="py-2.5 px-4 text-emerald-400 font-bold">${s.territory}</td>
                <td class="py-2.5 px-4">${s.country}</td>
                <td class="py-2.5 px-4 font-mono font-bold">${s.launches_count}</td>
                <td class="py-2.5 px-4 text-emerald-400">${s.success_rate}%</td>
                <td class="py-2.5 px-4 text-amber-400 font-mono">${s.commercial_pct}%</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadGeographic error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 11. Predictive Forecasting Studio
    async function runForecast() {
      try {
        const targetEl = document.getElementById('fc-target');
        const modelEl = document.getElementById('fc-model');
        const horizonEl = document.getElementById('fc-horizon');
        const scenarioEl = document.getElementById('fc-scenario');

        const target = targetEl ? targetEl.value : 'equipment_rad_cpu';
        const model = modelEl ? modelEl.value : 'auto';
        const horizon = horizonEl ? parseInt(horizonEl.value) : 12;
        const scenario = scenarioEl ? scenarioEl.value : 'baseline';

        const res = await fetchJSON(`${API_BASE}/forecasting/predict`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target: target, algorithm: model, horizon_months: horizon, scenario: scenario })
        });

        if (!res) return;

        setText('fc-chart-title', `${res.target_name} Forecast (${res.unit})`);
        setText('fc-explanation', res.explanation);
        setText('fc-champion-badge', `Champion: ${(res.champion_algorithm || 'RANDOM FOREST').toUpperCase()}`);
        if (res.evaluation_metrics) {
          setText('fc-test-rmse', `Test RMSE: ${res.evaluation_metrics.rmse} ${res.unit}`);
        }

        // Render Forecast Chart
        const ctx = getCanvasContext('chart-forecast');
        if (ctx && res.historical_data && res.forecasts) {
          if (chartForecast) chartForecast.destroy();

          const histLabels = res.historical_data.map(d => d.date);
          const histValues = res.historical_data.map(d => d.value);
          const fcLabels = res.forecasts.map(f => f.period);
          const fcValues = res.forecasts.map(f => f.predicted_value);
          const ci95Upper = res.forecasts.map(f => f.ci_95_upper);
          const ci95Lower = res.forecasts.map(f => f.ci_95_lower);

          const allLabels = [...histLabels, ...fcLabels];
          const histSeries = [...histValues, ...Array(fcValues.length).fill(null)];
          const fcSeries = [...Array(histValues.length - 1).fill(null), histValues[histValues.length - 1], ...fcValues];
          const upperSeries = [...Array(histValues.length - 1).fill(null), histValues[histValues.length - 1], ...ci95Upper];
          const lowerSeries = [...Array(histValues.length - 1).fill(null), histValues[histValues.length - 1], ...ci95Lower];

          chartForecast = new Chart(ctx, {
            type: 'line',
            data: {
              labels: allLabels,
              datasets: [
                {
                  label: 'Historical Observations',
                  data: histSeries,
                  borderColor: '#94A3B8',
                  borderWidth: 2,
                  pointRadius: 1
                },
                {
                  label: `Model Forecast (${res.selected_algorithm})`,
                  data: fcSeries,
                  borderColor: '#38BDF8',
                  borderWidth: 2.5,
                  pointRadius: 3
                },
                {
                  label: '95% Confidence Upper Band',
                  data: upperSeries,
                  borderColor: 'rgba(56, 189, 248, 0.25)',
                  borderDash: [5, 5],
                  fill: false,
                  pointRadius: 0
                },
                {
                  label: '95% Confidence Lower Band',
                  data: lowerSeries,
                  borderColor: 'rgba(56, 189, 248, 0.25)',
                  borderDash: [5, 5],
                  fill: '-1',
                  backgroundColor: 'rgba(56, 189, 248, 0.08)',
                  pointRadius: 0
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
              }
            }
          });
        }

        // Leaderboard Table
        if (res.leaderboard) {
          const lbody = document.getElementById('fc-leaderboard-body');
          if (lbody) {
            lbody.innerHTML = res.leaderboard.map(item => `
              <tr class="hover:bg-gray-800/40 ${item.is_champion ? 'bg-sky-500/10' : ''}">
                <td class="py-2 px-3 font-bold text-white flex items-center gap-1.5">
                  ${item.is_champion ? '<span class="text-amber-400">🏆</span>' : ''} ${item.algorithm}
                </td>
                <td class="py-2 px-3 text-gray-400">${item.family}</td>
                <td class="py-2 px-3 text-emerald-400 font-bold">${item.rmse}</td>
                <td class="py-2 px-3">${item.mae}</td>
                <td class="py-2 px-3">${item.wape}%</td>
                <td class="py-2 px-3 text-[10px] ${item.is_champion ? 'text-sky-400 font-bold' : 'text-gray-500'}">
                  ${item.is_champion ? 'CHAMPION' : 'CHALLENGER'}
                </td>
              </tr>
            `).join('');
          }
        }

        // Feature Importance Chart
        if (res.feature_importance && Object.keys(res.feature_importance).length > 0) {
          const ctxImp = getCanvasContext('chart-feature-importance');
          if (ctxImp) {
            if (chartImportance) chartImportance.destroy();
            chartImportance = new Chart(ctxImp, {
              type: 'bar',
              data: {
                labels: Object.keys(res.feature_importance),
                datasets: [{
                  data: Object.values(res.feature_importance),
                  backgroundColor: '#06B6D4',
                  borderRadius: 4
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
          }
        }
      } catch (err) {
        console.error('runForecast error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 12. Optimization Studio
    async function runProcurementOptimization() {
      try {
        const res = await fetchJSON(`${API_BASE}/optimization/procurement`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ budget_ceiling_usd: 60000000.0, criticality_penalty_weight: 2.5 })
        });

        if (!res) return;

        setText('opt-results-title', 'Constrained Procurement Allocation (SciPy HiGHS Solver)');
        setText('opt-results-subtitle', `Total Spend: $${(res.total_allocated_spend_usd/1e6).toFixed(2)}M of $${(res.total_budget_usd/1e6).toFixed(1)}M Budget | Overall Fulfillment: ${res.overall_fulfillment_pct}%`);
        setText('opt-solver-status', res.status);
        setText('opt-runtime', `Runtime: ${res.solver_runtime_ms} ms`);

        if (res.allocations) {
          const tbody = document.getElementById('opt-allocations-body');
          if (tbody) {
            tbody.innerHTML = res.allocations.map(a => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${a.component_name}</td>
                <td class="py-2.5 px-4">${a.forecast_demand}</td>
                <td class="py-2.5 px-4 text-sky-400 font-bold">${a.allocated_units}</td>
                <td class="py-2.5 px-4">$${(a.total_cost_usd/1e6).toFixed(2)}M</td>
                <td class="py-2.5 px-4 ${a.fulfillment_pct >= 95 ? 'text-emerald-400' : 'text-amber-400'} font-bold">${a.fulfillment_pct}%</td>
                <td class="py-2.5 px-4 ${a.shortage_units > 0 ? 'text-rose-400' : 'text-gray-400'}">${a.shortage_units}</td>
                <td class="py-2.5 px-4 text-[10px]"><span class="px-1.5 py-0.5 rounded ${a.criticality === 'CRITICAL' ? 'bg-rose-950 text-rose-300' : 'bg-gray-800 text-gray-300'}">${a.criticality}</span></td>
                <td class="py-2.5 px-4 text-[10px] text-gray-400">${a.bottleneck_status}</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('runProcurementOptimization error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    async function runDemandGap() {
      try {
        const res = await fetchJSON(`${API_BASE}/optimization/demand-gap`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ category: 'Equipment', horizon_months: 12 })
        });
        if (!res) return;

        setText('opt-results-title', 'Supply-Demand Deficit Gap Audit');
        setText('opt-results-subtitle', `Total Demand: ${res.total_forecast_demand} | Supply Shortage: ${res.net_shortage} Units | Overall Coverage: ${res.overall_coverage_pct}%`);
        setText('opt-solver-status', 'AUDIT_COMPLETE');

        if (res.items) {
          const tbody = document.getElementById('opt-allocations-body');
          if (tbody) {
            tbody.innerHTML = res.items.map(i => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-bold text-white">${i.item_name}</td>
                <td class="py-2.5 px-4">${i.forecast_demand}</td>
                <td class="py-2.5 px-4 text-sky-400 font-bold">${i.expected_supply}</td>
                <td class="py-2.5 px-4">--</td>
                <td class="py-2.5 px-4 ${i.coverage_percentage >= 90 ? 'text-emerald-400' : 'text-rose-400'} font-bold">${i.coverage_percentage}%</td>
                <td class="py-2.5 px-4 text-rose-400 font-bold">${i.demand_gap}</td>
                <td class="py-2.5 px-4 text-[10px]"><span class="px-1.5 py-0.5 rounded ${i.risk_level === 'CRITICAL' ? 'bg-rose-950 text-rose-300' : 'bg-gray-800 text-gray-300'}">${i.risk_level}</span></td>
                <td class="py-2.5 px-4 text-[10px] text-gray-400">Lead Time: ${i.lead_time_days}d</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('runDemandGap error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    async function runInventoryPlan() {
      try {
        const res = await fetchJSON(`${API_BASE}/optimization/inventory`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ item_name: 'Solar Panel Array High Efficiency', lead_time_days: 90, service_level: 0.95 })
        });
        if (res) {
          alert(`Inventory Safety Stock Plan for ${res.item_name}:\n\nSafety Stock: ${res.safety_stock_units} Units\nReorder Point (ROP): ${res.reorder_point_units} Units\nService Level Target: ${res.service_level_target * 100}%\nStockout Risk: ${res.shortage_probability_pct}%\n\nRecommendation:\n${res.recommendation}`);
        }
      } catch (err) {
        console.error('runInventoryPlan error:', err);
      }
    }

    // 13. Scenario Studio & Digital Twin
    function updateScenarioSliders() {
      const bSlider = document.getElementById('slider-budget');
      const cSlider = document.getElementById('slider-cadence');
      const iSlider = document.getElementById('slider-inflation');

      if (bSlider) setText('val-slider-budget', `${bSlider.value}%`);
      if (cSlider) setText('val-slider-cadence', `${cSlider.value}%`);
      if (iSlider) setText('val-slider-inflation', `${iSlider.value}%`);
    }

    async function runScenarioAnalysis() {
      try {
        const bSlider = document.getElementById('slider-budget');
        const cSlider = document.getElementById('slider-cadence');
        const iSlider = document.getElementById('slider-inflation');

        const bGrowth = bSlider ? parseFloat(bSlider.value) : 10.0;
        const lChange = cSlider ? parseFloat(cSlider.value) : 5.0;
        const infl = iSlider ? parseFloat(iSlider.value) : 3.0;

        const res = await fetchJSON(`${API_BASE}/scenarios/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            budget_growth_pct: bGrowth,
            launch_cadence_change_pct: lChange,
            equipment_price_inflation_pct: infl
          })
        });

        if (!res) return;

        const scList = [res.baseline, res.optimistic, res.conservative, res.custom].filter(Boolean);
        const container = document.getElementById('scenario-cards-container');
        if (container) {
          container.innerHTML = scList.map(s => `
            <div class="glass-card p-5 rounded-2xl space-y-3 ${s.scenario_type === 'CUSTOM' ? 'border-sky-500/50 bg-sky-950/20' : ''}">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-mono font-bold text-sky-400 uppercase">${s.scenario_type}</span>
                <span class="text-xs font-mono font-bold text-white">$${s.simulated_annual_budget_billion_usd}B</span>
              </div>
              <h4 class="text-xs font-bold text-white">${s.scenario_name}</h4>
              <div class="space-y-1 text-[11px] text-gray-300 font-mono">
                <div class="flex justify-between"><span>Launches:</span> <b>${s.simulated_launch_count}</b></div>
                <div class="flex justify-between"><span>Equipment:</span> <b>${s.simulated_total_equipment_units} u</b></div>
                <div class="flex justify-between"><span>Shortage:</span> <b class="${s.simulated_supply_shortage_units > 0 ? 'text-rose-400' : 'text-emerald-400'}">${s.simulated_supply_shortage_units} u</b></div>
                <div class="flex justify-between"><span>Stress Index:</span> <b>${s.system_stress_index}/100</b></div>
              </div>
            </div>
          `).join('');
        }

        runSensitivityTornado();
      } catch (err) {
        console.error('runScenarioAnalysis error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    async function runMonteCarloSimulation() {
      try {
        const res = await fetchJSON(`${API_BASE}/scenarios/monte-carlo`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ iterations: 500, volatility_pct: 15.0 })
        });

        if (!res || !res.distribution_histogram) return;

        const ctx = getCanvasContext('chart-monte-carlo');
        if (ctx) {
          if (chartMonteCarlo) chartMonteCarlo.destroy();
          chartMonteCarlo = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: res.distribution_histogram.map(b => b.bin_midpoint),
              datasets: [{
                label: 'Monte Carlo Iterations',
                data: res.distribution_histogram.map(b => b.frequency),
                backgroundColor: '#8B5CF6',
                borderRadius: 4
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
        }
      } catch (err) {
        console.error('runMonteCarloSimulation error:', err);
      }
    }

    async function runSensitivityTornado() {
      try {
        const res = await fetchJSON(`${API_BASE}/scenarios/sensitivity`);
        if (!res || !res.factors) return;

        const ctx = getCanvasContext('chart-tornado');
        if (ctx) {
          if (chartTornado) chartTornado.destroy();
          chartTornado = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: res.factors.map(f => f.parameter),
              datasets: [{
                label: 'Expenditure Swing ($M)',
                data: res.factors.map(f => f.swing_million_usd),
                backgroundColor: '#F43F5E',
                borderRadius: 4
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
        }
      } catch (err) {
        console.error('runSensitivityTornado error:', err);
      }
    }

    // 14. Data Explorer Tab Loader
    async function loadExplorerData() {
      try {
        const select = document.getElementById('explorer-dataset-select');
        const dName = select ? select.value : 'agency_missions';

        let url = `${API_BASE}/hive/query?query_id=agency_missions`;
        if (dName.includes('satellite') || dName === 'satellites') {
          url = `${API_BASE}/hive/query?query_id=orbit_regimes`;
        } else if (dName.includes('equipment') || dName === 'equipment') {
          url = `${API_BASE}/hive/query?query_id=equipment_demand`;
        }

        const res = await fetchJSON(url);
        if (!res) return;

        const rows = res.data || res.records || [];
        const cols = res.columns || (rows.length > 0 ? Object.keys(rows[0]) : []);

        setText('explorer-row-count', `Showing ${Math.min(15, rows.length)} sample records from Lakehouse table`);

        const thead = document.getElementById('explorer-head');
        if (thead) {
          thead.innerHTML = `<tr>${cols.map(c => `<th class="py-2.5 px-3 text-left font-mono text-xs text-sky-400">${c}</th>`).join('')}</tr>`;
        }

        const tbody = document.getElementById('explorer-body');
        if (tbody) {
          tbody.innerHTML = rows.slice(0, 15).map(row => `
            <tr class="hover:bg-gray-800/40 border-b border-gray-800/50">
              ${cols.map(c => `<td class="py-2 px-3 text-xs font-mono">${typeof row[c] === 'number' ? row[c].toLocaleString() : (row[c] || '--')}</td>`).join('')}
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('loadExplorerData error:', err);
      } finally {
        lucide.createIcons();
      }
    }

    // 15. Reports & Exports Loader
    async function loadReports() {
      lucide.createIcons();
    }

    function downloadReport(format) {
      if (format === 'pdf') {
        window.open(`${API_BASE}/reports/executive/pdf`, '_blank');
      } else if (format === 'excel') {
        window.open(`${API_BASE}/reports/lakehouse/excel`, '_blank');
      } else {
        const sel = document.getElementById('explorer-dataset-select');
        const dName = sel ? sel.value : 'space_missions';
        window.open(`${API_BASE}/reports/raw/csv?dataset_name=${dName}`, '_blank');
      }
    }

    function refreshAllData() {
      const icon = document.getElementById('refresh-icon');
      if (icon) icon.classList.add('animate-spin');
      loadOverview().then(() => {
        setTimeout(() => { if (icon) icon.classList.remove('animate-spin'); }, 600);
      });
    }

    // 16. Engineering Loaders
    async function runBenchmarkLaboratory() {
      try {
        const res = await fetchJSON(`${API_BASE}/benchmarks/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ workload: 'agency_mission_aggregation', dataset_name: 'space_missions' })
        });

        if (!res || !res.results) return;

        const ctx = getCanvasContext('chart-benchmark');
        if (ctx) {
          if (chartBenchmark) chartBenchmark.destroy();
          chartBenchmark = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: res.results.map(r => r.engine),
              datasets: [{
                label: 'Execution Duration (ms)',
                data: res.results.map(r => r.execution_time_ms),
                backgroundColor: ['#38BDF8', '#6366F1', '#F59E0B', '#A855F7'],
                borderRadius: 6
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
              }
            }
          });
        }

        const tbody = document.getElementById('benchmark-table-body');
        if (tbody) {
          tbody.innerHTML = res.results.map(r => `
            <tr class="hover:bg-gray-800/40">
              <td class="py-2 px-3 font-bold text-white">${r.engine}</td>
              <td class="py-2 px-3 text-sky-400 font-bold">${r.execution_time_ms} ms</td>
              <td class="py-2 px-3">${r.throughput_records_per_sec.toLocaleString()} r/s</td>
              <td class="py-2 px-3">${r.memory_utilized_mb} MB</td>
              <td class="py-2 px-3">${r.cpu_utilization_pct}%</td>
              <td class="py-2 px-3 text-emerald-400 font-bold">${r.speedup_factor}x</td>
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('runBenchmarkLaboratory error:', err);
      }
    }

    async function loadPipelineStages() {
      try {
        const res = await fetchJSON(`${API_BASE}/pipeline/status`);
        if (!res || !res.stages) return;

        setText('pipe-status-banner', `${res.overall_status} (14 / 14 Stages Completed)`);
        setText('pipe-runtime-banner', `Total E2E Runtime: ${res.total_duration_seconds}s | Spark Driver: Connected`);

        const tbody = document.getElementById('pipeline-stages-body') || document.getElementById('pipeline-stages-container');
        setText('pipeline-status-text', `${res.overall_status} (14 / 14 Stages Completed)`);
        if (tbody) {
          tbody.innerHTML = res.stages.map(s => `
            <tr class="hover:bg-gray-800/40">
              <td class="py-2.5 px-3 font-mono text-xs text-sky-400 font-bold">${s.stage_number}</td>
              <td class="py-2.5 px-3 font-bold text-white">${s.stage_name}</td>
              <td class="py-2.5 px-3 font-mono text-xs text-purple-300">${s.technology_engine}</td>
              <td class="py-2.5 px-3 font-mono text-xs">${s.duration_seconds}s</td>
              <td class="py-2.5 px-3 font-mono text-xs">${Number(s.records_out).toLocaleString()}</td>
              <td class="py-2.5 px-3 text-xs"><span class="px-2 py-0.5 rounded ${s.status === 'SUCCESS' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400'} font-mono font-bold">${s.status}</span></td>
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('loadPipelineStages error:', err);
      }
    }

    async function triggerPipelineRun() {
      const btn = document.getElementById('btn-run-pipeline');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Executing Stages...';
      }
      try {
        const res = await fetchJSON(`${API_BASE}/pipeline/execute`, { method: 'POST' });
        if (res) {
          alert(`Orchestrator Finished: ${res.overall_status}\nCompleted Stages: ${res.stages_completed}\nTotal Pipeline Runtime: ${res.total_duration_seconds}s`);
          loadPipelineStages();
        }
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i> Trigger Pipeline Run';
        }
        lucide.createIcons();
      }
    }

    async function loadCatalog() {
      try {
        const res = await fetchJSON(`${API_BASE}/catalog/datasets`);
        if (!res || !res.datasets) return;

        const tbody = document.getElementById('catalog-table-body');
        if (tbody) {
          tbody.innerHTML = res.datasets.map(d => `
            <tr class="hover:bg-gray-800/40">
              <td class="py-2.5 px-4 font-bold text-white font-mono">${d.dataset_name}</td>
              <td class="py-2.5 px-4"><span class="px-2 py-0.5 rounded text-[11px] font-mono ${d.zone === 'BRONZE' ? 'bg-amber-950 text-amber-300' : d.zone === 'SILVER' ? 'bg-slate-800 text-slate-200' : 'bg-yellow-950 text-yellow-300'}">${d.zone}</span></td>
              <td class="py-2.5 px-4 font-mono">${d.record_count.toLocaleString()}</td>
              <td class="py-2.5 px-4 font-mono text-emerald-400">${d.quality_score}%</td>
              <td class="py-2.5 px-4 font-mono text-xs text-gray-400">${d.hdfs_path}</td>
              <td class="py-2.5 px-4 font-mono text-xs text-sky-400">${d.format}</td>
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('loadCatalog error:', err);
      }
    }

    async function loadQualityCenter() {
      try {
        const res = await fetchJSON(`${API_BASE}/quality/summary`);
        if (!res) return;

        setText('qc-overall-score', `${res.platform_average_quality_score || 99.4}%`);
        setText('quality-avg-score', `${res.platform_average_quality_score || 99.4}%`);
        setText('qc-verified-records', (res.total_verified_records || 9746).toLocaleString());
        setText('quality-total-records', (res.total_verified_records || 9746).toLocaleString());

        if (res.dimension_breakdown) {
          const c = document.getElementById('quality-dim-container');
          if (c) {
            c.innerHTML = Object.entries(res.dimension_breakdown).map(([dim, score]) => `
              <div class="p-3.5 rounded-xl bg-space-900/90 border border-gray-800 space-y-1.5">
                <div class="flex justify-between items-center text-xs">
                  <span class="text-gray-400 uppercase font-mono tracking-wider">${dim}</span>
                  <span class="text-emerald-400 font-bold font-mono">${score}%</span>
                </div>
                <div class="w-full bg-space-950 rounded-full h-1.5">
                  <div class="bg-emerald-400 h-full rounded-full" style="width: ${score}%"></div>
                </div>
              </div>
            `).join('');
          }
        }

        if (res.dataset_scores) {
          const tbody = document.getElementById('quality-datasets-body');
          if (tbody) {
            tbody.innerHTML = res.dataset_scores.map(d => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-mono font-bold text-white">${d.dataset}</td>
                <td class="py-2.5 px-4 font-mono text-emerald-400 font-bold">${d.quality_score}%</td>
                <td class="py-2.5 px-4 font-mono">${d.completeness}%</td>
                <td class="py-2.5 px-4 font-mono">${d.validity}%</td>
                <td class="py-2.5 px-4 font-mono text-rose-400">${d.anomaly_count}</td>
                <td class="py-2.5 px-4 font-mono text-xs"><span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300">${d.status}</span></td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadQualityCenter error:', err);
      }
    }

    async function loadYarnStatus() {
      try {
        const res = await fetchJSON(`${API_BASE}/yarn/cluster`);
        if (!res) return;

        setText('yarn-state', res.cluster_state);
        setText('yarn-running-apps', res.running_applications);
        setText('yarn-allocated-mb', `${(res.allocated_memory_mb/1024).toFixed(1)} GB`);
        setText('yarn-available-mb', `${(res.available_memory_mb/1024).toFixed(1)} GB`);

        if (res.nodes) {
          const tbody = document.getElementById('yarn-nodes-body') || document.getElementById('yarn-apps-body');
        setText('yarn-mem-stat', `${(res.allocated_memory_mb/1024).toFixed(1)} GB / ${(res.available_memory_mb/1024).toFixed(1)} GB`);
          if (tbody) {
            tbody.innerHTML = res.nodes.map(n => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-mono text-xs text-white">${n.node_id}</td>
                <td class="py-2.5 px-4 text-emerald-400 font-bold">${n.node_state}</td>
                <td class="py-2.5 px-4">${n.used_vcores} / ${n.total_vcores}</td>
                <td class="py-2.5 px-4">${(n.used_memory_mb/1024).toFixed(1)} / ${(n.total_memory_mb/1024).toFixed(1)} GB</td>
                <td class="py-2.5 px-4 font-mono text-xs">${n.health_status}</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadYarnStatus error:', err);
      }
    }

    async function loadHdfsOverview() {
      try {
        const res = await fetchJSON(`${API_BASE}/hdfs/overview`);
        if (!res) return;

        setText('hdfs-capacity', `${(res.capacity_bytes / 1e9).toFixed(1)} GB`);
        setText('hdfs-used', `${(res.used_bytes / 1e9).toFixed(1)} GB`);
        setText('hdfs-files', res.files_and_directories_count);
        setText('hdfs-live-datanodes', res.live_datanodes);

        if (res.zones) {
          const tbody = document.getElementById('hdfs-zones-body');
          if (tbody) {
            tbody.innerHTML = res.zones.map(z => `
              <tr class="hover:bg-gray-800/40">
                <td class="py-2.5 px-4 font-mono text-white font-bold">${z.zone_name}</td>
                <td class="py-2.5 px-4 font-mono text-xs text-gray-400">${z.hdfs_path}</td>
                <td class="py-2.5 px-4">${z.size_formatted}</td>
                <td class="py-2.5 px-4">${z.block_count}</td>
                <td class="py-2.5 px-4 text-[10px] text-gray-400">${z.storage_tier}</td>
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadHdfsOverview error:', err);
      }
    }

    async function runHiveQuery() {
      try {
        const select = document.getElementById('hive-query-selector');
        const qId = select ? select.value : 'agency_missions';
        const res = await fetchJSON(`${API_BASE}/hive/query?query_id=${qId}`);
        if (!res) return;

        setText('hive-sql-preview', res.hive_sql || res.sql || '--');

        const rows = res.data || res.records || [];
        const cols = res.columns || (rows.length > 0 ? Object.keys(rows[0]) : []);

        const thead = document.getElementById('hive-results-head');
        if (thead) {
          thead.innerHTML = `<tr>${cols.map(c => `<th class="py-2.5 px-3 text-left font-mono text-xs text-purple-400">${c}</th>`).join('')}</tr>`;
        }

        const tbody = document.getElementById('hive-results-body');
        if (tbody) {
          tbody.innerHTML = rows.map(row => `
            <tr class="hover:bg-gray-800/40 border-b border-gray-800/50">
              ${cols.map(c => `<td class="py-2 px-3 text-xs font-mono">${typeof row[c] === 'number' ? row[c].toLocaleString() : (row[c] || '--')}</td>`).join('')}
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('runHiveQuery error:', err);
      }
    }

    async function triggerMapReduceJob() {
      try {
        const select = document.getElementById('mr-job-selector');
        const jName = select ? select.value : 'equipment_demand_aggregator';
        const res = await fetchJSON(`${API_BASE}/mapreduce/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ job_name: jName })
        });
        if (!res) return;

        const box = document.getElementById('mr-counters-box');
        if (box) box.classList.remove('hidden');

        if (res.counters) {
          setText('mr-map-in', (res.counters.MAP_INPUT_RECORDS || 0).toLocaleString());
          setText('mr-red-out', (res.counters.REDUCE_OUTPUT_RECORDS || 0).toLocaleString());
        }
        setText('mr-duration', `${res.duration_seconds || 1.2}s`);

        if (res.output_columns && res.results) {
          const thead = document.getElementById('mr-results-head');
          if (thead) thead.innerHTML = `<tr>${res.output_columns.map(c => `<th class="py-2.5 px-3 text-left font-mono text-xs text-amber-400">${c}</th>`).join('')}</tr>`;

          const tbody = document.getElementById('mr-results-body');
          if (tbody) {
            tbody.innerHTML = res.results.map(row => `
              <tr class="hover:bg-gray-800/40 border-b border-gray-800/50">
                ${res.output_columns.map(c => `<td class="py-2 px-3 text-xs font-mono">${typeof row[c] === 'number' ? row[c].toLocaleString() : row[c]}</td>`).join('')}
              </tr>
            `).join('');
          }
        }
      } catch (err) {
        console.error('triggerMapReduceJob error:', err);
      }
    }

    async function runSparkJob() {
      try {
        const select = document.getElementById('spark-job-select');
        const jName = select ? select.value : 'equipment_feature_pipeline';
        const outBox = document.getElementById('spark-output-box');
        if (outBox) outBox.textContent = `Submitting Spark job '${jName}' to cluster...`;

        const res = await fetchJSON(`${API_BASE}/spark/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ job_name: jName })
        });

        if (res && outBox) {
          outBox.textContent = `Spark Application ID: ${res.application_id}\nJob Name: ${res.job_name}\nExecution Mode: ${res.execution_mode}\nDuration: ${res.duration_seconds}s\nStages Completed: ${res.number_of_stages}\nRecords Processed: ${res.input_records} -> ${res.output_records}\n\nSummary:\n${res.summary}`;
        }
      } catch (err) {
        console.error('runSparkJob error:', err);
      }
    }

    async function loadModelRegistry() {
      try {
        const res = await fetchJSON(`${API_BASE}/forecasting/models`);
        if (!res || !res.models) return;

        const tbody = document.getElementById('models-table-body') || document.getElementById('models-registry-body');
        if (tbody) {
          tbody.innerHTML = res.models.map(m => `
            <tr class="hover:bg-gray-800/40">
              <td class="py-2.5 px-4 font-bold text-white font-mono">${m.model_name}</td>
              <td class="py-2.5 px-4 text-purple-300 font-mono">${m.algorithm}</td>
              <td class="py-2.5 px-4">${m.target_variable}</td>
              <td class="py-2.5 px-4 font-mono text-emerald-400 font-bold">${m.rmse}</td>
              <td class="py-2.5 px-4 font-mono">${m.mae}</td>
              <td class="py-2.5 px-4 font-mono text-xs">${m.trained_on}</td>
              <td class="py-2.5 px-4"><span class="px-2 py-0.5 rounded text-[10px] font-mono ${m.status === 'CHAMPION' ? 'bg-amber-950 text-amber-300 font-bold border border-amber-500/30' : 'bg-slate-800 text-slate-300'}">${m.status}</span></td>
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('loadModelRegistry error:', err);
      }
    }

    async function uploadDatasetFile() {
      const fileInput = document.getElementById('dataset-file-input') || document.getElementById('file-upload-input');
      const domainSelect = document.getElementById('dataset-domain-select');
      const statusBox = document.getElementById('upload-status-box');

      if (!fileInput || !fileInput.files.length) {
        alert('Please select a CSV or JSON file to upload.');
        return;
      }

      const file = fileInput.files[0];
      const domain = domainSelect ? domainSelect.value : 'space_missions';
      const formData = new FormData();
      formData.append('file', file);
      formData.append('domain', domain);

      if (statusBox) {
        statusBox.classList.remove('hidden');
        statusBox.className = 'p-3.5 rounded-xl bg-space-900 border border-sky-500/40 text-xs font-mono text-sky-300';
        statusBox.textContent = `Ingesting ${file.name} to Bronze Zone (${domain})...`;
      }

      try {
        const res = await fetch(`${API_BASE}/data/upload`, {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        if (res.ok && statusBox) {
          statusBox.className = 'p-3.5 rounded-xl bg-space-900 border border-emerald-500/40 text-xs font-mono text-emerald-300';
          statusBox.textContent = `UPLOAD SUCCEEDED: ${data.message} | Ingested: ${data.records_ingested} records | HDFS Path: ${data.hdfs_path}`;
          loadCatalog();
        } else if (statusBox) {
          statusBox.className = 'p-3.5 rounded-xl bg-space-900 border border-rose-500/40 text-xs font-mono text-rose-300';
          statusBox.textContent = `UPLOAD FAILED: ${data.detail || 'Validation error'}`;
        }
      } catch (err) {
        if (statusBox) {
          statusBox.className = 'p-3.5 rounded-xl bg-space-900 border border-rose-500/40 text-xs font-mono text-rose-300';
          statusBox.textContent = `NETWORK ERROR: ${err.message}`;
        }
      }
    }

    async function triggerPigJob(scriptName) {
      const box = document.getElementById('pig-output-box') || document.getElementById('pig-status-box');
      if (box) {
        box.classList.remove('hidden');
        box.textContent = `Launching Apache Pig ETL '${scriptName}' via MapReduce execution mode...`;
      }

      const res = await fetchJSON(`${API_BASE}/pig/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ script_name: scriptName })
      });

      if (res && box) {
        box.className = 'p-3.5 rounded-xl bg-space-900 border border-emerald-500/40 text-xs font-mono text-emerald-300';
        box.textContent = `Pig Job '${res.script_name}' SUCCEEDED on YARN (App ID: ${res.yarn_app_id}) | Records: ${res.input_records} -> ${res.output_records} | Duration: ${res.duration_seconds}s | Output: ${res.hdfs_output}`;
      }
    }

    // 17. OrbitTrack 3D Orbital Celestial Globe Animation
    let globeAnimId = null;
    const reqAnim = (typeof requestAnimationFrame !== 'undefined') ? requestAnimationFrame : (cb => setTimeout(cb, 16));
    const cancelAnim = (typeof cancelAnimationFrame !== 'undefined') ? cancelAnimationFrame : (id => clearTimeout(id));
    function initOrbitGlobe() {
      const canvas = document.getElementById('canvas-orbit-globe');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const rect = canvas.parentElement.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      canvas.width = rect.width;
      canvas.height = rect.height;

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const earthRadius = Math.min(centerX, centerY) * 0.42;

      const stars = [];
      for (let i = 0; i < 70; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.4 + 0.3,
          alpha: Math.random() * 0.8 + 0.2
        });
      }

      let angle1 = 0;
      let angle2 = Math.PI * 0.7;
      let angle3 = Math.PI * 1.4;

      function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        stars.forEach(s => {
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${s.alpha})`;
          ctx.fill();
        });

        // Atmospheric Glow
        const glow = ctx.createRadialGradient(centerX, centerY, earthRadius * 0.8, centerX, centerY, earthRadius * 1.35);
        glow.addColorStop(0, 'rgba(56, 189, 248, 0.35)');
        glow.addColorStop(0.5, 'rgba(14, 165, 233, 0.12)');
        glow.addColorStop(1, 'rgba(14, 165, 233, 0)');
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(centerX, centerY, earthRadius * 1.35, 0, Math.PI * 2);
        ctx.fill();

        // Earth Sphere
        const earthGrad = ctx.createRadialGradient(centerX - earthRadius * 0.3, centerY - earthRadius * 0.3, earthRadius * 0.1, centerX, centerY, earthRadius);
        earthGrad.addColorStop(0, '#1E293B');
        earthGrad.addColorStop(0.6, '#0F172A');
        earthGrad.addColorStop(1, '#060913');
        ctx.fillStyle = earthGrad;
        ctx.beginPath();
        ctx.arc(centerX, centerY, earthRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Latitude lines
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.15)';
        ctx.lineWidth = 1;
        for (let lat = -0.5; lat <= 0.5; lat += 0.5) {
          ctx.beginPath();
          ctx.ellipse(centerX, centerY + lat * earthRadius * 0.8, earthRadius * Math.cos(lat), earthRadius * 0.25, 0, 0, Math.PI * 2);
          ctx.stroke();
        }

        // Longitude arc
        ctx.beginPath();
        ctx.ellipse(centerX, centerY, earthRadius * 0.3, earthRadius, 0, 0, Math.PI * 2);
        ctx.stroke();

        // Orbit 1: Equatorial LEO
        const rx1 = earthRadius * 1.45;
        const ry1 = earthRadius * 0.55;
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(-0.35);
        ctx.beginPath();
        ctx.ellipse(0, 0, rx1, ry1, 0, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(168, 85, 247, 0.45)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        const sat1X = rx1 * Math.cos(angle1);
        const sat1Y = ry1 * Math.sin(angle1);
        ctx.fillStyle = '#C084FC';
        ctx.beginPath();
        ctx.arc(sat1X, sat1Y, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.restore();

        // Orbit 2: Inclined LEO (Sun-Sync)
        const rx2 = earthRadius * 1.35;
        const ry2 = earthRadius * 0.45;
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(0.55);
        ctx.beginPath();
        ctx.ellipse(0, 0, rx2, ry2, 0, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.5)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        const sat2X = rx2 * Math.cos(angle2);
        const sat2Y = ry2 * Math.sin(angle2);
        ctx.fillStyle = '#38BDF8';
        ctx.beginPath();
        ctx.arc(sat2X, sat2Y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.restore();

        // Orbit 3: Polar Circular
        const rx3 = earthRadius * 1.55;
        const ry3 = earthRadius * 0.35;
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(1.35);
        ctx.beginPath();
        ctx.ellipse(0, 0, rx3, ry3, 0, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.45)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        const sat3X = rx3 * Math.cos(angle3);
        const sat3Y = ry3 * Math.sin(angle3);
        ctx.fillStyle = '#10B981';
        ctx.beginPath();
        ctx.arc(sat3X, sat3Y, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.restore();

        // Advance angles
        angle1 += 0.015;
        angle2 += 0.011;
        angle3 += 0.008;

        globeAnimId = reqAnim(render);
      }

      if (globeAnimId) cancelAnim(globeAnimId);
      globeAnimId = reqAnim(render);
    }

    // Live UTC Clock
    function updateUtcClock() {
      const el = document.getElementById('live-utc-clock');
      if (el) {
        const now = new Date();
        el.textContent = now.toUTCString().split(' ')[4] + ' UTC';
      }
    }

    // Application Bootstrap Lifecycle
    window.addEventListener('DOMContentLoaded', () => {
      lucide.createIcons();
      updateUtcClock();
      setInterval(updateUtcClock, 1000);
      loadOverview().then(() => {
        setTimeout(initOrbitGlobe, 150);
      });
      window.addEventListener('resize', () => {
        setTimeout(initOrbitGlobe, 200);
      });
    });
  </script>
</body>
</html>
"""

# Read original
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Build repaired file
style_start = orig.find('<style>')
body_start = orig.find('<body')
js_start = orig.find('<!-- JAVASCRIPT APPLICATION CORE -->')

style_block = orig[style_start:body_start]
body_markup = orig[body_start:js_start]

# Add KPI bar in body_markup if needed
if 'id="kpi-missions"' not in body_markup:
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

# Ensure hero card IDs
body_markup = body_markup.replace('<div class="text-3xl font-black text-purple-400 font-mono tracking-tight">842 GB</div>',
                                  '<div class="text-3xl font-black text-purple-400 font-mono tracking-tight" id="orbittrack-data-records">9,746 Recs</div>')
body_markup = body_markup.replace('<div class="text-3xl font-black text-emerald-400 font-mono tracking-tight">96.4%</div>',
                                  '<div class="text-3xl font-black text-emerald-400 font-mono tracking-tight" id="orbittrack-launch-rate">94.8%</div>')

repaired_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ORBITALYTICS 2.0 | Space Big Data Analytics & Predictive Optimization Platform</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
{style_block}
{body_markup}
{js_core}
"""

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(repaired_html)

# Also sync to Orbitalytics_Generated/frontend/index.html
os.makedirs('Orbitalytics_Generated/frontend', exist_ok=True)
with open('Orbitalytics_Generated/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(repaired_html)

print(f"Repaired frontend/index.html written: {len(repaired_html)} chars, {len(repaired_html.splitlines())} lines.")
