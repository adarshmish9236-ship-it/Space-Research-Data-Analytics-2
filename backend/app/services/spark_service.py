"""
ORBITALYTICS Phase 7 — PySpark Distributed Analytics Service
Provides access to Apache Spark job manifests, Gold Layer Parquet datasets,
feature engineering schemas, and Spark SQL analytical query results.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger("orbitalytics.spark_service")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DOCS_PHASE7 = BASE_DIR / "docs" / "phase_7"
MANIFEST_FILE = DOCS_PHASE7 / "phase7_execution_manifest.json"
LOGS_DIR = DOCS_PHASE7 / "logs"

GOLD_DATASETS_CATALOG = [
    {
        "dataset_name": "annual_equipment_demand_trend",
        "domain": "demand_analytics",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/demand_analytics/annual_equipment_demand_trend",
        "partition_key": "year",
        "record_count": 17,
        "description": "Annual equipment demand trends, YoY growth percentages, and cumulative units demanded"
    },
    {
        "dataset_name": "component_demand_summary",
        "domain": "demand_analytics",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/demand_analytics/component_demand_summary",
        "partition_key": "category_partition",
        "record_count": 8,
        "description": "Component-level demand, manufactured vs procured quantities, and fulfillment rates"
    },
    {
        "dataset_name": "annual_resource_consumption_trend",
        "domain": "resource_analytics",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/resource_analytics/annual_resource_consumption_trend",
        "partition_key": "year",
        "record_count": 119,
        "description": "Annual consumable resource consumption by category with YoY change percentage"
    },
    {
        "dataset_name": "annual_launch_trends",
        "domain": "mission_analytics",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/mission_analytics/annual_launch_trends",
        "partition_key": "year",
        "record_count": 17,
        "description": "Annual launch cadence, mission success rates, commercial market share, and 3-year moving avg"
    },
    {
        "dataset_name": "annual_research_investment",
        "domain": "research_analytics",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/research_analytics/annual_research_investment",
        "partition_key": "year",
        "record_count": 119,
        "description": "Space agency annual R&D capital allocation, infrastructure spend, and investment rankings"
    },
    {
        "dataset_name": "equipment_demand_features",
        "domain": "forecast_features",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/forecast_features/equipment_demand_features",
        "partition_key": "year",
        "record_count": 952,
        "description": "Complete ML feature store containing 24 time-series, lag, rolling, and contextual features"
    },
    {
        "dataset_name": "train_dataset",
        "domain": "forecast_features",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/forecast_features/train_dataset",
        "partition_key": "year",
        "record_count": 728,
        "description": "Time-aware training partition (years 2010 through 2023) with no future leakage"
    },
    {
        "dataset_name": "test_dataset",
        "domain": "forecast_features",
        "hdfs_path": "hdfs://namenode:9000/orbitalytics/gold/forecast_features/test_dataset",
        "partition_key": "year",
        "record_count": 168,
        "description": "Holdout test partition (years 2024 through 2026) for out-of-time model evaluation"
    }
]


class SparkService:
    def __init__(self):
        self.master_url = "spark://spark-master:7077"
        self.spark_version = "3.1.2"
        self.catalog = GOLD_DATASETS_CATALOG

    def get_manifest(self) -> Dict[str, Any]:
        """Returns execution manifest of all 4 Phase 7 PySpark jobs."""
        if MANIFEST_FILE.exists():
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "status": "NOT_FOUND",
            "message": "Phase 7 execution manifest not found. Run phase7_orchestrator.py first."
        }

    def get_gold_catalog(self) -> Dict[str, Any]:
        """Returns metadata catalog of all 8 Gold layer datasets in HDFS."""
        return {
            "total_gold_datasets": len(self.catalog),
            "storage_format": "PARQUET",
            "compression": "SNAPPY",
            "hdfs_base": "hdfs://namenode:9000/orbitalytics/gold",
            "datasets": self.catalog
        }

    def get_gold_dataset_info(self, dataset_name: str) -> Dict[str, Any]:
        """Returns details for a specific Gold dataset."""
        match = next((d for d in self.catalog if d["dataset_name"] == dataset_name), None)
        if match:
            return match
        return {"error": f"Dataset '{dataset_name}' not found in Gold catalog"}

    def get_feature_schema(self) -> Dict[str, Any]:
        """Returns the complete 24-feature schema definition for time-series forecasting."""
        features = [
            {"name": "year", "type": "Integer", "role": "Temporal index / Partition key"},
            {"name": "agency_id", "type": "String", "role": "Entity identifier"},
            {"name": "component_id", "type": "String", "role": "Entity identifier"},
            {"name": "component_category", "type": "String", "role": "Categorical domain"},
            {"name": "annual_units_demanded", "type": "Double", "role": "Target variable (Y)"},
            {"name": "annual_demand_value_m_usd", "type": "Double", "role": "Historical demand spend"},
            {"name": "avg_lead_time_days", "type": "Double", "role": "Procurement latency metric"},
            {"name": "annual_units_manufactured", "type": "Double", "role": "Internal production capacity"},
            {"name": "annual_units_procured", "type": "Double", "role": "External vendor fulfillment"},
            {"name": "lag_1_units", "type": "Double", "role": "Prior year demand (t-1)"},
            {"name": "lag_2_units", "type": "Double", "role": "2-year lag demand (t-2)"},
            {"name": "lag_3_units", "type": "Double", "role": "3-year lag demand (t-3)"},
            {"name": "lag_4_units", "type": "Double", "role": "4-year lag demand (t-4)"},
            {"name": "lag_1_value", "type": "Double", "role": "Prior year spend value (t-1)"},
            {"name": "rolling_3yr_mean", "type": "Double", "role": "3-year rolling mean [t-3, t-1]"},
            {"name": "rolling_3yr_std", "type": "Double", "role": "3-year rolling volatility [t-3, t-1]"},
            {"name": "yoy_growth_pct", "type": "Double", "role": "Year-over-Year demand change %"},
            {"name": "growth_3yr_pct", "type": "Double", "role": "3-year compounded demand change %"},
            {"name": "fulfillment_rate_pct", "type": "Double", "role": "Supply-demand fulfillment ratio"},
            {"name": "prev_yr_mission_count", "type": "Long", "role": "Agency mission volume at (t-1)"},
            {"name": "prev_yr_launch_count", "type": "Long", "role": "Global industry launch volume at (t-1)"},
            {"name": "prev_yr_satellite_deploy_count", "type": "Long", "role": "Global satellite deployment at (t-1)"},
            {"name": "years_since_start", "type": "Integer", "role": "Secular linear trend indicator (t - 2010)"},
            {"name": "is_recent_period", "type": "Integer", "role": "Regime shift indicator (year >= 2020)"}
        ]
        return {
            "feature_count": len(features),
            "train_observations": 728,
            "test_observations": 168,
            "total_observations": 896,
            "train_ratio_pct": 81.25,
            "temporal_cutoff_year": 2023,
            "leakage_prevention": "Strictly historical windowing [t-3, t-1] and prior-year activity joins (year - 1)",
            "features": features
        }
