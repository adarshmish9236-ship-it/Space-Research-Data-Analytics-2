"""
ORBITALYTICS Phase 9 — Comprehensive Test Suite
Validates:
  - Input data loading and empirical parameter extraction
  - Shortage, surplus, and safety-stock equations
  - Procurement planning with lead-time offsetting and budget capping
  - Mixed-Integer Linear Programming (MILP) optimality and inventory balance constraints
  - Priority-weighted mission resource allocation hierarchy
  - Edge cases: infeasible constraints, zero inventory, insufficient budget, 5x demand surges
  - Scenario comparison consistency (High-Demand, Low-Demand, Austerity, Production Expansion)
  - Persistent output artifacts and JSON manifests
"""

import json
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import milp, LinearConstraint, Bounds

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PHASE9_RESULTS_DIR = PROJECT_ROOT / "docs" / "phase_9" / "results"

from resource_optimisation.data_input import OptimizationDataLoader
from resource_optimisation.shortage_engine import ShortageDetectionEngine
from resource_optimisation.procurement_planner import ProcurementPlanner
from resource_optimisation.optimiser import ResourceOptimiser
from resource_optimisation.scenario_manager import ScenarioManager


def test_optimization_data_loader():
    """Verify loading Phase 8 forecasts and empirical historical parameters."""
    loader = OptimizationDataLoader()
    fc_df = loader.load_forecast_projections()
    assert not fc_df.empty, "Forecast projections DataFrame must not be empty"
    assert "forecast" in fc_df.columns
    assert "period" in fc_df.columns
    assert len(fc_df["period"].unique()) == 4, "Must span exactly 4 future quarters"

    eq_params = loader.get_equipment_parameters()
    assert len(eq_params) == 8, f"Expected 8 equipment categories, got {len(eq_params)}"
    for eq, p in eq_params.items():
        assert p["unit_procurement_cost_k"] > 0
        assert p["avg_lead_time_days"] > 0
        assert p["default_initial_stock"] >= 0

    res_params = loader.get_resource_parameters()
    assert len(res_params) == 7, f"Expected 7 consumable resource categories, got {len(res_params)}"

    priorities = loader.get_mission_priority_weights()
    assert len(priorities) == 4, "Must define 4 mission priority tiers"
    assert priorities["Tier 1: Critical Strategic"]["weight"] > priorities["Tier 2: High Priority"]["weight"]


def test_shortage_and_surplus_detection():
    """Verify mathematical definitions of Safety Stock, Shortage, Surplus, and Fill Rate."""
    engine = ShortageDetectionEngine(service_level_z=1.645)

    # 1. Safety stock formula test
    ss = engine.calculate_safety_stock(
        demand_mean=500.0,
        demand_std=50.0,
        lead_time_days=270.0,  # 3 quarters
        lead_time_std_days=15.0
    )
    assert ss > 0, "Safety stock must be positive"
    # Under 3 quarters lead time, sqrt(3 * 50^2 + 500^2 * (15/90)^2) = sqrt(7500 + 6944) = sqrt(14444) = 120.18
    # Z * 120.18 = 1.645 * 120.18 = 197.7
    assert 150.0 <= ss <= 250.0, f"Safety stock {ss} outside expected bounds"

    # 2. Shortage / Surplus calculation test
    periods = ["2026Q4", "2027Q1", "2027Q2", "2027Q3"]
    demands = [500.0, 500.0, 500.0, 500.0]

    # Ample supply case: init_stock 2000, production 0 -> no shortage, surplus exists
    res_surplus = engine.evaluate_series_shortages(
        series_name="Test Component",
        forecast_periods=periods,
        forecast_demands=demands,
        initial_inventory=2500.0,
        planned_production_per_quarter=0.0,
        unit_cost_k=500.0,
        demand_std=30.0,
        lead_time_days=90.0,
        safety_stock_override=50.0
    )
    assert res_surplus["total_shortage_units_4q"] == 0.0
    assert res_surplus["aggregate_fill_rate_pct"] == 100.0
    assert res_surplus["total_surplus_units_4q"] > 0.0

    # Deficit supply case: init_stock 0, production 100 -> shortage exists
    res_shortage = engine.evaluate_series_shortages(
        series_name="Test Component Deficit",
        forecast_periods=periods,
        forecast_demands=demands,
        initial_inventory=0.0,
        planned_production_per_quarter=100.0,
        unit_cost_k=500.0,
        demand_std=30.0,
        lead_time_days=90.0,
        safety_stock_override=50.0
    )
    assert res_shortage["total_shortage_units_4q"] > 0.0
    assert res_shortage["aggregate_fill_rate_pct"] < 100.0


