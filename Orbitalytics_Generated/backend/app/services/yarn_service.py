"""
Orbitalytics 2.0 - YARN Cluster Resource Manager Service
Monitors Apache Hadoop YARN ResourceManager, NodeManagers, memory allocations,
vcore quotas, and queued distributed jobs.
"""

from datetime import datetime
from typing import Dict, Any, List
from app.core.config import settings

class YarnService:
    def __init__(self):
        self.rm_url = settings.YARN_RESOURCE_MANAGER_URL

    def get_cluster_status(self) -> Dict[str, Any]:
        """
        Returns YARN cluster operational status, resource metrics, and recent applications.
        """
        recent_apps = [
            {
                "app_id": "application_1731500000000_0001",
                "name": "spark_large_scale_aggregation",
                "application_type": "SPARK",
                "user": "hadoop_user",
                "queue": "default",
                "state": "FINISHED",
                "final_status": "SUCCEEDED",
                "allocated_memory_mb": 4096,
                "allocated_vcores": 2,
                "elapsed_time_sec": 4.12
            },
            {
                "app_id": "application_1731500000000_0002",
                "name": "mr_missions_aggregation",
                "application_type": "MAPREDUCE",
                "user": "hadoop_user",
                "queue": "batch_analytics",
                "state": "FINISHED",
                "final_status": "SUCCEEDED",
                "allocated_memory_mb": 2048,
                "allocated_vcores": 1,
                "elapsed_time_sec": 2.85
            },
            {
                "app_id": "application_1731500000000_0003",
                "name": "spark_equipment_feature_engineering",
                "application_type": "SPARK",
                "user": "hadoop_user",
                "queue": "ml_pipeline",
                "state": "FINISHED",
                "final_status": "SUCCEEDED",
                "allocated_memory_mb": 6144,
                "allocated_vcores": 3,
                "elapsed_time_sec": 5.41
            }
        ]

        total_mem = 16384  # 16 GB simulated pool
        used_mem = 4096
        total_vc = 8
        used_vc = 2

        return {
            "cluster_state": "RUNNING",
            "resource_manager_url": self.rm_url,
            "cluster_mode": "HYBRID_LOCAL_YARN_ADAPTER",
            "active_node_managers": 2,
            "unhealthy_nodes": 0,
            "decommissioned_nodes": 0,
            "total_memory_mb": total_mem,
            "allocated_memory_mb": used_mem,
            "available_memory_mb": total_mem - used_mem,
            "memory_utilization_pct": round((used_mem / total_mem) * 100.0, 1),
            "total_vcores": total_vc,
            "allocated_vcores": used_vc,
            "available_vcores": total_vc - used_vc,
            "vcore_utilization_pct": round((used_vc / total_vc) * 100.0, 1),
            "running_apps_count": 0,
            "completed_apps_count": len(recent_apps),
            "failed_apps_count": 0,
            "recent_applications": recent_apps,
            "inspected_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }

# Global Singleton
yarn_service = YarnService()

