# Orbitalytics Phase 1: Canonical Data Model & Star Schema Architecture

## 1. Overview
Phase 1 establishes a canonical relational data model designed for seamless distributed processing in the Hadoop ecosystem. The logical model defines:
- **Reference Dimensions:** Master entities for agencies, components, resources, and time.
- **Transactional Entities:** Mission manifests, satellite telemetry records, and launch logs.
- **Analytical Fact Tables:** Discrete component demand observations, resource consumption metrics, and agency expenditures.

---

## 2. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    DIM_AGENCIES ||--o{ SPACE_MISSIONS : "operates"
    DIM_AGENCIES ||--o{ SATELLITES_ORBITAL : "operates"
    DIM_AGENCIES ||--o{ EQUIPMENT_COMPONENT_DEMAND : "demands"
    DIM_AGENCIES ||--o{ AGENCY_RESEARCH_EXPENDITURES : "expends"
    DIM_AGENCIES ||--o{ SATELLITE_MANUFACTURING : "commissions"
    DIM_AGENCIES ||--o{ SPACE_INFRASTRUCTURE : "manages"
    DIM_AGENCIES ||--o{ FUTURE_PROJECTS : "sponsors"

    DIM_COMPONENTS ||--o{ EQUIPMENT_COMPONENT_DEMAND : "procured_in"
    DIM_RESOURCES ||--o{ RESOURCE_CONSUMPTION : "consumed_in"

    SPACE_MISSIONS ||--o{ SATELLITES_ORBITAL : "deploys"
    SPACE_MISSIONS ||--o{ LAUNCH_ACTIVITIES : "launched_via"
    SPACE_MISSIONS ||--o{ RESOURCE_CONSUMPTION : "consumes"

    DIM_AGENCIES {
        string agency_id PK
        string agency_name
        string agency_code
        string country
        string agency_type
    }

    DIM_COMPONENTS {
        string component_id PK
        string component_name
        string component_category
        string subsystem
        int typical_lead_time_days
    }

    DIM_RESOURCES {
        string resource_id PK
        string resource_name
        string resource_category
        string unit_of_measure
        float base_cost_usd_per_unit
    }

    SPACE_MISSIONS {
        string mission_id PK
        string agency_id FK
        string mission_type
        date launch_date
        float budget_million_usd
        float payload_mass_kg
        string status
    }

    EQUIPMENT_COMPONENT_DEMAND {
        string demand_id PK
        date date
        string component_id FK
        string agency_id FK
        int units_demanded
        int units_manufactured
        int units_procured
        float total_demand_value_million_usd
        int lead_time_days
        string shortage_risk
    }

    RESOURCE_CONSUMPTION {
        string consumption_id PK
        date date
        string resource_id FK
        string agency_id FK
        string mission_id FK
        float quantity_consumed
        float procurement_cost_k_usd
    }

    LAUNCH_ACTIVITIES {
        string launch_id PK
        string mission_id FK
        date launch_date
        string vehicle
        string launch_site
        string launch_outcome
        float launch_cost_million_usd
    }
```

---

## 3. Logical Star-Schema Proposal for Apache Hive Data Warehousing
To prepare for distributed analytical queries (Apache Hive and PySpark SQL in subsequent phases), the relational model maps directly into a star-schema data warehouse:

### Dimension Tables:
1. **`dim_agencies`:** `agency_id` (PK), `agency_name`, `agency_code`, `country`, `agency_type`.
2. **`dim_components`:** `component_id` (PK), `component_name`, `component_category`, `subsystem`, `criticality_tier`.
3. **`dim_resources`:** `resource_id` (PK), `resource_name`, `resource_category`, `unit_of_measure`.
4. **`dim_time`:** `date` (PK), `year`, `quarter`, `month`, `month_name`, `day_of_year`, `is_weekend`.
5. **`dim_orbits`:** `orbit_code` (PK), `orbit_name`, `altitude_regime`, `typical_mission_types`.

### Fact Tables:
1. **`fact_equipment_demand`:**
   - Keys: `demand_id` (PK), `date` (FK), `component_id` (FK), `agency_id` (FK)
   - Metrics: `units_demanded`, `units_manufactured`, `units_procured`, `avg_unit_cost_thousand_usd`, `total_demand_value_million_usd`, `lead_time_days`.
   - Partitioning Strategy: Partitioned by `year` and `component_category`.
2. **`fact_resource_consumption`:**
   - Keys: `consumption_id` (PK), `date` (FK), `resource_id` (FK), `agency_id` (FK), `mission_id` (FK)
   - Metrics: `quantity_consumed`, `procurement_cost_k_usd`.
   - Partitioning Strategy: Partitioned by `year` and `resource_category`.
3. **`fact_space_missions`:**
   - Keys: `mission_id` (PK), `agency_id` (FK), `launch_date` (FK)
   - Metrics: `budget_million_usd`, `payload_mass_kg`, `duration_days`, `crew_size`.
   - Partitioning Strategy: Partitioned by `agency` and `year`.

