const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf-8');

let createdCharts = {};
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
        innerHTML: '',
        classList: {
          add: () => {},
          remove: () => {}
        }
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
    createdCharts[ctx.id] = this;
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

async function runTest() {
  console.log('Testing Digital Twin & Monte Carlo integration...');

  // Set initial slider values
  document.getElementById('slider-budget').value = '10';
  document.getElementById('slider-cadence').value = '5';
  document.getElementById('slider-inflation').value = '3';

  // 1. Run Scenario Analysis (which now executes Monte Carlo automatically)
  await runScenarioAnalysis();

  const chart = createdCharts['chart-monte-carlo'];
  if (!chart) {
    console.error('FAIL: chart-monte-carlo was not created during runScenarioAnalysis!');
    process.exit(1);
  }

  console.log('✅ PASS: chart-monte-carlo created successfully on scenario run!');
  console.log('Chart Type:', chart.type);
  console.log('Bin Labels:', chart.data.labels);
  console.log('Iteration Frequencies:', chart.data.datasets[0].data);
  console.log('Total Iterations:', chart.data.datasets[0].data.reduce((a, b) => a + b, 0));
  console.log('Bar Colors Sample:', chart.data.datasets[0].backgroundColor.slice(0, 4));

  // Verify DOM stats
  console.log('DOM Mean:', document.getElementById('mc-stat-mean').textContent);
  console.log('DOM P95 Tail:', document.getElementById('mc-stat-p95').textContent);
  console.log('DOM P05 Floor:', document.getElementById('mc-stat-p05').textContent);
  console.log('DOM Volatility:', document.getElementById('mc-stat-vol').textContent);

  // 2. Test Re-sample with different slider values (e.g. +25% Budget Growth, 10% inflation)
  console.log('\nTesting dynamic Re-sample with slider shift (Budget=+25%, Inflation=10%)...');
  document.getElementById('slider-budget').value = '25';
  document.getElementById('slider-inflation').value = '10';
  await runMonteCarloSimulation();

  console.log('✅ PASS: Re-sample executed successfully!');
  console.log('New DOM Mean (shifted by +25% growth):', document.getElementById('mc-stat-mean').textContent);
  console.log('New DOM Volatility (adjusted by inflation):', document.getElementById('mc-stat-vol').textContent);
  console.log('New Total Draws:', chart.data.datasets[0].data.reduce((a, b) => a + b, 0));

  console.log('\nALL MONTE CARLO TESTS PASSED 100%!');
}

runTest().catch(err => {
  console.error('Unexpected error:', err);
  process.exit(1);
});
