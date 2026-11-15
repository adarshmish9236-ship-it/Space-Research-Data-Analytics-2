"""
Orbitalytics - Data Helpers & Pagination
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List

def paginate_dataframe(df: pd.DataFrame, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """Paginates DataFrame cleanly for Data Explorer table views."""
    total_records = len(df)
    total_pages = max(1, (total_records + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    
    subset = df.iloc[start_idx:end_idx].copy()
    
    # Replace NaN/inf with None for JSON compliance
    subset = subset.replace({np.nan: None, np.inf: None, -np.inf: None})
    records = subset.to_dict(orient="records")
    
    columns_meta = []
    for col in df.columns:
        dtype_str = str(df[col].dtype)
        columns_meta.append({
            "name": col,
            "type": dtype_str,
            "sample_value": None if df[col].empty else str(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else None
        })

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_records,
        "total_pages": total_pages,
        "columns": columns_meta,
        "records": records
    }

