import { fetchJson } from './api';
import { ForecastResult } from '../types';

export const forecastApi = {
  getTargets: () => fetchJson<Array<{ id: string; name: string; unit: string; category: string }>>('/forecasting/targets'),
  getModels: () => fetchJson<Array<{ id: string; name: string; type: string }>>('/forecasting/models'),
  predict: (target: string, horizonMonths: number = 12, model: string = "RandomForest") => {
    return fetchJson<ForecastResult>(`/forecasting/predict?target=${target}&horizon_months=${horizonMonths}&model=${model}`);
  },
  runScenario: (payload: { target: string; horizon_months: number; investment_growth_pct: number; launch_activity_growth_pct: number; cost_variation_pct: number }) => {
    return fetchJson<any>('/forecasting/scenario', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  }
};

