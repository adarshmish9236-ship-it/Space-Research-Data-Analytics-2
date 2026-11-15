#!/usr/bin/env python3
"""
ORBITALYTICS Phase 7 — Master Orchestrator
Copies PySpark scripts to spark-master container and submits all jobs sequentially.
Collects execution logs and writes the Phase 7 results manifest.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_ROOT   = Path(__file__).resolve().parent.parent
SPARK_DIR      = PROJECT_ROOT / "spark_analytics"
DOCS_PHASE7    = PROJECT_ROOT / "docs" / "phase_7"
LOGS_DIR       = DOCS_PHASE7 / "logs"
MANIFEST_FILE  = DOCS_PHASE7 / "phase7_execution_manifest.json"

SPARK_MASTER_URL = "spark://spark-master:7077"
CONTAINER        = "spark-master"
CONTAINER_PATH   = "/opt/spark_analytics"
PYSPARK_PATH     = "/spark/bin/spark-submit"
PYPATH_ENV       = f"PYTHONPATH={CONTAINER_PATH}"

JOBS = [
    {"id": "01", "file": "jobs/01_data_access_verification.py",    "name": "Data Access & Schema Verification"},
    {"id": "02", "file": "jobs/02_integration_and_transformations.py", "name": "Multi-Dataset Integration & Distributed Transformations"},
    {"id": "03", "file": "jobs/03_feature_engineering.py",          "name": "Time-Series Feature Engineering Pipeline"},
    {"id": "04", "file": "jobs/04_spark_sql_analytics.py",          "name": "Spark SQL Analytics & Performance"},
]

SPARK_SUBMIT_OPTS = [
    "--master", SPARK_MASTER_URL,
    "--driver-memory", "1024m",
    "--executor-memory", "1536m",
    "--conf", "spark.sql.adaptive.enabled=true",
    "--conf", "spark.serializer=org.apache.spark.serializer.KryoSerializer",
    "--conf", "spark.sql.shuffle.partitions=8",
]


def run(cmd, timeout=1800):
    """Run a shell command and return returncode, stdout, stderr."""
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, timeout=timeout
    )
    return result.returncode, result.stdout


def sync_to_container():
    print("[SYNC] Copying spark_analytics to spark-master container...")
    run(f'docker exec {CONTAINER} rm -rf {CONTAINER_PATH}')
    run(f'docker exec {CONTAINER} mkdir -p {CONTAINER_PATH}')
    code, out = run(f'docker cp "{SPARK_DIR}/." {CONTAINER}:{CONTAINER_PATH}')
    if code != 0:
        print(f"[ERROR] docker cp failed: {out}")
        sys.exit(1)
    # Also copy the session factory separately for PYTHONPATH
    print("[SYNC] Done.")


def run_spark_job(job):
    container_script = f"{CONTAINER_PATH}/{job['file']}"
    opts = " ".join(SPARK_SUBMIT_OPTS)
    cmd = f'docker exec -e {PYPATH_ENV} {CONTAINER} {PYSPARK_PATH} {opts} {container_script}'

    log_file = LOGS_DIR / f"{job['id']}_{job['name'].replace(' ', '_').replace('&', 'and')}.log"
    print(f"\n[JOB {job['id']}] {job['name']}")
    print(f"  Script: {container_script}")

    t0 = time.time()
    code, output = run(cmd, timeout=1800)
    elapsed = round(time.time() - t0, 2)

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"JOB: {job['name']}\nTIMESTAMP: {datetime.now().isoformat()}\n")
        f.write(f"EXIT CODE: {code}\nDURATION: {elapsed}s\n")
        f.write("=" * 60 + "\n")
        f.write(output)

    status = "SUCCESS" if code == 0 else "FAILED"
    print(f"  [{status}] {elapsed}s  |  Log: {log_file.name}")

    # Print last 20 lines of output for quick inspection
    lines = output.strip().splitlines()
    for line in lines[-20:]:
        if any(x in line for x in ["ERROR", "SUCCESS", "complete", "Written", "Rows:", "partitions"]):
            print(f"    {line}")

    return {
        "job_id": job["id"],
        "job_name": job["name"],
        "status": status,
        "exit_code": code,
        "duration_s": elapsed,
        "log_file": str(log_file),
        "timestamp": datetime.now().isoformat()
    }


def main():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_PHASE7.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*80)
    print("ORBITALYTICS PHASE 7 — APACHE SPARK ANALYTICS MASTER ORCHESTRATOR")
    print("="*80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Spark master: {SPARK_MASTER_URL}")
    print(f"Container: {CONTAINER}")

    sync_to_container()

    manifest_entries = []
    total_start = time.time()

    for job in JOBS:
        entry = run_spark_job(job)
        manifest_entries.append(entry)

    total_elapsed = round(time.time() - total_start, 2)
    successes = sum(1 for e in manifest_entries if e["status"] == "SUCCESS")

    print("\n" + "="*80)
    print("PHASE 7 EXECUTION SUMMARY")
    print("="*80)
    print(f"Jobs Run:       {len(manifest_entries)}")
    print(f"Successful:     {successes} / {len(manifest_entries)}")
    print(f"Total Duration: {total_elapsed}s")
    for e in manifest_entries:
        print(f"  [{e['status']:7}] {e['job_id']} — {e['job_name']} ({e['duration_s']}s)")

    final_manifest = {
        "phase": 7,
        "run_timestamp": datetime.now().isoformat(),
        "spark_master": SPARK_MASTER_URL,
        "total_jobs": len(manifest_entries),
        "successful_jobs": successes,
        "total_duration_s": total_elapsed,
        "jobs": manifest_entries
    }
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(final_manifest, f, indent=2)
    print(f"\nManifest saved: {MANIFEST_FILE}")
    print("="*80 + "\n")

    if successes < len(manifest_entries):
        sys.exit(1)


if __name__ == "__main__":
    main()
