export interface KPIOverview {
  total_missions: number;
  total_satellites_cataloged: number;
  active_satellites_in_orbit: number;
  total_launches: number;
  launch_success_rate_pct: number;
  total_processed_records: number;
  cumulative_budget_billion_usd: number;
  total_equipment_units_demanded: number;
  pipeline_state: string;
}

export interface AutomatedInsight {
  category: string;
  headline: string;
  detail: string;
  importance: string;
  metric_value?: string;
  observation_period?: string;
}

export interface ForecastEvaluation {
  mae: number;
  rmse: number;
  r2_score: number;
  mape: number;
  smape: number;
  accuracy_pct: number;
}

export interface ForecastPoint {
  date: string;
  year: number;
  month: number;
  predicted_value: number;
  lower_bound_95: number;
  upper_bound_95: number;
  growth_rate_pct: number;
}

export interface ForecastResult {
  target: string;
  target_display_name: string;
  unit: string;
  model_used: string;
  horizon_months: number;
  last_historical_date: string;
  evaluation_metrics: ForecastEvaluation;
  feature_importance: Record<string, number>;
  historical_actuals: Array<{ date: string; actual_value: number }>;
  future_forecasts: ForecastPoint[];
  summary: {
    historical_baseline_avg: number;
    forecast_projected_avg: number;
    projected_growth_rate_pct: number;
    insight: string;
  };
}

export interface HDFSOwerview {
  cluster_status: string;
  environment_mode: string;
  active_namenodes: number;
  active_datanodes: number;
  default_block_size_mb: number;
  replication_factor: number;
  total_files: number;
  total_size_mb: number;
  total_size_formatted: string;
  simulated_hdfs_blocks: number;
  zones: Array<{
    zone_name: string;
    hdfs_path: string;
    file_count: number;
    size_formatted: string;
  }>;
}

export interface DatasetItem {
  name: string;
  display_name: string;
  description: string;
  file_name: string;
  record_count: number;
  size_formatted: string;
  data_source: string;
  is_synthetic: boolean;
  curated_format: string;
}

