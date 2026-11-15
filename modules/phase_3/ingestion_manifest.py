"""
Orbitalytics Phase 3: Data Ingestion Metadata Registry
Tracks Ingestion IDs, Provenance, Checksums, and Processing Status
"""

import json
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

class IngestionRecord:
    """Represents a single atomic dataset ingestion event."""

    def __init__(
        self,
        dataset_name: str,
        domain: str,
        source_filename: str,
        data_origin: str,
        record_count: int,
        raw_file_size_bytes: int,
        schema_version: str = "1.0.0",
        data_format: str = "CSV",
        validation_status: str = "VALIDATED",
        processing_status: str = "SUCCESS",
        bronze_path: str = "",
        silver_path: str = "",
        partition_keys: Optional[List[str]] = None,
        partition_count: int = 1,
        md5_checksum: str = "",
        sha256_checksum: str = "",
        error_details: Optional[str] = None
    ):
        self.ingestion_id = f"ING-{uuid.uuid4().hex[:12].upper()}"
        self.dataset_name = dataset_name
        self.domain = domain
        self.source_filename = source_filename
        self.data_origin = data_origin
        self.ingestion_timestamp = datetime.now(timezone.utc).isoformat()
        self.record_count = record_count
        self.raw_file_size_bytes = raw_file_size_bytes
        self.schema_version = schema_version
        self.data_format = data_format
        self.validation_status = validation_status
        self.processing_status = processing_status
        self.bronze_path = bronze_path
        self.silver_path = silver_path
        self.partition_keys = partition_keys or []
        self.partition_count = partition_count
        self.md5_checksum = md5_checksum
        self.sha256_checksum = sha256_checksum
        self.error_details = error_details

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ingestion_id": self.ingestion_id,
            "dataset_name": self.dataset_name,
            "domain": self.domain,
            "source_filename": self.source_filename,
            "data_origin": self.data_origin,
            "ingestion_timestamp": self.ingestion_timestamp,
            "record_count": self.record_count,
            "raw_file_size_bytes": self.raw_file_size_bytes,
            "schema_version": self.schema_version,
            "data_format": self.data_format,
            "validation_status": self.validation_status,
            "processing_status": self.processing_status,
            "bronze_path": self.bronze_path,
            "silver_path": self.silver_path,
            "partition_keys": self.partition_keys,
            "partition_count": self.partition_count,
            "md5_checksum": self.md5_checksum,
            "sha256_checksum": self.sha256_checksum,
            "error_details": self.error_details
        }


class IngestionManifest:
    """Persistent catalog storing all lakehouse ingestion transactions."""

    def __init__(self, manifest_file: Optional[Path] = None):
        self.manifest_file = manifest_file or Path("E:/PROJECTS/BDT/datasets/metadata/ingestion_manifest.json")
        self.records: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.records = data.get("ingestions", [])
            except Exception:
                self.records = []
        else:
            self.records = []

    def save(self):
        self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "manifest_version": "1.0.0",
            "lakehouse": "HDFS /orbitalytics",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_ingestions": len(self.records),
            "ingestions": self.records
        }
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def add_record(self, record: IngestionRecord):
        self.records.append(record.to_dict())
        self.save()

    def find_by_checksum(self, md5_hash: str) -> Optional[Dict[str, Any]]:
        for r in self.records:
            if r.get("md5_checksum") == md5_hash and r.get("processing_status") == "SUCCESS":
                return r
        return None

    def get_summary(self) -> Dict[str, Any]:
        total_records = sum(r.get("record_count", 0) for r in self.records)
        total_bytes = sum(r.get("raw_file_size_bytes", 0) for r in self.records)
        successful = sum(1 for r in self.records if r.get("processing_status") == "SUCCESS")
        failed = sum(1 for r in self.records if r.get("processing_status") == "FAILED")
        quarantined = sum(1 for r in self.records if r.get("validation_status") == "QUARANTINED")

        return {
            "total_ingestion_jobs": len(self.records),
            "successful_ingestions": successful,
            "failed_ingestions": failed,
            "quarantined_ingestions": quarantined,
            "total_records_ingested": total_records,
            "total_raw_bytes_ingested": total_bytes,
            "last_ingestion_time": self.records[-1]["ingestion_timestamp"] if self.records else None
        }

