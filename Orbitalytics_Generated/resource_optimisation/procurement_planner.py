"""
ORBITALYTICS Phase 9 — Procurement Planning Engine
Calculates suggested procurement quantities, order timing, and financial commitments
considering existing inventory, forecast demand, planned internal production, lead times,
safety stocks, and quarterly budget boundaries.

Core Formulations:
  Lead-Time Protection Interval = L_q + 1 (order placed in t covers through t + L_q)
  Demand Over Protection Horizon = sum_{tau=t}^{t+L_q} Forecast_Demand(tau)
  Order-Up-To Target (Base Stock S) = Demand Over Protection Horizon + Safety Stock
  Net Requirement = max(0, S - (On-Hand Inventory + In-Flight Orders + Planned Production))
  Budget-Constrained Order = min(Net Requirement, floor(Allocated Budget / Unit Cost))
"""

import math
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd


class ProcurementPlanner:
    """Computes suggested multi-period procurement schedules and capital requirements."""

    def __init__(self):
        pass

    def generate_procurement_plan(self,
                                  series_name: str,
                                  forecast_periods: List[str],
                                  forecast_demands: List[float],
                                  initial_inventory: float,
                                  planned_production_per_quarter: float,
                                  safety_stock: float,
                                  unit_cost_k: float,
                                  lead_time_days: float,
                                  quarterly_budget_k: float,
                                  vendor_max_supply: float) -> Dict[str, Any]:
        """
        Generates a 4-quarter rolling procurement plan for an individual item.
        """
        lead_time_quarters = max(1, int(round(lead_time_days / 90.0)))
        n_periods = len(forecast_periods)

        procurement_orders = []
        curr_stock = float(initial_inventory)
        remaining_budget = float(quarterly_budget_k)
        total_procured_units = 0.0
        total_procurement_expenditure_k = 0.0

        # In-flight pipeline tracking: orders placed in t arrive at t + lead_time_quarters
        # Pipeline array for incoming deliveries per quarter index
        pipeline_arrivals = [0.0] * (n_periods + lead_time_quarters + 2)

        for t_idx in range(n_periods):
            period = forecast_periods[t_idx]
            d_curr = float(forecast_demands[t_idx])

            # Influx from pipeline arriving at this quarter
            arrivals = pipeline_arrivals[t_idx]

            # Available stock before new orders
            avail_before_demand = curr_stock + planned_production_per_quarter + arrivals

            # Calculate demand over the lead-time protection horizon
            # An order placed now arrives in t_idx + lead_time_quarters
            horizon_end = min(n_periods, t_idx + lead_time_quarters + 1)
            future_demand_sum = sum(forecast_demands[t_idx:horizon_end])

            # If horizon extends beyond forecast periods, extrapolate using average
            extra_periods = (t_idx + lead_time_quarters + 1) - horizon_end
            if extra_periods > 0:
                avg_demand = float(np.mean(forecast_demands))
                future_demand_sum += avg_demand * extra_periods

            # Base stock target S = demand over horizon + safety stock
            base_stock_target = future_demand_sum + safety_stock

            # Inventory position = on-hand + in-flight orders arriving before horizon_end
            future_arrivals = sum(pipeline_arrivals[t_idx:horizon_end])
            inventory_position = curr_stock + planned_production_per_quarter + future_arrivals

            # Unconstrained suggested order
            unconstrained_qty = max(0.0, base_stock_target - inventory_position)

            # Apply vendor supplier capacity limit
            supplier_capped_qty = min(unconstrained_qty, vendor_max_supply)

            # Apply quarterly budget constraint
            max_affordable_qty = math.floor(remaining_budget / max(unit_cost_k, 1e-4))
            recommended_order_qty = min(supplier_capped_qty, max_affordable_qty)

            # Expenditure
            order_cost_k = round(recommended_order_qty * unit_cost_k, 2)

            # Register order in pipeline for future arrival
            arrival_idx = t_idx + lead_time_quarters
            if arrival_idx < len(pipeline_arrivals):
                pipeline_arrivals[arrival_idx] += recommended_order_qty

            # Expected delivery period
            if arrival_idx < n_periods:
                delivery_period = forecast_periods[arrival_idx]
            else:
                extra_q = arrival_idx - n_periods + 1
                delivery_period = f"T+{extra_q}Q Beyond Horizon"

            # Update ending stock for this quarter
            ending_stock = max(0.0, avail_before_demand - d_curr)
            curr_stock = ending_stock

            procurement_orders.append({
                "order_period": period,
                "forecast_demand": round(d_curr, 1),
                "on_hand_inventory": round(avail_before_demand, 1),
                "pipeline_arrivals": round(arrivals, 1),
                "base_stock_target": round(base_stock_target, 1),
                "unconstrained_suggested_order": round(unconstrained_qty, 1),
                "supplier_capacity_cap": round(vendor_max_supply, 1),
                "recommended_procurement_qty": round(recommended_order_qty, 1),
                "order_cost_thousand_usd": order_cost_k,
                "lead_time_days": round(lead_time_days, 1),
                "lead_time_quarters": lead_time_quarters,
                "expected_delivery_period": delivery_period,
                "projected_ending_inventory": round(ending_stock, 1)
            })

            total_procured_units += recommended_order_qty
            total_procurement_expenditure_k += order_cost_k

        return {
            "series_name": series_name,
            "unit_cost_k": unit_cost_k,
            "lead_time_quarters": lead_time_quarters,
            "safety_stock_target": safety_stock,
            "total_procured_units_4q": round(total_procured_units, 1),
            "total_expenditure_k": round(total_procurement_expenditure_k, 2),
            "quarterly_procurement_schedule": procurement_orders,
            "assumptions": {
                "base_stock_policy": "Protection horizon = Lead Time + 1 Review Period",
                "budget_enforcement": "Strict non-exceedance of quarterly allocated budget",
                "vendor_capacity": f"Capped at {vendor_max_supply} units/quarter",
                "service_level_target": "95% (Z=1.645)"
            }
        }

    def generate_fleet_procurement_plan(self,
                                        forecast_df: pd.DataFrame,
                                        item_parameters: Dict[str, Dict[str, Any]],
                                        quarterly_total_budget_k: float,
                                        service_level_z: float = 1.645) -> Dict[str, Any]:
        """
        Allocates quarterly budget across all items based on demand value share
        and generates comprehensive fleet procurement recommendations.
        """
        from resource_optimisation.shortage_engine import ShortageDetectionEngine
        shortage_engine = ShortageDetectionEngine(service_level_z=service_level_z)

        # Calculate demand value share to divide total budget among items
        item_demand_values = {}
        for item_name, params in item_parameters.items():
            sub = forecast_df[forecast_df["series_name"] == item_name]
            if not sub.empty:
                tot_d = float(sub["forecast"].sum())
                cost_k = params.get("unit_procurement_cost_k", 500.0)
                item_demand_values[item_name] = tot_d * cost_k

        tot_val = max(1.0, sum(item_demand_values.values()))

        plans = []
        fleet_total_expenditure_k = 0.0
        fleet_total_units = 0.0

        for item_name, params in item_parameters.items():
            sub = forecast_df[forecast_df["series_name"] == item_name].sort_values("period")
            if sub.empty:
                continue

            periods = sub["period"].tolist()
            demands = sub["forecast"].tolist()
            d_mean = float(np.mean(demands))
            d_std = params.get("historical_quarterly_demand_std", params.get("historical_quarterly_std", 25.0))
            lead_days = params.get("avg_lead_time_days", 250.0)
            lead_std = params.get("lead_time_std_days", 15.0)
            init_stock = params.get("default_initial_stock", 50.0)
            prod_cap = params.get("default_mfg_capacity_per_quarter", params.get("default_production_capacity", 40.0))
            cost_k = params.get("unit_procurement_cost_k", 500.0)
            vendor_max = params.get("default_vendor_max_supply", d_mean * 1.5)

            ss = shortage_engine.calculate_safety_stock(d_mean, d_std, lead_days, lead_std)

            # Proportional budget allocation
            share = item_demand_values.get(item_name, 0.0) / tot_val
            item_q_budget = quarterly_total_budget_k * share

            item_plan = self.generate_procurement_plan(
                series_name=item_name,
                forecast_periods=periods,
                forecast_demands=demands,
                initial_inventory=init_stock,
                planned_production_per_quarter=prod_cap,
                safety_stock=ss,
                unit_cost_k=cost_k,
                lead_time_days=lead_days,
                quarterly_budget_k=item_q_budget,
                vendor_max_supply=vendor_max
            )
            item_plan["domain"] = sub["domain"].iloc[0]
            plans.append(item_plan)
            fleet_total_expenditure_k += item_plan["total_expenditure_k"]
            fleet_total_units += item_plan["total_procured_units_4q"]

        return {
            "quarterly_total_budget_k": quarterly_total_budget_k,
            "fleet_total_procured_units_4q": round(fleet_total_units, 1),
            "fleet_total_expenditure_k": round(fleet_total_expenditure_k, 2),
            "budget_utilization_pct": round((fleet_total_expenditure_k / max(quarterly_total_budget_k * 4.0, 1e-4)) * 100.0, 2),
            "item_plans": plans
        }
