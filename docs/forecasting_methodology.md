# ORBITALYTICS 2.0 — Advanced Time-Series Forecasting Methodology

---

## 1. Mathematical Formulation & Target Definitions

The ORBITALYTICS forecasting engine models future demand for mission-critical satellite hardware components and propellant resources. The primary target is quarterly demand:
$$Y_t = f(Y_{t-1}, Y_{t-2}, \dots, Y_{t-p}, \mathbf{X}_t) + \varepsilon_t$$
where $Y_t$ represents component unit demand or resource consumption in quarter $t$, $\mathbf{X}_t$ is an exogenous feature vector (e.g., active satellites in orbit, agency budget appropriations, secular time indices), and $\varepsilon_t \sim \mathcal{N}(0, \sigma^2)$ is white-noise innovation.

### Default Target Parameters:
- **Primary Domain:** Satellite Component Demand (Units).
- **Secondary Domain:** Propellant & Cryogenic Consumption (Metric Tons).
- **Temporal Frequency:** Quarterly aggregated ($s = 4$).
- **Historical Observations:** 67 quarters (2010 Q1 through 2026 Q3).
- **Forecast Horizon:** Four quarters forward ($H = 4$: 2026 Q4 to 2027 Q3).

---

## 2. Model Family Taxonomy

ORBITALYTICS benchmarks 13 distinct forecasting algorithms across four algorithmic families:

### 2.1 Baseline Models
1. **Naive Forecast:** $\hat{Y}_{t+h|t} = Y_t$ (Persistence baseline).
2. **Seasonal Naive:** $\hat{Y}_{t+h|t} = Y_{t+h-4k}$ where $k$ is the smallest integer ensuring the index falls within the historical sample.
3. **Moving Average (k=4):** $\hat{Y}_{t+h|t} = \frac{1}{4} \sum_{i=0}^3 Y_{t-i}$.
4. **Linear Regression Baseline:** $\hat{Y}_{t+h|t} = \hat{\beta}_0 + \hat{\beta}_1 (t+h)$ fitted via Ordinary Least Squares.

### 2.2 Classical Statistical Models
5. **ARIMA(1,1,1):** Non-seasonal auto-regressive moving average with first-order differencing:
   $$(1 - \phi_1 B)(1 - B) Y_t = c + (1 + \theta_1 B) \varepsilon_t$$
6. **SARIMA(1,1,1)x(1,0,0)[4]:** Seasonal autoregressive integrated moving average capturing quarterly annual seasonality ($s = 4$):
   $$(1 - \phi_1 B)(1 - \Phi_1 B^4)(1 - B) Y_t = c + (1 + \theta_1 B) \varepsilon_t$$
7. **Simple Exponential Smoothing (SES):** $\hat{Y}_{t+1|t} = \alpha Y_t + (1 - \alpha) \hat{Y}_{t|t-1}$ with optimal parameter $\alpha \in (0, 1)$.
8. **Holt-Winters Additive:** Triple exponential smoothing decomposing level $(\ell_t)$, additive trend $(b_t)$, and seasonal components $(s_t)$:
   $$\ell_t = \alpha(Y_t - s_{t-m}) + (1-\alpha)(\ell_{t-1} + b_{t-1})$$
   $$b_t = \beta(\ell_t - \ell_{t-1}) + (1-\beta)b_{t-1}$$
   $$s_t = \gamma(Y_t - \ell_{t-1} - b_{t-1}) + (1-\gamma)s_{t-m}$$
   $$\hat{Y}_{t+h|t} = \ell_t + h b_t + s_{t-m + (h \pmod m)}$$

### 2.3 Machine Learning Ensembles
9. **Random Forest Regressor:** Non-linear ensemble of 150 bagged decision trees trained on 23 autoregressive lag and rolling window features.
10. **XGBoost Regressor:** Gradient boosted decision trees optimizing regularized objective function:
    $$\mathcal{L} = \sum_i l(\hat{y}_i, y_i) + \sum_k \left( \gamma T_k + \frac{1}{2} \lambda \|\mathbf{w}_k\|^2 \right)$$
11. **Gradient Boosting Regressor (sklearn):** Sequential shallow tree boosting optimizing Huber loss with learning rate $\eta = 0.05$.

### 2.4 Distributed Cluster Models
12. **Spark MLlib RandomForestRegressor:** Distributed tree ensembles fitted across YARN cluster nodes on HDFS Gold data.
13. **Spark MLlib GBTRegressor:** Distributed gradient boosting fitted across worker partitions.

---

## 3. Evaluation Protocol: Chronological Rolling-Origin Backtesting

To completely prevent target leakage, data shuffling is strictly prohibited. The backtester uses an **expanding window** evaluation strategy:
- **Initial Training Window:** 44 quarters (11 years: 2010 Q1 – 2020 Q4).
- **Step Size:** 4 quarters per fold.
- **Evaluation Folds:** Fold 1 (2021), Fold 2 (2022), Fold 3 (2023), Fold 4 (2024), Fold 5 (2025).
- **Non-Overlap Invariant:** For every fold $k$, $\max(\text{train\_indices}) < \min(\text{test\_indices})$.

---

## 4. Evaluation Metrics & Formulation

1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|$$
2. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2}$$
3. **Weighted Absolute Percentage Error (WAPE %):**
   $$\text{WAPE} = \frac{\sum_{i=1}^N |y_i - \hat{y}_i|}{\sum_{i=1}^N y_i} \times 100\%$$
4. **Mean Absolute Percentage Error (MAPE %):**
   $$\text{MAPE} = \frac{1}{N} \sum_{i=1}^N \frac{|y_i - \hat{y}_i|}{\max(y_i, 1.0)} \times 100\%$$
5. **Forecast Bias (%):**
   $$\text{Bias} = \frac{\sum_{i=1}^N (\hat{y}_i - y_i)}{\sum_{i=1}^N y_i} \times 100\%$$
6. **Coefficient of Determination ($R^2$):**
   $$R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2}$$

---

## 5. Confidence Interval Calculation (80% and 95%)

Uncertainty bounds around point predictions $\hat{Y}_{t+h}$ are computed using out-of-sample residual variance $\hat{\sigma}_e$:
$$\text{CI}_{1-\alpha}(h) = \left[ \max\left(0, \hat{Y}_{t+h} - z_{1-\alpha/2} \cdot \hat{\sigma}_e \sqrt{h}\right), \; \hat{Y}_{t+h} + z_{1-\alpha/2} \cdot \hat{\sigma}_e \sqrt{h} \right]$$
where $z_{0.975} = 1.96$ for the 95% interval and $z_{0.90} = 1.28$ for the 80% interval. The scaling term $\sqrt{h}$ accounts for compounding multi-step horizon variance.
