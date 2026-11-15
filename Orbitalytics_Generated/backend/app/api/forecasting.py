"""
Orbitalytics - Demand Forecasting API Router
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional
from app.services.demand_forecaster import DemandForecaster
from app.services.scenario_service import ScenarioService
from app.schemas.forecasting import ForecastRequest, ScenarioRequest

router = APIRouter(prefix="/forecasting", tags=["Forecasting"])
forecaster = DemandForecaster()
scenario_service = ScenarioService()

@router.get("/targets")
def get_targets():
    return forecaster.get_supported_targets()

@router.get("/models")
def get_models():
    return [
        {"id": "RandomForest", "name": "Random Forest Regressor (Ensemble)", "type": "Machine Learning"},
        {"id": "GradientBoosting", "name": "Gradient Boosting Regressor (GBM)", "type": "Machine Learning"},
        {"id": "ExponentialSmoothing", "name": "Exponential Smoothing (Holt-Winters)", "type": "Statistical"},
        {"id": "MovingAverage", "name": "6-Month Historical Moving Average", "type": "Baseline"},
        {"id": "LinearTrend", "name": "Linear & Cyclical Trend Regression", "type": "Parametric"}
    ]

@router.get("/predict")
def predict_get(
    target: str = Query("equipment", description="Options: equipment, launches, satellites, expenditures, resources"),
    horizon_months: int = Query(12, description="3, 6, 12, 36"),
    model: str = Query("RandomForest", description="Algorithm model"),
    agency: Optional[str] = Query(None)
):
    try:
        return forecaster.predict(target=target, horizon_months=horizon_months, model_name=model, agency=agency)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict")
def predict_post(req: ForecastRequest):
    try:
        return forecaster.predict(target=req.target, horizon_months=req.horizon_months, model_name=req.model, agency=req.agency)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/scenario")
def run_scenario(req: ScenarioRequest):
    try:
        return scenario_service.run_scenario(
            target=req.target,
            horizon_months=req.horizon_months,
            investment_growth_pct=req.investment_growth_pct,
            launch_activity_growth_pct=req.launch_activity_growth_pct,
            cost_variation_pct=req.cost_variation_pct
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

