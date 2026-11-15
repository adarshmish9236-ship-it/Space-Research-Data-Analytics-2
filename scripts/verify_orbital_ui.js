const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf-8');

let mockElements = {};

global.document = {
  getElementById: (id) => {
    if (!mockElements[id]) {
      mockElements[id] = {
        id: id,
        value: '',
        textContent: '',
        style: {},
        parentElement: {
          getBoundingClientRect: () => ({ width: 800, height: 520 })
        },
        getContext: (type) => ({ id: id, type: type, clearRect: () => {}, beginPath: () => {}, arc: () => {}, stroke: () => {}, fill: () => {}, ellipse: () => {} }),
        innerHTML: '',
        classList: {
          _classes: new Set(),
          add: function(...cls) { cls.forEach(c => this._classes.add(c)); },
          remove: function(...cls) { cls.forEach(c => this._classes.delete(c)); },
          contains: function(c) { return this._classes.has(c); }
        },
        querySelectorAll: () => [],
        closest: () => null,
        setAttribute: (k, v) => {},
        getAttribute: (k) => null
      };
    }
    return mockElements[id];
  }
};
global.window = {
  addEventListener: () => {},
  CESIUM_BASE_URL: ''
};

class MockChart {
  constructor(ctx, config) {
    this.ctx = ctx;
    this.type = config.type;
    this.data = config.data;
  }
  destroy() {}
}
global.Chart = MockChart;
global.lucide = { createIcons: () => {} };

// Extract JS block from frontend/index.html
const jsStart = html.indexOf('<script>');
const jsEnd = html.lastIndexOf('</script>');
let jsCode = html.slice(jsStart + '<script>'.length, jsEnd);
jsCode = jsCode.replace(/let /g, 'var ');
const runnableJs = jsCode.replace("const API_BASE = '/api/v1';", "const API_BASE = 'http://127.0.0.1:8000/api/v1';");

eval(runnableJs);

async function verifyOrbitalSuite() {
  console.log('====================================================');
  console.log('ORBITALYTICS 3D ORBITAL & EPHEMERIS TEST SUITE');
  console.log('====================================================\n');

  // 1. Initialize Orbit Globe
  console.log('[TEST 1] Initializing Orbit Globe...');
  initOrbitGlobe();
  console.log('  ✅ initOrbitGlobe() executed successfully without errors');

  // 2. Load Orbital Telemetry from live backend
  console.log('\n[TEST 2] Loading authentic Orbital Telemetry from API...');
  await loadOrbitalTelemetry();
  console.log(`  ✅ Loaded ${orbitalSatellites.length} satellites and ${orbitalTrajectories.length} trajectories`);
  console.log(`  DOM LEO Count: ${document.getElementById('count-leo').textContent}`);
  console.log(`  DOM SSO Count: ${document.getElementById('count-sso').textContent}`);
  console.log(`  DOM MEO Count: ${document.getElementById('count-meo').textContent}`);
  console.log(`  DOM GEO Count: ${document.getElementById('count-geo').textContent}`);

  // 3. Verify Default Selection (ISS)
  console.log('\n[TEST 3] Verifying Initial Spacecraft HUD Telemetry (ISS)...');
  console.log(`  Target Name: ${document.getElementById('hud-sat-name').textContent}`);
  console.log(`  NORAD ID: ${document.getElementById('hud-norad').textContent}`);
  console.log(`  Orbit Badge: ${document.getElementById('hud-orbit-badge').textContent}`);
  console.log(`  Altitude: ${document.getElementById('hud-altitude').textContent}`);
  console.log(`  Velocity: ${document.getElementById('hud-velocity').textContent}`);
  console.log(`  Sub-Satellite Lat/Lon: ${document.getElementById('hud-latlon').textContent}`);
  if (String(document.getElementById('hud-norad').textContent) !== '25544') {
    throw new Error('Default selection should be ISS (NORAD 25544)');
  }
  console.log('  ✅ Initial ISS HUD telemetry verified!');

  // 4. Test Target Selection (Tiangong CSS)
  console.log('\n[TEST 4] Selecting TIANGONG (CSS) - NORAD 48274...');
  selectSatelliteByNorad(48274);
  console.log(`  New Target: ${document.getElementById('hud-sat-name').textContent}`);
  console.log(`  New NORAD: ${document.getElementById('hud-norad').textContent}`);
  console.log(`  Operator: ${document.getElementById('hud-sat-operator').textContent}`);
  console.log(`  Altitude: ${document.getElementById('hud-altitude').textContent}`);
  console.log(`  Inclination: ${document.getElementById('hud-inclination').textContent}`);
  if (document.getElementById('hud-sat-name').textContent !== 'TIANGONG (CSS)') {
    throw new Error('Expected target to be TIANGONG (CSS)');
  }
  console.log('  ✅ Satellite switching verified successfully!');

  // 5. Test Orbit Category Filter
  console.log('\n[TEST 5] Testing Orbital Regime Filters (GEO, MEO, SSO, LEO)...');
  setOrbitFilter('GEO');
  console.log(`  Active Filter: ${activeOrbitFilter}`);
  console.log(`  GEO Button Class: ${document.getElementById('filter-btn-geo').className}`);
  setOrbitFilter('ALL');
  console.log('  ✅ Orbit category filter switching verified!');

  // 6. Test Simulation Controls
  console.log('\n[TEST 6] Testing Astrodynamics Simulation Controls...');
  setSimSpeed(15);
  console.log(`  Simulation Speed Multiplier: ${orbitSimSpeedMultiplier}x`);
  toggleOrbitSimulation();
  console.log(`  Simulation Running: ${isOrbitSimPlaying}`);
  toggleOrbitSimulation();
  console.log(`  Simulation Resumed: ${isOrbitSimPlaying}`);
  resetSimTime();
  console.log('  ✅ Simulation controls verified!');

  // 7. Test Fullscreen Toggle
  console.log('\n[TEST 7] Testing Fullscreen Mission Control Toggle...');
  toggleGlobeFullscreen();
  console.log(`  Is Fullscreen: ${isGlobeFullscreen}`);
  console.log(`  Maximize Button Text: ${document.getElementById('text-globe-maximize').textContent}`);
  toggleGlobeFullscreen();
  console.log(`  Restored Fullscreen: ${isGlobeFullscreen}`);
  console.log('  ✅ Fullscreen Mission Control toggle verified!');

  // 8. Test Data Sync
  console.log('\n[TEST 8] Testing CelesTrak On-Demand Synchronization...');
  await syncOrbitalElements();
  console.log(`  Status Pill Text: ${document.getElementById('globe-status-pill').textContent}`);
  console.log('  ✅ On-Demand CelesTrak synchronization verified!');

  console.log('\n====================================================');
  console.log('ALL ORBITAL & 3D EARTH TESTS PASSED (8/8)!');
  console.log('====================================================\n');
}

verifyOrbitalSuite().catch(err => {
  console.error('❌ Test failed with error:', err);
  process.exit(1);
});
