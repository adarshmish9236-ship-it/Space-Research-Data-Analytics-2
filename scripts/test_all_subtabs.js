const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf-8');

const idRegex = /id=["']([^"']+)["']/g;
const validIds = new Set();
let match;
while ((match = idRegex.exec(html)) !== null) {
  validIds.add(match[1]);
}

const domNodes = {};
function getMockElement(id) {
  if (!validIds.has(id)) {
    return null;
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

global.document = { getElementById: getMockElement };
global.window = {
  location: { href: '' },
  open: (url) => {},
  addEventListener: () => {}
};
class MockChart {
  constructor(ctx, config) { this.type = config.type; this.destroyed = false; }
  destroy() { this.destroyed = true; }
}
global.Chart = MockChart;
global.lucide = { createIcons: () => {} };

const jsStart = html.indexOf('<script>');
const jsEnd = html.lastIndexOf('</script>');
const jsCode = html.slice(jsStart + '<script>'.length, jsEnd);
const runnableJs = jsCode.replace("const API_BASE = '/api/v1';", "const API_BASE = 'http://127.0.0.1:8000/api/v1';");
eval(runnableJs);

async function runAllTabs() {
  const tabs = [
    'research-overview', 'research-missions', 'research-satellites', 'research-launches',
    'research-equipment', 'research-resources', 'research-investments', 'research-geographic',
    'research-forecasting', 'research-optimization', 'research-scenario', 'research-explorer', 'research-reports',
    'eng-pipeline', 'eng-catalog', 'eng-quality', 'eng-hdfs', 'eng-hive', 'eng-mapreduce', 'eng-spark', 'eng-benchmarks', 'eng-yarn', 'eng-models'
  ];

  let passed = 0;
  let failed = 0;

  console.log(`Testing all ${tabs.length} platform subtabs...`);
  for (const t of tabs) {
    try {
      await switchSubTab(t);
      passed++;
    } catch (err) {
      console.error(`Tab ${t} failed:`, err);
      failed++;
    }
  }

  console.log(`Results: ${passed} passed, ${failed} failed out of ${tabs.length}`);
  process.exit(failed > 0 ? 1 : 0);
}

runAllTabs();
