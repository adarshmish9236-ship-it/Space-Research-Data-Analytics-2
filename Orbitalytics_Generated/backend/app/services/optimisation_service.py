"""
ORBITALYTICS Phase 9 — Optimization Service for FastAPI
Provides backend methods for:
  - Scenario comparison matrices
  - Shortage and surplus reports
  - Suggested procurement schedules
  - Mission priority resource allocation plans
  - Dynamic on-demand MILP scenario solver for custom user parameters
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PHASE9_RESULTS_DIR = PROJECT_ROOT / "docs" / "phase_9" / "results"
MASTER_JSON = PHASE9_RESULTS_DIR / "orbitalytics_resource_optimisation.json"
SCENARIO_CSV = PHASE9_RESULTS_DIR / "scenario_comparison_matrix.csv"
SHORTAGE_CSV = PHASE9_RESULTS_DIR / "shortage_surplus_report.csv"
PROCUREMENT_CSV = PHASE9_RESULTS_DIR / "procurement_recommendations.csv"
ALLOCATION_CSV = PHASE9_RESULTS_DIR / "priority_allocation_plan.csv"

from resource_optimisation.data_input import OptimizationDataLoader
from resource_optimisation.optimiser import ResourceOptimiser
from resource_optimisation.scenario_manager import ScenarioManager


class OptimisationService:
    """FastAPI Service bridge for Phase 9 Resource Optimisation."""

    def __init__(self):
        self._cached_manifest: Optional[Dict[str, Any]] = None
        self.loader = OptimizationDataLoader()
        self.optimiser = ResourceOptimiser()
        self.scenario_mgr = ScenarioManager()

    def _load_master_json(self) -> Dict[str, Any]:
        if self._cached_manifest is None:
            if not MASTER_JSON.exists():
                return {"error": "Optimisation manifest not found. Run pipeline first."}
            with open(MASTER_JSON, "r", encoding="utf-8") as f:
                self._cached_manifest = json.load(f)
        return self._cached_manifest

    def get_scenario_comparison(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns comparison matrix across all 5 operational scenarios."""
        if not SCENARIO_CSV.exists():
            return []
        df = pd.read_csv(SCENARIO_CSV)
        if domain:
            df = df[df["domain"] == domain]
        return df.to_dict(orient="records")

    def get_shortage_report(self, domain: Optional[str] = None, item_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns quarterly shortage, surplus, and fill rate reports."""
        if not SHORTAGE_CSV.exists():
            return []
        df = pd.read_csv(SHORTAGE_CSV)
        if domain:
            df = df[df["domain"] == domain]
        if item_name:
            df = df[df["item_name"].str.contains(item_name, case=False, na=False)]
        return df.to_dict(orient="records")

    def get_procurement_recommendations(self, domain: Optional[str] = None, item_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns suggested procurement orders, timing, and lead-time schedules."""
        if not PROCUREMENT_CSV.exists():
            return []
        df = pd.read_csv(PROCUREMENT_CSV)
        if domain:
            df = df[df["domain"] == domain]
        if item_name:
            df = df[df["item_name"].str.contains(item_name, case=False, na=False)]
        return df.to_dict(orient="records")

    def get_priority_allocations(self, domain: Optional[str] = None, tier: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns mission priority resource allocations across tiers."""
        if not ALLOCATION_CSV.exists():
            return []
        df = pd.read_csv(ALLOCATION_CSV)
        if domain:
            df = df[df["domain"] == domain]
        if tier:
            df = df[df["mission_priority_tier"].str.contains(tier, case=False, na=False)]
        return df.to_dict(orient="records")

    def get_fleet_summary(self, domain: str = "equipment_demand") -> Dict[str, Any]:
        """Returns aggregate fleet procurement and operational metrics."""
        manifest = self._load_master_json()
        plans = manifest.get("fleet_procurement_plans", {}).get(domain, {})
        domains_data = manifest.get("domains", {}).get(domain, {})
        base_scenario = domains_data.get("scenarios", [{}])[0]
        return {
            "domain": domain,
            "fleet_procurement": plans,
            "baseline_metrics": base_scenario.get("metrics_summary", {}),
            "assumptions": manifest.get("domains", {}).get(domain, {}).get("assumptions_documentation", {})
        }

    def solve_custom_scenario(self,
                              domain: str = "equipment_demand",
                              budget_multiplier: float = 1.0,
                              capacity_multiplier: float = 1.0,
                              demand_multiplier: float = 1.0) -> Dict[str, Any]:
        """
        Dynamically solves custom user scenario using the HiGHS MILP solver.
        """
        fc_df = self.loader.load_forecast_projections(domain)

        if domain == "equipment_demand":
            params = self.loader.get_equipment_parameters()
            is_integer = True
            base_budget = 850_000.0
            base_cap = 1200.0
        else:
            params = self.loader.get_resource_parameters()
            is_integer = False
            base_budget = 250_000.0
            base_cap = 2000.0

        item_names = list(params.keys())
        periods = sorted(fc_df["period"].unique().tolist())
        M = len(item_names)
        T = len(periods)

        demands = np.zeros((M, T), dtype=float)
        for i, name in enumerate(item_names):
            sub = fc_df[fc_df["series_name"] == name].sort_values("period")
            demands[i, :] = sub["forecast"].values * demand_multiplier

        init_stock = np.array([params[k]["default_initial_stock"] for k in item_names], dtype=float)
        p_costs = np.array([params[k]["unit_procurement_cost_k"] for k in item_names], dtype=float)
        m_costs = np.array([
            params[k].get("unit_manufacturing_cost_k", params[k].get("unit_internal_production_cost_k", 400.0))
            for k in item_names
        ], dtype=float)
        h_costs = np.array([params[k]["holding_cost_per_quarter_k"] for k in item_names], dtype=float)
        s_costs = np.array([params[k]["shortage_penalty_k"] for k in item_names], dtype=float)
        tooling_caps = np.array([
            params[k].get("default_mfg_capacity_per_quarter", params[k].get("default_production_capacity", 150.0))
            for k in item_names
        ], dtype=float) * capacity_multiplier
        supplier_caps = np.array([params[k]["default_vendor_max_supply"] for k in item_names], dtype=float)

        budgets = np.full(T, base_budget * budget_multiplier, dtype=float)
        cleanroom_cap = base_cap * capacity_multiplier

        sol = self.optimiser.solve_multi_period_procurement_milp(
            item_names=item_names,
            periods=periods,
            demands_matrix=demands,
            initial_inventory=init_stock,
            procurement_costs=p_costs,
            manufacturing_costs=m_costs,
            holding_costs=h_costs,
            shortage_penalties=s_costs,
            quarterly_budgets=budgets,
            cleanroom_capacity_per_quarter=cleanroom_cap,
            tooling_caps=tooling_caps,
            supplier_caps=supplier_caps,
            is_integer=is_integer
        )

        return sol
