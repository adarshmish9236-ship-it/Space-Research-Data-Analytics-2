"""
Orbitalytics - Demand Forecasting Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ForecastRequest(BaseModel):
    target: str = Field("equipment", description="Forecast target dimension (equipment, launches, satellites, expenditures, resources)")
    horizon_months: int = Field(12, description="Horizon in months: 3, 6, 12, 36")
    model: str = Field("RandomForest", description="Algorithm: RandomForest, GradientBoosting, ExponentialSmoothing, MovingAverage, LinearTrend")
    agency: Optional[str] = None
    country: Optional[str] = None

class ForecastEvaluation(BaseModel):
    mae: float
    rmse: float
    r2_score: float
    mape: float
    smape: float
    accuracy_pct: float

class ForecastPoint(BaseModel):
    date: str
    year: int
    month: int
    predicted_value: float
    lower_bound_95: float
    upper_bound_95: float
    growth_rate_pct: float

class ForecastHistoricalPoint(BaseModel):
    date: str
    actual_value: float

class ForecastResponse(BaseModel):
    target: str
    target_display_name: str
    unit: str
    model_used: str
    horizon_months: int
    last_historical_date: str
    evaluation_metrics: ForecastEvaluation
    feature_importance: Dict[str, float]
    historical_actuals: List[ForecastHistoricalPoint]
    future_forecasts: List[ForecastPoint]
    summary: Dict[str, Any]

class ScenarioRequest(BaseModel):
    target: str = "equipment"
    horizon_months: int = 12
    investment_growth_pct: float = 0.0
    launch_activity_growth_pct: float = 0.0
    cost_variation_pct: float = 0.0

