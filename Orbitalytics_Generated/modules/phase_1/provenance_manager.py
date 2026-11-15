"""
ORBITALYTICS - Phase 1 Provenance Manager
Manages data provenance, lineage, data origin ('real' vs 'synthetic'), source references,
and transformation auditing across all space research datasets.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

class ProvenanceManager:
    def __init__(self, metadata_dir: Path = None):
        if metadata_dir is None:
            self.metadata_dir = Path(__file__).resolve().parent.parent.parent / "datasets" / "metadata"
        else:
            self.metadata_dir = Path(metadata_dir)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.provenance_log_file = self.metadata_dir / "data_provenance_registry.json"

    def record_provenance(
        self,
        dataset_name: str,
        data_origin: str,
        record_count: int,
        source_publisher: str,
        licence: str,
        transformation_pipeline: List[str],
        schema_version: str = "2.0.0",
        additional_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Records full provenance metadata for a dataset.
        Enforces strict compliance with data origin standards.
        """
        if data_origin not in ["real", "synthetic"]:
            raise ValueError(f"Invalid data_origin: {data_origin}. Must be 'real' or 'synthetic'.")

        record = {
            "dataset_name": dataset_name,
            "data_origin": data_origin,
            "is_synthetic": (data_origin == "synthetic"),
            "record_count": record_count,
            "source_publisher": source_publisher,
            "licence": licence,
            "schema_version": schema_version,
            "registered_at_utc": datetime.now(timezone.utc).isoformat(),
            "transformation_pipeline": transformation_pipeline,
            "metadata": additional_metadata or {}
        }

        registry = self.load_registry()
        registry[dataset_name] = record

        with open(self.provenance_log_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

        return record

    def load_registry(self) -> Dict[str, Any]:
        if not self.provenance_log_file.exists():
            return {}
        try:
            with open(self.provenance_log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def get_provenance(self, dataset_name: str) -> Dict[str, Any]:
        registry = self.load_registry()
        return registry.get(dataset_name, {
            "dataset_name": dataset_name,
            "data_origin": "unknown",
            "status": "UNREGISTERED"
        })