def test_procurement_planner_logic():
    """Verify base-stock target, lead-time offsetting, and budget constraints."""
    planner = ProcurementPlanner()
    periods = ["2026Q4", "2027Q1", "2027Q2", "2027Q3"]
    demands = [400.0, 400.0, 400.0, 400.0]

    plan = planner.generate_procurement_plan(
        series_name="Star Trackers",
        forecast_periods=periods,
        forecast_demands=demands,
        initial_inventory=100.0,
        planned_production_per_quarter=50.0,
        safety_stock=50.0,
        unit_cost_k=500.0,
        lead_time_days=180.0,  # 2 quarters
        quarterly_budget_k=500_000.0,
        vendor_max_supply=800.0
    )

    assert plan["total_procured_units_4q"] > 0
    assert plan["total_expenditure_k"] > 0
    assert plan["lead_time_quarters"] == 2
    assert len(plan["quarterly_procurement_schedule"]) == 4

    # Verify orders do not exceed max affordable under budget
    for q in plan["quarterly_procurement_schedule"]:
        max_affordable = 500_000.0 / 500.0
        assert q["recommended_procurement_qty"] <= max_affordable
        assert q["recommended_procurement_qty"] <= 800.0


def test_milp_optimization_feasibility_and_optimality():
    """Verify that multi-period MILP solver achieves OPTIMAL status and strict inventory balance."""
    loader = OptimizationDataLoader()
    fc_df = loader.load_forecast_projections("equipment_demand")
    eq_params = loader.get_equipment_parameters()

    item_names = list(eq_params.keys())
    periods = sorted(fc_df["period"].unique().tolist())
    M = len(item_names)
    T = len(periods)

    demands = np.zeros((M, T))
    for i, name in enumerate(item_names):
        sub = fc_df[fc_df["series_name"] == name].sort_values("period")
        demands[i, :] = sub["forecast"].values

    init_stock = np.array([eq_params[k]["default_initial_stock"] for k in item_names])
    p_costs = np.array([eq_params[k]["unit_procurement_cost_k"] for k in item_names])
    m_costs = np.array([eq_params[k]["unit_manufacturing_cost_k"] for k in item_names])
    h_costs = np.array([eq_params[k]["holding_cost_per_quarter_k"] for k in item_names])
    s_costs = np.array([eq_params[k]["shortage_penalty_k"] for k in item_names])
    budgets = np.full(T, 850_000.0)
    cleanroom_cap = 1200.0
    tooling_caps = np.array([eq_params[k]["default_mfg_capacity_per_quarter"] for k in item_names])
    supplier_caps = np.array([eq_params[k]["default_vendor_max_supply"] for k in item_names])

    opt = ResourceOptimiser()
    sol = opt.solve_multi_period_procurement_milp(
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
        is_integer=True
    )

    assert sol["status"] == "OPTIMAL"
    assert sol["is_optimal"] is True
    assert sol["solve_time_seconds"] < 5.0, "MILP solve time must be under 5 seconds"

    # Verify inventory balance for every single item and period:
    # I_{t-1} + p_t + x_t + s_t - I_t = Demand_t
    for i, item in enumerate(sol["item_solutions"]):
        prev_I = init_stock[i]
        for t, q in enumerate(item["quarterly_plans"]):
            x_val = q["procurement_order_units"]
            p_val = q["internal_manufacturing_units"]
            I_val = q["ending_inventory_units"]
            s_val = q["shortage_units"]
            d_val = q["forecast_demand"]

            lhs = prev_I + p_val + x_val + s_val - I_val
            assert abs(lhs - d_val) < 1e-4, f"Inventory balance violated for {item['item_name']} at {q['period']}: {lhs} != {d_val}"
            prev_I = I_val

    # Verify budget constraint was not violated in any quarter
    for b in sol["budget_utilization"]:
        assert b["budget_spent_k"] <= b["budget_allocated_k"] + 1e-3, f"Budget exceeded in {b['period']}"

    # Verify cleanroom capacity was not violated in any quarter
    for c in sol["capacity_utilization"]:
        assert c["cleanroom_units_used"] <= c["cleanroom_capacity_units"] + 1e-3, f"Capacity exceeded in {c['period']}"


def test_priority_weighted_mission_allocation():
    """Verify that limited resources are routed strictly to higher-priority missions first."""
    opt = ResourceOptimiser()
    item_names = ["Optical_Links", "Rad750_CPUs"]
    # Supply is strictly less than total demand across all tiers
    avail_supply = np.array([100.0, 100.0])

    tier_names = ["Tier 1: Critical", "Tier 2: High", "Tier 3: Science", "Tier 4: Exploratory"]
    tier_weights = np.array([100.0, 60.0, 30.0, 10.0])

    # Demand: 60 for Tier 1, 60 for Tier 2, 40 for Tier 3, 20 for Tier 4 (Total = 180, Supply = 100)
    demand_by_tier = np.array([
        [60.0, 60.0, 40.0, 20.0],
        [60.0, 60.0, 40.0, 20.0]
    ])

    sol = opt.solve_mission_priority_allocation(item_names, avail_supply, tier_names, tier_weights, demand_by_tier)
    assert sol["status"] == "OPTIMAL"

    summary = sol["tier_allocations_summary"]
    # Tier 1 (weight 100) must receive 100% of its requirement (60 units allocated)
    assert summary[0]["tier_fulfillment_rate_pct"] == 100.0
    # Tier 2 (weight 60) receives remaining 40 units (40 / 60 = 66.67%)
    assert summary[1]["tier_fulfillment_rate_pct"] > 60.0
    # Tier 3 and 4 should receive 0% because supply was exhausted by Tier 1 & 2
    assert summary[2]["tier_fulfillment_rate_pct"] == 0.0
    assert summary[3]["tier_fulfillment_rate_pct"] == 0.0


