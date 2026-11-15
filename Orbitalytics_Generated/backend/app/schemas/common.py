"""
Orbitalytics - Common Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class APIResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Optional[Any] = None

class DateRangeFilter(BaseModel):
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    agency: Optional[str] = None
    country: Optional[str] = None

