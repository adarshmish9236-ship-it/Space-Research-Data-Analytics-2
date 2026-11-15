# Dataset Profile: equipment_component_demand
- **Total Rows:** 11312
- **Total Columns:** 20
- **Memory Usage:** 3725.68 KB

## Column Summary
| Column | Type | Null Count (%) | Unique Values | Details |
| :--- | :--- | :--- | :--- | :--- |
| `demand_id` | `str` | 0 (0.0%) | 11312 | DEM-2010-00001 (1), DEM-2010-00002 (1), DEM-2010-00003 (1) |
| `date` | `str` | 0 (0.0%) | 202 | 2010-01-01 to 2026-10-01 (6117d) |
| `year` | `int64` | 0 (0.0%) | 17 | Min: 2010.0, Max: 2026.0, Mean: 2017.921 |
| `month` | `int64` | 0 (0.0%) | 12 | Min: 1.0, Max: 12.0, Mean: 6.45 |
| `quarter` | `str` | 0 (0.0%) | 4 | Q1 (2856), Q2 (2856), Q3 (2856) |
| `component_id` | `str` | 0 (0.0%) | 8 | CMP-001 (1414), CMP-002 (1414), CMP-003 (1414) |
| `component_name` | `str` | 0 (0.0%) | 8 | High-Efficiency Multi-Junction Solar Panels (1414), Radiation-Hardened Rad-750 Single Board Computers (1414), Hall-Effect Ion Propulsion Thrusters (1414) |
| `component_category` | `str` | 0 (0.0%) | 7 | Propulsion (2828), Power Systems (1414), Avionics (1414) |
| `agency_id` | `str` | 0 (0.0%) | 7 | AGY-001 (1616), AGY-002 (1616), AGY-003 (1616) |
| `agency_name` | `str` | 0 (0.0%) | 7 | National Aeronautics and Space Administration (1616), European Space Agency (1616), Indian Space Research Organisation (1616) |
| `target_satellite_class` | `str` | 0 (0.0%) | 4 | Heavy Geosynchronous Bus (>2000kg) (2897), Medium Satellite (500-2000kg) (2852), CubeSat (1U-12U) (2790) |
| `units_demanded` | `int64` | 0 (0.0%) | 104 | Min: 2.0, Max: 105.0, Mean: 50.469 |
| `units_manufactured` | `int64` | 0 (0.0%) | 115 | Min: 2.0, Max: 117.0, Mean: 47.875 |
| `units_procured` | `int64` | 0 (0.0%) | 120 | Min: 2.0, Max: 121.0, Mean: 50.539 |
| `unit_of_measure` | `str` | 0 (0.0%) | 1 | Units (11312) |
| `avg_unit_cost_thousand_usd` | `float64` | 0 (0.0%) | 6188 | Min: 85.2, Max: 920.0, Mean: 501.858 |
| `total_demand_value_million_usd` | `float64` | 0 (0.0%) | 10134 | Min: 0.398, Max: 93.014, Mean: 25.286 |
| `lead_time_days` | `int64` | 0 (0.0%) | 360 | Min: 127.0, Max: 486.0, Mean: 275.16 |
| `shortage_risk` | `str` | 0 (0.0%) | 4 | Low (5615), Medium (4365), High (1327) |
| `data_origin` | `str` | 0 (0.0%) | 1 | synthetic (11312) |
