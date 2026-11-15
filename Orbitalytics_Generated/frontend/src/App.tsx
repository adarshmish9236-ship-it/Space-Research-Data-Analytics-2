import React, { useState } from 'react';

export default function App() {
  const [layer, setLayer] = useState<'research' | 'engineering'>('research');
  const [tab, setTab] = useState<string>('overview');

  return (
    <div className="min-h-screen bg-[#060913] text-gray-200 flex flex-col font-sans">
      <header className="border-b border-gray-800 bg-[#0B1120]/90 px-6 py-3 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white font-bold">
            OA
          </div>
          <div>
            <h1 className="text-lg font-extrabold text-white tracking-tight">ORBITALYTICS</h1>
            <p className="text-xs text-gray-400">Space Research Data Analytics & Demand Forecasting</p>
          </div>
        </div>

        <div className="flex bg-[#0F172A] p-1 rounded-xl border border-gray-800">
          <button
            onClick={() => setLayer('research')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition ${layer === 'research' ? 'bg-sky-600 text-white' : 'text-gray-400'}`}
          >
            Research Intelligence
          </button>
          <button
            onClick={() => setLayer('engineering')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition ${layer === 'engineering' ? 'bg-purple-600 text-white' : 'text-gray-400'}`}
          >
            Big Data Engineering
          </button>
        </div>
      </header>

      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-sky-500/20">
            <h2 className="text-2xl font-bold text-white">Orbitalytics High-Performance Lakehouse</h2>
            <p className="text-sm text-gray-400 mt-1">
              Active Layer: <b className="text-sky-400 uppercase">{layer}</b> | Connects to FastAPI on port 8000.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

