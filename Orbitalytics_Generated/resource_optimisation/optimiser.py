"""
ORBITALYTICS Phase 9 — Mathematical Resource Optimisation Engine
Implements Linear Programming (LP) and Mixed-Integer Linear Programming (MILP)
using scipy.optimize (HiGHS branch-and-cut and simplex solvers).

Objectives:
  1. Joint Procurement & Production Cost Minimization:
     min sum_{t} sum_{i} [ c_i^proc * x_{i,t} + c_i^mfg * p_{i,t} + h_i * I_{i,t} + pi_i * s_{i,t} ]
  2. Priority-Weighted Mission Resource Allocation:
     max sum_{t} sum_{i} sum_{m} w_m * a_{i,m,t} - penalty * u_{i,m,t}

Constraints:
  - Inventory balance: I_{i,t-1} + p_{i,t} + x_{i,t} + s_{i,t} - I_{i,t} = Demand_{i,t}
  - Quarterly budget: sum_i [ c_i^proc * x_{i,t} + c_i^mfg * p_{i,t} ] <= Budget_t
  - Total cleanroom manufacturing capacity: sum_i p_{i,t} <= CleanroomCap_t
  - Component tooling capacity: p_{i,t} <= ToolingCap_{i,t}
  - Supplier procurement delivery limits: x_{i,t} <= SupplierCap_{i,t}
  - Non-negativity and integer constraints: x_{i,t}, p_{i,t} in Z_+
"""

import time
import math
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from scipy.optimize import milp, linprog, LinearConstraint, Bounds


