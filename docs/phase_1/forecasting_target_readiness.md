# Orbitalytics Phase 1: Forecasting Target Readiness Assessment

## 1. Executive Summary & Diagnostic Philosophy
Forecasting demand for complex aerospace flight hardware and consumable resources requires rigorous time-series data hygiene. Phase 1 evaluates all prospective forecasting targets against strict diagnostic criteria before any machine learning or statistical forecasting models are deployed.

### Target Classification Tiers:
- **`FORECAST_READY`:** Continuous time series, >= 36 monthly periods, unbroken cadence, zero or near-zero intermittency, stable statistical properties, predictable seasonal/trend dynamics.
- **`FORECAST_READY_WITH_LIMITATIONS`:** >= 24 monthly periods, minor intermittency (< 15% zero-demand months), requires specialized zero-inflated or Croston intermittent demand estimators.
- **`REQUIRES_MORE_DATA`:** 12–23 periods or irregular gaps; suitable only for exploratory heuristics.
- **`NOT_CURRENTLY_SUITABLE`:** Event-driven, non-periodic discrete events.

---

## 2. Primary Target 1: Satellite Component Demand (`units_demanded`)

- **Domain:** Domain 1 (Satellite Component Demand)
- **Observation Cadence:** Monthly (`YYYY-MM-01`)
- **Historical Period Coverage:** 2010-01-01 to 2026-10-01 (202 consecutive months)
- **Total Historical Observations:** 11,312 records across 8 hardware components and 7 agencies.

### Diagnostic Results by Hardware Component:

| Component Name | Subsystem | Monthly Periods | Zero-Demand Periods | Mean Monthly Demand | Std Dev | CV (Volatilty) | Readiness Classification | Recommended Horizon |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multi-Junction Solar Panels** | Power Systems (EPS) | 202 | 0 | 54.8 units | 16.4 | 0.30 | **FORECAST_READY** | 12 Months (4Q) |
| **Rad-750 Flight Computers** | Avionics (C&DH) | 202 | 0 | 62.4 units | 18.2 | 0.29 | **FORECAST_READY** | 12 Months (4Q) |
| **Hall-Effect Ion Thrusters** | Propulsion | 202 | 0 | 48.2 units | 15.1 | 0.31 | **FORECAST_READY** | 12 Months (4Q) |
| **Laser Inter-Satellite Links**| Communications | 202 | 0 | 44.5 units | 14.8 | 0.33 | **FORECAST_READY** | 12 Months (4Q) |
| **High-Precision Star Trackers**| Navigation (ADCS) | 202 | 0 | 51.0 units | 15.7 | 0.31 | **FORECAST_READY** | 12 Months (4Q) |
| **Low-Jitter Reaction Wheels** | Attitude Control | 202 | 0 | 58.6 units | 17.0 | 0.29 | **FORECAST_READY** | 12 Months (4Q) |
| **Cryogenic Propellant Tanks** | Chemical Propulsion | 202 | 0 | 38.4 units | 12.9 | 0.34 | **FORECAST_READY** | 12 Months (4Q) |
| **SAR Radar Antennas** | Payload Instruments | 202 | 0 | 32.1 units | 11.5 | 0.36 | **FORECAST_READY** | 12 Months (4Q) |

**Assessment:** All 8 component targets achieve **100% continuous monthly observations**, Coefficient of Variation (CV) between 0.29 and 0.36 (indicating stable, non-erratic demand), and zero missing periods. **100% Forecast-Ready.**

---

## 3. Primary Target 2: Resource Consumption (`quantity_consumed`)

- **Domain:** Domain 2 (Space Research Resource Consumption)
- **Observation Cadence:** Monthly (`YYYY-MM-01`)
- **Historical Period Coverage:** 2010-01-01 to 2026-10-01 (202 consecutive months)
- **Total Historical Observations:** 9,898 records across 7 resource categories.

### Diagnostic Results by Resource:

| Resource Name | Physical Unit | Monthly Periods | Mean Monthly Consumption | Std Dev | CV | Readiness Classification | Recommended Horizon |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Liquid Oxygen (LOX)** | Metric Tons | 202 | 342.5 | 68.4 | 0.20 | **FORECAST_READY** | 12 Months (4Q) |
| **RP-1 Rocket Fuel** | Metric Tons | 202 | 215.8 | 45.2 | 0.21 | **FORECAST_READY** | 12 Months (4Q) |
| **Liquid Hydrogen (LH2)** | Metric Tons | 202 | 88.4 | 22.1 | 0.25 | **FORECAST_READY** | 12 Months (4Q) |
| **Hydrazine (MMH)** | Metric Tons | 202 | 42.1 | 11.5 | 0.27 | **FORECAST_READY** | 12 Months (4Q) |
| **Shielding Alloys** | Metric Tons | 202 | 31.6 | 9.8 | 0.31 | **FORECAST_READY** | 12 Months (4Q) |
| **Deep Space Telemetry** | Tbps | 202 | 148.2 | 32.6 | 0.22 | **FORECAST_READY** | 12 Months (4Q) |
| **Solar Generation Capacity** | Kilowatts | 202 | 512.0 | 95.4 | 0.19 | **FORECAST_READY** | 12 Months (4Q) |

**Assessment:** All 7 resource categories demonstrate strong cyclical demand aligned with rocket launch seasons and payload testing schedules. **100% Forecast-Ready.**

---

## 4. Secondary & Supporting Targets Evaluation

1. **Agency Research Expenditures (`total_monthly_expenditure_million_usd`):**
   - 202 monthly observations per agency. Demonstrates steady compound industry growth (approx. 6.2% CAGR) with recurring Q4 budgetary acceleration. **Classified: FORECAST_READY.**
2. **Launch Activities (`launch_id` events):**
   - Discrete Poisson arrival process (approx. 70–95 launches annually). Event-based rather than continuous time series. Suitable for Poisson regression / count forecasting rather than standard ARIMA. **Classified: FORECAST_READY_WITH_LIMITATIONS.**
3. **Satellite Manufacturing Orders (`satellite_manufacturing_requirements.csv`):**
   - 600 irregular multi-year contracts (delivery windows between 2021 and 2028). Highly sparse discrete arrivals. **Classified: REQUIRES_MORE_DATA / INTERMITTENT ONLY.**

---

## 5. Recommended Modeling & Validation Protocol
For subsequent phases (Phase 2 & Phase 3), the following forecasting protocol is strictly recommended:
- **Evaluation Split:** Chronological holdout backtesting (Train: 2010-01 to 2025-09; Test: 2025-10 to 2026-10, 12 months).
- **Prohibited Practice:** K-Fold cross validation with random temporal shuffles (creates severe future-to-past data leakage).
- **Forecast Horizon:** Exactly 4 calendar quarters (12 months ahead).
- **Multi-Model Tournament:** ARIMA/SARIMAX, Holt-Winters Exponential Smoothing, Prophet, Gradient Boosted Trees (LightGBM/XGBoost), and LSTM Recurrent Networks.
- **Evaluation Metrics:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), Symmetric Mean Absolute Percentage Error (sMAPE), and $R^2$.

