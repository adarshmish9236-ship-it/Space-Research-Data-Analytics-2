import { fetchJson } from './api';
import { KPIOverview, AutomatedInsight } from '../types';

export const analyticsApi = {
  getKPIs: () => fetchJson<KPIOverview>('/overview/kpis'),
  getInsights: () => fetchJson<AutomatedInsight[]>('/analytics/insights'),
  getMissions: (agency?: string, country?: string) => {
    const params = new URLSearchParams();
    if (agency) params.append('agency', agency);
    if (country) params.append('country', country);
    return fetchJson<any>(`/analytics/missions?${params.toString()}`);
  },
  getSatellites: () => fetchJson<any>('/analytics/satellites'),
  getLaunches: () => fetchJson<any>('/analytics/launches'),
  getEquipmentDemand: () => fetchJson<any>('/analytics/equipment-demand'),
  getResources: () => fetchJson<any[]>('/analytics/resources'),
  getInvestments: () => fetchJson<any>('/analytics/investments'),
  getInfrastructure: () => fetchJson<any>('/analytics/infrastructure'),
  getGeographicDistribution: () => fetchJson<any>('/analytics/geographic-distribution')
};

