#!/usr/bin/env python3
"""
ORBITALYTICS Phase 6 — Apache Hive Data Warehouse Master Orchestrator
Executes DDL schemas, dynamic partition ETL, analytical query suite, and validation.
Connects directly to live HiveServer2 via Beeline on Docker container hive-server.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

DOCKER_CONTAINER = "hive-server"
HIVE_JDBC = "jdbc:hive2://localhost:10000/orbitalytics"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_PHASE6 = os.path.join(PROJECT_ROOT, "docs", "phase_6")
LOGS_DIR = os.path.join(DOCS_PHASE6, "logs")
RESULTS_DIR = os.path.join(DOCS_PHASE6, "results")
MANIFEST_FILE = os.path.join(DOCS_PHASE6, "hive_execution_manifest.json")

DDL_SCRIPTS = [
    "01_create_database.sql",
    "02_create_staging_tables.sql",
    "03_create_dimensions.sql",
    "04_create_facts.sql",
    "05_populate_dimensions.sql",
    "06_populate_facts.sql",
    "07_create_views.sql"
]

ANALYTICAL_QUERIES = [
    {"id": "01", "name": "01_total_demand_by_component", "desc": "Total demand and fulfillment rate by component"},
    {"id": "02", "name": "02_annual_demand_trend", "desc": "Annual demand trend and YoY growth rate using LAG window function"},
    {"id": "03", "name": "03_quarterly_demand_trend", "desc": "Quarterly demand trend across Q1-Q4 with risk profile"},
    {"id": "04", "name": "04_demand_by_agency", "desc": "Component demand and spend by space agency with market share and rank"},
    {"id": "05", "name": "05_resource_consumption_by_year", "desc": "Annual consumable resource consumption by category"},
    {"id": "06", "name": "06_resource_consumption_by_mission", "desc": "Resource consumption profile by space mission"},
    {"id": "07", "name": "07_mission_counts_by_agency", "desc": "Mission counts, success rates, and budget performance by agency"},
    {"id": "08", "name": "08_satellite_deployment_by_orbit", "desc": "Satellite deployment metrics by orbital regime"},
    {"id": "09", "name": "09_launch_activity_trends", "desc": "Launch activity trends, commercialization rate, and success rate"},
    {"id": "10", "name": "10_manufacturing_requirements_by_component", "desc": "Manufacturing requirements by satellite class and QA pass rate"},
    {"id": "11", "name": "11_research_expenditure_by_agency", "desc": "Research expenditure portfolio breakdown by space agency"},
    {"id": "12", "name": "12_investment_by_year", "desc": "Annual research investment with cumulative running total and moving avg"},
    {"id": "13", "name": "13_infrastructure_by_location", "desc": "Spaceport infrastructure throughput by geographic location"},
    {"id": "14", "name": "14_mission_demand_correlation", "desc": "Cross-domain mission activity and component demand correlation"},
    {"id": "15", "name": "15_resource_launch_correlation", "desc": "Propellant consumption and launch activity correlation"},
    {"id": "16", "name": "16_partition_pruning_demonstration", "desc": "Partition pruning validation and EXPLAIN execution plan"}
]

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

def sync_to_container():
    print("[INIT] Synchronizing Hive warehouse scripts to hive-server container...")
    run_cmd(f"docker exec {DOCKER_CONTAINER} mkdir -p /opt/hive_warehouse")
    hive_local = os.path.join(PROJECT_ROOT, "hive_warehouse")
    code, _, err = run_cmd(f'docker cp "{hive_local}/." {DOCKER_CONTAINER}:/opt/hive_warehouse')
    if code != 0:
        print(f"[ERROR] Failed to docker cp: {err}")
        sys.exit(1)
    print("[INIT] Synchronization complete.")

def execute_beeline_file(container_path, log_file, output_format="csv2"):
    cmd = (
        f'docker exec {DOCKER_CONTAINER} beeline '
        f'-u "{HIVE_JDBC}" -n root '
        f'--outputformat={output_format} '
        f'-f "{container_path}"'
    )
    start_time = time.time()
    code, stdout, stderr = run_cmd(cmd)
    duration = round(time.time() - start_time, 2)

    combined_log = stdout + "\n" + stderr
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(combined_log)

    return code, stdout, stderr, duration

def run_ddl_pipeline():
    print("\n" + "=" * 80)
    print("PHASE 6: EXECUTING HIVE DDL & DATA WAREHOUSE POPULATION PIPELINE")
    print("=" * 80)

    for ddl_file in DDL_SCRIPTS:
        container_path = f"/opt/hive_warehouse/ddl/{ddl_file}"
        log_file = os.path.join(LOGS_DIR, f"ddl_{ddl_file}.log")
        print(f"--> Executing DDL: {ddl_file} ...", end=" ", flush=True)

        code, stdout, stderr, duration = execute_beeline_file(container_path, log_file, output_format="table")
        if code == 0:
            print(f"[SUCCESS] ({duration}s)")
        else:
            print(f"[FAILED] ({duration}s)")
            print(f"Log: {log_file}")
            sys.exit(1)

def run_analytical_queries():
    print("\n" + "=" * 80)
    print("PHASE 6: EXECUTING ANALYTICAL HIVE QUERY SUITE (16 QUERIES)")
    print("=" * 80)

    manifest = []
    total_start = time.time()

    for q in ANALYTICAL_QUERIES:
        q_name = q["name"]
        container_path = f"/opt/hive_warehouse/queries/{q_name}.sql"
        log_file = os.path.join(LOGS_DIR, f"{q_name}.log")
        result_file = os.path.join(RESULTS_DIR, f"{q_name}.csv")

        print(f"--> [{q['id']}/16] {q_name} ...", end=" ", flush=True)
        code, stdout, stderr, duration = execute_beeline_file(container_path, log_file, output_format="csv2")

        status = "SUCCESS" if code == 0 else "FAILED"
        
        # Filter clean tabular result rows
        result_lines = []
        for line in stdout.splitlines():
            line_str = line.strip()
            if line_str and not line_str.startswith("SLF4J:") and not line_str.startswith("Connecting") and not line_str.startswith("Connected") and not line_str.startswith("Driver") and not line_str.startswith("Transaction") and not line_str.startswith("Beeline") and not line_str.startswith("Closing:"):
                result_lines.append(line_str)

        row_count = max(0, len(result_lines) - 1) if result_lines else 0
        with open(result_file, "w", encoding="utf-8") as f:
            f.write("\n".join(result_lines))

        sample_rows = result_lines[1:4] if len(result_lines) > 1 else []

        record = {
            "query_id": q["id"],
            "query_name": q_name,
            "description": q["desc"],
            "status": status,
            "exit_code": code,
            "duration_seconds": duration,
            "row_count": row_count,
            "result_file": result_file,
            "log_file": log_file,
            "sample_rows": sample_rows,
            "timestamp": datetime.now().isoformat()
        }
        manifest.append(record)
        print(f"[{status}] ({duration}s, {row_count} rows)")

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    total_duration = round(time.time() - total_start, 2)
    successful = sum(1 for r in manifest if r["status"] == "SUCCESS")

    print("\n" + "=" * 80)
    print("HIVE QUERY SUITE EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Queries:     {len(manifest)}")
    print(f"Successful:        {successful} / {len(manifest)}")
    print(f"Total Duration:    {total_duration}s")
    print(f"Manifest Saved:    {MANIFEST_FILE}")
    print("=" * 80)

    if successful != len(manifest):
        sys.exit(1)

def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    sync_to_container()
    if "--skip-ddl" not in sys.argv:
        run_ddl_pipeline()
    else:
        print("[INFO] Skipping DDL pipeline (--skip-ddl specified). Tables & views already loaded.")
    run_analytical_queries()

if __name__ == '__main__':
    main()
