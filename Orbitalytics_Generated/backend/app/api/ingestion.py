"""
Orbitalytics - Ingestion API Router
"""
from fastapi import APIRouter, HTTPException
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])
service = IngestionService()

@router.post("/run")
def run_ingestion():
    try:
        return service.run_full_ingestion_and_curation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

