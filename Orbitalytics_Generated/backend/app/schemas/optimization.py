"""
Orbitalytics 2.0 - Optimization Schemas
Defines request and response contracts for Demand-to-Capacity Gap Analysis,
Safety Stock Inventory Planning, Constrained Procurement Optimization, and Budget Allocation.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class DemandGapRequest(BaseModel):
    category: str = Field(default="Equipment", description="Resource or Equipment category")
    item_name: Optional[str] = Field(default=None, description="Specific component or resource")
    horizon_months: int = Field(default=12, ge=1, le=36)
    capacity_override: Optional[float] = Field(default=None, description="Simulated supplier capacity limit")

class DemandGapItem(BaseModel):
    item_name: str
    forecast_demand: float
    available_capacity: float
    existing_inventory: float
    expected_supply: float
    demand_gap: float
    surplus_quantity: float
    coverage_percentage: float
    risk_level: str  # LOW, MODERATE, CRITICAL
    unit: str

class DemandGapResponse(BaseModel):
    total_forecast_demand: float
    total_available_capacity: float
    net_shortage: float
    overall_coverage_pct: float
    high_risk_items_count: int
    items: List[DemandGapItem]
    methodology: str

class InventoryPlanningRequest(BaseModel):
    item_name: str = Field(default="Solar Panel Array High Efficiency")
    lead_time_days: int = Field(default=90, ge=10, le=720)
    service_level: float = Field(default=0.95, ge=0.80, le=0.999)  # 95% service level
    holding_cost_annual_pct: float = Field(default=0.18, ge=0.05, le=0.50)

class InventoryPlanningResponse(BaseModel):
    item_name: str
    annual_demand: float
    daily_demand_mean: float
    daily_demand_std: float
    lead_time_days: int
    service_level_target: float
    z_score: float
    safety_stock_units: float
    lead_time_demand_units: float
    reorder_point_units: float
    shortage_probability_pct: float
    annual_holding_cost_usd: float
    recommendation: str

class ProcurementOptimizationRequest(BaseModel):
    budget_ceiling_usd: float = Field(default=50000000.0, ge=1000000.0)
    criticality_penalty_weight: float = Field(default=2.5, ge=1.0, le=10.0)
    allow_partial_fulfillment: bool = Field(default=True)
    custom_supplier_limits: Optional[Dict[str, float]] = Field(default=None)

class AllocationItem(BaseModel):
    component_name: str
    forecast_demand: float
    allocated_units: float
    unit_cost_usd: float
    total_cost_usd: float
    fulfillment_pct: float
    shortage_units: float
    criticality: str
    supplier_capacity_max: float
    bottleneck_status: str

class ProcurementOptimizationResponse(BaseModel):
    status: str  # OPTIMAL, SUBOPTIMAL, FEASIBLE
    solver: str
    total_budget_usd: float
    total_allocated_spend_usd: float
    budget_utilization_pct: float
    total_demand_units: float
    total_allocated_units: float
    overall_fulfillment_pct: float
    unmet_critical_shortage: float
    allocations: List[AllocationItem]
    solver_runtime_ms: float
    interpretation: str

class BudgetAllocationRequest(BaseModel):
    total_research_budget_usd: float = Field(default=25000000000.0, ge=1000000000.0)
    focus_domain: Optional[str] = Field(default="Balanced", description="Balanced, Lunar/DeepSpace, SatelliteConstellation, EarthObservation")

class ProgramBudget(BaseModel):
    program_name: str
    historical_spend_usd: float
    recommended_allocation_usd: float
    variance_pct: float
    projected_roi_score: float
    justification: str

class BudgetAllocationResponse(BaseModel):
    total_budget_usd: float
    focus_domain: str
    programs: List[ProgramBudget]
    unallocated_contingency_usd: float
    strategic_insights: List[str]

