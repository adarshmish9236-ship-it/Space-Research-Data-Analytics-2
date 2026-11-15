# Orbitalytics Phase 1: Synthetic Data Generation Methodology

## 1. Rationale & Ethical Scientific Transparency
In aerospace data engineering, public availability of hardware supply chain data is strictly constrained by national security and commercial confidentiality:
- Space agencies (NASA, ESA, ISRO) do not publicly release detailed component-level procurement manifests under **ITAR** (International Traffic in Arms Regulations).
- Commercial space manufacturers (SpaceX, Blue Origin, Rocket Lab) protect bill of materials (BOM) as proprietary industrial secrets.

Rather than inventing or scraping unauthorized data, Orbitalytics implements a **mathematically rigorous, physics-informed, seed-controlled synthetic data generation engine** (`SyntheticDataGenerator`).

---

## 2. Core Methodological Principles

### 1. Deterministic Reproducibility
- Seed control is strictly locked:
  ```python
  SEED = 42
  np.random.seed(SEED)
  random.seed(SEED)
  ```
- Any execution with identical parameters yields bitwise identical datasets across all nodes.

### 2. Explicit Provenance Tagging
- Every generated row includes mandatory metadata:
  - `data_origin = 'synthetic'`
  - `is_synthetic = True`
- Real public records carry `data_origin = 'real'`. No synthetic record is ever presented as real agency telemetry.

### 3. Guaranteed Referential Integrity
- Generated records do not invent floating foreign keys.
- All foreign keys are strictly sampled from valid canonical entities in `datasets/reference/`:
  - `agency_id` $\in$ `reference_agencies.csv` (`AGY-001` through `AGY-007`)
  - `component_id` $\in$ `reference_components.csv` (`CMP-001` through `CMP-008`)
  - `resource_id` $\in$ `reference_resources.csv` (`RES-001` through `RES-007`)
  - `mission_id` $\in$ generated valid mission table (`MSN-YYYY-NNNN`)

---

## 3. Mathematical Time-Series Formulation
For time-series entities (Component Demand, Resource Consumption, Agency Expenditures), values are generated using additive decomposition with non-linear trend, seasonal harmonic oscillation, and Gaussian noise:

$$Y_t = \text{Base} + \text{Trend}(t) + \text{Seasonal}(t) + \epsilon_t$$

Where:
1. **Baseline Level ($\text{Base}$):** Calibrated to component criticality (e.g., higher baseline for Rad-750 flight computers and multi-junction solar panels).
2. **Compound Industrial Expansion Trend ($\text{Trend}(t)$):**
   $$\text{Trend}(t) = \left(t^{1.12}\right) \times 0.22$$
   Reflects the exponential expansion of the global satellite constellation industry from 2010 to 2026.
3. **Harmonic Seasonal Cycle ($\text{Seasonal}(t)$):**
   $$\text{Seasonal}(t) = A \cdot \sin\left(\frac{2\pi t}{12}\right)$$
   Models the operational launch windows and fiscal procurement surges in Q3 and Q4.
4. **Stochastic Volatility ($\epsilon_t$):**
   $$\epsilon_t \sim \mathcal{N}(0, \sigma^2)$$
   Gaussian white noise modeling manufacturing tolerances and unexpected project re-schedules.
5. **Non-Negativity Constraint:**
   $$Y_t = \max(Y_{\min}, \lfloor Y_t \rceil)$$
   Enforces strictly positive physical unit quantities ($Y_t \ge 2$ units).

---

## 4. Configurable Scale Profiles

| Profile Name | Multiplier | Space Missions | Satellites | Launches | Component Demand | Resource Consumption | Total Records | Target Use Case |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Small** | 1.0x | 1,500 | 2,400 | 1,200 | 11,312 | 9,898 | **29,494** | Local development, unit testing, CI/CD pipeline verification. |
| **Medium** | 10.0x | 15,000 | 24,000 | 12,000 | 113,120 | 98,980 | **294,940** | Single-node Spark/Hive analytics, medium-scale machine learning. |
| **Large** | 100.0x | 150,000 | 240,000 | 120,000 | 1,131,200 | 989,800 | **2,949,400** | Distributed multi-node Hadoop cluster benchmarking (HDFS, YARN, Spark). |

To generate any profile via CLI:
```bash
python scripts/data_generation/generate_synthetic_data.py --profile small
python scripts/data_generation/generate_synthetic_data.py --profile medium
python scripts/data_generation/generate_synthetic_data.py --profile large
```