class ResourceOptimiser:
    """Mathematical optimization solver for aerospace resource planning."""

    def __init__(self):
        pass

    def solve_multi_period_procurement_milp(self,
                                            item_names: List[str],
                                            periods: List[str],
                                            demands_matrix: np.ndarray,      # shape (M, T)
                                            initial_inventory: np.ndarray,   # shape (M,)
                                            procurement_costs: np.ndarray,   # shape (M,)
                                            manufacturing_costs: np.ndarray, # shape (M,)
                                            holding_costs: np.ndarray,       # shape (M,)
                                            shortage_penalties: np.ndarray,  # shape (M,)
                                            quarterly_budgets: np.ndarray,   # shape (T,)
                                            cleanroom_capacity_per_quarter: float,
                                            tooling_caps: np.ndarray,        # shape (M,)
                                            supplier_caps: np.ndarray,       # shape (M,)
                                            is_integer: bool = True) -> Dict[str, Any]:
        """
        Solves multi-item multi-period joint procurement and manufacturing optimization.
        Decision variables per (item i, period t):
          - x[i, t]: Procurement quantity
          - p[i, t]: Internal manufacturing quantity
          - I[i, t]: Ending inventory
          - s[i, t]: Shortage (unmet demand)
        Total variables = 4 * M * T.
        """
        t0 = time.time()
        M = len(item_names)
        T = len(periods)
        n_vars = 4 * M * T

        # Helper indexing:
        # idx_x(i, t) = 0 * M*T + i*T + t
        # idx_p(i, t) = 1 * M*T + i*T + t
        # idx_I(i, t) = 2 * M*T + i*T + t
        # idx_s(i, t) = 3 * M*T + i*T + t
        def idx_x(i, t): return i * T + t
        def idx_p(i, t): return M * T + i * T + t
        def idx_I(i, t): return 2 * M * T + i * T + t
        def idx_s(i, t): return 3 * M * T + i * T + t

        # 1. Objective function coefficients (to minimize c^T * v)
        c = np.zeros(n_vars, dtype=float)
        for i in range(M):
            for t in range(T):
                c[idx_x(i, t)] = procurement_costs[i]
                c[idx_p(i, t)] = manufacturing_costs[i]
                c[idx_I(i, t)] = holding_costs[i]
                c[idx_s(i, t)] = shortage_penalties[i]

        # 2. Variable bounds and integrality
        lb = np.zeros(n_vars, dtype=float)
        ub = np.full(n_vars, np.inf, dtype=float)
        integrality = np.zeros(n_vars, dtype=int)

        for i in range(M):
            for t in range(T):
                ub[idx_x(i, t)] = supplier_caps[i]
                ub[idx_p(i, t)] = tooling_caps[i]
                if is_integer:
                    integrality[idx_x(i, t)] = 1  # integer
                    integrality[idx_p(i, t)] = 1  # integer
                    integrality[idx_I(i, t)] = 0  # inventory can be continuous/integer
                    integrality[idx_s(i, t)] = 0

        # 3. Constraints Construction
        # A) Inventory Balance Constraints: M * T equations
        # For t = 0: p[i,0] + x[i,0] + s[i,0] - I[i,0] = Demand[i,0] - I_init[i]
        # For t > 0: I[i,t-1] + p[i,t] + x[i,t] + s[i,t] - I[i,t] = Demand[i,t]
        n_balance_constrs = M * T
        # B) Budget Constraints: T inequalities
        # sum_i ( c_i^proc * x[i,t] + c_i^mfg * p[i,t] ) <= Budget[t]
        n_budget_constrs = T
        # C) Cleanroom Capacity Constraints: T inequalities
        # sum_i p[i,t] <= CleanroomCapacity
        n_capacity_constrs = T

        total_constrs = n_balance_constrs + n_budget_constrs + n_capacity_constrs
        A = np.zeros((total_constrs, n_vars), dtype=float)
        lhs = np.zeros(total_constrs, dtype=float)
        rhs = np.zeros(total_constrs, dtype=float)

        row_idx = 0
        # A) Inventory Balance Rows (Equality constraints)
        for i in range(M):
            for t in range(T):
                A[row_idx, idx_p(i, t)] = 1.0
                A[row_idx, idx_x(i, t)] = 1.0
                A[row_idx, idx_s(i, t)] = 1.0
                A[row_idx, idx_I(i, t)] = -1.0

                if t == 0:
                    req = demands_matrix[i, 0] - initial_inventory[i]
                else:
                    A[row_idx, idx_I(i, t - 1)] = 1.0
                    req = demands_matrix[i, t]

                lhs[row_idx] = req
                rhs[row_idx] = req
                row_idx += 1

        # B) Budget Rows (Inequality: 0 <= expr <= Budget[t])
        budget_row_start = row_idx
        for t in range(T):
            for i in range(M):
                A[row_idx, idx_x(i, t)] = procurement_costs[i]
                A[row_idx, idx_p(i, t)] = manufacturing_costs[i]
            lhs[row_idx] = -np.inf
            rhs[row_idx] = quarterly_budgets[t]
            row_idx += 1

        # C) Cleanroom Capacity Rows (Inequality: 0 <= sum_i p[i,t] <= Cap)
        capacity_row_start = row_idx
        for t in range(T):
            for i in range(M):
                A[row_idx, idx_p(i, t)] = 1.0
            lhs[row_idx] = -np.inf
            rhs[row_idx] = cleanroom_capacity_per_quarter
            row_idx += 1

        # 4. Invoke SciPy MILP Solver
        constraints = LinearConstraint(A, lhs, rhs)
        bounds = Bounds(lb, ub)

        res = milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints)
        solve_time = round(time.time() - t0, 3)

        if not res.success:
            return {
                "status": "INFEASIBLE_OR_FAILED",
                "solver_message": res.message,
                "solve_time_seconds": solve_time,
                "is_optimal": False
            }

        x_sol = res.x
        total_procurement_cost_k = 0.0
        total_manufacturing_cost_k = 0.0
        total_holding_cost_k = 0.0
        total_shortage_cost_k = 0.0
        total_demand_volume = float(np.sum(demands_matrix))
        total_shortage_units = 0.0

        item_solutions = []
        for i in range(M):
            item_record = {
                "item_name": item_names[i],
                "initial_stock": round(float(initial_inventory[i]), 1),
                "quarterly_plans": []
            }
            item_tot_shortage = 0.0
            for t in range(T):
                x_val = round(float(x_sol[idx_x(i, t)]), 1)
                p_val = round(float(x_sol[idx_p(i, t)]), 1)
                I_val = round(float(x_sol[idx_I(i, t)]), 1)
                s_val = round(float(x_sol[idx_s(i, t)]), 1)
                d_val = round(float(demands_matrix[i, t]), 1)

                total_procurement_cost_k += x_val * procurement_costs[i]
                total_manufacturing_cost_k += p_val * manufacturing_costs[i]
                total_holding_cost_k += I_val * holding_costs[i]
                total_shortage_cost_k += s_val * shortage_penalties[i]
                total_shortage_units += s_val
                item_tot_shortage += s_val

                item_record["quarterly_plans"].append({
                    "period": periods[t],
                    "forecast_demand": d_val,
                    "procurement_order_units": x_val,
                    "internal_manufacturing_units": p_val,
                    "ending_inventory_units": I_val,
                    "shortage_units": s_val,
                    "fill_rate_pct": round(max(0.0, 1.0 - (s_val / max(d_val, 1e-4))) * 100.0, 2)
                })
            item_record["total_shortage_units_4q"] = round(item_tot_shortage, 1)
            item_solutions.append(item_record)

        # Constraint utilization
        budget_utilization = []
        for t in range(T):
            spent = float(np.dot(A[budget_row_start + t], x_sol))
            cap = quarterly_budgets[t]
            budget_utilization.append({
                "period": periods[t],
                "budget_allocated_k": round(cap, 2),
                "budget_spent_k": round(spent, 2),
                "utilization_pct": round((spent / max(cap, 1e-4)) * 100.0, 2)
            })

        capacity_utilization = []
        for t in range(T):
            used = float(np.dot(A[capacity_row_start + t], x_sol))
            cap = cleanroom_capacity_per_quarter
            capacity_utilization.append({
                "period": periods[t],
                "cleanroom_capacity_units": round(cap, 1),
                "cleanroom_units_used": round(used, 1),
                "utilization_pct": round((used / max(cap, 1e-4)) * 100.0, 2)
            })

        overall_fill_rate = max(0.0, 1.0 - (total_shortage_units / max(total_demand_volume, 1e-4)))

        return {
            "status": "OPTIMAL",
            "solver": "HiGHS Branch-and-Cut (scipy.optimize.milp)",
            "solve_time_seconds": solve_time,
            "is_optimal": True,
            "objective_value_k": round(float(res.fun), 2),
            "cost_breakdown": {
                "procurement_cost_k": round(total_procurement_cost_k, 2),
                "manufacturing_cost_k": round(total_manufacturing_cost_k, 2),
                "inventory_holding_cost_k": round(total_holding_cost_k, 2),
                "shortage_penalty_cost_k": round(total_shortage_cost_k, 2),
                "total_operational_cost_k": round(total_procurement_cost_k + total_manufacturing_cost_k + total_holding_cost_k, 2)
            },
            "performance_summary": {
                "total_demand_units_4q": round(total_demand_volume, 1),
                "total_shortage_units_4q": round(total_shortage_units, 1),
                "aggregate_fill_rate_pct": round(overall_fill_rate * 100.0, 2)
            },
            "budget_utilization": budget_utilization,
            "capacity_utilization": capacity_utilization,
            "item_solutions": item_solutions
        }

    def solve_mission_priority_allocation(self,
                                          item_names: List[str],
                                          available_supply: np.ndarray,      # shape (M,)
                                          tier_names: List[str],
                                          tier_weights: np.ndarray,          # shape (K,)
                                          demand_by_tier: np.ndarray         # shape (M, K)
                                          ) -> Dict[str, Any]:
        """
        Allocates limited available supply of M items across K mission priority tiers.
        Maximizes priority-weighted fulfillment while minimizing unfulfilled demand.
        Decision variables:
          - a[i, m]: allocation of item i to tier m
          - u[i, m]: unfulfilled demand of item i for tier m
        """
        M = len(item_names)
        K = len(tier_names)
        n_vars = 2 * M * K

        def idx_a(i, m): return i * K + m
        def idx_u(i, m): return M * K + i * K + m

        # Objective: Maximize sum (w_m * a[i,m] - 1.5 * w_m * u[i,m])
        # In linprog (minimize): c = -w_m for a, +1.5 * w_m for u
        c = np.zeros(n_vars, dtype=float)
        for i in range(M):
            for m in range(K):
                c[idx_a(i, m)] = -float(tier_weights[m])
                c[idx_u(i, m)] = float(tier_weights[m]) * 1.5

        # Constraints:
        # 1. Fulfillment balance: a[i,m] + u[i,m] = Demand[i,m] (M*K rows)
        # 2. Supply capacity: sum_m a[i,m] <= Supply[i] (M rows)
        n_constrs = M * K + M
        A_eq = np.zeros((M * K, n_vars), dtype=float)
        b_eq = np.zeros(M * K, dtype=float)
        for i in range(M):
            for m in range(K):
                row = i * K + m
                A_eq[row, idx_a(i, m)] = 1.0
                A_eq[row, idx_u(i, m)] = 1.0
                b_eq[row] = demand_by_tier[i, m]

        A_ub = np.zeros((M, n_vars), dtype=float)
        b_ub = np.zeros(M, dtype=float)
        for i in range(M):
            for m in range(K):
                A_ub[i, idx_a(i, m)] = 1.0
            b_ub[i] = available_supply[i]

        bounds = [(0, None) for _ in range(n_vars)]
        res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

        if not res.success:
            return {"status": "FAILED", "is_optimal": False, "message": res.message}

        alloc_matrix = np.zeros((M, K), dtype=float)
        unmet_matrix = np.zeros((M, K), dtype=float)
        for i in range(M):
            for m in range(K):
                alloc_matrix[i, m] = round(float(res.x[idx_a(i, m)]), 1)
                unmet_matrix[i, m] = round(float(res.x[idx_u(i, m)]), 1)

        tier_summary = []
        for m in range(K):
            tot_dem = float(np.sum(demand_by_tier[:, m]))
            tot_alloc = float(np.sum(alloc_matrix[:, m]))
            tot_unmet = float(np.sum(unmet_matrix[:, m]))
            fill_pct = round((tot_alloc / max(tot_dem, 1e-4)) * 100.0, 2)
            tier_summary.append({
                "tier_name": tier_names[m],
                "priority_weight": float(tier_weights[m]),
                "total_demand_units": round(tot_dem, 1),
                "allocated_units": round(tot_alloc, 1),
                "unmet_units": round(tot_unmet, 1),
                "tier_fulfillment_rate_pct": fill_pct
            })

        return {
            "status": "OPTIMAL",
            "solver": "HiGHS Simplex (scipy.optimize.linprog)",
            "is_optimal": True,
            "tier_allocations_summary": tier_summary,
            "item_allocations": [
                {
                    "item_name": item_names[i],
                    "available_supply": round(float(available_supply[i]), 1),
                    "allocations_by_tier": {
                        tier_names[m]: {
                            "demand": round(float(demand_by_tier[i, m]), 1),
                            "allocated": round(float(alloc_matrix[i, m]), 1),
                            "unmet": round(float(unmet_matrix[i, m]), 1)
                        }
                        for m in range(K)
                    }
                }
                for i in range(M)
            ]
        }
