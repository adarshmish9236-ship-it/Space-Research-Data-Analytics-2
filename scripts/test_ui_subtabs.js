const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf-8');

// Extract all element IDs defined in the HTML
const idRegex = /id=["']([^"']+)["']/g;
const validIds = new Set();
let match;
while ((match = idRegex.exec(html)) !== null) {
  validIds.add(match[1]);
}

console.log(`Loaded ${validIds.size} valid DOM IDs from frontend/index.html`);

// Build a Mock DOM
const domNodes = {};
function getMockElement(id) {
  if (!validIds.has(id)) {
    return null; // Mirrors browser behavior: non-existent ID returns null!
  }
  if (!domNodes[id]) {
    domNodes[id] = {
      id: id,
      textContent: '',
      innerHTML: '',
      className: '',
      value: (id === 'fc-target' ? 'equipment_rad_cpu' :
              id === 'fc-model' ? 'auto' :
              id === 'fc-horizon' ? '12' :
              id === 'fc-scenario' ? 'baseline' :
              id === 'slider-budget' ? '10' :
              id === 'slider-cadence' ? '5' :
              id === 'slider-inflation' ? '3' :
              id === 'explorer-dataset-select' ? 'agency_missions' :
              id === 'hive-query-selector' ? 'agency_missions' :
              id === 'mr-job-selector' ? 'equipment_demand_aggregator' :
              id === 'spark-job-select' ? 'equipment_feature_pipeline' : ''),
      classList: {
        add: function(c) {},
        remove: function(c) {},
        contains: function(c) { return false; }
      },
      parentElement: {
        getBoundingClientRect: () => ({ width: 800, height: 320 })
      },
      getContext: function(type) {
        return {
          clearRect: () => {},
          beginPath: () => {},
          arc: () => {},
          fill: () => {},
          stroke: () => {},
          save: () => {},
          restore: () => {},
          translate: () => {},
          rotate: () => {},
          ellipse: () => {},
          createRadialGradient: () => ({ addColorStop: () => {} })
        };
      }
    };
  }
  return domNodes[id];
}

// Global browser mocks
global.document = {
  getElementById: getMockElement
};

global.window = {
  location: { href: '' },
  open: (url) => console.log(`  [Window Open] ${url}`),
  addEventListener: () => {}
};

class MockChart {
  constructor(ctx, config) {
    this.type = config.type;
    this.data = config.data;
    this.options = config.options;
    this.destroyed = false;
  }
  destroy() {
    this.destroyed = true;
  }
}
global.Chart = MockChart;

global.lucide = {
  createIcons: () => {}
};

// Extract JS block from frontend/index.html
const jsStart = html.indexOf('<script>');
const jsEnd = html.lastIndexOf('</script>');
const jsCode = html.slice(jsStart + '<script>'.length, jsEnd);

// Fix API_BASE for Node environment test
const runnableJs = jsCode.replace("const API_BASE = '/api/v1';", "const API_BASE = 'http://127.0.0.1:8000/api/v1';");

// Execute the JS code in this global scope
eval(runnableJs);

// Now execute and test every single Research Layer tab
async function runVerification() {
  console.log('\n======================================================');
  console.log('ORBITALYTICS RESEARCH LAYER SUBTAB TEST SUITE');
  console.log('======================================================\n');

  const testTabs = [
    { name: '1. Executive Overview', fn: () => switchSubTab('research-overview') },
    { name: '2. Space Missions', fn: () => switchSubTab('research-missions') },
    { name: '3. Satellites & Orbits', fn: () => switchSubTab('research-satellites') },
    { name: '4. Launch Intelligence', fn: () => switchSubTab('research-launches') },
    { name: '5. Equipment Demand', fn: () => switchSubTab('research-equipment') },
    { name: '6. Resource Consumption', fn: () => switchSubTab('research-resources') },
    { name: '7. Research Investments', fn: () => switchSubTab('research-investments') },
    { name: '8. Territory & Spaceports', fn: () => switchSubTab('research-geographic') },
    { name: '9. Forecasting Studio', fn: () => switchSubTab('research-forecasting') },
    { name: '10. Optimization Studio', fn: () => switchSubTab('research-optimization') },
    { name: '11. Digital Twin / Scenarios', fn: () => switchSubTab('research-scenario') },
    { name: '12. Data Explorer', fn: () => switchSubTab('research-explorer') },
    { name: '13. Reports & Exports', fn: () => switchSubTab('research-reports') }
  ];

  let passed = 0;
  let failed = 0;

  for (const t of testTabs) {
    try {
      console.log(`[TESTING] ${t.name}...`);
      await t.fn();
      // Wait a moment for any async operations to settle
      await new Promise(r => setTimeout(r, 100));
      console.log(`  ✅ PASSED: ${t.name} executed without error!`);
      passed++;
    } catch (err) {
      console.error(`  ❌ FAILED: ${t.name} encountered error:`, err);
      failed++;
    }
  }

  // Also test interactive buttons in Forecasting and Optimization
  console.log('\n[TESTING] Additional Interactive Actions...');
  try {
    await runDemandGap();
    console.log('  ✅ PASSED: runDemandGap()');
    passed++;
  } catch (err) {
    console.error('  ❌ FAILED: runDemandGap()', err);
    failed++;
  }

  try {
    await runMonteCarloSimulation();
    console.log('  ✅ PASSED: runMonteCarloSimulation()');
    passed++;
  } catch (err) {
    console.error('  ❌ FAILED: runMonteCarloSimulation()', err);
    failed++;
  }

  try {
    await runSensitivityTornado();
    console.log('  ✅ PASSED: runSensitivityTornado()');
    passed++;
  } catch (err) {
    console.error('  ❌ FAILED: runSensitivityTornado()', err);
    failed++;
  }

  // Sample check on rendered values
  console.log('\n--- VERIFYING POPULATED DOM METRICS ---');
  const checkIds = [
    'kpi-missions', 'kpi-satellites', 'kpi-launch-rate', 'kpi-records', 'kpi-budget', 'kpi-equipment',
    'missions-total-count', 'missions-total-budget', 'sats-active-count', 'eq-total-units',
    'res-total-consumed', 'inv-total-spend', 'opt-solver-status', 'fc-champion-badge'
  ];

  for (const cid of checkIds) {
    const el = domNodes[cid];
    console.log(`  DOM #${cid}: "${el ? el.textContent : 'NOT_FOUND'}"`);
  }

  console.log(`\n======================================================`);
  console.log(`TOTAL SUBTABS & ACTIONS TESTED: ${passed + failed}`);
  console.log(`PASSED: ${passed} | FAILED: ${failed}`);
  console.log(`======================================================\n`);

  if (failed > 0) {
    process.exit(1);
  } else {
    process.exit(0);
  }
}

runVerification();
