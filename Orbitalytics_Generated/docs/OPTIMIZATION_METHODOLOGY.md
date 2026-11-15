# ORBITALYTICS 2.0 — DEMAND-TO-CAPACITY OPTIMIZATION METHODOLOGY

## 1. Problem Formulation & Mission Objectives

Forecasting predicts future demand ($D_i$), but space research organizations require prescriptive intelligence: how to allocate constrained budgets ($B$), manage supplier manufacturing capacities ($C_i$), and safeguard mission readiness against critical component shortages ($S_i$).

---

## 2. Mathematical Optimization Models

### 2.1 Constrained Linear Procurement Allocation (SciPy HiGHS Solver)

Let $x_i$ be the number of units procured for aerospace component $i \in \{1, \dots, n\}$.

#### Objective Function
Minimize total procurement cost plus weighted shortage penalties:

$$\min_{x} \sum_{i=1}^{n} c_i x_i + \sum_{i=1}^{n} w_i \cdot p_i \cdot (D_i - x_i)$$

Where:
- $c_i$: Unit procurement cost of component $i$.
- $D_i$: Forecasted demand for component $i$.
- $w_i$: Mission criticality weight ($w_i \in [1.0, 5.0]$).
- $p_i$: Penalty cost per unmet unit.
- $x_i$: Allocated procurement quantity.

#### Constraints
1. **Total Budget Ceiling:**
   $$\sum_{i=1}^{n} c_i x_i \le B_{total}$$
2. **Supplier Capacity Ceilings:**
   $$0 \le x_i \le \min(D_i, C_i), \quad \forall i$$

Solved via the **HiGHS Dual Simplex Simplex / Interior-Point Solver** in `scipy.optimize.linprog`.

---

### 2.2 Statistical Inventory Planning & Safety Stock

To guard against stochastic lead-time demand volatility:

- **Lead-Time Demand ($LTD$):**
  $$LTD = \bar{d} \times L$$
  where $\bar{d}$ is the average daily demand, and $L$ is lead time in days.
- **Safety Stock ($SS$):**
  $$SS = Z \times \sqrt{L \times \sigma_d^2}$$
  where $Z = 1.645$ for a 95% service level guarantee, and $\sigma_d$ is daily demand standard deviation.
- **Reorder Point ($ROP$):**
  $$ROP = LTD + SS = \bar{d} \times L + Z \times \sigma_L$$

---

### 2.3 Strategic Research Capital Allocation

Redistributes multi-billion dollar research portfolios across core space domains:
1. Earth Observation & Climate Telemetry
2. Lunar & Deep Space Exploration (Artemis / Robotic)
3. Satellite Internet & Constellations
4. Reusable Launch Vehicle Development
5. Space Situational Awareness & Debris Removal

