"""
ORBITALYTICS Phase 10 — Dataset Scaler Service
Generates reproducible, statistically consistent benchmark datasets across 3 scale tiers:
  - Small (1x scale, ~5,730 total records across core tables)
  - Medium (15x scale, ~85,950 total records)
  - Large (60x scale, ~343,800 total records)

Ensures strict referential integrity (e.g., mission_id matching between space_missions and launch_activities),
calculates exact byte sizes and record counts, and registers datasets in HDFS.
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PROCESSED_DIR = PROJECT_ROOT / "datasets" / "processed"
BENCHMARK_DIR = PROJECT_ROOT / "datasets" / "benchmark"


class DatasetScaler:
    """Manages benchmark dataset scaling, cataloging, and HDFS deployment."""

    def __init__(self):
        self.processed_dir = PROCESSED_DIR
        self.benchmark_dir = BENCHMARK_DIR
        self.benchmark_dir.mkdir(parents=True, exist_ok=True)
        self.scales = {
            "small": {"multiplier": 1, "description": "Baseline Historical Space Data (~5.7k records)"},
            "medium": {"multiplier": 15, "description": "Medium Enterprise Scale (~86k records, 15x)"},
            "large": {"multiplier": 60, "description": "Large High-Throughput Scale (~344k records, 60x)"}
        }

    def generate_all_scales(self) -> Dict[str, Any]:
        """Generates all 3 scale tiers locally and writes dataset catalog."""
        print("\n" + "="*80)
        print("ORBITALYTICS PHASE 10 — GENERATING CONTROLLED BENCHMARK DATASET TIERS")
        print("="*80)

        catalog = {}
        for scale_name, scale_info in self.scales.items():
            mult = scale_info["multiplier"]
            print(f"\n[GENERATING] Scale Tier: {scale_name.upper()} (Multiplier = {mult}x) ...")
            target_dir = self.benchmark_dir / scale_name
            target_dir.mkdir(parents=True, exist_ok=True)

            tier_catalog = {"scale_tier": scale_name, "multiplier": mult, "tables": {}}
            total_bytes = 0
            total_records = 0

            # 1. Equipment Component Demand
            eq_src = pd.read_csv(self.processed_dir / "equipment_component_demand_cleaned.csv")
            eq_scaled = self._replicate_dataframe(eq_src, mult, id_col="demand_id", jitter_cols=["units_demanded", "total_demand_value_million_usd"])
            eq_path = target_dir / "equipment_component_demand.csv"
            eq_scaled.to_csv(eq_path, index=False)
            eq_bytes = eq_path.stat().st_size
            total_bytes += eq_bytes
            total_records += len(eq_scaled)
            tier_catalog["tables"]["equipment_component_demand"] = {
                "records": len(eq_scaled), "bytes": eq_bytes, "size_mb": round(eq_bytes / (1024**2), 3), "columns": list(eq_scaled.columns)
            }
            print(f"  -> equipment_component_demand: {len(eq_scaled):,} rows, {round(eq_bytes/(1024**2), 2)} MB")

            # 2. Resource Consumption
            res_src = pd.read_csv(self.processed_dir / "resource_consumption_cleaned.csv")
            res_scaled = self._replicate_dataframe(res_src, mult, id_col="consumption_id", jitter_cols=["quantity_consumed", "procurement_cost_k_usd"])
            res_path = target_dir / "resource_consumption.csv"
            res_scaled.to_csv(res_path, index=False)
            res_bytes = res_path.stat().st_size
            total_bytes += res_bytes
            total_records += len(res_scaled)
            tier_catalog["tables"]["resource_consumption"] = {
                "records": len(res_scaled), "bytes": res_bytes, "size_mb": round(res_bytes / (1024**2), 3), "columns": list(res_scaled.columns)
            }
            print(f"  -> resource_consumption: {len(res_scaled):,} rows, {round(res_bytes/(1024**2), 2)} MB")

            # 3. Space Missions (Primary for joins)
            msn_src = pd.read_csv(self.processed_dir / "space_missions_cleaned.csv")
            msn_scaled = self._replicate_missions(msn_src, mult)
            msn_path = target_dir / "space_missions.csv"
            msn_scaled.to_csv(msn_path, index=False)
            msn_bytes = msn_path.stat().st_size
            total_bytes += msn_bytes
            total_records += len(msn_scaled)
            tier_catalog["tables"]["space_missions"] = {
                "records": len(msn_scaled), "bytes": msn_bytes, "size_mb": round(msn_bytes / (1024**2), 3), "columns": list(msn_scaled.columns)
            }
            print(f"  -> space_missions: {len(msn_scaled):,} rows, {round(msn_bytes/(1024**2), 2)} MB")

            # 4. Launch Activities
            lnch_src = pd.read_csv(self.processed_dir / "launch_activities_cleaned.csv")
            lnch_scaled = self._replicate_dataframe(lnch_src, mult, id_col="launch_id", jitter_cols=["launch_cost_million_usd", "payload_to_orbit_kg"])
            lnch_path = target_dir / "launch_activities.csv"
            lnch_scaled.to_csv(lnch_path, index=False)
            lnch_bytes = lnch_path.stat().st_size
            total_bytes += lnch_bytes
            total_records += len(lnch_scaled)
            tier_catalog["tables"]["launch_activities"] = {
                "records": len(lnch_scaled), "bytes": lnch_bytes, "size_mb": round(lnch_bytes / (1024**2), 3), "columns": list(lnch_scaled.columns)
            }
            print(f"  -> launch_activities: {len(lnch_scaled):,} rows, {round(lnch_bytes/(1024**2), 2)} MB")

            # 5. Agency Research Expenditures
            exp_src = pd.read_csv(self.processed_dir / "agency_research_expenditures_cleaned.csv")
            exp_scaled = self._replicate_dataframe(exp_src, mult, id_col="expenditure_id", jitter_cols=["rd_expenditure_million_usd", "total_monthly_expenditure_million_usd"])
            exp_path = target_dir / "agency_research_expenditures.csv"
            exp_scaled.to_csv(exp_path, index=False)
            exp_bytes = exp_path.stat().st_size
            total_bytes += exp_bytes
            total_records += len(exp_scaled)
            tier_catalog["tables"]["agency_research_expenditures"] = {
                "records": len(exp_scaled), "bytes": exp_bytes, "size_mb": round(exp_bytes / (1024**2), 3), "columns": list(exp_scaled.columns)
            }
            print(f"  -> agency_research_expenditures: {len(exp_scaled):,} rows, {round(exp_bytes/(1024**2), 2)} MB")

            tier_catalog["total_records"] = total_records
            tier_catalog["total_bytes"] = total_bytes
            tier_catalog["total_size_mb"] = round(total_bytes / (1024**2), 3)
            catalog[scale_name] = tier_catalog

        # Write catalog JSON
        catalog_path = self.benchmark_dir / "dataset_catalog.json"
        with open(catalog_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
        print(f"\n[OK] Benchmark Dataset Catalog persisted at: {catalog_path}")
        return catalog

    def _replicate_dataframe(self, df: pd.DataFrame, multiplier: int, id_col: str, jitter_cols: List[str]) -> pd.DataFrame:
        if multiplier == 1:
            return df.copy()

        frames = [df.copy()]
        np.random.seed(42)
        for rep in range(1, multiplier):
            sub = df.copy()
            if id_col in sub.columns:
                sub[id_col] = sub[id_col].astype(str) + f"_R{rep:02d}"
            for c in jitter_cols:
                if c in sub.columns:
                    noise = np.random.uniform(0.95, 1.05, size=len(sub))
                    if np.issubdtype(sub[c].dtype, np.integer):
                        sub[c] = np.maximum(1, np.round(sub[c] * noise).astype(int))
                    else:
                        sub[c] = np.maximum(0.1, np.round(sub[c] * noise, 2))
            frames.append(sub)

        res = pd.concat(frames, ignore_index=True)
        return res

    def _replicate_missions(self, df: pd.DataFrame, multiplier: int) -> pd.DataFrame:
        if multiplier == 1:
            return df.copy()

        frames = [df.copy()]
        np.random.seed(42)
        for rep in range(1, multiplier):
            sub = df.copy()
            sub["mission_id"] = sub["mission_id"].astype(str) + f"_R{rep:02d}"
            sub["budget_million_usd"] = np.round(sub["budget_million_usd"] * np.random.uniform(0.95, 1.05, size=len(sub)), 2)
            sub["payload_mass_kg"] = np.round(sub["payload_mass_kg"] * np.random.uniform(0.95, 1.05, size=len(sub)), 1)
            frames.append(sub)

        return pd.concat(frames, ignore_index=True)

    def _replicate_launches(self, df: pd.DataFrame, multiplier: int, valid_mission_ids: List[str]) -> pd.DataFrame:
        if multiplier == 1:
            return df.copy()

        frames = [df.copy()]
        np.random.seed(42)
        for rep in range(1, multiplier):
            sub = df.copy()
            sub["launch_id"] = sub["launch_id"].astype(str) + f"_R{rep:02d}"
            sub["mission_id"] = sub["mission_id"].astype(str) + f"_R{rep:02d}"
            # Ensure mission_id exists in valid_mission_ids
            sub["launch_cost_million_usd"] = np.round(sub["launch_cost_million_usd"] * np.random.uniform(0.95, 1.05, size=len(sub)), 2)
            sub["payload_to_orbit_kg"] = np.round(sub["payload_to_orbit_kg"] * np.random.uniform(0.95, 1.05, size=len(sub)), 1)
            frames.append(sub)

        res = pd.concat(frames, ignore_index=True)
        # Filter to ensure referential integrity
        res = res[res["mission_id"].isin(valid_mission_ids)].reset_index(drop=True)
        return res

    def upload_to_hdfs(self) -> bool:
        """Uploads Small, Medium, and Large datasets to HDFS."""
        print("\n[HDFS SYNC] Transferring benchmark datasets into HDFS ...")
        for scale in ["small", "medium", "large"]:
            scale_dir = self.benchmark_dir / scale
            if not scale_dir.exists():
                continue

            hdfs_target = f"/orbitalytics/benchmark/{scale}"
            # Create HDFS dir
            cmd_mkdir = f'docker exec hadoop-namenode hdfs dfs -mkdir -p {hdfs_target}'
            subprocess.run(cmd_mkdir, shell=True, capture_output=True)

            # Copy files into hadoop-namenode container and put into HDFS
            for csv_file in scale_dir.glob("*.csv"):
                cmd_cp = f'docker cp "{csv_file}" hadoop-namenode:/tmp/{csv_file.name}'
                subprocess.run(cmd_cp, shell=True, capture_output=True)
                cmd_put = f'docker exec hadoop-namenode hdfs dfs -put -f /tmp/{csv_file.name} {hdfs_target}/{csv_file.name}'
                subprocess.run(cmd_put, shell=True, capture_output=True)

            print(f"  -> Uploaded {scale.upper()} tier into {hdfs_target}")

        return True


if __name__ == "__main__":
    scaler = DatasetScaler()
    scaler.generate_all_scales()
    scaler.upload_to_hdfs()
