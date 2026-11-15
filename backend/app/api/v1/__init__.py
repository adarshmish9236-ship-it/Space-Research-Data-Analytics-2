"""
ORBITALYTICS Phase 11 — API v1 Root Router
Aggregates routers for all 8 core platform modules.
"""

from fastapi import APIRouter

from app.api.v1.overview import router as overview_router
from app.api.v1.data_management import router as data_mgmt_router
from app.api.v1.ecosystem import router as ecosystem_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.forecasting import router as forecasting_router
from app.api.v1.optimization import router as optimization_router
from app.api.v1.benchmarks import router as benchmarks_router
from app.api.v1.reports import router as reports_router

api_v1_router = APIRouter()

api_v1_router.include_router(overview_router)
api_v1_router.include_router(data_mgmt_router)
api_v1_router.include_router(ecosystem_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(forecasting_router)
api_v1_router.include_router(optimization_router)
api_v1_router.include_router(benchmarks_router)
api_v1_router.include_router(reports_router)
