"""
Orbitalytics - FastAPI Dependencies
"""
from typing import Generator
from app.core.config import settings

def get_settings():
    return settings
