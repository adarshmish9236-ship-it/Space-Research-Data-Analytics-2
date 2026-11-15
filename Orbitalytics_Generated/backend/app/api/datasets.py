"""
Orbitalytics - Datasets & Explorer API Router
"""
import json
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import FileResponse
from typing import Optional

from app.core.config import settings
from app.services.data_validation_service import DataValidationService
from app.utils.data_helpers import paginate_dataframe
from app.utils.file_utils import format_bytes

router = APIRouter(prefix="/datasets", tags=["Datasets"])
validator = DataValidationService()

DATASET_DISPLAY_NAMES = {
    "space_missions": ("Space Missions Catalog", "Global scientific & exploration flights", "space_missions.csv"),
    "satellites_orbital": ("Satellite Constellations & Orbital Data", "Orbital mechanics and operational satellite payloads", "satellites_orbital.csv"),
    "launch_activities": ("Launch Activities & Vehicle Operations", "Rocket flights, costs, spaceports, and outcomes", "launch_activities.csv"),
    "equipment_component_demand": ("Space Equipment & Component Demand", "Monthly component demand, lead times, and shortage risks", "equipment_component_demand.csv"),
    "agency_research_expenditures": ("Space Agency Research Expenditures", "Monthly R&D, infrastructure, and ops expenditures", "agency_research_expenditures.csv"),
    "resource_consumption": ("Critical Resource Consumption", "Propellants, LOX, LH2, telemetry, and solar arrays", "resource_consumption.csv"),
    "satellite_manufacturing_requirements": ("Satellite Manufacturing Requirements", "Assembly orders, cleanroom hours, and shortage projections", "satellite_manufacturing_requirements.csv"),
    "space_infrastructure_requirements": ("Space Infrastructure Requirements", "Tracking antennas, cryogenic depots, and cleanrooms", "space_infrastructure_requirements.csv"),
    "research_investment_future_projects": ("Future Research Investment Projects", "Strategic multi-year roadmaps (Artemis, Mars Sample Return)", "research_investment_future_projects.csv")
}

@router.get("")
def list_datasets():
    datasets = []
    for name, (disp, desc, fname) in DATASET_DISPLAY_NAMES.items():
        fpath = settings.RAW_DATA_DIR / fname
        row_cnt = 0
        sz_bytes = 0
        if fpath.exists():
            sz_bytes = fpath.stat().st_size
            try:
                # fast line count
                with open(fpath, "r", encoding="utf-8") as f:
                    row_cnt = max(0, sum(1 for _ in f) - 1)
            except Exception:
                row_cnt = 0
        
        datasets.append({
            "name": name,
            "display_name": disp,
            "description": desc,
            "file_name": fname,
            "record_count": row_cnt,
            "size_formatted": format_bytes(sz_bytes),
            "data_source": "Orbitalytics Verified Lakehouse Schema",
            "is_synthetic": True,
            "curated_format": "Apache Parquet"
        })
    return datasets

@router.get("/{dataset_name}/metadata")
def get_dataset_metadata(dataset_name: str):
    if dataset_name not in DATASET_DISPLAY_NAMES:
        raise HTTPException(status_code=404, detail="Dataset not found")
    disp, desc, fname = DATASET_DISPLAY_NAMES[dataset_name]
    fpath = settings.RAW_DATA_DIR / fname
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="Dataset file not found on disk")
    
    df = pd.read_csv(fpath, nrows=5)
    cols = [{"name": c, "type": str(df[c].dtype)} for c in df.columns]
    
    return {
        "name": dataset_name,
        "display_name": disp,
        "description": desc,
        "file_name": fname,
        "size_bytes": fpath.stat().st_size,
        "size_formatted": format_bytes(fpath.stat().st_size),
        "columns": cols
    }

@router.get("/{dataset_name}/preview")
def preview_dataset(
    dataset_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=100),
    search: Optional[str] = None
):
    if dataset_name not in DATASET_DISPLAY_NAMES:
        raise HTTPException(status_code=404, detail="Dataset not found")
    _, _, fname = DATASET_DISPLAY_NAMES[dataset_name]
    fpath = settings.RAW_DATA_DIR / fname
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="Dataset file not found")
    
    df = pd.read_csv(fpath)
    if search:
        mask = df.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        df = df[mask]
        
    return paginate_dataframe(df, page=page, page_size=page_size)

@router.get("/{dataset_name}/quality")
def get_dataset_quality(dataset_name: str):
    return validator.validate_dataset(dataset_name)

@router.get("/{dataset_name}/download")
def download_dataset(dataset_name: str):
    if dataset_name not in DATASET_DISPLAY_NAMES:
        raise HTTPException(status_code=404, detail="Dataset not found")
    _, _, fname = DATASET_DISPLAY_NAMES[dataset_name]
    fpath = settings.RAW_DATA_DIR / fname
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="Dataset file not found")
    return FileResponse(str(fpath), media_type="text/csv", filename=fname)

