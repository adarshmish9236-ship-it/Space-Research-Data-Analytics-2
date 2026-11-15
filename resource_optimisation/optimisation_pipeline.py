"""
ORBITALYTICS Phase 9 — Master Resource Optimisation Pipeline
Executes end-to-end shortage detection, procurement planning, mathematical optimization,
scenario evaluation, and report generation for space equipment and consumable resources.

Exports:
  - docs/phase_9/results/orbitalytics_resource_optimisation.json
  - docs/phase_9/results/scenario_comparison_matrix.csv
  - docs/phase_9/results/shortage_surplus_report.csv
  - docs/phase_9/results/procurement_recommendations.csv
  - docs/phase_9/results/priority_allocation_plan.csv
  - docs/phase_9/results/optimisation_manifest.json
"""

import time
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PHASE9_DOCS_DIR = PROJECT_ROOT / "docs" / "phase_9"
RESULTS_DIR = PHASE9_DOCS_DIR / "results"

from resource_optimisation.data_input import OptimizationDataLoader
from resource_optimisation.shortage_engine import ShortageDetectionEngine
from resource_optimisation.procurement_planner import ProcurementPlanner
from resource_optimisation.optimiser import ResourceOptimiser
from resource_optimisation.scenario_manager import ScenarioManager


class MasterOptimisationPipeline:
    """Orchestrates Phase 9 execution and exports persistent artifacts."""

    def __init__(self):
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        self.loader = OptimizationDataLoader()
        self.shortage_engine = ShortageDetectionEngine()
        self.procurement_planner = ProcurementPlanner()
        self.optimiser = ResourceOptimiser()
        self.scenario_mgr = ScenarioManager()

    def run_pipeline(self) -> Dict[str, Any]:
        print("\n" + "="*80)
        print("ORBITALYTICS PHASE 9 — MASTER RESOURCE OPTIMISATION PIPELINE")
        print("="*80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        t_start = time.time()

        # 1. Execute Scenarios for Target 1: Satellite Equipment Demand
        print("\n[STEP 1/4] Running 5 Scenarios for Satellite Equipment Demand ...")
        t0 = time.time()
        eq_scenarios = self.scenario_mgr.run_all_scenarios(domain="equipment_demand")
        eq_time = round(time.time() - t0, 2)
        print(f"  -> Equipment Demand Scenarios completed in {eq_time}s.")

        # 2. Execute Scenarios for Target 2: Space Research Resource Consumption
        print("\n[STEP 2/4] Running 5 Scenarios for Space Research Resource Consumption ...")
        t0 = time.time()
        res_scenarios = self.scenario_mgr.run_all_scenarios(domain="resource_consumption")
        res_time = round(time.time() - t0, 2)
        print(f"  -> Resource Consumption Scenarios completed in {res_time}s.")

        # 3. Generate Baseline Detailed Procurement & Shortage Reports
        print("\n[STEP 3/4] Generating Detailed Fleet Reports ...")
        fc_eq = self.loader.load_forecast_projections("equipment_demand")
        eq_params = self.loader.get_equipment_parameters()
        fleet_proc_eq = self.procurement_planner.generate_fleet_procurement_plan(
            fc_eq, eq_params, quarterly_total_budget_k=850_000.0
        )

        fc_res = self.loader.load_forecast_projections("resource_consumption")
        res_params = self.loader.get_resource_parameters()
        fleet_proc_res = self.procurement_planner.generate_fleet_procurement_plan(
            fc_res, res_params, quarterly_total_budget_k=250_000.0
        )

        # 4. Export Persistent CSV Artifacts
        print("\n[STEP 4/4] Exporting Reports and Manifests to docs/phase_9/results/ ...")

        # A) Scenario Comparison Matrix CSV
        comp_records = []
        for r in eq_scenarios["comparison_matrix"]:
            rec = {"domain": "equipment_demand"}
            rec.update(r)
            comp_records.append(rec)
        for r in res_scenarios["comparison_matrix"]:
            rec = {"domain": "resource_consumption"}
            rec.update(r)
            comp_records.append(rec)

        comp_df = pd.DataFrame(comp_records)
        comp_csv_path = RESULTS_DIR / "scenario_comparison_matrix.csv"
        comp_df.to_csv(comp_csv_path, index=False)
        print(f"  -> Saved Scenario Comparison Matrix: {comp_csv_path}")

        # B) Shortage & Surplus Detailed Report CSV
        shortage_rows = []
        base_eq_sol = eq_scenarios["scenarios"][0]["solver_solution"]
        for item in base_eq_sol["item_solutions"]:
            for q in item["quarterly_plans"]:
                shortage_rows.append({
                    "domain": "equipment_demand",
                    "item_name": item["item_name"],
                    "period": q["period"],
                    "forecast_demand": q["forecast_demand"],
                    "procurement_order_units": q["procurement_order_units"],
                    "internal_manufacturing_units": q["internal_manufacturing_units"],
                    "ending_inventory_units": q["ending_inventory_units"],
                    "shortage_units": q["shortage_units"],
                    "fill_rate_pct": q["fill_rate_pct"],
                    "scenario": "baseline"
                })

        base_res_sol = res_scenarios["scenarios"][0]["solver_solution"]
        for item in base_res_sol["item_solutions"]:
            for q in item["quarterly_plans"]:
                shortage_rows.append({
                    "domain": "resource_consumption",
                    "item_name": item["item_name"],
                    "period": q["period"],
                    "forecast_demand": q["forecast_demand"],
                    "procurement_order_units": q["procurement_order_units"],
                    "internal_manufacturing_units": q["internal_manufacturing_units"],
                    "ending_inventory_units": q["ending_inventory_units"],
                    "shortage_units": q["shortage_units"],
                    "fill_rate_pct": q["fill_rate_pct"],
                    "scenario": "baseline"
                })

        shortage_df = pd.DataFrame(shortage_rows)
        shortage_csv_path = RESULTS_DIR / "shortage_surplus_report.csv"
        shortage_df.to_csv(shortage_csv_path, index=False)
        print(f"  -> Saved Shortage & Surplus Report: {shortage_csv_path}")

        # C) Procurement Recommendations CSV
        proc_rows = []
        for plan in fleet_proc_eq["item_plans"]:
            for q in plan["quarterly_procurement_schedule"]:
                proc_rows.append({
                    "domain": "equipment_demand",
                    "item_name": plan["series_name"],
                    "order_period": q["order_period"],
                    "forecast_demand": q["forecast_demand"],
                    "recommended_procurement_qty": q["recommended_procurement_qty"],
                    "order_cost_thousand_usd": q["order_cost_thousand_usd"],
                    "lead_time_quarters": q["lead_time_quarters"],
                    "expected_delivery_period": q["expected_delivery_period"],
                    "projected_ending_inventory": q["projected_ending_inventory"]
                })

        for plan in fleet_proc_res["item_plans"]:
            for q in plan["quarterly_procurement_schedule"]:
                proc_rows.append({
                    "domain": "resource_consumption",
                    "item_name": plan["series_name"],
                    "order_period": q["order_period"],
                    "forecast_demand": q["forecast_demand"],
                    "recommended_procurement_qty": q["recommended_procurement_qty"],
                    "order_cost_thousand_usd": q["order_cost_thousand_usd"],
                    "lead_time_quarters": q["lead_time_quarters"],
                    "expected_delivery_period": q["expected_delivery_period"],
                    "projected_ending_inventory": q["projected_ending_inventory"]
                })

        proc_df = pd.DataFrame(proc_rows)
        proc_csv_path = RESULTS_DIR / "procurement_recommendations.csv"
        proc_df.to_csv(proc_csv_path, index=False)
        print(f"  -> Saved Procurement Recommendations: {proc_csv_path}")

        # D) Priority Allocation Plan CSV
        prio_rows = []
        base_eq_prio = eq_scenarios["scenarios"][0]["priority_allocation"]
        for item in base_eq_prio["item_allocations"]:
            for tier, alloc in item["allocations_by_tier"].items():
                prio_rows.append({
                    "domain": "equipment_demand",
                    "item_name": item["item_name"],
                    "mission_priority_tier": tier,
                    "demand_units": alloc["demand"],
                    "allocated_units": alloc["allocated"],
                    "unmet_units": alloc["unmet"],
                    "fulfillment_pct": round((alloc["allocated"] / max(alloc["demand"], 1e-4)) * 100.0, 2)
                })

        base_res_prio = res_scenarios["scenarios"][0]["priority_allocation"]
        for item in base_res_prio["item_allocations"]:
            for tier, alloc in item["allocations_by_tier"].items():
                prio_rows.append({
                    "domain": "resource_consumption",
                    "item_name": item["item_name"],
                    "mission_priority_tier": tier,
                    "demand_units": alloc["demand"],
                    "allocated_units": alloc["allocated"],
                    "unmet_units": alloc["unmet"],
                    "fulfillment_pct": round((alloc["allocated"] / max(alloc["demand"], 1e-4)) * 100.0, 2)
                })

        prio_df = pd.DataFrame(prio_rows)
        prio_csv_path = RESULTS_DIR / "priority_allocation_plan.csv"
        prio_df.to_csv(prio_csv_path, index=False)
        print(f"  -> Saved Priority Allocation Plan: {prio_csv_path}")

        # E) Master JSON Manifest
        total_pipeline_duration = round(time.time() - t_start, 2)
        master_manifest = {
            "pipeline": "ORBITALYTICS Phase 9 Resource Optimisation and Shortage Detection",
            "executed_at": datetime.now().isoformat(),
            "execution_duration_seconds": total_pipeline_duration,
            "solvers_utilized": [
                "HiGHS Branch-and-Cut MILP (scipy.optimize.milp)",
                "HiGHS Simplex LP (scipy.optimize.linprog)"
            ],
            "total_items_modeled": len(eq_params) + len(res_params),
            "domains": {
                "equipment_demand": eq_scenarios,
                "resource_consumption": res_scenarios
            },
            "fleet_procurement_plans": {
                "equipment_demand": fleet_proc_eq,
                "resource_consumption": fleet_proc_res
            }
        }

        # Serializer helper for numpy types
        def np_encoder(obj):
            if isinstance(obj, (np.integer, np.int64, np.int32)):
                return int(obj)
            if isinstance(obj, (np.floating, np.float64, np.float32)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        json_path = RESULTS_DIR / "orbitalytics_resource_optimisation.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(master_manifest, f, indent=2, default=np_encoder)
        print(f"  -> Saved Master Optimisation JSON: {json_path}")

        # F) Optimisation Manifest Summary
        manifest_summary = {
            "phase": 9,
            "component": "Resource_Optimisation_and_Shortage_Detection",
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": total_pipeline_duration,
            "status": "SUCCESS",
            "scenarios_evaluated": 10,  # 5 for eq, 5 for res
            "equipment_categories": len(eq_params),
            "resource_categories": len(res_params),
            "artifacts_generated": [
                str(comp_csv_path.relative_to(PROJECT_ROOT)),
                str(shortage_csv_path.relative_to(PROJECT_ROOT)),
                str(proc_csv_path.relative_to(PROJECT_ROOT)),
                str(prio_csv_path.relative_to(PROJECT_ROOT)),
                str(json_path.relative_to(PROJECT_ROOT))
            ]
        }
        manifest_path = RESULTS_DIR / "optimisation_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_summary, f, indent=2)
        print(f"  -> Saved Manifest Summary: {manifest_path}")

        print("\n" + "="*80)
        print(f"PHASE 9 PIPELINE COMPLETED SUCCESSFULLY IN {total_pipeline_duration}s")
        print("="*80)
        return master_manifest


if __name__ == "__main__":
    pipeline = MasterOptimisationPipeline()
    pipeline.run_pipeline()
