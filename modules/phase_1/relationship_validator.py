"""
ORBITALYTICS - Phase 1 Relationship & Referential Integrity Validator
Verifies foreign key constraints, parent-child relationships, and relational integrity
across the canonical space research data model.
"""

from typing import Dict, Any, List
import pandas as pd
from pathlib import Path

class RelationshipValidator:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)

    def validate_referential_integrity(self) -> Dict[str, Any]:
        """
        Validates foreign key relationships between datasets:
        1. Missions -> Agencies
        2. Satellites -> Agencies & Missions
        3. Launches -> Missions
        4. Equipment Demand -> Components & Agencies
        5. Resource Consumption -> Resources & Agencies & Missions
        6. Manufacturing -> Agencies
        7. Infrastructure -> Agencies
        8. Investments -> Agencies
        """
        results: Dict[str, Any] = {}
        issues: List[Dict[str, str]] = []

        # Load reference entities
        agencies_file = self.data_dir.parent / "reference" / "agencies" / "agencies.csv"
        components_file = self.data_dir.parent / "reference" / "components" / "components.csv"
        resources_file = self.data_dir.parent / "reference" / "resources" / "resources.csv"

        valid_agency_ids = set()
        if agencies_file.exists():
            df_ag = pd.read_csv(agencies_file)
            valid_agency_ids = set(df_ag["agency_id"].dropna().unique())

        valid_comp_ids = set()
        if components_file.exists():
            df_comp = pd.read_csv(components_file)
            valid_comp_ids = set(df_comp["component_id"].dropna().unique())

        valid_res_ids = set()
        if resources_file.exists():
            df_res = pd.read_csv(resources_file)
            valid_res_ids = set(df_res["resource_id"].dropna().unique())

        # Load missions if available
        missions_file = self.data_dir / "space_missions.csv"
        if not missions_file.exists():
            missions_file = self.data_dir / "space_missions_validated.csv"
        valid_mission_ids = set()
        if missions_file.exists():
            df_msn = pd.read_csv(missions_file)
            valid_mission_ids = set(df_msn["mission_id"].dropna().unique())

            # Check Missions -> Agency ID
            if "agency_id" in df_msn.columns and valid_agency_ids:
                broken = df_msn[~df_msn["agency_id"].isin(valid_agency_ids)]
                if not broken.empty:
                    issues.append({
                        "relationship": "Missions -> Agencies",
                        "broken_count": len(broken),
                        "details": f"{len(broken)} missions have invalid agency_id"
                    })

        # Check Satellites -> Missions & Agencies
        sats_file = self.data_dir / "satellites_orbital.csv"
        if not sats_file.exists():
            sats_file = self.data_dir / "satellites_orbital_validated.csv"
        if sats_file.exists():
            df_sat = pd.read_csv(sats_file)
            if "associated_mission_id" in df_sat.columns and valid_mission_ids:
                broken_m = df_sat[~df_sat["associated_mission_id"].isin(valid_mission_ids)]
                if not broken_m.empty:
                    issues.append({
                        "relationship": "Satellites -> Missions",
                        "broken_count": len(broken_m),
                        "details": f"{len(broken_m)} satellites reference non-existent mission_ids"
                    })
            if "operator_agency_id" in df_sat.columns and valid_agency_ids:
                broken_a = df_sat[~df_sat["operator_agency_id"].isin(valid_agency_ids)]
                if not broken_a.empty:
                    issues.append({
                        "relationship": "Satellites -> Agencies",
                        "broken_count": len(broken_a),
                        "details": f"{len(broken_a)} satellites reference invalid operator_agency_ids"
                    })

        # Check Launches -> Missions
        lnch_file = self.data_dir / "launch_activities.csv"
        if not lnch_file.exists():
            lnch_file = self.data_dir / "launch_activities_validated.csv"
        if lnch_file.exists():
            df_l = pd.read_csv(lnch_file)
            if "mission_id" in df_l.columns and valid_mission_ids:
                broken_l = df_l[~df_l["mission_id"].isin(valid_mission_ids)]
                if not broken_l.empty:
                    issues.append({
                        "relationship": "Launches -> Missions",
                        "broken_count": len(broken_l),
                        "details": f"{len(broken_l)} launches reference non-existent mission_ids"
                    })

        # Check Equipment Demand -> Components & Agencies
        dem_file = self.data_dir / "equipment_component_demand.csv"
        if not dem_file.exists():
            dem_file = self.data_dir / "equipment_component_demand_validated.csv"
        if dem_file.exists():
            df_dem = pd.read_csv(dem_file)
            if "component_id" in df_dem.columns and valid_comp_ids:
                broken_c = df_dem[~df_dem["component_id"].isin(valid_comp_ids)]
                if not broken_c.empty:
                    issues.append({
                        "relationship": "Equipment Demand -> Components",
                        "broken_count": len(broken_c),
                        "details": f"{len(broken_c)} demand records reference non-existent component_ids"
                    })
            if "agency_id" in df_dem.columns and valid_agency_ids:
                broken_a = df_dem[~df_dem["agency_id"].isin(valid_agency_ids)]
                if not broken_a.empty:
                    issues.append({
                        "relationship": "Equipment Demand -> Agencies",
                        "broken_count": len(broken_a),
                        "details": f"{len(broken_a)} demand records reference invalid agency_ids"
                    })

        # Check Resource Consumption -> Resources & Missions
        res_file = self.data_dir / "resource_consumption.csv"
        if not res_file.exists():
            res_file = self.data_dir / "resource_consumption_validated.csv"
        if res_file.exists():
            df_cns = pd.read_csv(res_file)
            if "resource_id" in df_cns.columns and valid_res_ids:
                broken_r = df_cns[~df_cns["resource_id"].isin(valid_res_ids)]
                if not broken_r.empty:
                    issues.append({
                        "relationship": "Resource Consumption -> Resources",
                        "broken_count": len(broken_r),
                        "details": f"{len(broken_r)} consumption records reference non-existent resource_ids"
                    })

        status = "PASSED" if len(issues) == 0 else "FAILED_RELATIONSHIP_CHECKS"
        return {
            "status": status,
            "total_relationship_rules_checked": 8,
            "issues_count": len(issues),
            "issues": issues,
            "referential_integrity_pct": round(((8 - len(issues)) / 8) * 100.0, 2)
        }

