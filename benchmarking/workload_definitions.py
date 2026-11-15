"""
ORBITALYTICS Phase 10 — Workload Definitions
Defines five standardized analytical workloads to compare execution across:
  1. Local Python / Pandas
  2. Hadoop MapReduce (Python Streaming)
  3. Apache Hive (HiveQL on HiveServer2)
  4. Apache Spark / PySpark (SparkSession DataFrame & Spark SQL)
  5. Apache Pig (Pig Latin)

All systems execute identical filtering, identical grouping keys, and produce identical schemas.
"""

from typing import Dict, List, Any

WORKLOADS: Dict[str, Dict[str, Any]] = {
    "WL1_EQUIPMENT_DEMAND": {
        "id": "WL1_EQUIPMENT_DEMAND",
        "name": "Workload 1: Equipment Demand Aggregation by Component",
        "description": "Groups equipment component records by equipment_type, calculating total demanded units, average unit cost, total demand value, and record count.",
        "primary_table": "equipment_component_demand",
        "group_by": ["equipment_type"],
        "aggregations": {
            "total_units_demanded": "SUM(units_demanded)",
            "avg_unit_cost_k": "AVG(avg_unit_cost_thousand_usd)",
            "total_demand_value_m": "SUM(total_demand_value_million_usd)",
            "record_count": "COUNT(*)"
        },
        "order_by": ["equipment_type ASC"],
        "complexity": "Single-table compute-bound aggregation with grouping."
    },
    "WL2_RESOURCE_CONSUMPTION": {
        "id": "WL2_RESOURCE_CONSUMPTION",
        "name": "Workload 2: Resource Consumption Aggregation by Year",
        "description": "Groups consumable space research resources by calendar year, computing total quantity consumed, total procurement cost, average quantity, and record count.",
        "primary_table": "resource_consumption",
        "group_by": ["year"],
        "aggregations": {
            "total_quantity": "SUM(quantity_consumed)",
            "total_cost_k": "SUM(procurement_cost_k_usd)",
            "avg_quantity": "AVG(quantity_consumed)",
            "record_count": "COUNT(*)"
        },
        "order_by": ["year ASC"],
        "complexity": "Temporal time-series aggregation across multi-year horizon."
    },
    "WL3_MISSIONS_BY_AGENCY": {
        "id": "WL3_MISSIONS_BY_AGENCY",
        "name": "Workload 3: Mission Activity by Space Agency",
        "description": "Groups orbital and deep space missions by executing agency, calculating total missions, total budget, average payload mass, and average duration.",
        "primary_table": "space_missions",
        "group_by": ["agency"],
        "aggregations": {
            "total_missions": "COUNT(*)",
            "total_budget_m": "SUM(budget_million_usd)",
            "avg_payload_kg": "AVG(payload_mass_kg)",
            "avg_duration_days": "AVG(duration_days)"
        },
        "order_by": ["total_missions DESC"],
        "complexity": "Categorical dimension aggregation with multiple numeric metrics."
    },
    "WL4_MANUFACTURING_SUMMARY": {
        "id": "WL4_MANUFACTURING_SUMMARY",
        "name": "Workload 4: Supply & Equipment Aggregation by Component and Year",
        "description": "Multi-dimensional grouping across equipment_type and year, computing demand volume and average lead time.",
        "primary_table": "equipment_component_demand",
        "group_by": ["equipment_type", "year"],
        "aggregations": {
            "total_units": "SUM(units_demanded)",
            "total_value_m": "SUM(total_demand_value_million_usd)",
            "avg_lead_time_days": "AVG(lead_time_days)"
        },
        "order_by": ["equipment_type ASC", "year ASC"],
        "complexity": "Compound multi-key grouping with medium cardinality."
    },
    "WL5_MULTI_DATASET_JOIN": {
        "id": "WL5_MULTI_DATASET_JOIN",
        "name": "Workload 5: Multi-Dataset Join and Aggregation",
        "description": "Performs relational join between space_missions and agency_research_expenditures on agency and year, computing mission budget share of total R&D expenditures.",
        "primary_table": "space_missions",
        "join_table": "agency_research_expenditures",
        "join_condition": "space_missions.agency = agency_research_expenditures.agency AND space_missions.year = agency_research_expenditures.year",
        "group_by": ["agency", "year"],
        "aggregations": {
            "missions_count": "COUNT(space_missions.mission_id)",
            "total_mission_budget_m": "SUM(space_missions.budget_million_usd)",
            "total_annual_expenditure_m": "SUM(agency_research_expenditures.total_monthly_expenditure_million_usd)",
            "budget_share_of_rd_pct": "(total_mission_budget / total_annual_expenditure) * 100"
        },
        "order_by": ["agency ASC", "year ASC"],
        "complexity": "Distributed relational join across two distinct domains with multi-key aggregation."
    }
}
