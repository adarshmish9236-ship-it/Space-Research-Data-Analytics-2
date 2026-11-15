from fastapi import APIRouter
from .overview import router as overview_router
from .analytics import router as analytics_router
from .datasets import router as datasets_router
from .ingestion import router as ingestion_router
from .forecasting import router as forecasting_router
from .hdfs import router as hdfs_router
from .hive import router as hive_router
from .mapreduce import router as mapreduce_router
from .spark import router as spark_router
from .pipeline import router as pipeline_router
from .reports import router as reports_router
from .system import router as system_router

api_router = APIRouter(prefix="/api")
api_router.include_router(overview_router)
api_router.include_router(analytics_router)
api_router.include_router(datasets_router)
api_router.include_router(ingestion_router)
api_router.include_router(forecasting_router)
api_router.include_router(hdfs_router)
api_router.include_router(hive_router)
api_router.include_router(mapreduce_router)
api_router.include_router(spark_router)
api_router.include_router(pipeline_router)
api_router.include_router(reports_router)
api_router.include_router(system_router)

