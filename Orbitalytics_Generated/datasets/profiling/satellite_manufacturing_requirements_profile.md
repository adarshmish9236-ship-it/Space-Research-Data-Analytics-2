# Dataset Profile: satellite_manufacturing_requirements
- **Total Rows:** 600
- **Total Columns:** 11
- **Memory Usage:** 107.11 KB

## Column Summary
| Column | Type | Null Count (%) | Unique Values | Details |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `str` | 0 (0.0%) | 600 | ORD-MFG-2018-1000 (1), ORD-MFG-2019-1001 (1), ORD-MFG-2020-1002 (1) |
| `agency_id` | `str` | 0 (0.0%) | 7 | AGY-006 (98), AGY-003 (98), AGY-002 (90) |
| `agency_client` | `str` | 0 (0.0%) | 7 | State Space Corporation Roscosmos (98), Indian Space Research Organisation (98), European Space Agency (90) |
| `satellite_class` | `str` | 0 (0.0%) | 4 | Heavy Geosynchronous Bus (>2000kg) (159), SmallSat (<500kg) (155), Medium Satellite (500-2000kg) (147) |
| `units_ordered` | `int64` | 0 (0.0%) | 24 | Min: 1.0, Max: 24.0, Mean: 12.475 |
| `delivery_year` | `int64` | 0 (0.0%) | 8 | Min: 2021.0, Max: 2028.0, Mean: 2024.468 |
| `cleanroom_hours_required` | `int64` | 0 (0.0%) | 577 | Min: 430.0, Max: 7478.0, Mean: 3976.768 |
| `vibration_testing_pass` | `bool` | 0 (0.0%) | 2 | Min: 0.0, Max: 1.0, Mean: 0.72 |
| `contract_value_million_usd` | `float64` | 0 (0.0%) | 598 | Min: 6.75, Max: 318.5, Mean: 160.62 |
| `data_origin` | `str` | 0 (0.0%) | 1 | synthetic (600) |
| `country` | `str` | 0 (0.0%) | 6 | United States (152), Russia (98), India (98) |
