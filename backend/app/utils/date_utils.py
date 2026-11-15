"""
Orbitalytics - Date & Time Utilities
"""
from datetime import datetime, date, timedelta
from typing import Tuple
import pandas as pd
import numpy as np

def parse_iso_date(date_str: str) -> date:
    try:
        return datetime.fromisoformat(str(date_str)).date()
    except Exception:
        return datetime.strptime(str(date_str).split()[0], "%Y-%m-%d").date()

def format_year_month(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}-01"

def chronological_train_test_split(df: pd.DataFrame, time_col: str, test_ratio: float = 0.15) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Strict chronological train/test split to prevent temporal data leakage.
    Never shuffles.
    """
    sorted_df = df.sort_values(by=time_col).reset_index(drop=True)
    split_idx = int(len(sorted_df) * (1.0 - test_ratio))
    train_df = sorted_df.iloc[:split_idx].copy()
    test_df = sorted_df.iloc[split_idx:].copy()
    return train_df, test_df
