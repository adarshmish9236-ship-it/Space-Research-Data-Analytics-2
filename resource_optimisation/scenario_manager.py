"""
ORBITALYTICS Phase 9 — Scenario Analysis Manager
Manages multi-scenario operational simulations comparing:
  1. Baseline Scenario (nominal forecast, standard budget & capacity)
  2. High-Demand Scenario (upper 95% prediction interval surge)
  3. Low-Demand Scenario (lower 95% prediction interval trough)
  4. Limited-Budget Scenario (-35% fiscal austerity)
  5. Increased-Production Scenario (+35% internal manufacturing expansion)

Provides side-by-side trade-off matrices, constraint utilization audits,
and explanation of assumptions.
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from resource_optimisation.data_input import OptimizationDataLoader
from resource_optimisation.shortage_engine import ShortageDetectionEngine
from resource_optimisation.procurement_planner import ProcurementPlanner
from resource_optimisation.optimiser import ResourceOptimiser


class ScenarioManager:
    """Orchestrates scenario evaluations across equipment and consumable resources."""

    def __init__(self):
        self.loader = OptimizationDataLoader()
        self.shortage_engine = ShortageDetectionEngine()
        self.procurement_planner = ProcurementPlanner()
        self.optimiser = ResourceOptimiser()

    def run_all_scenarios(self, domain: str = "equipment_demand") -> Dict[str, Any]:
        """
        Executes all 5 scenarios for the specified domain and compiles comparative metrics.
        """
        fc_df = self.loader.load_forecast_projections(domain)

        if domain == "equipment_demand":
            params = self.loader.get_equipment_parameters()
            is_integer = True
            base_budget_q = 850_000.0   # $850M/quarter in $k
            base_capacity_q = 1200.0    # units/quarter
        else:
            params = self.loader.get_resource_parameters()
            is_integer = False
            base_budget_q = 250_000.0   # $250M/quarter in $k
            base_capacity_q = 2000.0

        item_names = list(params.keys())
        periods = sorted(fc_df["period"].unique().tolist())
        M = len(item_names)
        T = len(periods)

        # Scenario definitions
        scenarios_def = [
            {
                "id": "baseline",
                "name": "1. Baseline Scenario",
                "demand_col": "forecast",
                "budget_mult": 1.0,
                "cap_mult": 1.0,
                "description": "Nominal Phase 8 forecast with authorized quarterly budgets and baseline cleanroom capacity."
            },
            {
                "id": "high_demand",
                "name": "2. High-Demand Scenario (95% Upper Bound)",
                "demand_col": "upper_95",
                "budget_mult": 1.0,
                "cap_mult": 1.0,
                "description": "Upper 95% confidence interval demand surge (+10% to +15%) testing supply chain resilience."
            },
            {
                "id": "low_demand",
                "name": "3. Low-Demand Scenario (95% Lower Bound)",
                "demand_col": "lower_95",
                "budget_mult": 1.0,
                "cap_mult": 1.0,
                "description": "Lower 95% confidence interval contraction evaluating surplus inventory holding risks."
            },
            {
                "id": "limited_budget",
                "name": "4. Limited-Budget Scenario (-35% Austerity)",
                "demand_col": "forecast",
                "budget_mult": 0.65,
                "cap_mult": 1.0,
                "description": "Severe budgetary contraction (-35%) forcing optimal trade-offs and priority triage."
            },
            {
                "id": "increased_production",
                "name": "5. Increased-Production Scenario (+35% Capacity)",
                "demand_col": "forecast",
                "budget_mult": 1.0,
                "cap_mult": 1.35,
                "description": "Internal manufacturing expansion (+35% tooling capacity) testing make-vs-buy shift."
            }
        ]

        # Extract fixed item arrays
        init_stock = np.array([params[k]["default_initial_stock"] for k in item_names], dtype=float)
        p_costs = np.array([params[k]["unit_procurement_cost_k"] for k in item_names], dtype=float)
        m_costs = np.array([
            params[k].get("unit_manufacturing_cost_k", params[k].get("unit_internal_production_cost_k", 400.0))
            for k in item_names
        ], dtype=float)
        h_costs = np.array([params[k]["holding_cost_per_quarter_k"] for k in item_names], dtype=float)
        s_costs = np.array([params[k]["shortage_penalty_k"] for k in item_names], dtype=float)
        tooling_caps_base = np.array([
            params[k].get("default_mfg_capacity_per_quarter", params[k].get("default_production_capacity", 150.0))
            for k in item_names
        ], dtype=float)
        supplier_caps = np.array([params[k]["default_vendor_max_supply"] for k in item_names], dtype=float)

        # Mission priority setup
        priorities = self.loader.get_mission_priority_weights()
        tier_names = list(priorities.keys())
        tier_weights = np.array([priorities[k]["weight"] for k in tier_names], dtype=float)
        tier_shares = np.array([priorities[k]["allocation_demand_share"] for k in tier_names], dtype=float)

        scenario_results = []
        comparison_matrix = []

        for sc in scenarios_def:
            demand_col = sc["demand_col"]
            budget_mult = sc["budget_mult"]
            cap_mult = sc["cap_mult"]

            # 1. Build demand matrix for this scenario
            demands = np.zeros((M, T), dtype=float)
            for i, name in enumerate(item_names):
                sub = fc_df[fc_df["series_name"] == name].sort_values("period")
                demands[i, :] = sub[demand_col].values

            # 2. Scaled budgets and capacities
            budgets = np.full(T, base_budget_q * budget_mult, dtype=float)
            cleanroom_cap = base_capacity_q * cap_mult
            tooling_caps = tooling_caps_base * cap_mult

            # 3. Solve MILP / LP Optimization
            opt_sol = self.optimiser.solve_multi_period_procurement_milp(
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

            # 4. Unconstrained Shortage Detection for benchmark
            shortage_evals = self.shortage_engine.evaluate_all_items(
                forecast_df=fc_df,
                item_parameters=params,
                demand_column=demand_col,
                capacity_multiplier=cap_mult
            )

            # 5. Mission Priority Allocation
            # Available supply for Q1
            q1_procured = np.array([
                opt_sol["item_solutions"][i]["quarterly_plans"][0]["procurement_order_units"]
                for i in range(M)
            ])
            q1_mfg = np.array([
                opt_sol["item_solutions"][i]["quarterly_plans"][0]["internal_manufacturing_units"]
                for i in range(M)
            ])
            avail_q1 = init_stock + q1_procured + q1_mfg
            demands_q1_by_tier = demands[:, 0:1] * tier_shares.reshape(1, -1)

            prio_sol = self.optimiser.solve_mission_priority_allocation(
                item_names=item_names,
                available_supply=avail_q1,
                tier_names=tier_names,
                tier_weights=tier_weights,
                demand_by_tier=demands_q1_by_tier
            )

            # Extract Critical Mission fill rate
            crit_fill_pct = prio_sol["tier_allocations_summary"][0]["tier_fulfillment_rate_pct"]

            # Summary metrics
            tot_demand = opt_sol["performance_summary"]["total_demand_units_4q"]
            tot_shortage = opt_sol["performance_summary"]["total_shortage_units_4q"]
            fill_rate = opt_sol["performance_summary"]["aggregate_fill_rate_pct"]
            op_cost_m = round(opt_sol["cost_breakdown"]["total_operational_cost_k"] / 1000.0, 2)
            avg_budget_util = round(float(np.mean([b["utilization_pct"] for b in opt_sol["budget_utilization"]])), 2)
            avg_cap_util = round(float(np.mean([c["utilization_pct"] for c in opt_sol["capacity_utilization"]])), 2)

            # Total units procured and manufactured
            tot_proc = sum(
                sum(q["procurement_order_units"] for q in item["quarterly_plans"])
                for item in opt_sol["item_solutions"]
            )
            tot_mfg = sum(
                sum(q["internal_manufacturing_units"] for q in item["quarterly_plans"])
                for item in opt_sol["item_solutions"]
            )

            comparison_record = {
                "scenario_id": sc["id"],
                "scenario_name": sc["name"],
                "demand_volume_4q": tot_demand,
                "procured_units_4q": round(tot_proc, 1),
                "manufactured_units_4q": round(tot_mfg, 1),
                "shortage_units_4q": tot_shortage,
                "aggregate_fill_rate_pct": fill_rate,
                "critical_tier1_fill_rate_pct": crit_fill_pct,
                "operational_expenditure_million_usd": op_cost_m,
                "avg_quarterly_budget_utilization_pct": avg_budget_util,
                "avg_manufacturing_capacity_utilization_pct": avg_cap_util,
                "solver_status": opt_sol["status"]
            }
            comparison_matrix.append(comparison_record)

            scenario_record = {
                "scenario_meta": sc,
                "solver_solution": opt_sol,
                "priority_allocation": prio_sol,
                "unconstrained_shortage_benchmark": shortage_evals,
                "metrics_summary": comparison_record
            }
            scenario_results.append(scenario_record)

        return {
            "domain": domain,
            "total_scenarios_evaluated": len(scenarios_def),
            "comparison_matrix": comparison_matrix,
            "scenarios": scenario_results,
            "assumptions_documentation": {
                "baseline_quarterly_budget": f"${round(base_budget_q/1000, 1)} Million per quarter",
                "cleanroom_tooling_capacity": f"{round(base_capacity_q)} total units per quarter across components",
                "lead_times": "Empirical historical means (247-266 days, ~3 quarters)",
                "holding_cost": "2.5% of unit procurement price per quarter",
                "shortage_penalty": "5.0x unit procurement price",
                "service_level": "95% (Z=1.645) stochastic safety stock"
            }
        }
