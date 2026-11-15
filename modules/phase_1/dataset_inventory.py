"""
ORBITALYTICS - Phase 1 Dataset Inventory
Catalogs all datasets across raw, reference, validated, rejected, staging, and processed layers.
Extracts row counts, byte sizes, column counts, data origins, and domain classifications.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from modules.phase_1.schema_registry import SchemaRegistry

class DatasetInventory:
    def __init__(self, base_dir: Path = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parent.parent.parent
        self.datasets_dir = self.base_dir / "datasets"
        self.metadata_dir = self.datasets_dir / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def scan_inventory(self) -> Dict[str, Any]:
        """
        Scans all dataset directories and builds comprehensive catalog.
        """
        inventory: Dict[str, List[Dict[str, Any]]] = {
            "reference": [],
            "raw_public": [],
            "raw_synthetic": [],
            "raw_existing": [],
            "validated": [],
            "rejected": [],
            "processed": []
        }

        scan_targets = [
            ("reference", self.datasets_dir / "reference", "**/*.csv"),
            ("raw_public", self.datasets_dir / "raw" / "public", "*.csv"),
            ("raw_synthetic", self.datasets_dir / "raw" / "synthetic", "*.csv"),
            ("raw_existing", self.datasets_dir / "raw" / "existing", "*.csv"),
            ("validated", self.datasets_dir / "validated", "*.csv"),
            ("rejected", self.datasets_dir / "rejected", "*.csv"),
            ("processed", self.datasets_dir / "processed", "*.csv")
        ]

        total_files = 0
        total_rows = 0

        for category, path, pattern in scan_targets:
            if not path.exists():
                continue
            for file_path in path.glob(pattern):
                try:
                    df = pd.read_csv(file_path, low_memory=False)
                    rows, cols = df.shape
                    origin = df["data_origin"].iloc[0] if "data_origin" in df.columns and len(df) > 0 else ("real" if "public" in str(file_path) else "synthetic")
                    base_name = file_path.stem.replace("_validated", "").replace("_cleaned", "").replace("_rejected", "")
                    domain = SchemaRegistry.get_domain(base_name) if base_name in SchemaRegistry.list_datasets() else "Reference / Master Data"

                    entry = {
                        "filename": file_path.name,
                        "relative_path": str(file_path.relative_to(self.base_dir)),
                        "category": category,
                        "rows": rows,
                        "columns": cols,
                        "size_bytes": file_path.stat().st_size,
                        "data_origin": origin,
                        "domain": domain,
                        "sample_columns": list(df.columns)[:8]
                    }
                    inventory[category].append(entry)
                    total_files += 1
                    total_rows += rows
                except Exception as e:
                    inventory[category].append({
                        "filename": file_path.name,
                        "relative_path": str(file_path.relative_to(self.base_dir)),
                        "error": str(e)
                    })

        result = {
            "total_files": total_files,
            "total_records_cataloged": total_rows,
            "categories": {k: len(v) for k, v in inventory.items()},
            "inventory": inventory
        }

        with open(self.metadata_dir / "dataset_inventory.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result

