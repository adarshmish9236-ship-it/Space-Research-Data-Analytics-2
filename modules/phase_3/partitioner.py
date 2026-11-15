"""
Orbitalytics Phase 3: Partitioning Strategy
Dynamic Partition Engine for HDFS Silver Layer
"""

import re
from typing import Dict, List, Tuple
import pandas as pd

class LakehousePartitioner:
    """Partitions tabular datasets based on domain-driven access patterns.
    
    Prevents the Hadoop small-file problem by setting a minimum partition record threshold.
    """

    PARTITION_STRATEGY = {
        "missions": ["year"],
        "launches": ["year"],
        "equipment_demand": ["component_category"],
        "agency_expenditure": ["year"],
        "resource_consumption": ["resource_category"],
        "satellites": ["orbit_type"],
        "manufacturing": ["satellite_class"],
        "infrastructure": ["facility_type"],
        "research_projects": ["priority_tier"]
    }

    MIN_PARTITION_RECORDS = 5  # Partitions smaller than this are consolidated

    @classmethod
    def sanitize_val(cls, val: str) -> str:
        """Sanitizes partition values for HDFS path compatibility."""
        s = str(val).strip()
        s = re.sub(r"[^\w\-\.]", "_", s)
        return s

    @classmethod
    def partition_dataframe(cls, domain: str, df: pd.DataFrame) -> List[Tuple[str, pd.DataFrame]]:
        """Partitions a DataFrame into Hive-style directory paths (key=value).
        
        Returns a list of tuples: [(relative_hdfs_partition_path, partition_df), ...]
        """
        partition_keys = cls.PARTITION_STRATEGY.get(domain, [])
        if not partition_keys or not all(k in df.columns for k in partition_keys):
            return [("all", df)]

        # Check cardinality
        primary_col = partition_keys[0]
        unique_vals = df[primary_col].dropna().unique()

        partitions = []
        for val in unique_vals:
            part_df = df[df[primary_col] == val].copy()
            if len(part_df) < cls.MIN_PARTITION_RECORDS and len(unique_vals) > 10:
                continue  # skip outlier fragments

            clean_val = cls.sanitize_val(val)
            dir_name = f"{primary_col}={clean_val}"
            partitions.append((dir_name, part_df))

        if not partitions:
            return [("all", df)]

        return partitions

