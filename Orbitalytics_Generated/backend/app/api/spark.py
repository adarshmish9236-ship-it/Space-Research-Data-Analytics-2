"""
Orbitalytics - Apache Spark API Router
"""
from fastapi import APIRouter, HTTPException, Query
from app.services.spark_service import SparkService

router = APIRouter(prefix="/spark", tags=["Apache Spark"])
service = SparkService()

@router.post("/run")
def run_spark_job(job_name: str = Query("spark_etl_pipeline", description="Options: spark_etl_pipeline, spark_analytics, spark_forecasting_preparation")):
    try:
        return service.run_spark_job(job_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

