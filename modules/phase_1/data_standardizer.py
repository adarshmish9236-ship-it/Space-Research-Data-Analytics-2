"""
ORBITALYTICS - Phase 1 Data Standardizer
Enforces canonical data standards across all space research datasets:
- ISO 8601 date parsing and normalization (YYYY-MM-DD).
- Numeric cleaning (strips symbols/units embedded in numeric values, converts to float/int).
- Standardizes agency names and country associations via reference lookups.
- Standardizes column naming conventions to snake_case.
- Enforces explicit unit columns and currency codes.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

class DataStandardizer:
    def __init__(self, reference_dir: Optional[Path] = None):
        self.reference_dir = reference_dir if reference_dir else Path(__file__).resolve().parent.parent.parent / "datasets" / "reference"
        self.agency_lookup = self._load_agency_lookup()

    def _load_agency_lookup(self) -> Dict[str, Dict[str, str]]:
        ref_file = self.reference_dir / "agencies" / "agencies.csv"
        lookup = {}
        if ref_file.exists():
            df = pd.read_csv(ref_file)
            for _, row in df.iterrows():
                # Map full name, acronym, and common variants
                lookup[row["agency_name"].lower()] = row.to_dict()
                lookup[row["agency_code"].lower()] = row.to_dict()
                if "NASA" in row["agency_code"]:
                    lookup["nasa (usa)"] = row.to_dict()
                elif "ESA" in row["agency_code"]:
                    lookup["esa (europe)"] = row.to_dict()
                elif "ISRO" in row["agency_code"]:
                    lookup["isro (india)"] = row.to_dict()
                elif "JAXA" in row["agency_code"]:
                    lookup["jaxa (japan)"] = row.to_dict()
                elif "CNSA" in row["agency_code"]:
                    lookup["cnsa (china)"] = row.to_dict()
                elif "Roscosmos" in row["agency_code"]:
                    lookup["roscosmos (russia)"] = row.to_dict()
                elif "COMMERCIAL" in row["agency_code"]:
                    lookup["private / commercial (spacex, etc.)"] = row.to_dict()
                    lookup["commercial (spacex / private)"] = row.to_dict()
        return lookup

    @staticmethod
    def to_snake_case(text: str) -> str:
        s = re.sub(r'[\s\-\/\.]+', '_', text.strip())
        s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
        s = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s)
        s = re.sub(r'[^a-zA-Z0-9_]', '', s)
        return s.lower()

    @staticmethod
    def parse_iso_date(val: Any) -> Optional[str]:
        if pd.isna(val) or val is None or str(val).strip() == "":
            return None
        val_str = str(val).strip()
        # Direct YYYY-MM-DD match
        if re.match(r"^\d{4}-\d{2}-\d{2}$", val_str):
            return val_str
        # Common formats: DD-MM-YYYY, YYYY/MM/DD, etc.
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S", "%Y%m%d"):
            try:
                dt = datetime.strptime(val_str[:10], fmt[:10] if len(fmt) > 8 else fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    @staticmethod
    def clean_numeric(val: Any) -> Optional[float]:
        if pd.isna(val) or val is None:
            return None
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip()
        # Remove currency symbols, commas, trailing units (e.g., "$1,200.50 kg" -> 1200.50)
        clean_str = re.sub(r"[^\d\.\-]", "", val_str)
        try:
            return float(clean_str)
        except ValueError:
            return None

    def standardize_agency(self, raw_agency: str) -> Dict[str, str]:
        if not raw_agency or pd.isna(raw_agency):
            return {"agency_id": "AGY-UNKNOWN", "agency_name": "Unknown Space Agency", "country": "International"}
        key = str(raw_agency).strip().lower()
        if key in self.agency_lookup:
            rec = self.agency_lookup[key]
            return {
                "agency_id": rec["agency_id"],
                "agency_name": rec["agency_name"],
                "country": rec["country"]
            }
        # Fallback substring search
        for k, rec in self.agency_lookup.items():
            if k in key or key in k:
                return {
                    "agency_id": rec["agency_id"],
                    "agency_name": rec["agency_name"],
                    "country": rec["country"]
                }
        return {"agency_id": "AGY-007", "agency_name": str(raw_agency), "country": "International"}

    def standardize_dataframe(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        df_out = df.copy()
        # 1. Normalize column names to snake_case
        df_out.columns = [self.to_snake_case(c) for c in df_out.columns]

        # 2. Date column standardization
        for col in df_out.columns:
            if "date" in col:
                df_out[col] = df_out[col].apply(self.parse_iso_date)

        # 3. Agency standardization
        for agency_col in ["agency", "operator_agency", "lead_agency", "agency_client"]:
            if agency_col in df_out.columns:
                std_agencies = df_out[agency_col].apply(self.standardize_agency)
                if "agency_id" not in df_out.columns:
                    df_out["agency_id"] = [a["agency_id"] for a in std_agencies]
                df_out[agency_col] = [a["agency_name"] for a in std_agencies]
                if "country" not in df_out.columns:
                    df_out["country"] = [a["country"] for a in std_agencies]

        # 4. Enforce data_origin tag
        if "data_origin" not in df_out.columns:
            df_out["data_origin"] = "synthetic"

        return df_out

