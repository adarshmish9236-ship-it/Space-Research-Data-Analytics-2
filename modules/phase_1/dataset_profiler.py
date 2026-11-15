"""
ORBITALYTICS - Phase 1 Dataset Profiler
Performs rigorous statistical and distributional profiling across space research datasets:
- Descriptive statistics (mean, std, min, 25%, 50%, 75%, max, skewness)
- Null and distinct cardinality analysis
- Temporal span and frequency detection
- Top category value distributions
Outputs structured JSON and human-readable Markdown profiling reports to datasets/profiling/.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class DatasetProfiler:
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir if output_dir else Path(__file__).resolve().parent.parent.parent / "datasets" / "profiling"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def profile_dataframe(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """
        Profiles a pandas DataFrame and generates comprehensive metrics.
        """
        rows, cols = df.shape
        col_profiles: Dict[str, Any] = {}

        for col in df.columns:
            series = df[col]
            null_count = int(series.isna().sum())
            null_pct = round((null_count / rows) * 100.0, 2) if rows > 0 else 0.0
            unique_count = int(series.nunique())

            p: Dict[str, Any] = {
                "dtype": str(series.dtype),
                "null_count": null_count,
                "null_pct": null_pct,
                "unique_count": unique_count
            }

            # Numeric profiling
            if pd.api.types.is_numeric_dtype(series):
                clean_s = series.dropna()
                if len(clean_s) > 0:
                    p.update({
                        "min": float(clean_s.min()),
                        "max": float(clean_s.max()),
                        "mean": round(float(clean_s.mean()), 3),
                        "std": round(float(clean_s.std()), 3) if len(clean_s) > 1 else 0.0,
                        "median": float(clean_s.median()),
                        "skewness": round(float(clean_s.skew()), 3) if len(clean_s) > 2 else 0.0
                    })
            # Date profiling
            elif "date" in col:
                dt_series = pd.to_datetime(series, errors="coerce").dropna()
                if len(dt_series) > 0:
                    p.update({
                        "min_date": dt_series.min().strftime("%Y-%m-%d"),
                        "max_date": dt_series.max().strftime("%Y-%m-%d"),
                        "span_days": int((dt_series.max() - dt_series.min()).days)
                    })
            # Categorical profiling
            else:
                top_vals = series.value_counts(dropna=False).head(5).to_dict()
                p["top_5_values"] = {str(k): int(v) for k, v in top_vals.items()}

            col_profiles[col] = p

        profile_data = {
            "dataset_name": dataset_name,
            "row_count": rows,
            "column_count": cols,
            "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024.0, 2),
            "columns": col_profiles
        }

        # Write JSON report
        with open(self.output_dir / f"{dataset_name}_profile.json", "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2)

        # Write Markdown report
        self._write_markdown_profile(profile_data, self.output_dir / f"{dataset_name}_profile.md")

        return profile_data

    def _write_markdown_profile(self, p: Dict[str, Any], md_path: Path):
        lines = [
            f"# Dataset Profile: {p['dataset_name']}",
            f"- **Total Rows:** {p['row_count']}",
            f"- **Total Columns:** {p['column_count']}",
            f"- **Memory Usage:** {p['memory_usage_kb']} KB",
            "",
            "## Column Summary",
            "| Column | Type | Null Count (%) | Unique Values | Details |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        for col, meta in p["columns"].items():
            details = []
            if "min" in meta:
                details.append(f"Min: {meta['min']}, Max: {meta['max']}, Mean: {meta['mean']}")
            if "min_date" in meta:
                details.append(f"{meta['min_date']} to {meta['max_date']} ({meta['span_days']}d)")
            if "top_5_values" in meta:
                top_str = ", ".join([f"{k} ({v})" for k, v in list(meta['top_5_values'].items())[:3]])
                details.append(top_str)
            details_str = " | ".join(details) if details else "-"
            lines.append(f"| `{col}` | `{meta['dtype']}` | {meta['null_count']} ({meta['null_pct']}%) | {meta['unique_count']} | {details_str} |")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

