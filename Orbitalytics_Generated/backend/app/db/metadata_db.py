"""
Orbitalytics 2.0 - Lakehouse Metadata & Execution Registry (SQLite Persistence)
Provides persistent storage for pipeline runs, model registry, optimization records, and audit logs.
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.core.config import settings

logger = logging.getLogger("orbitalytics.db")

class MetadataRepository:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = str(db_path or settings.DATABASE_PATH)
        self._init_tables()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Pipeline execution history
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_executions (
                job_id TEXT PRIMARY KEY,
                pipeline_name TEXT NOT NULL,
                status TEXT NOT NULL,
                execution_mode TEXT NOT NULL,
                stages_json TEXT NOT NULL,
                duration_sec REAL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                error_message TEXT
            )
            """)

            # Model Registry
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_registry (
                model_id TEXT PRIMARY KEY,
                target_name TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                model_family TEXT NOT NULL,
                version TEXT NOT NULL,
                mae REAL,
                rmse REAL,
                wape REAL,
                r2_score REAL,
                parameters_json TEXT,
                is_champion INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """)

            # Optimization Runs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS optimization_runs (
                run_id TEXT PRIMARY KEY,
                scenario_name TEXT NOT NULL,
                objective TEXT NOT NULL,
                total_budget REAL,
                total_cost REAL,
                shortage_quantity REAL,
                fulfillment_pct REAL,
                results_json TEXT,
                created_at TEXT NOT NULL
            )
            """)

            # Distributed Processing Benchmark Runs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                run_id TEXT PRIMARY KEY,
                workload TEXT NOT NULL,
                engine TEXT NOT NULL,
                input_records INTEGER,
                output_records INTEGER,
                duration_ms REAL,
                throughput_rec_sec REAL,
                memory_mb REAL,
                created_at TEXT NOT NULL
            )
            """)

            # Data Quality Audit Runs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_audit_runs (
                audit_id TEXT PRIMARY KEY,
                dataset_id TEXT NOT NULL,
                quality_score REAL,
                records_tested INTEGER,
                anomalies_detected INTEGER,
                checks_passed INTEGER,
                checks_total INTEGER,
                report_json TEXT,
                created_at TEXT NOT NULL
            )
            """)

            # System Audit Trail
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )
            """)
            conn.commit()

    # --- Pipeline Methods ---
    def record_pipeline_run(self, job_id: str, pipeline_name: str, status: str, execution_mode: str, stages: list, duration_sec: float = 0.0, started_at: Optional[str] = None, completed_at: Optional[str] = None, error: Optional[str] = None):
        started_at = started_at or datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO pipeline_executions (job_id, pipeline_name, status, execution_mode, stages_json, duration_sec, started_at, completed_at, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (job_id, pipeline_name, status, execution_mode, json.dumps(stages), duration_sec, started_at, completed_at, error))
            conn.commit()

    def list_pipeline_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pipeline_executions ORDER BY started_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["stages"] = json.loads(item["stages_json"])
                del item["stages_json"]
                result.append(item)
            return result

    # --- Model Registry Methods ---
    def register_model(self, model_id: str, target: str, algorithm: str, family: str, version: str, mae: float, rmse: float, wape: float, r2: float, params: dict, is_champion: bool = False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if is_champion:
                cursor.execute("UPDATE model_registry SET is_champion = 0 WHERE target_name = ?", (target,))
            cursor.execute("""
            INSERT OR REPLACE INTO model_registry (model_id, target_name, algorithm, model_family, version, mae, rmse, wape, r2_score, parameters_json, is_champion, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (model_id, target, algorithm, family, version, mae, rmse, wape, r2, json.dumps(params), 1 if is_champion else 0, datetime.utcnow().isoformat()))
            conn.commit()

    def get_registered_models(self, target: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if target:
                cursor.execute("SELECT * FROM model_registry WHERE target_name = ? ORDER BY is_champion DESC, rmse ASC", (target,))
            else:
                cursor.execute("SELECT * FROM model_registry ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    # --- Optimization Methods ---
    def record_optimization_run(self, run_id: str, scenario: str, objective: str, total_budget: float, total_cost: float, shortage_qty: float, fulfillment_pct: float, results: dict):
        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO optimization_runs (run_id, scenario_name, objective, total_budget, total_cost, shortage_quantity, fulfillment_pct, results_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (run_id, scenario, objective, total_budget, total_cost, shortage_qty, fulfillment_pct, json.dumps(results), datetime.utcnow().isoformat()))
            conn.commit()

    def get_optimization_runs(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM optimization_runs ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            out = []
            for r in rows:
                item = dict(r)
                if item["results_json"]:
                    item["results"] = json.loads(item["results_json"])
                out.append(item)
            return out

    # --- Benchmark Methods ---
    def record_benchmark_run(self, run_id: str, workload: str, engine: str, in_rec: int, out_rec: int, duration_ms: float, throughput: float, memory_mb: float):
        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO benchmark_runs (run_id, workload, engine, input_records, output_records, duration_ms, throughput_rec_sec, memory_mb, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (run_id, workload, engine, in_rec, out_rec, duration_ms, throughput, memory_mb, datetime.utcnow().isoformat()))
            conn.commit()

    def get_benchmark_runs(self, limit: int = 30) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM benchmark_runs ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    # --- Audit Trail ---
    def log_audit(self, category: str, action: str, details: str):
        with self._get_connection() as conn:
            conn.execute("INSERT INTO audit_logs (category, action, details, timestamp) VALUES (?, ?, ?, ?)",
                         (category, action, details, datetime.utcnow().isoformat()))
            conn.commit()

# Global Singleton
metadata_repo = MetadataRepository()

