"""
Orbitalytics 2.0 - Scenario Simulation & Digital Twin Schemas
Defines schemas for deterministic scenarios, Monte Carlo simulation, and parameter sensitivity ranking.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ScenarioParameters(BaseModel):
    name: str = Field(default="Custom Scenario")
    budget_growth_pct: float = Field(default=0.0, ge=-50.0, le=100.0)
    launch_cadence_change_pct: float = Field(default=0.0, ge=-50.0, le=100.0)
    satellite_deployment_change_pct: float = Field(default=0.0, ge=-50.0, le=100.0)
    equipment_price_inflation_pct: float = Field(default=3.0, ge=-10.0, le=50.0)
    supplier_capacity_change_pct: float = Field(default=0.0, ge=-50.0, le=100.0)
    lead_time_change_days: int = Field(default=0, ge=-60, le=180)
    resource_consumption_change_pct: float = Field(default=0.0, ge=-50.0, le=100.0)

class ScenarioOutput(BaseModel):
    scenario_name: str
    scenario_type: str  # BASELINE, OPTIMISTIC, CONSERVATIVE, CUSTOM
    simulated_annual_budget_usd: float
    simulated_launch_count: int
    simulated_satellite_deployments: int
    simulated_total_equipment_units: float
    simulated_total_equipment_cost_usd: float
    simulated_supply_shortage_units: float
    estimated_funding_gap_usd: float
    system_stress_index: float  # 0.0 - 100.0 scale

class ScenarioComparisonResponse(BaseModel):
    baseline: ScenarioOutput
    optimistic: ScenarioOutput
    conservative: ScenarioOutput
    custom: Optional[ScenarioOutput]
    comparison_summary: str

class MonteCarloRequest(BaseModel):
    target: str = Field(default="equipment_demand", description="Target metric for stochastic simulation")
    iterations: int = Field(default=500, ge=100, le=2000)
    volatility_pct: float = Field(default=15.0, ge=5.0, le=50.0)
    seed: int = Field(default=42)

class MonteCarloPercentiles(BaseModel):
    p05: float
    p10: float
    p25: float
    p50_median: float
    p75: float
    p90: float
    p95: float
    mean: float
    std_dev: float

class MonteCarloResponse(BaseModel):
    target: str
    iterations: int
    seed: int
    distribution_histogram: List[Dict[str, Any]]
    percentiles: MonteCarloPercentiles
    risk_of_exceeding_capacity_pct: float
    interpretation: str

class SensitivityFactor(BaseModel):
    parameter: str
    low_impact_value: float
    high_impact_value: float
    swing_usd: float
    relative_sensitivity_score: float

class SensitivityAnalysisResponse(BaseModel):
    target_metric: str
    base_value_usd: float
    factors: List[SensitivityFactor]
    top_driver: str
    tornado_summary: str

