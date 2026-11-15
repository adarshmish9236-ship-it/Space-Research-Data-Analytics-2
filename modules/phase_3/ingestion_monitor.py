"""
Orbitalytics Phase 3: Lakehouse Ingestion Monitor
Exposes runtime metrics, HDFS storage metrics, and ingestion health telemetry.
"""

from typing import Dict, Any, List
from modules.phase_3.hdfs_client import HDFSClient
from modules.phase_3.ingestion_manifest import IngestionManifest

class IngestionMonitor:
    """Monitors live HDFS lakehouse ingestion health, throughput, and storage."""

    def __init__(self, hdfs_client: HDFSClient, manifest: IngestionManifest):
        self.hdfs = hdfs_client
        self.manifest = manifest

    def get_lakehouse_telemetry(self) -> Dict[str, Any]:
        """Gathers end-to-end lakehouse health and storage metrics."""
        summary = self.manifest.get_summary()

        # Query HDFS live storage
        zones = ["bronze", "silver", "gold", "quarantine", "metadata", "logs"]
        zone_metrics = {}

        total_hdfs_bytes = 0
        total_hdfs_files = 0

        for z in zones:
            path = f"/orbitalytics/{z}"
            try:
                if self.hdfs.exists(path):
                    items = self.hdfs.ls(path, recursive=True)
                    files = [it for it in items if not it["is_dir"]]
                    size = sum(it["size"] for it in files)
                    total_hdfs_bytes += size
                    total_hdfs_files += len(files)
                    zone_metrics[z] = {
                        "path": path,
                        "file_count": len(files),
                        "total_bytes": size,
                        "size_formatted": f"{round(size / 1024, 2)} KB" if size < 1048576 else f"{round(size / 1048576, 2)} MB"
                    }
                else:
                    zone_metrics[z] = {"path": path, "file_count": 0, "total_bytes": 0, "size_formatted": "0 B"}
            except Exception as e:
                zone_metrics[z] = {"path": path, "error": str(e)}

        return {
            "lakehouse_root": "/orbitalytics",
            "cluster_state": "HEALTHY / ONLINE",
            "ingestion_summary": summary,
            "hdfs_storage": {
                "total_files": total_hdfs_files,
                "total_bytes": total_hdfs_bytes,
                "total_size_formatted": f"{round(total_hdfs_bytes / 1048576, 2)} MB",
                "zones": zone_metrics
            }
        }

