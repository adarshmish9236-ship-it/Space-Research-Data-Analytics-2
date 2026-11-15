"""
Orbitalytics - Analytics Schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class KPIOverviewResponse(BaseModel):
    total_missions: int
    total_satellites_cataloged: int
    active_satellites_in_orbit: int
    total_launches: int
    launch_success_rate_pct: float
    total_processed_records: int
    cumulative_budget_billion_usd: float
    pipeline_state: str

class AgencyMissionStat(BaseModel):
    agency: str
    country: str
    total_missions: int
    total_budget_million_usd: float
    avg_payload_kg: float
    success_rate_pct: float

class YearlyLaunchTrend(BaseModel):
    year: int
    total_launches: int
    successful_launches: int
    commercial_launches: int
    avg_launch_cost_million_usd: float

class SatelliteOrbitStat(BaseModel):
    orbit_type: str
    total_satellites: int
    avg_altitude_km: float
    avg_power_kw: float
    avg_lifetime_years: float

class ResourceConsumptionStat(BaseModel):
    resource_type: str
    total_consumed: float
    unit: str
    total_cost_million_usd: float

class AutomatedInsight(BaseModel):
    category: str
    headline: str
    detail: str
    importance: str
    metric_value: Optional[str] = None
    observation_period: Optional[str] = None

