const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf-8');

let createdCharts = [];
let mockElements = {};

global.document = {
  getElementById: (id) => {
    if (!mockElements[id]) {
      mockElements[id] = {
        id: id,
        value: '',
        textContent: '',
        parentElement: { getBoundingClientRect: () => ({ width: 600, height: 260 }) },
        getContext: () => ({ id: id }),
        innerHTML: ''
      };
    }
    return mockElements[id];
  }
};
global.window = { addEventListener: () => {} };
class MockChart {
  constructor(ctx, config) {
    this.ctx = ctx;
    this.type = config.type;
    this.data = config.data;
    this.options = config.options;
    createdCharts.push(this);
  }
  destroy() {
    this.destroyed = true;
  }
}
global.Chart = MockChart;
global.lucide = { createIcons: () => {} };

const jsStart = html.indexOf('<script>');
const jsEnd = html.lastIndexOf('</script>');
let jsCode = html.slice(jsStart + '<script>'.length, jsEnd);
jsCode = jsCode.replace(/let chart/g, 'var chart');
const runnableJs = jsCode.replace("const API_BASE = '/api/v1';", "const API_BASE = 'http://127.0.0.1:8000/api/v1';");
eval(runnableJs);

async function testFilter() {
  await loadMissions();
  console.log('Initial agencies on chart:', chartTabMissions.data.labels);

  // Simulate typing "NASA" into search
  document.getElementById('filter-mission-search').value = 'NASA';
  filterMissionsTable();
  console.log('Filtered agencies on chart (search="NASA"):', chartTabMissions.data.labels);
  console.log('Filtered mission count:', chartTabMissions.data.datasets[0].data);

  // Clear search and test sort by budget
  document.getElementById('filter-mission-search').value = '';
  sortMissionsTable('budget');
  console.log('Sorted agencies on chart (by budget):', chartTabMissions.data.labels);
}

testFilter();