def test_edge_case_zero_inventory_and_insufficient_budget():
    """Verify behavior when initial stock is 0 and budget is severely restricted."""
    opt = ResourceOptimiser()
    item_names = ["Cryogenic Tanks", "Solar Arrays"]
    periods = ["2026Q4"]
    demands = np.array([[500.0], [500.0]])
    init_stock = np.array([0.0, 0.0])
    p_costs = np.array([500.0, 500.0])
    m_costs = np.array([375.0, 375.0])
    h_costs = np.array([12.5, 12.5])
    s_costs = np.array([2500.0, 2500.0])

    # Severe budget: $50k when $500k is needed
    budgets = np.array([50_000.0])
    cleanroom_cap = 50.0
    tooling_caps = np.array([50.0, 50.0])
    supplier_caps = np.array([500.0, 500.0])

    sol = opt.solve_multi_period_procurement_milp(
        item_names, periods, demands, init_stock, p_costs, m_costs, h_costs, s_costs,
        budgets, cleanroom_cap, tooling_caps, supplier_caps, is_integer=True
    )

    assert sol["status"] == "OPTIMAL"
    assert sol["performance_summary"]["total_shortage_units_4q"] > 800.0
    assert sol["performance_summary"]["aggregate_fill_rate_pct"] < 25.0
    assert sol["budget_utilization"][0]["budget_spent_k"] <= 50_000.0


def test_edge_case_extreme_demand_surge():
    """Verify stability under 5x extreme demand spike."""
    opt = ResourceOptimiser()
    item_names = ["Cryogenic Tanks"]
    periods = ["2026Q4"]
    # 5x demand spike: 2,500 units
    demands = np.array([[2500.0]])
    init_stock = np.array([50.0])
    p_costs = np.array([500.0])
    m_costs = np.array([375.0])
    h_costs = np.array([12.5])
    s_costs = np.array([2500.0])

    budgets = np.array([500_000.0])
    cleanroom_cap = 200.0
    tooling_caps = np.array([200.0])
    supplier_caps = np.array([600.0])  # supplier cannot provide 2,500

    sol = opt.solve_multi_period_procurement_milp(
        item_names, periods, demands, init_stock, p_costs, m_costs, h_costs, s_costs,
        budgets, cleanroom_cap, tooling_caps, supplier_caps, is_integer=True
    )

    assert sol["status"] == "OPTIMAL"
    # Must cap procurement at supplier cap (600) and manufacturing at cleanroom cap (200)
    q_plan = sol["item_solutions"][0]["quarterly_plans"][0]
    assert q_plan["procurement_order_units"] <= 600.0
    assert q_plan["internal_manufacturing_units"] <= 200.0
    assert q_plan["shortage_units"] > 1600.0


def test_scenario_manager_comparisons():
    """Verify that ScenarioManager executes all 5 scenarios with correct comparative dynamics."""
    sm = ScenarioManager()
    res = sm.run_all_scenarios(domain="equipment_demand")
    assert res["total_scenarios_evaluated"] == 5

    df = pd.DataFrame(res["comparison_matrix"]).set_index("scenario_id")

    # High Demand must have higher demand volume than Baseline
    assert df.loc["high_demand", "demand_volume_4q"] > df.loc["baseline", "demand_volume_4q"]

    # Low Demand must have lower demand volume than Baseline
    assert df.loc["low_demand", "demand_volume_4q"] < df.loc["baseline", "demand_volume_4q"]

    # Limited Budget must spend significantly less operational expenditure
    assert df.loc["limited_budget", "operational_expenditure_million_usd"] < df.loc["baseline", "operational_expenditure_million_usd"]

    # Increased Production must manufacture more units than Baseline
    assert df.loc["increased_production", "manufactured_units_4q"] > df.loc["baseline", "manufactured_units_4q"]


def test_output_artifacts_manifest():
    """Verify that all Phase 9 CSV and JSON artifacts are persisted and non-empty."""
    expected_files = [
        "scenario_comparison_matrix.csv",
        "shortage_surplus_report.csv",
        "procurement_recommendations.csv",
        "priority_allocation_plan.csv",
        "orbitalytics_resource_optimisation.json",
        "optimisation_manifest.json"
    ]

    for fname in expected_files:
        p = PHASE9_RESULTS_DIR / fname
        assert p.exists(), f"Phase 9 artifact missing: {p}"
        assert p.stat().st_size > 0, f"Phase 9 artifact is empty: {p}"

    # Verify JSON structure
    with open(PHASE9_RESULTS_DIR / "orbitalytics_resource_optimisation.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["pipeline"].startswith("ORBITALYTICS Phase 9")
    assert "equipment_demand" in data["domains"]
    assert "resource_consumption" in data["domains"]
