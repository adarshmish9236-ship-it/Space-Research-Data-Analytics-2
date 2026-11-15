"""
Orbitalytics 2.0 - Space Research Digital Twin & Scenario Studio
Implements:
1. Multi-Dimensional Deterministic Scenarios (Baseline, Optimistic, Conservative, Custom)
2. Probabilistic Monte Carlo Simulation (P05 through P95 distributions and capacity breach risk)
3. Tornado Parameter Sensitivity Analysis ranking system drivers
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings

class ScenarioService:
    def __init__(self):
        pass

    def run_scenario_comparison(
        self,
        budget_growth_pct: float = 0.0,
        launch_cadence_change_pct: float = 0.0,
        satellite_deployment_change_pct: float = 0.0,
        equipment_price_inflation_pct: float = 3.0,
        supplier_capacity_change_pct: float = 0.0
    ) -> Dict[str, Any]:
        """
        Simulates deterministic scenario impacts across system metrics.
        Contrasts Baseline vs Optimistic vs Conservative vs Custom user parameters.
        """
        base_budget_b = 24.5
        base_launches = 186
        base_sats = 1420
        base_eq_units = 8400
        base_eq_cost_m = 124.0
        base_capacity_units = 7800

        def calculate_scenario(name: str, s_type: str, b_growth: float, l_change: float, sat_change: float, infl: float, cap_change: float):
            sim_budget = round(base_budget_b * (1.0 + b_growth / 100.0), 2)
            sim_launches = int(round(base_launches * (1.0 + l_change / 100.0)))
            sim_sats = int(round(base_sats * (1.0 + sat_change / 100.0)))
            
            # Demand elasticity
            eq_elasticity = (l_change * 0.40) + (sat_change * 0.50)
            sim_eq_units = round(base_eq_units * (1.0 + eq_elasticity / 100.0), 0)
            
            sim_cost_m = round(base_eq_cost_m * (sim_eq_units / base_eq_units) * (1.0 + infl / 100.0), 2)
            sim_capacity = round(base_capacity_units * (1.0 + cap_change / 100.0), 0)
            
            shortage = max(0.0, sim_eq_units - sim_capacity)
            funding_gap_m = max(0.0, (sim_cost_m - (sim_budget * 1000.0 * 0.005)))  # Assumed equipment share
            
            stress_index = min(100.0, round(((shortage / sim_eq_units) * 60.0) + (infl * 1.5) + (abs(l_change) * 0.2), 1))

            return {
                "scenario_name": name,
                "scenario_type": s_type,
                "simulated_annual_budget_billion_usd": sim_budget,
                "simulated_launch_count": sim_launches,
                "simulated_satellite_deployments": sim_sats,
                "simulated_total_equipment_units": sim_eq_units,
                "simulated_total_equipment_cost_million_usd": sim_cost_m,
                "simulated_supply_shortage_units": shortage,
                "estimated_funding_gap_million_usd": round(funding_gap_m, 2),
                "system_stress_index": stress_index
            }

        baseline = calculate_scenario("Baseline Reality", "BASELINE", 0.0, 0.0, 0.0, 3.0, 0.0)
        optimistic = calculate_scenario("Accelerated Exploration Expansion", "OPTIMISTIC", 20.0, 25.0, 35.0, 2.0, 15.0)
        conservative = calculate_scenario("Constrained Fiscal Retraction", "CONSERVATIVE", -15.0, -12.0, -20.0, 6.0, -10.0)
        
        custom = calculate_scenario(
            "User Custom Simulation",
            "CUSTOM",
            budget_growth_pct,
            launch_cadence_change_pct,
            satellite_deployment_change_pct,
            equipment_price_inflation_pct,
            supplier_capacity_change_pct
        )

        return {
            "baseline": baseline,
            "optimistic": optimistic,
            "conservative": conservative,
            "custom": custom,
            "comparison_summary": (
                f"Under the custom scenario, simulated equipment demand reaches {custom['simulated_total_equipment_units']} units "
                f"resulting in a projected shortage of {custom['simulated_supply_shortage_units']} units. "
                f"The system stress index evaluates to {custom['system_stress_index']}/100."
            )
        }

    def run_monte_carlo(self, target: str = "equipment_demand", iterations: int = 500, volatility_pct: float = 15.0, seed: int = 42) -> Dict[str, Any]:
        """
        Runs probabilistic Monte Carlo simulation using log-normal perturbations.
        Returns histogram distributions, P05 through P95 percentiles, and capacity breach risk.
        """
        np.random.seed(seed)
        base_demand = 8400.0
        supplier_capacity_limit = 9200.0

        sigma = volatility_pct / 100.0
        # Draw from lognormal distribution centered at base_demand
        mu = np.log(base_demand) - 0.5 * (sigma ** 2)
        draws = np.random.lognormal(mean=mu, sigma=sigma, size=iterations)

        p05 = float(np.percentile(draws, 5))
        p10 = float(np.percentile(draws, 10))
        p25 = float(np.percentile(draws, 25))
        p50 = float(np.percentile(draws, 50))
        p75 = float(np.percentile(draws, 75))
        p90 = float(np.percentile(draws, 90))
        p95 = float(np.percentile(draws, 95))
        mean_val = float(np.mean(draws))
        std_val = float(np.std(draws))

        # Breach percentage
        breach_count = int(np.sum(draws > supplier_capacity_limit))
        breach_pct = round((breach_count / iterations) * 100.0, 1)

        # Build histogram
        counts, bin_edges = np.histogram(draws, bins=12)
        histogram = []
        for i in range(len(counts)):
            histogram.append({
                "bin_range": f"{int(bin_edges[i])} - {int(bin_edges[i+1])}",
                "bin_midpoint": round(float((bin_edges[i] + bin_edges[i+1]) / 2.0), 0),
                "frequency": int(counts[i])
            })

        return {
            "target": target,
            "iterations": iterations,
            "volatility_pct": volatility_pct,
            "seed": seed,
            "supplier_capacity_threshold": supplier_capacity_limit,
            "risk_of_exceeding_capacity_pct": breach_pct,
            "percentiles": {
                "p05": round(p05, 1),
                "p10": round(p10, 1),
                "p25": round(p25, 1),
                "p50_median": round(p50, 1),
                "p75": round(p75, 1),
                "p90": round(p90, 1),
                "p95": round(p95, 1),
                "mean": round(mean_val, 1),
                "std_dev": round(std_val, 1)
            },
            "distribution_histogram": histogram,
            "interpretation": (
                f"Across {iterations} stochastic Monte Carlo realizations, median projected demand is {round(p50, 0)} units. "
                f"There is a {breach_pct}% probability that demand will exceed supplier manufacturing capacity ({int(supplier_capacity_limit)} units), "
                f"warranting strategic reserve capacity or multi-source supplier agreements."
            )
        }

    def run_sensitivity_analysis(self) -> Dict[str, Any]:
        """
        Computes Tornado factor sensitivity analysis ranking variables by net impact on equipment spend.
        """
        base_spend_m = 124.0

        factors = [
            {"parameter": "Launch Cadence Volatility (+/- 25%)", "low_m": 105.4, "high_m": 142.6},
            {"parameter": "Component Price Inflation (+/- 15%)", "low_m": 111.6, "high_m": 136.4},
            {"parameter": "Satellite Deployment Scale (+/- 20%)", "low_m": 114.1, "high_m": 133.9},
            {"parameter": "Supplier Capacity Deficit (+/- 30%)", "low_m": 116.5, "high_m": 131.5},
            {"parameter": "Lead Time Expediting Surcharge (+/- 45d)", "low_m": 119.0, "high_m": 129.0}
        ]

        scored_factors = []
        for f in factors:
            swing = round(f["high_m"] - f["low_m"], 2)
            rel_score = round((swing / base_spend_m) * 100.0, 1)
            scored_factors.append({
                "parameter": f["parameter"],
                "low_impact_value_million_usd": f["low_m"],
                "high_impact_value_million_usd": f["high_m"],
                "swing_million_usd": swing,
                "relative_sensitivity_score": rel_score
            })

        scored_factors.sort(key=lambda x: x["swing_million_usd"], reverse=True)

        return {
            "target_metric": "Annual Spacecraft Equipment Expenditure",
            "base_value_million_usd": base_spend_m,
            "top_driver": scored_factors[0]["parameter"],
            "factors": scored_factors,
            "tornado_summary": (
                f"Tornado ranking identifies '{scored_factors[0]['parameter']}' as the primary sensitivity driver, "
                f"inducing a ${scored_factors[0]['swing_million_usd']}M swing ({scored_factors[0]['relative_sensitivity_score']}%) in annual system capital requirements."
            )
        }

# Global Singleton
scenario_service = ScenarioService()
