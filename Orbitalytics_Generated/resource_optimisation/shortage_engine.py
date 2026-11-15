"""
ORBITALYTICS Phase 9 — Shortage and Surplus Detection Engine
Implements deterministic and stochastic shortage detection, safety-stock computation,
and multi-period inventory balance simulation for space mission hardware and resources.

Core Formulations:
  Safety Stock = Z * sqrt( L_q * sigma_D^2 + D_bar^2 * sigma_Lq^2 )
  Gross Demand = Forecast Demand + Safety Stock
  Available Supply = Starting Inventory + Planned Production + Incoming Pipeline
  Shortage = max(0, Gross Demand - Available Supply)
  Surplus = max(0, Available Supply - Gross Demand)
  Fill Rate = 1 - (Shortage / max(Forecast Demand, 1))
"""

import math
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd


class ShortageDetectionEngine:
    """Computes safety stocks, shortages, surpluses, and fill rates across multi-quarter horizons."""

    def __init__(self, service_level_z: float = 1.645):
        """
        service_level_z: Z-score for cycle service level.
                         1.645 corresponds to 95% service level.
                         2.055 corresponds to 98% service level.
        """
        self.z = service_level_z

    def calculate_safety_stock(self,
                               demand_mean: float,
                               demand_std: float,
                               lead_time_days: float,
                               lead_time_std_days: float = 15.0) -> float:
        """
        Calculates stochastic safety stock accounting for both demand variability
        and procurement lead time uncertainty:
          SS = Z * sqrt( L_q * sigma_D^2 + D_bar^2 * sigma_Lq^2 )
        """
        lead_time_quarters = max(0.5, lead_time_days / 90.0)
        lead_time_std_quarters = max(0.1, lead_time_std_days / 90.0)

        term1 = lead_time_quarters * (demand_std ** 2)
        term2 = (demand_mean ** 2) * (lead_time_std_quarters ** 2)
        combined_variance = max(1.0, term1 + term2)

        safety_stock = self.z * math.sqrt(combined_variance)
        return round(safety_stock, 1)

    def evaluate_series_shortages(self,
                                 series_name: str,
                                 forecast_periods: List[str],
                                 forecast_demands: List[float],
                                 initial_inventory: float,
                                 planned_production_per_quarter: float,
                                 unit_cost_k: float,
                                 demand_std: float,
                                 lead_time_days: float,
                                 lead_time_std_days: float = 15.0,
                                 safety_stock_override: Optional[float] = None) -> Dict[str, Any]:
        """
        Evaluates quarter-by-quarter inventory balance, shortage, and surplus for a specific item.
        """
        demand_mean = float(np.mean(forecast_demands))
        if safety_stock_override is not None:
            ss = float(safety_stock_override)
        else:
            ss = self.calculate_safety_stock(demand_mean, demand_std, lead_time_days, lead_time_std_days)

        quarterly_evaluations = []
        curr_inventory = float(initial_inventory)
        total_shortage = 0.0
        total_surplus = 0.0
        total_demand = 0.0

        for period, d_val in zip(forecast_periods, forecast_demands):
            d_val = float(d_val)
            total_demand += d_val

            # Available Supply = inventory carried over + planned production in period
            avail_supply = curr_inventory + planned_production_per_quarter
            gross_demand = d_val + ss

            shortage = max(0.0, gross_demand - avail_supply)
            surplus = max(0.0, avail_supply - gross_demand)
            fill_rate = max(0.0, min(1.0, 1.0 - (shortage / max(d_val, 1e-4))))

            # Ending physical stock (after serving actual demand d_val)
            ending_inventory = max(0.0, avail_supply - d_val)

            # Financial implications
            shortage_cost_k = round(shortage * unit_cost_k * 5.0, 2)  # 5x penalty
            surplus_capital_k = round(surplus * unit_cost_k, 2)

            risk_level = "CRITICAL" if fill_rate < 0.75 else ("ELEVATED" if fill_rate < 0.95 else "NOMINAL")

            quarterly_evaluations.append({
                "period": period,
                "forecast_demand": round(d_val, 1),
                "safety_stock": round(ss, 1),
                "gross_demand": round(gross_demand, 1),
                "starting_inventory": round(curr_inventory, 1),
                "planned_production": round(planned_production_per_quarter, 1),
                "available_supply": round(avail_supply, 1),
                "shortage_units": round(shortage, 1),
                "surplus_units": round(surplus, 1),
                "ending_inventory": round(ending_inventory, 1),
                "fill_rate_pct": round(fill_rate * 100.0, 2),
                "estimated_shortage_penalty_k": shortage_cost_k,
                "surplus_capital_tied_k": surplus_capital_k,
                "shortage_risk": risk_level
            })

            total_shortage += shortage
            total_surplus += surplus
            # Carry ending inventory forward
            curr_inventory = ending_inventory

        aggregate_fill_rate = max(0.0, min(1.0, 1.0 - (total_shortage / max(total_demand, 1e-4))))

        return {
            "series_name": series_name,
            "unit_cost_k": unit_cost_k,
            "safety_stock_recommended": ss,
            "total_forecast_demand_4q": round(total_demand, 1),
            "total_shortage_units_4q": round(total_shortage, 1),
            "total_surplus_units_4q": round(total_surplus, 1),
            "aggregate_fill_rate_pct": round(aggregate_fill_rate * 100.0, 2),
            "total_potential_shortage_penalty_k": round(total_shortage * unit_cost_k * 5.0, 2),
            "max_surplus_capital_tied_k": round(max(q["surplus_capital_tied_k"] for q in quarterly_evaluations), 2),
            "quarterly_evaluations": quarterly_evaluations
        }

    def evaluate_all_items(self,
                           forecast_df: pd.DataFrame,
                           item_parameters: Dict[str, Dict[str, Any]],
                           demand_column: str = "forecast",
                           capacity_multiplier: float = 1.0) -> List[Dict[str, Any]]:
        """
        Runs shortage and surplus evaluation for all items present in forecast_df.
        """
        results = []
        for item_name, params in item_parameters.items():
            sub = forecast_df[forecast_df["series_name"] == item_name].sort_values("period")
            if sub.empty:
                continue

            periods = sub["period"].tolist()
            demands = sub[demand_column].tolist()
            init_stock = params.get("default_initial_stock", 50.0)
            prod_cap = params.get("default_mfg_capacity_per_quarter", params.get("default_production_capacity", 40.0)) * capacity_multiplier
            unit_cost = params.get("unit_procurement_cost_k", 500.0)
            d_std = params.get("historical_quarterly_demand_std", params.get("historical_quarterly_std", 25.0))
            lead_time = params.get("avg_lead_time_days", 250.0)
            lead_time_std = params.get("lead_time_std_days", 15.0)

            eval_res = self.evaluate_series_shortages(
                series_name=item_name,
                forecast_periods=periods,
                forecast_demands=demands,
                initial_inventory=init_stock,
                planned_production_per_quarter=prod_cap,
                unit_cost_k=unit_cost,
                demand_std=d_std,
                lead_time_days=lead_time,
                lead_time_std_days=lead_time_std
            )
            eval_res["domain"] = sub["domain"].iloc[0]
            results.append(eval_res)

        return results
