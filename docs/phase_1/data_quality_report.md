# Orbitalytics Phase 1: Data Quality & Validation Report

## 1. Quality Framework Overview
The Phase 1 Data Quality Engine evaluates datasets across five core dimensions:
1. **Completeness:** Verifies zero null or empty cells across all mandatory columns defined in `SchemaRegistry`.
2. **Uniqueness:** Guarantees zero duplicate primary keys and composite key integrity.
3. **Validity:** Enforces strictly non-negative quantities for all numeric metrics (mass, cost, power, units) and valid ISO-8601 calendar date formats (`YYYY-MM-DD`).
4. **Consistency:** Validates categorical domain members against predefined aerospace taxonomy lists.
5. **Temporal Consistency:** Verifies chronological order and unbroken monthly intervals for all time-series datasets.

---

## 2. Multi-Dimensional Quality Scores by Dataset

| Dataset Name | Input Records | Accepted Records | Rejected Records | Completeness (%) | Uniqueness (%) | Validity (%) | Overall Quality Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `space_missions` | 1,500 | 1,500 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `satellites_orbital` | 2,400 | 2,400 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `launch_activities` | 1,200 | 1,200 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `equipment_component_demand` | 11,312 | 11,312 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `agency_research_expenditures`| 1,414 | 1,414 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `resource_consumption` | 9,898 | 9,898 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `satellite_manufacturing_requirements` | 600 | 600 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `space_infrastructure_requirements` | 1,010 | 1,010 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| `research_investment_future_projects` | 160 | 160 | 0 | 100.0% | 100.0% | 100.0% | **100.0%** |
| **Consolidated Total** | **29,494** | **29,494** | **0** | **100.0%** | **100.0%** | **100.0%** | **100.0%** |

---

## 3. Referential Integrity Cross-Verification
Referential integrity was evaluated across all 8 relational linkages using `RelationshipValidator`:

| Relational Constraint | Parent Table | Child Table | Foreign Key Column | Broken Keys | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| Missions to Agencies | `reference_agencies` | `space_missions` | `agency_id` | 0 | **PASSED** |
| Satellites to Missions | `space_missions` | `satellites_orbital` | `associated_mission_id`| 0 | **PASSED** |
| Satellites to Agencies | `reference_agencies` | `satellites_orbital` | `operator_agency_id` | 0 | **PASSED** |
| Launches to Missions | `space_missions` | `launch_activities` | `mission_id` | 0 | **PASSED** |
| Equipment to Components | `reference_components`| `equipment_component_demand`| `component_id` | 0 | **PASSED** |
| Equipment to Agencies | `reference_agencies` | `equipment_component_demand`| `agency_id` | 0 | **PASSED** |
| Resources to Resource Master | `reference_resources` | `resource_consumption` | `resource_id` | 0 | **PASSED** |
| Resources to Missions | `space_missions` | `resource_consumption` | `mission_id` | 0 | **PASSED** |

**Consolidated Referential Integrity Score: 100.0% (8 / 8 rules passed)**

---

## 4. Rejection & Error Quarantine Policy
Orbitalytics enforces a strict **Zero Silent Data Loss** rule:
- Defective rows (e.g. missing required fields, unparseable dates, negative values, broken foreign keys) are never deleted without a trace.
- Any row failing validation is automatically written to `datasets/rejected/<dataset_name>_rejected.csv`.
- Each quarantined record includes:
  - `record_index`: Line number in the raw source file.
  - `rejection_code`: Standard error classification (e.g. `ERR_MISSING_REQUIRED_FIELD`, `ERR_DUPLICATE_PRIMARY_KEY`, `ERR_INVALID_NUMERIC_RANGE`).
  - `reason`: Specific explanation of the failure.
  - `raw_record`: Stringified snapshot of the original record for auditing.

