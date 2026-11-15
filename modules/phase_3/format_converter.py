"""
Orbitalytics Phase 3: File Format Strategy & Compression
Converts tabular datasets to Snappy-compressed columnar Parquet files.
"""

import io
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from typing import Dict, Any, Tuple

class FormatConverter:
    """Manages format transformations and Snappy compression benchmarks."""

    @staticmethod
    def to_snappy_parquet(df: pd.DataFrame) -> bytes:
        """Converts a pandas DataFrame into Snappy-compressed Parquet bytes."""
        table = pa.Table.from_pandas(df, preserve_index=False)
        sink = io.BytesIO()
        pq.write_table(
            table,
            sink,
            compression="snappy",
            flavor="spark"
        )
        return sink.getvalue()

    @classmethod
    def benchmark_compression(cls, df: pd.DataFrame, csv_bytes: int) -> Dict[str, Any]:
        """Calculates compression metrics between raw CSV and Snappy Parquet."""
        parquet_bytes = len(cls.to_snappy_parquet(df))
        savings_pct = round(((csv_bytes - parquet_bytes) / csv_bytes) * 100, 2) if csv_bytes > 0 else 0.0
        ratio = round(csv_bytes / parquet_bytes, 2) if parquet_bytes > 0 else 1.0

        return {
            "raw_csv_bytes": csv_bytes,
            "snappy_parquet_bytes": parquet_bytes,
            "compression_ratio": f"{ratio}:1",
            "space_savings_pct": savings_pct,
            "compression_codec": "SNAPPY",
            "column_count": len(df.columns),
            "record_count": len(df)
        }

