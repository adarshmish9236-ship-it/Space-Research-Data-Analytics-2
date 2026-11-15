const endpoints = [
  'http://127.0.0.1:8000/api/v1/orbital/data-status',
  'http://127.0.0.1:8000/api/v1/orbital/catalog',
  'http://127.0.0.1:8000/api/v1/orbital/satellites',
  'http://127.0.0.1:8000/api/v1/orbital/satellites?orbit_type=LEO',
  'http://127.0.0.1:8000/api/v1/orbital/satellites/25544',
  'http://127.0.0.1:8000/api/v1/orbital/positions',
  'http://127.0.0.1:8000/api/v1/orbital/trajectories'
];

async function testAll() {
  console.log('Testing Orbital API endpoints...');
  for (const url of endpoints) {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        console.error(`❌ FAILED ${url} - Status ${res.status}`);
        process.exit(1);
      }
      const data = await res.json();
      const count = Array.isArray(data) ? `${data.length} items` : 'Object';
      console.log(`✅ [HTTP 200] ${url.replace('http://127.0.0.1:8000/api/v1', '')} -> ${count}`);
    } catch (e) {
      console.error(`❌ ERROR on ${url}:`, e);
      process.exit(1);
    }
  }
  console.log('All Orbital endpoints verified successfully!');
}

testAll();
