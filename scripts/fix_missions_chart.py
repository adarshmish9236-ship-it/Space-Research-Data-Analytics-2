with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the new renderMissionsTabChart function
render_missions_tab_chart_code = """
    function renderMissionsTabChart(agencies) {
      const ctx = getCanvasContext('chart-tab-missions');
      if (!ctx) return;
      if (chartTabMissions) chartTabMissions.destroy();

      const labels = agencies.map(a => a.agency);
      const missionCounts = agencies.map(a => a.mission_count);
      const budgets = agencies.map(a => (a.total_budget_million / 1000).toFixed(1));
      const successRates = agencies.map(a => a.success_rate_pct);

      chartTabMissions = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Cataloged Flight Missions',
            data: missionCounts,
            backgroundColor: [
              'rgba(56, 189, 248, 0.85)',
              'rgba(99, 102, 241, 0.85)',
              'rgba(16, 185, 129, 0.85)',
              'rgba(245, 158, 11, 0.85)',
              'rgba(168, 85, 247, 0.85)',
              'rgba(236, 72, 153, 0.85)',
              'rgba(6, 182, 212, 0.85)'
            ],
            borderColor: [
              '#38BDF8',
              '#6366F1',
              '#10B981',
              '#F59E0B',
              '#A855F7',
              '#EC4899',
              '#06B6D4'
            ],
            borderWidth: 1.5,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#0F172A',
              titleColor: '#FFFFFF',
              bodyColor: '#94A3B8',
              borderColor: 'rgba(56, 189, 248, 0.3)',
              borderWidth: 1,
              padding: 10,
              callbacks: {
                label: function(context) {
                  const idx = context.dataIndex;
                  return [
                    ` Missions: ${context.parsed.y} flights`,
                    ` Budget: $${budgets[idx]}B`,
                    ` Success Rate: ${successRates[idx]}%`
                  ];
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: '#94A3B8', font: { family: 'JetBrains Mono', size: 11 } }
            },
            y: {
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: '#94A3B8', font: { family: 'JetBrains Mono', size: 11 } }
            }
          }
        }
      });
    }
"""

# Replace renderMissionsChart call inside loadMissions with renderMissionsTabChart
old_call = "renderMissionsChart(data.agencies);"
new_call = "renderMissionsTabChart(data.agencies);"
if old_call in html:
    html = html.replace(old_call, new_call)
    print("Replaced renderMissionsChart call in loadMissions with renderMissionsTabChart")
else:
    print("Warning: old_call not found in html!")

# Insert renderMissionsTabChart before loadMissions
pos_load = html.find('async function loadMissions() {')
if pos_load != -1:
    html = html[:pos_load] + render_missions_tab_chart_code + "\n    " + html[pos_load:]
    print("Inserted renderMissionsTabChart function before loadMissions")

# Also update filterMissionsTable and sortMissionsTable to also update the chart
html = html.replace(
    "renderMissionsTableBody(filtered);",
    "renderMissionsTableBody(filtered);\n      renderMissionsTabChart(filtered);"
)
html = html.replace(
    "renderMissionsTableBody(sorted);",
    "renderMissionsTableBody(sorted);\n      renderMissionsTabChart(sorted);"
)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('Orbitalytics_Generated/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated frontend/index.html and Orbitalytics_Generated/frontend/index.html")
