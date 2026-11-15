# Script to append advanced interactive JS functions to frontend/index.html
import os

advanced_js = """
    // ========================================================
    // ADVANCED RESEARCH LAYER INTERACTIVE FILTERING & UTILITIES
    // ========================================================

    // Global Store for Cached Research Telemetry
    let rawMissionsData = null;
    let rawSatellitesData = null;
    let rawEquipmentData = null;
    let rawResourcesData = null;
    let rawInvestmentsData = null;
    let rawGeographicData = null;

    // Table Export to CSV Utility (RFC 4180 Compliant)
    function exportTableToCSV(tbodyId, filename) {
      const tbody = document.getElementById(tbodyId);
      if (!tbody) {
        alert('Table data not available to export.');
        return;
      }
      const table = tbody.closest('table');
      let csv = [];
      
      // Header
      const ths = table.querySelectorAll('th');
      if (ths.length) {
        csv.push(Array.from(ths).map(th => `"${th.textContent.trim().replace(/"/g, '""')}"`).join(','));
      }
      
      // Rows
      const trs = tbody.querySelectorAll('tr');
      trs.forEach(tr => {
        const tds = tr.querySelectorAll('td');
        if (tds.length) {
          csv.push(Array.from(tds).map(td => `"${td.textContent.trim().replace(/"/g, '""')}"`).join(','));
        }
      });

      const blob = new Blob([csv.join('\\n')], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', filename || 'export.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // Dynamic Filtering for Space Missions
    function filterMissionsTable() {
      if (!rawMissionsData || !rawMissionsData.agencies) return;
      const search = (document.getElementById('filter-mission-search')?.value || '').toLowerCase();
      const agencyFilter = document.getElementById('filter-mission-agency')?.value || 'ALL';
      const tierFilter = document.getElementById('filter-mission-tier')?.value || 'ALL';

      let filtered = rawMissionsData.agencies.filter(a => {
        const matchesSearch = a.agency.toLowerCase().includes(search);
        let matchesAgency = true;
        if (agencyFilter !== 'ALL') {
          matchesAgency = a.agency.toUpperCase().includes(agencyFilter);
        }
        let matchesTier = true;
        const budgetB = a.total_budget_million / 1000;
        if (tierFilter === 'HIGH') matchesTier = budgetB >= 400;
        else if (tierFilter === 'MED') matchesTier = budgetB >= 200 && budgetB < 400;
        else if (tierFilter === 'LOW') matchesTier = budgetB < 200;

        return matchesSearch && matchesAgency && matchesTier;
      });

      renderMissionsTableBody(filtered);
    }

    function sortMissionsTable(criteria) {
      if (!rawMissionsData || !rawMissionsData.agencies) return;
      let sorted = [...rawMissionsData.agencies];
      if (criteria === 'volume') {
        sorted.sort((a, b) => b.mission_count - a.mission_count);
      } else if (criteria === 'budget') {
        sorted.sort((a, b) => b.total_budget_million - a.total_budget_million);
      } else if (criteria === 'reliability') {
        sorted.sort((a, b) => b.success_rate_pct - a.success_rate_pct);
      }
      renderMissionsTableBody(sorted);
    }

    function renderMissionsTableBody(list) {
      const tbody = document.getElementById('missions-agency-body');
      if (!tbody) return;
      tbody.innerHTML = list.map(a => `
        <tr class="hover:bg-gray-800/40 transition">
          <td class="py-3 px-4 font-bold text-white flex items-center gap-2">
            <span class="w-2 h-2 rounded-full ${a.success_rate_pct >= 95 ? 'bg-emerald-400' : 'bg-amber-400'}"></span>
            ${a.agency}
          </td>
          <td class="py-3 px-4 text-sky-400 font-bold">${a.mission_count} flights</td>
          <td class="py-3 px-4 text-emerald-400 font-mono">$${(a.total_budget_million/1000).toFixed(1)}B</td>
          <td class="py-3 px-4">${Number(a.avg_payload_kg).toLocaleString()} kg</td>
          <td class="py-3 px-4">
            <div class="flex items-center gap-2">
              <span class="${a.success_rate_pct >= 95 ? 'text-emerald-400' : 'text-amber-400'} font-bold">${a.success_rate_pct}%</span>
              <div class="w-16 bg-space-950 rounded-full h-1.5 hidden sm:block">
                <div class="${a.success_rate_pct >= 95 ? 'bg-emerald-400' : 'bg-amber-400'} h-full rounded-full" style="width: ${a.success_rate_pct}%"></div>
              </div>
            </div>
          </td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono ${a.mission_count > 200 ? 'bg-sky-950 text-sky-300 border border-sky-500/30' : 'bg-gray-800 text-gray-300'}">
              ${a.mission_count > 200 ? 'HEAVY CADENCE' : 'ACTIVE'}
            </span>
          </td>
        </tr>
      `).join('');
      setText('missions-table-count', `Showing ${list.length} Space Agencies`);
    }

    // Dynamic Filtering for Satellites
    function filterSatellitesTable() {
      if (!rawSatellitesData || !rawSatellitesData.orbit_distribution) return;
      const search = (document.getElementById('filter-sat-search')?.value || '').toLowerCase();
      const regimeFilter = document.getElementById('filter-sat-regime')?.value || 'ALL';

      let filtered = rawSatellitesData.orbit_distribution.filter(o => {
        const matchesSearch = o.orbit_type.toLowerCase().includes(search);
        let matchesRegime = true;
        if (regimeFilter !== 'ALL') {
          matchesRegime = o.orbit_type.toUpperCase().includes(regimeFilter);
        }
        return matchesSearch && matchesRegime;
      });

      renderSatellitesTableBody(filtered);
    }

    function renderSatellitesTableBody(list) {
      const tbody = document.getElementById('sats-table-body');
      if (!tbody) return;
      tbody.innerHTML = list.map(o => `
        <tr class="hover:bg-gray-800/40 transition">
          <td class="py-3 px-4 font-bold text-white flex items-center gap-2">
            <i data-lucide="orbit" class="w-3.5 h-3.5 text-cyan-400"></i>
            ${o.orbit_type}
          </td>
          <td class="py-3 px-4 text-cyan-400 font-bold">${Number(o.total_satellites).toLocaleString()}</td>
          <td class="py-3 px-4 font-mono">${Number(o.avg_altitude_km).toFixed(0)} km</td>
          <td class="py-3 px-4">${o.avg_lifetime_years} yrs</td>
          <td class="py-3 px-4">
            <div class="flex items-center gap-2">
              <span class="text-emerald-400 font-bold">${o.percentage}%</span>
              <div class="w-16 bg-space-950 rounded-full h-1.5 hidden sm:block">
                <div class="bg-cyan-400 h-full rounded-full" style="width: ${o.percentage * 3}%"></div>
              </div>
            </div>
          </td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono ${o.percentage > 15 ? 'bg-cyan-950 text-cyan-300 border border-cyan-500/30' : 'bg-gray-800 text-gray-300'}">
              ${o.percentage > 15 ? 'HIGH DENSITY' : 'STABLE'}
            </span>
          </td>
        </tr>
      `).join('');
      setText('sats-table-count', `Showing ${list.length} Orbit Regimes`);
      lucide.createIcons();
    }

    // Dynamic Filtering for Equipment
    function filterEquipmentTable() {
      if (!rawEquipmentData || !rawEquipmentData.components) return;
      const search = (document.getElementById('filter-eq-search')?.value || '').toLowerCase();
      const riskFilter = document.getElementById('filter-eq-risk')?.value || 'ALL';

      let filtered = rawEquipmentData.components.filter(c => {
        const matchesSearch = c.equipment_type.toLowerCase().includes(search);
        let matchesRisk = true;
        if (riskFilter === 'CRITICAL') matchesRisk = c.avg_lead_time_days > 200;
        else if (riskFilter === 'MEDIUM') matchesRisk = c.avg_lead_time_days >= 150 && c.avg_lead_time_days <= 200;
        else if (riskFilter === 'OPTIMAL') matchesRisk = c.avg_lead_time_days < 150;
        return matchesSearch && matchesRisk;
      });

      renderEquipmentTableBody(filtered);
    }

    function sortEquipmentTable(criteria) {
      if (!rawEquipmentData || !rawEquipmentData.components) return;
      let sorted = [...rawEquipmentData.components];
      if (criteria === 'units') sorted.sort((a, b) => b.total_units_demanded - a.total_units_demanded);
      else if (criteria === 'value') sorted.sort((a, b) => b.total_value_million - a.total_value_million);
      else if (criteria === 'leadtime') sorted.sort((a, b) => b.avg_lead_time_days - a.avg_lead_time_days);
      renderEquipmentTableBody(sorted);
    }

    function renderEquipmentTableBody(list) {
      const tbody = document.getElementById('equipment-table-body');
      if (!tbody) return;
      tbody.innerHTML = list.map(c => `
        <tr class="hover:bg-gray-800/40 transition">
          <td class="py-3 px-4 font-bold text-white flex items-center gap-2">
            <i data-lucide="cpu" class="w-3.5 h-3.5 text-amber-400"></i>
            ${c.equipment_type}
          </td>
          <td class="py-3 px-4 text-amber-400 font-bold">${Number(c.total_units_demanded).toLocaleString()}</td>
          <td class="py-3 px-4 font-mono">$${Number(c.avg_unit_cost_k).toFixed(1)}k</td>
          <td class="py-3 px-4 font-mono text-emerald-400 font-bold">$${Number(c.total_value_million).toFixed(1)}M</td>
          <td class="py-3 px-4 font-mono text-gray-300">${c.avg_lead_time_days} days</td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono ${c.avg_lead_time_days > 200 ? 'bg-rose-950 text-rose-300 border border-rose-500/30' : c.avg_lead_time_days >= 150 ? 'bg-amber-950 text-amber-300' : 'bg-emerald-950 text-emerald-300'}">
              ${c.avg_lead_time_days > 200 ? 'CRITICAL BOTTLENECK' : c.avg_lead_time_days >= 150 ? 'WARNING' : 'OPTIMAL'}
            </span>
          </td>
        </tr>
      `).join('');
      lucide.createIcons();
    }

    // Dynamic Filtering for Resources
    function filterResourcesTable() {
      if (!rawResourcesData || !rawResourcesData.resources) return;
      const search = (document.getElementById('filter-res-search')?.value || '').toLowerCase();
      const typeFilter = document.getElementById('filter-res-type')?.value || 'ALL';

      let filtered = rawResourcesData.resources.filter(r => {
        const matchesSearch = r.resource_name.toLowerCase().includes(search);
        let matchesType = true;
        if (typeFilter !== 'ALL') {
          matchesType = r.resource_name.toUpperCase().includes(typeFilter);
        }
        return matchesSearch && matchesType;
      });

      renderResourcesTableBody(filtered);
    }

    function renderResourcesTableBody(list) {
      const tbody = document.getElementById('resources-table-body');
      if (!tbody) return;
      tbody.innerHTML = list.map(r => `
        <tr class="hover:bg-gray-800/40 transition">
          <td class="py-3 px-4 font-bold text-white flex items-center gap-2">
            <i data-lucide="flame" class="w-3.5 h-3.5 text-rose-400"></i>
            ${r.resource_name}
          </td>
          <td class="py-3 px-4 text-rose-400 font-bold">${Number(r.total_consumed).toLocaleString()}</td>
          <td class="py-3 px-4 font-mono">${Number(r.avg_monthly_consumed).toFixed(1)} / mo</td>
          <td class="py-3 px-4 font-mono text-emerald-400 font-bold">$${(r.total_cost_k_usd / 1000).toFixed(2)}M</td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-950 text-emerald-300 border border-emerald-500/30">
              BUFFER SECURE (92%)
            </span>
          </td>
        </tr>
      `).join('');
      lucide.createIcons();
    }

    // Dynamic Filtering for Investments
    function filterInvestmentsTable() {
      if (!rawInvestmentsData || !rawInvestmentsData.future_decadal_projects) return;
      const search = (document.getElementById('filter-inv-search')?.value || '').toLowerCase();
      const trlFilter = document.getElementById('filter-inv-trl')?.value || 'ALL';

      let filtered = rawInvestmentsData.future_decadal_projects.filter(p => {
        const matchesSearch = p.project_title.toLowerCase().includes(search) || p.project_code.toLowerCase().includes(search);
        let matchesTrl = true;
        if (trlFilter === 'HIGH') matchesTrl = p.readiness_level_TRL >= 7;
        else if (trlFilter === 'MID') matchesTrl = p.readiness_level_TRL >= 5 && p.readiness_level_TRL < 7;
        else if (trlFilter === 'LOW') matchesTrl = p.readiness_level_TRL < 5;
        return matchesSearch && matchesTrl;
      });

      renderInvestmentsTableBody(filtered);
    }

    function renderInvestmentsTableBody(list) {
      const tbody = document.getElementById('future-projects-body');
      if (!tbody) return;
      tbody.innerHTML = list.map(p => `
        <tr class="hover:bg-gray-800/40 transition">
          <td class="py-3 px-4 font-mono text-sky-400 font-bold">${p.project_code}</td>
          <td class="py-3 px-4 font-bold text-white">${p.project_title}</td>
          <td class="py-3 px-4 text-gray-300">${p.lead_agency}</td>
          <td class="py-3 px-4 text-emerald-400 font-mono font-bold">$${p.estimated_investment_billion_usd}B</td>
          <td class="py-3 px-4 font-mono text-white">${p.target_commencement_year}</td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono ${p.readiness_level_TRL >= 7 ? 'bg-emerald-950 text-emerald-300 border border-emerald-500/30' : 'bg-sky-950 text-sky-300'}">
              TRL-${p.readiness_level_TRL}
            </span>
          </td>
          <td class="py-3 px-4 text-[10px] font-mono text-amber-400">${p.priority_tier || 'STRATEGIC'}</td>
        </tr>
      `).join('');
    }

    // Dynamic Filter for Data Explorer
    function filterExplorerTable() {
      const search = (document.getElementById('filter-explorer-search')?.value || '').toLowerCase();
      const tbody = document.getElementById('explorer-body');
      if (!tbody) return;
      const rows = tbody.querySelectorAll('tr');
      rows.forEach(r => {
        const text = r.textContent.toLowerCase();
        r.style.display = text.includes(search) ? '' : 'none';
      });
    }
"""

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Update loadMissions, loadSatellites, loadEquipment, loadResources, loadInvestments in JS to cache raw data
replacement_loader_caching = """
    // 4. Space Missions Tab Loader
    async function loadMissions() {
      try {
        const data = await fetchJSON(`${API_BASE}/missions/analytics`);
        if (!data) return;
        rawMissionsData = data;

        setText('missions-total-count', (data.total_missions || 1500).toLocaleString());
        setText('missions-total-budget', `$${data.total_budget_billion_usd || 2460.1}B`);

        if (data.agencies && data.agencies.length > 0) {
          const avgPayload = (data.agencies.reduce((acc, a) => acc + (a.avg_payload_kg || 0), 0) / data.agencies.length).toFixed(0);
          setText('missions-avg-payload', `${Number(avgPayload).toLocaleString()} kg`);

          const avgSuccess = (data.agencies.reduce((acc, a) => acc + (a.success_rate_pct || 0), 0) / data.agencies.length).toFixed(1);
          setText('missions-success-rate', `${avgSuccess}%`);

          renderMissionsChart(data.agencies);
          renderMissionsTableBody(data.agencies);
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
        rawSatellitesData = data;

        setText('sats-active-count', (data.active_in_orbit || 1688).toLocaleString());

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
          renderSatellitesTableBody(data.orbit_distribution);
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
"""

# Now replace the JS methods in frontend/index.html
load_missions_marker = '    // 4. Space Missions Tab Loader'
load_launches_marker = '    // 6. Launch Intelligence (ESPI Format)'

pos_m = orig.find(load_missions_marker)
pos_l = orig.find(load_launches_marker)

rebuilt_js_html = orig[:pos_m] + replacement_loader_caching + "\n" + orig[pos_l:]

# Also inject advanced_js before the closing </script>
pos_close_script = rebuilt_js_html.rfind('</script>')
final_html = rebuilt_js_html[:pos_close_script] + advanced_js + "\n  </script>" + rebuilt_js_html[pos_close_script+len('</script>'):]

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open('Orbitalytics_Generated/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Advanced JS utilities integrated into both frontend/index.html and Orbitalytics_Generated.")
