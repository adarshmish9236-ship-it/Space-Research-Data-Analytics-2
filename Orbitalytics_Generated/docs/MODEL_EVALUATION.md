# ORBITALYTICS 2.0 — FORECASTING MODEL EVALUATION & REGISTRY

## 1. Methodology & Validation Principles

Orbitalytics 2.0 enforces strict chronological time-series validation principles:
- **Zero Data Leakage:** Preprocessing, feature engineering (lags, rolling averages), and scaling are computed exclusively from observations preceding the forecast origin ($t \le T_0$).
- **Chronological Holdout:** The dataset is partitioned chronologically (last 12 to 24 months reserved as the holdout test set). No random shuffling or future lookahead.
- **Champion/Challenger Framework:** For each forecasting target, candidate models compete on the holdout test set. The model achieving the lowest Root Mean Squared Error (RMSE) is automatically crowned Champion and registered in the Lakehouse Metadata Registry.

---

## 2. Mathematical Metric Formulations

### Mean Absolute Error (MAE)
$$MAE = \frac{1}{N} \sum_{t=1}^{N} |y_t - \hat{y}_t|$$

### Root Mean Squared Error (RMSE)
$$RMSE = \sqrt{\frac{1}{N} \sum_{t=1}^{N} (y_t - \hat{y}_t)^2}$$

### Weighted Absolute Percentage Error (WAPE)
$$WAPE = \frac{\sum_{t=1}^{N} |y_t - \hat{y}_t|}{\sum_{t=1}^{N} |y_t|} \times 100\%$$

### Symmetric Mean Absolute Percentage Error (sMAPE)
$$sMAPE = \frac{100\%}{N} \sum_{t=1}^{N} \frac{2 |y_t - \hat{y}_t|}{|y_t| + |\hat{y}_t| + \epsilon}$$

### Coefficient of Determination ($R^2$)
$$R^2 = 1 - \frac{\sum_{t=1}^{N} (y_t - \hat{y}_t)^2}{\sum_{t=1}^{N} (y_t - \bar{y})^2}$$

---

## 3. Statistically Grounded Prediction Intervals

Rather than applying arbitrary percentage margins, prediction intervals are derived from the residual standard error ($s_e$) of the fitted model:

$$s_e = \sqrt{\frac{\sum_{t=1}^{N} (y_t - \hat{y}_t)^2}{N - p}}$$

For a forecast horizon step $h \in [1, H]$, the uncertainty standard deviation expands chronologically:

$$\sigma_h = s_e \sqrt{1 + \frac{h}{H}}$$

- **90% Confidence Interval ($Z = 1.645$):**
  $$[\hat{y}_{t+h} - 1.645 \cdot \sigma_h, \quad \hat{y}_{t+h} + 1.645 \cdot \sigma_h]$$
- **95% Confidence Interval ($Z = 1.960$):**
  $$[\hat{y}_{t+h} - 1.960 \cdot \sigma_h, \quad \hat{y}_{t+h} + 1.960 \cdot \sigma_h]$$

---

## 4. Empirical Benchmark Leaderboard (Space Equipment Target)

| Model Name | Model Family | Test RMSE | MAE | WAPE (%) | $R^2$ Score | Status |
|---|---|---|---|---|---|---|
| Ridge Regression | Linear / Regularized | 15.43 | 11.20 | 4.82% | 0.656 | **CHAMPION** |
| Random Forest | Tree Ensemble | 16.85 | 12.45 | 5.21% | 0.612 | CHALLENGER |
| Gradient Boosting | Boosting Ensemble | 18.20 | 13.80 | 5.75% | 0.584 | CHALLENGER |
| Exponential Smoothing | Statistical Holt Trend | 21.40 | 16.10 | 6.80% | 0.490 | CHALLENGER |
| Moving Average | Naive Baseline | 26.50 | 20.30 | 8.55% | 0.320 | BASELINE |

