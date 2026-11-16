"""
ORBITALYTICS Phase 6 — Apache Hive Warehouse Service
Connects to the enterprise Hive Data Warehouse (database: orbitalytics).
Provides dimensional metadata, fact table catalog, partition specifications,
BI views, execution manifests, and instant high-performance analytical query results.
"""

import os
import csv
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DOCS_PHASE6_DIR = BASE_DIR / "docs" / "phase_6"
RESULTS_DIR = DOCS_PHASE6_DIR / "results"
MANIFEST_PATH = DOCS_PHASE6_DIR / "hive_execution_manifest.json"
DOCKER_CONTAINER = "hive-server"
HIVE_JDBC = "jdbc:hive2://localhost:10000/orbitalytics"

class HiveService:
    def __init__(self):
        self.database_name = "orbitalytics"
        self.warehouse_hdfs_path = "/user/hive/warehouse/orbitalytics.db/"
        self._init_catalog()

    def _init_catalog(self):
        """Initialize metadata catalog for Dimensions, Facts, and Views."""
        self.dimensions_metadata = [
            {
                "table_name": "dim_date",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "date_key",
                "columns": ["date_key", "full_date", "year", "quarter", "month", "day", "is_weekend"],
                "description": "Enterprise temporal dimension across standard Gregorian calendar attributes"
            },
            {
                "table_name": "dim_agency",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "agency_key",
                "columns": ["agency_key", "agency_name", "country", "agency_type"],
                "description": "Global space research agencies, sovereign operators, and commercial aerospace entities"
            },
            {
                "table_name": "dim_component",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "component_key",
                "columns": ["component_key", "component_name", "component_category", "standard_lead_time_days"],
                "description": "Spaceflight hardware, avionics, sensors, thrusters, and payload components catalog"
            },
            {
                "table_name": "dim_resource",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "resource_key",
                "columns": ["resource_key", "resource_name", "resource_category", "unit_of_measure"],
                "description": "Consumables, propellants, cryogenic fuels, telemetry bandwidth, and power arrays"
            },
            {
                "table_name": "dim_mission",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "mission_key",
                "columns": ["mission_key", "mission_name", "agency_name", "mission_type", "status", "duration_days", "crew_size"],
                "description": "Space exploration missions, satellite deployment campaigns, and deep space probes"
            },
            {
                "table_name": "dim_satellite",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "satellite_key",
                "columns": ["satellite_key", "satellite_name", "operator", "orbit_type", "application", "expected_lifetime_years"],
                "description": "Orbital payloads, constellation constellations, Earth observation, and science platforms"
            },
            {
                "table_name": "dim_location",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "surrogate_key": "location_key",
                "columns": ["location_key", "site_name", "country", "launch_pads_count", "operational_status"],
                "description": "Terrestrial spaceports, launch complexes, and tracking ground station infrastructure"
            }
        ]

        self.facts_metadata = [
            {
                "table_name": "fact_equipment_demand",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "partition_column": "year (INT)",
                "record_count": 11312,
                "hdfs_location": f"{self.warehouse_hdfs_path}fact_equipment_demand",
                "metrics": ["units_demanded", "units_manufactured", "units_procured", "total_demand_value_m_usd", "lead_time_days"],
                "description": "Subsystem component order volume, procurement fulfillment, demand valuation, and lead times"
            },
            {
                "table_name": "fact_resource_consumption",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "partition_column": "year (INT)",
                "record_count": 1414,
                "hdfs_location": f"{self.warehouse_hdfs_path}fact_resource_consumption",
                "metrics": ["quantity_consumed", "procurement_cost_k_usd", "consumption_rate_per_day"],
                "description": "Strategic propellant and consumable resource utilization across launch complexes and orbiters"
            },
            {
                "table_name": "fact_launch_activity",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "partition_column": "year (INT)",
                "record_count": 1270,
                "hdfs_location": f"{self.warehouse_hdfs_path}fact_launch_activity",
                "metrics": ["payload_to_orbit_kg", "launch_cost_m_usd", "commercial_flag", "launch_outcome"],
                "description": "Orbital and suborbital launch vehicle operations, payload mass, and launch economics"
            },
            {
                "table_name": "fact_manufacturing",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "partition_column": "year (INT)",
                "record_count": 1414,
                "hdfs_location": f"{self.warehouse_hdfs_path}fact_manufacturing",
                "metrics": ["quantity_produced", "production_cost_m_usd", "qa_passed"],
                "description": "Aerospace component manufacturing batches, quality assurance yields, and defect rates"
            },
            {
                "table_name": "fact_research_investment",
                "table_type": "MANAGED_TABLE",
                "storage_format": "PARQUET",
                "compression": "SNAPPY",
                "partition_column": "year (INT)",
                "record_count": 1414,
                "hdfs_location": f"{self.warehouse_hdfs_path}fact_research_investment",
                "metrics": ["expenditure_m_usd"],
                "description": "Sovereign and corporate research & development capital allocation across space domains"
            }
        ]

        self.views_metadata = [
            {
                "view_name": "vw_annual_equipment_demand_summary",
                "description": "Annual equipment demand, aggregate unit requirements, fulfillment rates, and procurement capital"
            },
            {
                "view_name": "vw_agency_mission_performance",
                "description": "Space agency operational mission scorecards, mission success rates, and budget deployment"
            },
            {
                "view_name": "vw_launch_market_commercialization",
                "description": "Annual launch market commercialization index, payload throughput, and per-launch cost efficiency"
            }
        ]

        self.query_alias_map = {
            # UI Selector aliases (1 to 12)
            "annual_missions_by_agency": "07_mission_counts_by_agency",
            "launch_success_rates": "09_launch_activity_trends",
            "satellite_deployment_trends": "08_satellite_deployment_by_orbit",
            "orbit_distribution": "08_satellite_deployment_by_orbit",
            "equipment_demand_trend": "02_annual_demand_trend",
            "resource_utilization_by_mission": "06_resource_consumption_by_mission",
            "research_expenditure_by_agency": "11_research_expenditure_by_agency",
            "infrastructure_expenditure_trends": "13_infrastructure_by_location",
            "future_investments": "12_investment_by_year",
            "demand_aggregation_for_forecasting": "01_total_demand_by_component",
            "equipment_supply_demand_gap": "10_manufacturing_requirements_by_component",
            "high_risk_resource_shortages": "05_resource_consumption_by_year",

            # Legacy & direct aliases
            "agency_missions": "07_mission_counts_by_agency",
            "launch_vehicles": "09_launch_activity_trends",
            "01": "01_total_demand_by_component",
            "02": "02_annual_demand_trend",
            "03": "03_quarterly_demand_trend",
            "04": "04_demand_by_agency",
            "05": "05_resource_consumption_by_year",
            "06": "06_resource_consumption_by_mission",
            "07": "07_mission_counts_by_agency",
            "08": "08_satellite_deployment_by_orbit",
            "09": "09_launch_activity_trends",
            "10": "10_manufacturing_requirements_by_component",
            "11": "11_research_expenditure_by_agency",
            "12": "12_investment_by_year",
            "13": "13_infrastructure_by_location",
            "14": "14_mission_demand_correlation",
            "15": "15_resource_launch_correlation",
            "16": "16_partition_pruning_demonstration"
        }

    def get_tables_metadata(self) -> Dict[str, Any]:
        """Returns complete data catalog for the Orbitalytics Hive Data Warehouse."""
        all_tables = []
        for d in self.dimensions_metadata:
            all_tables.append({
                "table_name": d["table_name"],
                "table_type": d["table_type"],
                "storage_format": d["storage_format"],
                "compression": d["compression"],
                "partition_column": "None (Full Scan Optimized)",
                "hdfs_location": f"{self.warehouse_hdfs_path}{d['table_name']}",
                "description": d["description"]
            })
        for f in self.facts_metadata:
            all_tables.append({
                "table_name": f["table_name"],
                "table_type": f["table_type"],
                "storage_format": f["storage_format"],
                "compression": f["compression"],
                "partition_column": f["partition_column"],
                "record_count": f["record_count"],
                "hdfs_location": f["hdfs_location"],
                "description": f["description"]
            })
        for v in self.views_metadata:
            all_tables.append({
                "table_name": v["view_name"],
                "table_type": "VIEW",
                "storage_format": "LOGICAL",
                "compression": "N/A",
                "partition_column": "Inherited from underlying facts",
                "hdfs_location": "N/A (Metastore Logical View)",
                "description": v["description"]
            })

        return {
            "database": self.database_name,
            "warehouse_path": self.warehouse_hdfs_path,
            "total_entities": len(all_tables),
            "dimensions_count": len(self.dimensions_metadata),
            "facts_count": len(self.facts_metadata),
            "views_count": len(self.views_metadata),
            "tables": all_tables
        }

    def get_dimensions(self) -> List[Dict[str, Any]]:
        """Returns catalog of all 7 star-schema dimensions."""
        return self.dimensions_metadata

    def get_facts(self) -> List[Dict[str, Any]]:
        """Returns catalog of all 5 partitioned fact tables."""
        return self.facts_metadata

    def get_views(self) -> List[Dict[str, Any]]:
        """Returns catalog of all 3 analytical views."""
        return self.views_metadata

    def get_execution_manifest(self) -> Dict[str, Any]:
        """Loads and returns the analytical query execution manifest."""
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
            successful = sum(1 for m in manifest_data if m.get("status") == "SUCCESS")
            return {
                "status": "COMPLETED",
                "total_queries": len(manifest_data),
                "successful_queries": successful,
                "manifest": manifest_data
            }
        return {
            "status": "NOT_FOUND",
            "message": "Hive execution manifest not found. Execute hive_orchestrator.py first."
        }

    def execute_analytical_query(self, query_id: str) -> Dict[str, Any]:
        """
        Executes or retrieves analytical query results for the Hive Data Warehouse.
        Accepts legacy query IDs or Phase 6 IDs ('01' to '16', or full query name).
        """
        target_name = self.query_alias_map.get(query_id, query_id)
        if not target_name.endswith(".sql") and not target_name.endswith(".csv"):
            csv_file = RESULTS_DIR / f"{target_name}.csv"
            sql_file = BASE_DIR / "hive_warehouse" / "queries" / f"{target_name}.sql"
        else:
            base_name = target_name.split(".")[0]
            csv_file = RESULTS_DIR / f"{base_name}.csv"
            sql_file = BASE_DIR / "hive_warehouse" / "queries" / f"{base_name}.sql"

        sql_text = ""
        if sql_file.exists():
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_text = f.read()

        # If pre-computed result CSV exists, parse and return clean records
        if csv_file.exists():
            start_time = time.time()
            rows = []
            headers = []
            with open(csv_file, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                for line in reader:
                    if not line:
                        continue
                    first_cell = line[0].strip()
                    if first_cell.startswith("0: jdbc") or first_cell.startswith("SLF4J") or first_cell.startswith("."):
                        continue
                    if not headers:
                        headers = [h.strip() for h in line]
                    else:
                        row_dict = {}
                        for i, h in enumerate(headers):
                            val = line[i].strip() if i < len(line) else ""
                            # Safe numeric parse
                            try:
                                if "." in val:
                                    row_dict[h] = float(val)
                                else:
                                    row_dict[h] = int(val)
                            except ValueError:
                                row_dict[h] = val
                        rows.append(row_dict)

            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "query_id": query_id,
                "target_query": target_name,
                "hive_sql": sql_text,
                "database": self.database_name,
                "execution_time_ms": elapsed_ms,
                "rows_returned": len(rows),
                "columns": headers,
                "data": rows
            }

        # Live execution fallback via Beeline
        start_time = time.time()
        cmd = f'docker exec {DOCKER_CONTAINER} beeline -u "{HIVE_JDBC}" -n root --outputformat=csv2 -e "{sql_text}"'
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        if res.returncode != 0:
            raise RuntimeError(f"Hive execution error: {res.stderr}")

        rows = []
        headers = []
        for raw_line in res.stdout.splitlines():
            line_str = raw_line.strip()
            if not line_str or line_str.startswith("0: jdbc") or line_str.startswith("SLF4J") or line_str.startswith("."):
                continue
            cells = line_str.split(",")
            if not headers:
                headers = [c.strip() for c in cells]
            else:
                row_dict = {headers[i]: cells[i].strip() for i in range(min(len(headers), len(cells)))}
                rows.append(row_dict)

        return {
            "query_id": query_id,
            "target_query": target_name,
            "hive_sql": sql_text,
            "database": self.database_name,
            "execution_time_ms": elapsed_ms,
            "rows_returned": len(rows),
            "columns": headers,
            "data": rows
        }
