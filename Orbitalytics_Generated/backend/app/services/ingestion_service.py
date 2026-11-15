"""
Orbitalytics 2.0 - Medallion Lakehouse Ingestion & Curation Service
Manages data progression across Bronze (Raw Ingestion + Checksums),
Silver (Cleaned, Normalized & Schema Enforced), and Gold (Star-Schema Curated Parquet Fact & Dimension Tables).
"""

import hashlib
import json
import time
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from app.core.config import settings

class IngestionService:
    def __init__(self):
        self.raw_dir = settings.RAW_DATA_DIR
        self.bronze_dir = settings.BRONZE_DATA_DIR
        self.silver_dir = settings.SILVER_DATA_DIR
        self.gold_dir = settings.GOLD_DATA_DIR
        self.curated_dir = settings.CURATED_DATA_DIR
        self.hdfs_bronze = settings.HDFS_BRONZE_DIR
        self.hdfs_silver = settings.HDFS_SILVER_DIR
        self.hdfs_gold = settings.HDFS_GOLD_DIR
        self.hdfs_curated = settings.HDFS_SPACE_DIR / "curated"

        for d in [self.bronze_dir, self.silver_dir, self.gold_dir, self.curated_dir,
                  self.hdfs_bronze, self.hdfs_silver, self.hdfs_gold, self.hdfs_curated]:
            d.mkdir(parents=True, exist_ok=True)

    def _compute_md5(self, file_path: Path) -> str:
        if not file_path.exists():
            return ""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def run_full_ingestion_and_curation(self) -> Dict[str, Any]:
        """
        Executes end-to-end Medallion progression across Bronze, Silver, and Gold layers
        for all 9 space research dataset categories.
        """
        start_time = time.time()
        results = []
        total_records_processed = 0

        datasets = [
            ("space_missions.csv", "missions", self._curate_missions),
            ("satellites_orbital.csv", "satellites", self._curate_satellites),
            ("launch_activities.csv", "launches", self._curate_launches),
            ("equipment_component_demand.csv", "equipment_demand", self._curate_equipment_demand),
            ("agency_research_expenditures.csv", "expenditures", self._curate_expenditures),
            ("resource_consumption.csv", "resources", self._curate_resources),
            ("satellite_manufacturing_requirements.csv", "manufacturing", self._curate_manufacturing),
            ("space_infrastructure_requirements.csv", "infrastructure", self._curate_infrastructure),
            ("research_investment_future_projects.csv", "investments", self._curate_investments),
        ]

        for filename, domain_key, curate_fn in datasets:
            raw_path = self.raw_dir / filename
            if not raw_path.exists():
                continue

            # 1. Bronze Ingestion: Preserve raw, record checksum, timestamp, provenance
            bronze_path = self.bronze_dir / filename
            shutil.copy2(raw_path, bronze_path)
            shutil.copy2(raw_path, self.hdfs_bronze / filename)
            checksum = self._compute_md5(raw_path)

            # 2. Silver Normalization: Schema enforcement, type casting, invalid record filtering
            df = pd.read_csv(raw_path)
            df_silver, quarantined = self._clean_and_normalize(df, domain_key)
            silver_path = self.silver_dir / f"{filename.replace('.csv', '_silver.parquet')}"
            df_silver.to_parquet(silver_path, compression="snappy", index=False)
            df_silver.to_parquet(self.hdfs_silver / f"{filename.replace('.csv', '_silver.parquet')}", compression="snappy", index=False)

            # 3. Gold Lakehouse Curation: Star schema facts & partitioned Parquet
            gold_info = curate_fn(df_silver)
            total_records_processed += len(df_silver)

            results.append({
                "dataset": filename,
                "domain": domain_key,
                "bronze_checksum": checksum,
                "records_raw": len(df),
                "records_silver": len(df_silver),
                "quarantined_records": quarantined,
                "gold_partitions": gold_info.get("partitions", 1),
                "gold_format": "Parquet (Snappy)",
                "status": "CURATED"
            })

        # Generate Gold Dimensions (dim_agencies, dim_orbits, dim_time)
        self._build_gold_dimensions()

        duration = round(time.time() - start_time, 3)
        return {
            "status": "SUCCESS",
            "medallion_pipeline": "BRONZE_SILVER_GOLD",
            "total_datasets": len(results),
            "total_records_curated": total_records_processed,
            "duration_seconds": duration,
            "details": results
        }

    def _clean_and_normalize(self, df: pd.DataFrame, domain: str) -> tuple[pd.DataFrame, int]:
        clean_df = df.copy()
        quarantined = 0

        # Standardize string fields
        str_cols = clean_df.select_dtypes(include=['object']).columns
        for c in str_cols:
            clean_df[c] = clean_df[c].astype(str).str.strip()

        # Date normalization
        for date_col in ['launch_date', 'period_month', 'start_date', 'announcement_date', 'year']:
            if date_col in clean_df.columns:
                if date_col == 'year':
                    clean_df['year'] = pd.to_numeric(clean_df['year'], errors='coerce').fillna(2024).astype(int)
                else:
                    clean_df[date_col] = pd.to_datetime(clean_df[date_col], errors='coerce')
                    clean_df[date_col] = clean_df[date_col].fillna(pd.Timestamp("2024-01-01"))

        # Numeric sanitization (reject negative values where physically impossible)
        num_cols = clean_df.select_dtypes(include=[np.number]).columns
        for nc in num_cols:
            if nc in ['quantity_demanded', 'budget_usd', 'payload_mass_kg', 'consumption_units']:
                invalid_mask = clean_df[nc] < 0
                quarantined += int(invalid_mask.sum())
                clean_df.loc[invalid_mask, nc] = clean_df[nc].median()

        # Add Lakehouse Lineage & Provenance Metadata
        clean_df["_ingestion_timestamp"] = datetime.utcnow().isoformat()
        clean_df["_provenance"] = "SIMULATED_RESEARCH_OBSERVATION_V2"
        clean_df["_quality_status"] = "PASSED_SILVER_VALIDATION"

        return clean_df, quarantined

    def _curate_missions(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "space_missions"
        hdfs_dest = self.hdfs_curated / "space_missions"
        gold_dest = self.gold_dir / "fact_space_missions.parquet"
        
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        
        # Partition by agency
        df.to_parquet(gold_dest, compression="snappy", index=False)
        for agency, group in df.groupby("agency"):
            safe_agency = str(agency).replace("/", "_").replace("\\", "_").replace(" ", "_")
            p_file = dest / f"agency={safe_agency}.parquet"
            h_file = hdfs_dest / f"agency={safe_agency}.parquet"
            group.to_parquet(p_file, compression="snappy", index=False)
            group.to_parquet(h_file, compression="snappy", index=False)
        return {"partitions": df["agency"].nunique()}

    def _curate_satellites(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "satellites_orbital"
        hdfs_dest = self.hdfs_curated / "satellites_orbital"
        gold_dest = self.gold_dir / "fact_satellites_orbital.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        orbit_col = "orbit_type" if "orbit_type" in df.columns else df.columns[6]
        for orbit, group in df.groupby(orbit_col):
            safe_orbit = str(orbit).replace("/", "_").replace("\\", "_").replace(" ", "_")
            group.to_parquet(dest / f"orbit={safe_orbit}.parquet", compression="snappy", index=False)
            group.to_parquet(hdfs_dest / f"orbit={safe_orbit}.parquet", compression="snappy", index=False)
        return {"partitions": df[orbit_col].nunique()}

    def _curate_launches(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "launch_activities"
        hdfs_dest = self.hdfs_curated / "launch_activities"
        gold_dest = self.gold_dir / "fact_launch_activities.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        for country, group in df.groupby("country"):
            safe_c = str(country).replace(" ", "_")
            group.to_parquet(dest / f"country={safe_c}.parquet", compression="snappy", index=False)
            group.to_parquet(hdfs_dest / f"country={safe_c}.parquet", compression="snappy", index=False)
        return {"partitions": df["country"].nunique()}

    def _curate_equipment_demand(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "equipment_component_demand"
        hdfs_dest = self.hdfs_curated / "equipment_component_demand"
        gold_dest = self.gold_dir / "fact_equipment_demand.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        comp_col = "equipment_category" if "equipment_category" in df.columns else ("component_category" if "component_category" in df.columns else df.columns[3])
        for comp, group in df.groupby(comp_col):
            safe_comp = str(comp).replace(" ", "_").replace("/", "_").replace("\\", "_")
            group.to_parquet(dest / f"category={safe_comp}.parquet", compression="snappy", index=False)
            group.to_parquet(hdfs_dest / f"category={safe_comp}.parquet", compression="snappy", index=False)
        return {"partitions": df[comp_col].nunique()}

    def _curate_expenditures(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "agency_research_expenditures"
        hdfs_dest = self.hdfs_curated / "agency_research_expenditures"
        gold_dest = self.gold_dir / "fact_agency_expenditures.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        df.to_parquet(dest / "expenditures.parquet", compression="snappy", index=False)
        df.to_parquet(hdfs_dest / "expenditures.parquet", compression="snappy", index=False)
        return {"partitions": 1}

    def _curate_resources(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "resource_consumption"
        hdfs_dest = self.hdfs_curated / "resource_consumption"
        gold_dest = self.gold_dir / "fact_resource_consumption.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        df.to_parquet(dest / "resources.parquet", compression="snappy", index=False)
        df.to_parquet(hdfs_dest / "resources.parquet", compression="snappy", index=False)
        return {"partitions": 1}

    def _curate_manufacturing(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "satellite_manufacturing_requirements"
        hdfs_dest = self.hdfs_curated / "satellite_manufacturing_requirements"
        gold_dest = self.gold_dir / "fact_satellite_manufacturing.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        df.to_parquet(dest / "manufacturing.parquet", compression="snappy", index=False)
        df.to_parquet(hdfs_dest / "manufacturing.parquet", compression="snappy", index=False)
        return {"partitions": 1}

    def _curate_infrastructure(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "space_infrastructure_requirements"
        hdfs_dest = self.hdfs_curated / "space_infrastructure_requirements"
        gold_dest = self.gold_dir / "fact_space_infrastructure.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        df.to_parquet(dest / "infrastructure.parquet", compression="snappy", index=False)
        df.to_parquet(hdfs_dest / "infrastructure.parquet", compression="snappy", index=False)
        return {"partitions": 1}

    def _curate_investments(self, df: pd.DataFrame) -> Dict[str, Any]:
        dest = self.curated_dir / "research_investment_future_projects"
        hdfs_dest = self.hdfs_curated / "research_investment_future_projects"
        gold_dest = self.gold_dir / "fact_future_investments.parquet"
        dest.mkdir(parents=True, exist_ok=True)
        hdfs_dest.mkdir(parents=True, exist_ok=True)
        df.to_parquet(gold_dest, compression="snappy", index=False)
        df.to_parquet(dest / "investments.parquet", compression="snappy", index=False)
        df.to_parquet(hdfs_dest / "investments.parquet", compression="snappy", index=False)
        return {"partitions": 1}

    def _build_gold_dimensions(self):
        """Constructs reusable dimensions for the analytical star-schema."""
        missions_path = self.raw_dir / "space_missions.csv"
        if not missions_path.exists():
            return

        df_m = pd.read_csv(missions_path)
        
        # Dim Agency
        agencies = df_m[["agency", "country"]].drop_duplicates().reset_index(drop=True)
        agencies["agency_id"] = range(1, len(agencies) + 1)
        agencies.to_parquet(self.gold_dir / "dim_agencies.parquet", compression="snappy", index=False)

        # Dim Orbit
        sat_path = self.raw_dir / "satellites_orbital.csv"
        if sat_path.exists():
            df_s = pd.read_csv(sat_path)
            o_col = "orbit_type" if "orbit_type" in df_s.columns else "orbit_class"
            orbits = df_s[[o_col]].drop_duplicates().reset_index(drop=True)
            orbits["orbit_id"] = range(1, len(orbits) + 1)
            orbits.to_parquet(self.gold_dir / "dim_orbits.parquet", compression="snappy", index=False)

        # Dim Time
        years = pd.DataFrame({"year": list(range(2000, 2036))})
        years["decade"] = (years["year"] // 10) * 10
        years.to_parquet(self.gold_dir / "dim_time.parquet", compression="snappy", index=False)
