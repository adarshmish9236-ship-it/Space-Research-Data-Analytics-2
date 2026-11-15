fetch("http://127.0.0.1:8000/api/v1/scenarios/monte-carlo", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ iterations: 500, volatility_pct: 15.0 })
})
.then(r => r.json())
.then(d => console.log('API Response:', d))
.catch(e => console.error('Fetch error:', e));
