# ORBITALYTICS 2.0 — DATA GOVERNANCE & MEDALLION LAKEHOUSE SPECIFICATION

## 1. Governance Architecture

Orbitalytics 2.0 implements a strict **Medallion Data Architecture** across distributed storage layers:

```
[Raw CSV Sources]
       │ (MD5 Checksum Ingestion & Provenance Tagging)
       ▼
[Bronze Lakehouse] ─── /space_research/bronze/
       │ (PySpark Schema Enforcement, Type Casting, Quarantine)
       ▼
[Silver Lakehouse] ─── /space_research/silver/ (Snappy-Compressed Parquet)
       │ (Star-Schema Facts & Dimensional Modeling)
       ▼
[Gold Lakehouse]   ─── /space_research/gold/ (fact_missions, fact_equipment_demand, dim_agencies, dim_orbits)
```

## 2. Dataset Catalog & Schema Registry

| Dataset Identifier | Domain | Layer | Format | Partition Column | Quality Target | Provenance Classification |
|---|---|---|---|---|---|---|
| `space_missions` | Space Missions | Gold Fact | Parquet | `agency` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `satellites_orbital` | Orbital Telemetry | Gold Fact | Parquet | `orbit_type` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `launch_activities` | Launch Operations | Gold Fact | Parquet | `country` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `equipment_component_demand` | Spacecraft Equipment | Gold Fact | Parquet | `equipment_category` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `agency_research_expenditures` | Fiscal R&D Budgets | Gold Fact | Parquet | `agency` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `resource_consumption` | Propellants & Consumables | Gold Fact | Parquet | `resource_type` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `satellite_manufacturing_requirements` | Production Specs | Gold Fact | Parquet | `satellite_category` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `space_infrastructure_requirements` | Launch & Telemetry Facilities | Gold Fact | Parquet | `infrastructure_type` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |
| `research_investment_future_projects` | Future Capital Pipelines | Gold Fact | Parquet | `agency` | > 95% | `SIMULATED_RESEARCH_OBSERVATION_V2` |

## 3. Statistical Data Quality & Anomaly Detection Framework

Data quality is audited across four primary dimensions:
1. **Completeness ($C$):** Percentage of populated non-null attribute cells.
2. **Uniqueness ($U$):** Percentage of unique primary entity keys.
3. **Validity ($V$):** Conformity to domain bounds and statistical anomaly filtering.
4. **Consistency ($K$):** Schema typing integrity and foreign entity referential validity.

$$Quality\ Score = 0.35 C + 0.25 U + 0.25 V + 0.15 K$$

### Dual Anomaly Detection Methods
- **Interquartile Range (IQR):** Identifies observations outside $[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$.
- **Z-Score Normalization:** Identifies observations with standard score $|Z| > 3.0$:
  $$Z = \frac{x - \mu}{\sigma}$$
- Records violating structural bounds are quarantined rather than deleted, preserving full scientific auditability.

